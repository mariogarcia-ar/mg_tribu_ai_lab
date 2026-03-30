# decisions.md — Contrato de Gobernanza

Este archivo documenta las decisiones de diseño del sistema. Todo código debe respetar estas reglas. Si el código viola una decisión, se rechaza.

---

## D-01: Estados de tarea — Enum, no strings

**Decisión:** Los estados de tarea se definen como `TaskStatus(Enum)` con seis valores posibles.

**Valores:**
- `PENDING` — tarea creada, sin iniciar
- `IN_PROGRESS` — en ejecución
- `BLOCKED` — bloqueada por dependencia externa
- `REVIEW` — en revisión
- `DONE` — completada (estado terminal)
- `CANCELLED` — cancelada (estado terminal)

**Regla:** Nunca usar strings literales para estados. Siempre usar `TaskStatus.PENDING`, `TaskStatus.DONE`, etc.

---

## D-02: Estados terminales — definidos en el Enum

**Decisión:** Los estados terminales son `DONE` y `CANCELLED`. Se definen exclusivamente a través de `TaskStatus.terminal_states()`.

**Regla:** La verificación de si una tarea está en estado terminal se hace con:
```python
status in TaskStatus.terminal_states()
```
Nunca comparar contra strings como `"DONE"` o `"CANCELLED"` directamente.

**Consecuencia:** Una tarea en estado terminal no puede ser modificada.

---

## D-03: Prioridades — IntEnum con valores enteros

**Decisión:** Las prioridades se definen como `TaskPriority(IntEnum)` con cuatro niveles.

**Valores:**
- `LOW = 1`
- `MEDIUM = 2`
- `HIGH = 3`
- `URGENT = 4`

**Regla:** El ordenamiento de tareas por prioridad usa el valor entero del enum, no el nombre. `TaskPriority.URGENT > TaskPriority.HIGH` es verdadero por definición.

---

## D-04: Visibilidad — sin listado global

**Decisión:** No existe ninguna función `list_all` ni operación que devuelva todas las tareas del sistema.

**Regla:** Todo listado de tareas requiere un `user_id` explícito. Un usuario solo ve tareas donde es `owner_id` o `created_by`.

**Razón:** Diseño de privacidad desde el inicio. El listado global es un escape que rompe el modelo de visibilidad controlada.

---

## D-05: Propiedad de tareas — created_by requerido, owner_id opcional

**Decisión:** Toda tarea debe tener un `created_by` (usuario que creó la tarea). El campo `owner_id` (responsable de ejecutarla) es opcional.

**Regla:**
- `created_by` es NOT NULL en la base de datos.
- `owner_id` puede ser NULL — una tarea sin dueño es una tarea sin asignar (estado válido, no error).
- Toda mutación requiere un `user_id` para verificar permisos (el usuario debe ser owner o creator).

---

## D-06: Compartir tareas — fuera de scope

**Decisión:** El sistema no implementa compartir tareas entre usuarios.

**Regla:** No existe ninguna operación de transferencia de ownership ni asignación secundaria. Esta es una decisión explícita, no una omisión. Si se requiere en el futuro, debe abrir una nueva decisión documentada.

---

*Este archivo es el contrato. El código es la implementación del contrato.*
