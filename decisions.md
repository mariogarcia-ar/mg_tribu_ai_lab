# decisions.md

> Este archivo es el contrato de diseño del sistema.
> Cualquier código generado por AI debe respetar estas reglas.
> Si no las respeta, se rechaza — no importa si "funciona".

## Estados de tarea

- Representación: Python Enum (`TaskStatus`)
- Valores: `PENDING`, `IN_PROGRESS`, `BLOCKED`, `REVIEW`, `DONE`, `CANCELLED`
- Estados terminales: `DONE`, `CANCELLED` — sin transiciones posibles desde ahí
- Fuente de verdad: el Enum en el modelo + `TaskStatus.terminal_states()` — nowhere else
- Almacenamiento en DB: se guarda el `.value` del Enum (string), se reconstruye al leer

## Prioridad

- Representación: Python IntEnum (`TaskPriority`) con valor entero
- Valores: `LOW=1`, `MEDIUM=2`, `HIGH=3`, `URGENT=4`
- El orden numérico define la precedencia — no el nombre
- Sort en DB: `ORDER BY priority_value DESC`
- Almacenamiento en DB: se guarda el valor entero (1, 2, 3, 4)

## Ownership y creación

- `created_by`: entero requerido — quién creó la tarea. Nunca es NULL
- `owner_id`: entero opcional — quién tiene asignada la tarea. `None` = "sin asignar"
- `None` en `owner_id` es un estado válido, no un error
- Las funciones de listado filtran por `owner_id` OR `created_by`

## Visibilidad entre usuarios

- Un usuario solo ve sus propias tareas (`owner_id = user_id` OR `created_by = user_id`)
- `list_all` no existe — todo listado requiere un `user_id` explícito
- Excepción: rol ADMIN puede listar todo (fuera de scope — no implementar)

## Permisos de modificación

- Solo el owner o el creator pueden modificar una tarea
- Tareas en estados terminales (`DONE`, `CANCELLED`) no se pueden modificar
- Intentar modificar una tarea terminal → `ValueError`
- Intentar modificar sin permisos → `PermissionError`

## Compartir tareas

- **Out of scope** para esta versión — no implementar
- Motivo: requiere modelo de permisos que no está definido
- Decisión explícita de NO hacer

## Due date y overdue

- `due_date`: opcional en Task — `None` significa "sin vencimiento", nunca overdue
- Una tarea es overdue si: `due_date < hoy` AND `status NOT IN terminal_states`
- `terminal_states`: definido en `TaskStatus.terminal_states()` — única fuente de verdad
- Notificación va al `owner_id`; si es `None`, va al `created_by`
