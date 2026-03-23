# Laboratorio — Encuentro 2
## "El mismo sistema. Sin el loop."

**Stack:** Python · **Herramientas:** Claude + GitHub Copilot · **Modalidad:** Live coding

**Punto de partida:** el sistema roto del E1 — con todos sus estados inconsistentes,
su `user_id` nullable, su sort de prioridades ambiguo, y su loop de fixes sin salida.

---

## Contexto para el instructor

El E2 recorre exactamente las mismas etapas que el E1, en el mismo orden.
La diferencia no es el destino — es el proceso.

Cada vez que el instructor esté por escribir código, se detiene y hace una pregunta primero.
Esa pausa es el núcleo del modelo System-Centric.

**Para los dueños:** observar *cuándo* el instructor frena y *qué pregunta*.
**Para los seniors:** observar *qué cambia en el código* como resultado de esa decisión.

---

## El framework: Think / Decide / Execute / Verify

Presentar antes de tocar el teclado. Breve — no más de 5 minutos.

| Fase | Quién | Qué produce |
|---|---|---|
| **Think** | Humano | Preguntas sin responder |
| **Decide** | Humano | Reglas explícitas documentadas |
| **Execute** | AI dentro del marco definido | Código que respeta las reglas |
| **Verify** | Humano | Confirmación de que el código cumple lo decidido |

> La AI no desaparece. Cambia de rol: deja de decidir y pasa a proponer.

---

## Etapa 1 — TODO básico (reconstrucción)

### THINK — antes de escribir una línea

**Prompt para Claude (no pedir código todavía):**

```
I'm going to build a TODO app that will eventually support multiple users
and evolve into a CRM-like system.

Before I write any code, what are the decisions I need to make
about the task model that will be hard to change later?
List only the critical ones. Do NOT write code.
```

**Claude va a devolver algo como:**
- ¿Cómo representás los estados? ¿String, Enum, tabla externa?
- ¿Los estados son fijos o configurables?
- ¿`user_id` puede ser nulo? ¿Qué significa una tarea sin dueño?
- ¿Qué significa "tarea terminada"? ¿Hay más de un estado terminal?

**Para los dueños — decir en voz alta:**
> "Esto son las preguntas que en el E1 nunca hicimos.
> Copilot las respondió solo, sin que nos diéramos cuenta."

---

### DECIDE — responder las preguntas en voz alta y documentarlas

Crear `decisions.md` antes de escribir `todo.py`.

```markdown
# decisions.md

## Estados de tarea
- Representación: Python Enum (no strings)
- Valores: PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED
- Estados terminales: DONE, CANCELLED — sin transiciones posibles desde ahí
- Fuente de verdad: el Enum en el modelo, nowhere else

## Prioridad
- Representación: Python Enum con valor entero (LOW=1, MEDIUM=2, HIGH=3, URGENT=4)
- El orden numérico define la precedencia — no el nombre

## Tareas sin dueño
- user_id puede ser None — representa una tarea "sin asignar"
- Es un estado válido, no un error
- Las funciones de listado deben filtrar por owner explícitamente
```

**Para los seniors — señalar:**
> "Este archivo es el contrato. Cualquier código que genere la AI tiene que respetar esto.
> Si no lo respeta, lo rechazamos — no importa si 'funciona'."

---

### EXECUTE — ahora sí, generar el código

**Prompt para Claude:**

```
Build a TODO app in Python using the following decisions:

- Task status: Python Enum with PENDING, IN_PROGRESS, BLOCKED, REVIEW, DONE, CANCELLED
- Terminal states: DONE and CANCELLED — no transitions allowed out of these
- Priority: Python Enum with LOW=1, MEDIUM=2, HIGH=3, URGENT=4 (integer value for sorting)
- user_id: optional integer, None means unassigned — this is valid, not an error
- Single file, sqlite3, argparse CLI

The model must make invalid states impossible to represent.
Use the Enum values for all DB storage — not raw strings.
```

**Diferencia visible respecto al E1:**
- `status` es un `Enum`, no un string
- `priority` tiene un valor entero — el sort es `ORDER BY priority_value DESC`
- `user_id` es `Optional[int]` con semántica explícita

---

### VERIFY — antes de continuar

**Prompt para Claude:**

```
Review this code against decisions.md.
Check only these things:
1. Is TaskStatus an Enum? Are all comparisons using the Enum, not raw strings?
2. Is there a single place in the code that defines terminal states?
3. Is priority sorting using the integer value, not the string name?
4. Are there any raw status strings hardcoded outside the Enum definition?

Report violations only. No suggestions.
```

**Si hay violaciones:** corregirlas antes de avanzar.
**Si no hay:** mostrar al grupo que el sistema ya es más robusto que el E1 completo,
y todavía no agregamos ni un usuario.

---

## Etapa 2 — Módulo de usuarios (primer escalamiento)

### THINK

**Prompt para Claude:**

```
I'm going to add multi-user support to this TODO app.
Before I write any code, what decisions about visibility and ownership
will be hard to change later?
Do NOT write code.
```

**Preguntas que va a devolver:**
- ¿Un usuario puede ver tareas de otro?
- ¿Qué pasa con las tareas existentes sin dueño al agregar usuarios?
- ¿Hay roles? ¿Un admin ve todo?
- ¿Compartir una tarea es un concepto válido en este sistema?

---

### DECIDE — agregar al mismo `decisions.md`

