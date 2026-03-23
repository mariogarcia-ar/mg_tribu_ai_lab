# Laboratorio — Encuentro 1
## "Cómo se rompe un sistema aunque parezca que funciona"

**Stack:** Python · **Herramientas:** Claude + GitHub Copilot · **Modalidad:** Live coding

---

## Etapa 1 — TODO básico que funciona

**Objetivo:** construir algo simple, rápido, que ande. Sin fricción. Sin preguntas previas.

### Prompt inicial (Claude)

```
Build a simple TODO app in Python.
Single file, sqlite3, no external dependencies.
A task has: title, status (pending/done), created_at.
Add basic CRUD: create, list, update status, delete.
CLI with argparse.
```

### Lo que se construye

- `todo.py` — modelo + DB + CLI en un solo archivo
- Se ejecuta, funciona, se hace una demo rápida
- El instructor muestra: agregar tarea, listarlas, marcar como done

### ⚠️ Punto de quiebre (no decirlo todavía)

El status es un string libre. Copilot/Claude no definió qué valores son válidos.
Nadie lo cuestionó. **Anotar mentalmente — va a explotar en la Etapa 3.**

---

## Etapa 2 — Primer escalamiento: módulo de usuarios

**Objetivo:** agregar algo razonable. Parece simple. Sigue funcionando.

### Prompt (Claude)

```
The TODO app needs users.
Add a User model: id, name, email.
Tasks should have an owner (user_id).
Add: create_user, assign_task_to_user, list_tasks_by_user.
```

### Lo que se construye

- Tabla `users` en la misma DB
- `user_id` como FK en tasks (nullable por ahora — "para no romper lo existente")
- Funciones nuevas, CLI extendido

### Demo

Crear dos usuarios, asignar tareas, listar por usuario. Funciona.

### ⚠️ Puntos de quiebre (no decirlos todavía)

- `user_id` nullable: las tareas viejas no tienen dueño. ¿Es eso válido? Nadie decidió.
- ¿Un usuario puede ver tareas de otro? La función `list_tasks_by_user` filtra por user_id pero `list_all` sigue mostrando todo. Dos comportamientos, sin regla explícita.

---

## Etapa 3 — Múltiples usuarios con ambigüedades

**Objetivo:** agregar features que parecen razonables pero introducen conflictos reales.

### Prompt A — prioridades (Copilot, completar mientras se escribe)

```python
def set_priority(task_id, priority):
    # priority can be: low, medium, high, urgent
    # update in db

def get_tasks_sorted_by_priority():
    # return all tasks sorted by priority, highest first
```

**Dejar que Copilot complete.** Aceptar la primera sugerencia.

### Prompt B — estados adicionales (Claude)

```
We need more granular task states.
Add: pending, in_progress, blocked, review, done, cancelled.
Update all status handling in the app.
```

### Prompt C — tareas compartidas

```
Add the ability to share a task with another user.
A shared user can see and update the task status,
but cannot delete it or reassign it.
```

### Lo que pasa

Claude actualiza `status` en algunos lugares, no en todos.
Hay funciones que todavía esperan `"done"`, otras ahora usan `"completed"`.
La prioridad es un string — `"high"` y `"High"` son cosas distintas en los queries.
Las tareas compartidas tienen lógica de permisos... pero `list_all` sigue sin filtrar nada.

**No corregir nada. Dejar el sistema en este estado.**

---

## Etapa 4 — El loop infinito

**Objetivo:** intentar agregar una feature simple. Demostrar que cada fix rompe algo.

### La feature: notificaciones de tareas vencidas

```
Add a feature to notify users when their tasks are overdue.
A task is overdue when it's not done and its due_date has passed.
Print a notification to console.
```

### El loop

Esto es lo que va a pasar en vivo. Cada paso es un fix que introduce un nuevo problema:

---

**Fix 1** — Claude agrega `due_date` al modelo.

> Rompe: las tareas existentes no tienen `due_date`. El schema migration falla o devuelve errores.

---

**Fix 2** — Claude agrega `DEFAULT NULL` a `due_date`.

> Rompe: la lógica de "overdue" necesita saber si la tarea está terminada. ¿`"done"` o `"completed"`? Depende de qué función la creó.

---

**Fix 3** — Claude unifica los estados a `"done"`.

> Rompe: las tareas con estado `"completed"` (generadas en la Etapa 3) ya no se reconocen como terminadas. Aparecen como overdue aunque estén cerradas.

---

**Fix 4** — Claude busca y reemplaza `"completed"` → `"done"` en toda la DB.

> Rompe: `"cancelled"` tampoco es un estado terminal según la nueva lógica. Las tareas canceladas se notifican como vencidas.

---

**Fix 5** — Claude agrega `"cancelled"` a la lista de estados terminales.

> Rompe: esa lista está hardcodeada en la función de notificaciones. No está en el modelo. `list_tasks_by_user` no la usa. Ahora hay dos definiciones distintas de "qué es una tarea terminada" en el mismo archivo.

---

**El instructor para aquí.**

No hay Fix 6. El sistema está en un estado donde cualquier cambio rompe algo.

---

## Cierre — Autopsia

**Preguntar al grupo:**

- ¿Cuántos lugares del código definen qué es un estado válido?
- ¿Quién decidió que `user_id` podía ser nullable?
- ¿Qué es una tarea "terminada"? ¿Hay una respuesta única en el código?
- ¿Podemos explicar este sistema a alguien nuevo en 5 minutos?

**Tabla de decisiones implícitas** — construir en vivo con el grupo:

| Decisión | ¿Quién decidió? | Consecuencia |
|---|---|---|
| Status como string libre | Copilot (primera sugerencia) | Inconsistencia en todo el sistema |
| `user_id` nullable | Claude ("para no romper lo existente") | Tareas huérfanas sin regla |
| Orden de prioridades | Copilot (strings sin orden) | Sort incorrecto |
| Estados terminales | Nadie — está en 2 lugares distintos | Loop infinito de fixes |
| Visibilidad entre usuarios | Claude (asumió acceso total) | `list_all` sin filtro |

---

**Frase de cierre:**

> "No podés evolucionar lo que no podés explicar."

**Gancho hacia el E2:**

> "La próxima vez tomamos exactamente este sistema y lo reconstruimos. Misma velocidad. Sin el loop."