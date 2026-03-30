# Idea del Sistema

## TODO Avanzado con inicio de CRM

### Concepto

Un sistema de gestión de tareas (TODO app) que evoluciona progresivamente hacia un CRM básico. Comienza como una herramienta personal de tareas y escala a un entorno multi-usuario con asignaciones, prioridades, vencimientos y visibilidad controlada — las piezas fundamentales de cualquier CRM.

### Por qué este sistema

Es el vehículo perfecto para el laboratorio porque:

- **Empieza simple:** cualquiera entiende una TODO app en 30 segundos.
- **Escala naturalmente:** agregar usuarios, permisos, prioridades y notificaciones introduce exactamente los problemas de gobernanza que queremos demostrar.
- **Tiene decisiones reales:** estados, permisos, visibilidad, propiedad de datos — las mismas decisiones que enfrenta un CRM real.

### Funcionalidades core

1. **Gestión de tareas**
   - Crear, listar, actualizar y eliminar tareas
   - Estados con ciclo de vida definido: PENDING → IN_PROGRESS → BLOCKED → REVIEW → DONE / CANCELLED
   - Estados terminales (DONE, CANCELLED) sin transiciones de salida

2. **Prioridades**
   - Niveles con valor numérico: LOW(1), MEDIUM(2), HIGH(3), URGENT(4)
   - Ordenamiento por valor entero, no por nombre

3. **Usuarios y propiedad**
   - Modelo de usuario: id, nombre, email
   - Cada tarea tiene un creador (created_by) y opcionalmente un dueño (owner_id)
   - Sin dueño = tarea sin asignar (estado válido, no error)

4. **Visibilidad controlada**
   - Un usuario solo ve sus tareas (como owner o como creator)
   - No existe listado global — todo requiere un user_id explícito
   - Compartir tareas: fuera de scope (decisión explícita, no omisión)

5. **Vencimientos y notificaciones**
   - Fecha de vencimiento opcional en cada tarea
   - Detección de overdue: fecha pasada + estado no terminal
   - Notificación al owner; si no tiene, al creator

### Hacia CRM: extensiones naturales

Estas son las extensiones que convierten la TODO app en un CRM básico. No se implementan en el laboratorio, pero se mencionan para mostrar que el modelo System-Centric soporta la evolución:

- **Contactos:** vincular tareas a contactos externos (clientes, prospectos)
- **Pipeline:** estados configurables por tipo de tarea (venta, soporte, onboarding)
- **Roles y permisos:** admin, manager, operador — con visibilidad diferenciada
- **Historial:** log de cambios por tarea (quién hizo qué, cuándo)
- **Etiquetas y filtros:** categorización libre con búsqueda combinada

### Restricciones técnicas

- Python stdlib únicamente (sqlite3, argparse, enum, datetime)
- Sin dependencias externas, sin build system, sin CI/CD
- Archivo único (todo.py) con persistencia SQLite
- CLI con argparse — sin interfaz web ni API REST

### El punto

El sistema no es el objetivo — es el medio. Lo que importa es demostrar que las decisiones explícitas (documentadas antes de codear) eliminan el loop infinito de fixes que aparece cuando la AI toma decisiones implícitas.

> "No podés evolucionar lo que no podés explicar."