```markdown
## Visibilidad entre usuarios
- Un usuario solo ve sus propias tareas (owner) y las que le fueron compartidas
- list_all no existe — todo listado requiere un user_id explícito
- Excepción: rol ADMIN puede listar todo (fuera de scope por ahora — no implementar)

## Tareas existentes sin dueño
- Al migrar, las tareas sin user_id quedan como "unassigned"
- Son visibles solo para el usuario que las creó (created_by, nuevo campo)
- No se asignan automáticamente

## Compartir tareas
- Out of scope para esta versión — no implementar
- Motivo: requiere modelo de permisos que no está definido
```

**Para los dueños — señalar la última decisión:**
> "En el E1, Claude implementó el sharing igual.
> Acá decidimos explícitamente que no va — porque no tenemos las reglas.
> Esa decisión de *no hacer* también es parte del control."

---

### EXECUTE

**Prompt para Claude:**

```
Add multi-user support following decisions.md.

Rules:
- Add User model: id, name, email
- Add created_by (int, required) to Task — the user who created it
- owner_id (int, optional) stays as-is
- Remove any list_all function — replace with list_tasks_for_user(user_id)
  which returns tasks where owner_id = user_id OR created_by = user_id
- Do NOT implement task sharing
- Migration: existing tasks get created_by = 1 (seed user)
```

---

### VERIFY

**Prompt para Claude:**

```
Review the updated code against decisions.md.
Check:
1. Is there any function that returns tasks without filtering by user_id?
2. Is task sharing implemented anywhere? It should not be.
3. Does list_tasks_for_user cover both owner_id and created_by cases?

Report violations only.
```

---

## Etapa 3 — Múltiples usuarios, sin ambigüedades

Esta es la etapa donde el E1 explotó. Acá no explota — porque las decisiones ya están tomadas.

### La misma feature: prioridades

**Con Copilot — escribir el docstring primero:**

```python
def set_priority(task_id: int, priority: TaskPriority, user_id: int) -> Task:
    """
    Set priority for a task.
    Rules (from decisions.md):
    - priority must be a TaskPriority Enum value
    - user must be owner or creator of the task
    - tasks in terminal states cannot be modified
    Raises: ValueError if task is in terminal state
    Raises: PermissionError if user has no access to task
    """
```

**Dejar que Copilot complete el cuerpo.**

**Para los seniors — señalar:**
> "El docstring es el contrato. Copilot tiene que respetarlo.
> Si genera código que no maneja el PermissionError, lo rechazamos."

---

### La misma feature: estados adicionales

Los estados ya están definidos en el Enum desde la Etapa 1.
No hay prompt nuevo. No hay migración. No hay inconsistencia.

**Mostrar en voz alta:**
> "En el E1, agregar estados requirió un prompt, una migración rota,
> y dejó dos definiciones distintas de 'estado terminal' en el código.
> Acá ya estaban. Costo: cero."

---

### La feature que rompió todo: notificaciones de tareas vencidas

**THINK primero:**

```
I want to add overdue notifications.
Before I write any code, what do I need to decide?
Check against decisions.md — are there any gaps?
Do NOT write code.
```

**Claude va a identificar el gap:**
> "No hay definición de `due_date` en el modelo ni en decisions.md."

---

**DECIDE — cubrir el gap antes de codear:**

```markdown
## Due date y overdue
- due_date: opcional en Task — None significa "sin vencimiento", nunca overdue
- Una tarea es overdue si: due_date < hoy AND status NOT IN terminal_states
- terminal_states: definido en TaskStatus.terminal_states() — única fuente de verdad
- Notificación va al owner_id; si es None, va al created_by
```

---

**EXECUTE:**

```
Add overdue notification following decisions.md.

Rules:
- due_date is optional — tasks without due_date are never overdue
- Use TaskStatus.terminal_states() to determine if a task is closed
- Notify owner_id if set, otherwise created_by
- Print to console: "OVERDUE: [task title] — assigned to [user name]"
- Migration: add due_date column as nullable, default NULL
```

---

**VERIFY:**

```
Review the overdue notification code.
Check:
1. Is the terminal states check using TaskStatus.terminal_states()? Not a hardcoded list.
2. Does the notification fallback to created_by when owner_id is None?
3. Is due_date handled as truly optional — no errors on None?

Report violations only.
```

**La feature funciona. Sin loop. Sin fixes en cadena.**

---

## Cierre — Comparativa en vivo

Mostrar los dos archivos lado a lado (o el git diff si se trabajó en el mismo repo con branches).

| | E1 — Code-Centric | E2 — System-Centric |
|---|---|---|
| Definición de estados | String libre en 4 lugares | Enum, un solo lugar |
| Estados terminales | Hardcodeado en la función de notificaciones | `TaskStatus.terminal_states()` |
| Sort de prioridad | Alfabético (incorrecto) | Por valor entero del Enum |
| Visibilidad entre usuarios | `list_all` sin filtro | `list_tasks_for_user` obligatorio |
| Feature nueva | Rompió el schema, generó loop | Se agregó al contrato existente |
| Tiempo en debugging | ~40% del laboratorio | 0 |

---

## Frase de cierre

> "El problema nunca fue la velocidad.
> Fue la falta de gobierno."

> "La ventaja no está en usar AI.
> Está en usarla sin perder el control."

---

## Nota para el instructor

Si algún alumno pregunta *"¿y si el sistema es más complejo?"*:

> "La complejidad no cambia el modelo — lo hace más necesario.
> Un sistema complejo con decisiones implícitas es simplemente un loop más grande."