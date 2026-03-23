#!/usr/bin/env bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

error() { echo -e "${RED}$1${NC}"; }
info()  { echo -e "${CYAN}$1${NC}"; }
title() { echo -e "${BOLD}${YELLOW}$1${NC}"; }

# Clean start
rm -f todo.db

echo ""
title "=========================================="
title "  TODO App Demo — Encuentro 1"
title "=========================================="

# ══════════════════════════════════════════
#  ETAPA 3 — Ambiguedades acumuladas
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  ETAPA 3 — Ambiguedades acumuladas"
title "=========================================="
echo ""

# ─── Setup: usuarios y tareas ───
info "--- Setup: crear usuarios y tareas ---"
python todo.py create-user "Ana" "ana@example.com"
python todo.py create-user "Luis" "luis@example.com"
python todo.py add "Diseñar API"
python todo.py add "Escribir tests"
python todo.py add "Deploy a producción"
python todo.py add "Revisar PR de Luis"
python todo.py assign 1 1
python todo.py assign 2 1
python todo.py assign 3 2
python todo.py assign 4 1
python todo.py share 3 1
echo ""

# ─── 1. Status inconsistency ───
title "=========================================="
title "  BUG 1: Status inconsistente"
title "=========================================="
echo ""

info "Ana marca tarea 1 como 'done' con update-as (con permisos):"
python todo.py update-as 1 done 1
echo ""

info "Alguien marca tarea 2 como 'done' con update (SIN verificar usuario):"
python todo.py update 2 done
echo ""

error ">>> ERROR: update() no verifica permisos. Cualquiera puede cambiar el status."
error ">>> update-as() sí verifica, pero update() sigue existiendo sin control."
error ">>> Dos funciones, dos reglas distintas para lo mismo."
echo ""

info "Simulamos lo que pasa cuando otro módulo usa 'completed' en vez de 'done':"
python -c "
import sqlite3
conn = sqlite3.connect('todo.db')
conn.execute(\"UPDATE tasks SET status = 'completed' WHERE id = 3\")
conn.commit()
conn.close()
print('Task 3 status set to completed (direct DB update)')
"
echo ""

info "Listar tareas:"
python todo.py list
echo ""
error ">>> ERROR: La tarea 3 tiene status 'completed' pero VALID_STATUSES solo acepta 'done'."
error ">>> 'done' y 'completed' coexisten. No hay una definición única de 'terminada'."
echo ""

# ─── 2. Priority como string ───
title "=========================================="
title "  BUG 2: Prioridad como string libre"
title "=========================================="
echo ""

info "Seteamos prioridades:"
python todo.py set-priority 1 high
python todo.py set-priority 2 High
python todo.py set-priority 3 urgent
python todo.py set-priority 4 low
echo ""

info "Listar por prioridad (ORDER BY priority DESC — orden alfabético):"
python todo.py list-by-priority
echo ""

error ">>> ERROR: 'high' y 'High' son valores distintos. No hay validación."
error ">>> ORDER BY priority DESC ordena alfabéticamente: urgent > low > high > High."
error ">>> El sort no refleja la urgencia real. 'low' aparece antes que 'high'."
echo ""

# ─── 3. list_all sin filtro de usuario ───
title "=========================================="
title "  BUG 3: list muestra TODO sin filtrar"
title "=========================================="
echo ""

info "Tareas de Ana (list-user 1) — con permisos:"
python todo.py list-user 1
echo ""

info "Tareas de Luis (list-user 2) — con permisos:"
python todo.py list-user 2
echo ""

info "list (sin usuario) — muestra absolutamente todo:"
python todo.py list
echo ""

error ">>> ERROR: list() muestra TODAS las tareas de TODOS los usuarios."
error ">>> list-user() filtra por permisos, pero list() ignora todo eso."
error ">>> Dos comportamientos contradictorios. No hay regla de visibilidad única."
echo ""

# ─── 4. delete sin permisos ───
title "=========================================="
title "  BUG 4: delete ignora permisos"
title "=========================================="
echo ""

info "Luis intenta borrar tarea de Ana con delete-as (con permisos):"
python todo.py delete-as 1 2
echo ""

info "Pero con delete (sin verificar usuario)..."
python todo.py delete 1
echo ""

error ">>> ERROR: delete() no verifica quién borra. Cualquiera puede eliminar cualquier tarea."
error ">>> delete-as() protege, pero delete() sigue abierto. La protección es una ilusión."
echo ""

# ══════════════════════════════════════════
#  ETAPA 4 — El loop infinito
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  ETAPA 4 — El loop infinito"
title "  Feature: notificaciones de tareas vencidas"
title "=========================================="
echo ""

info "--- Setup: asignar due_date a tareas existentes ---"
python todo.py set-due 2 "2026-03-20"
python todo.py set-due 3 "2026-03-21"
python todo.py set-due 4 "2026-03-25"
echo ""

# ─── Primer intento: notify-overdue ───
title "------------------------------------------"
title "  Intento 1: ejecutar notify-overdue"
title "------------------------------------------"
echo ""

info "Verificamos estado actual de las tareas:"
python todo.py list
echo ""

info "Ejecutar notificaciones:"
python todo.py notify-overdue
echo ""

error ">>> ERROR: La tarea 3 tiene status 'completed' (de la Etapa 3)."
error ">>> notify_overdue() solo excluye status == 'done'."
error ">>> 'completed' NO es 'done' → la tarea 3 aparece como overdue aunque está terminada."
echo ""

# ─── Fix 1: unificar a 'done' ───
title "------------------------------------------"
title "  Fix 1: unificar 'completed' → 'done' en la DB"
title "------------------------------------------"
echo ""

info "Reemplazamos 'completed' por 'done' en toda la DB:"
python -c "
import sqlite3
conn = sqlite3.connect('todo.db')
cursor = conn.execute(\"UPDATE tasks SET status = 'done' WHERE status = 'completed'\")
conn.commit()
print(f'{cursor.rowcount} task(s) updated: completed → done')
conn.close()
"
echo ""

info "Ejecutar notificaciones de nuevo:"
python todo.py notify-overdue
echo ""

error ">>> ERROR: La tarea 3 ya no aparece. Pero..."
error ">>> ¿Y las tareas con status 'cancelled'? También son terminadas."
error ">>> Agreguemos una tarea cancelada con due_date pasada para verificar."
echo ""

# ─── Fix 2: cancelled también es terminal ───
title "------------------------------------------"
title "  Fix 2: ¿qué pasa con 'cancelled'?"
title "------------------------------------------"
echo ""

info "Creamos una tarea cancelada con due_date vencida:"
python todo.py add "Feature descartada"
python todo.py assign 5 1
python todo.py set-due 5 "2026-03-19"
python todo.py update 5 cancelled
echo ""

info "Ejecutar notificaciones:"
python todo.py notify-overdue
echo ""

error ">>> ERROR: La tarea 5 (cancelled) aparece como overdue."
error ">>> notify_overdue() solo excluye 'done'. 'cancelled' no está contemplado."
error ">>> ¿Dónde está la definición de 'tarea terminada'? En ningún lugar centralizado."
echo ""

# ─── Fix 3: hardcodear cancelled ───
title "------------------------------------------"
title "  Fix 3: agregar 'cancelled' al filtro de notify"
title "------------------------------------------"
echo ""

info "Parcheamos notify_overdue para excluir también 'cancelled':"
python -c "
import sqlite3
from datetime import datetime
conn = sqlite3.connect('todo.db')
rows = conn.execute(
    \"\"\"SELECT t.id, t.title, t.status, t.due_date, u.name
       FROM tasks t LEFT JOIN users u ON t.user_id = u.id
       WHERE t.due_date IS NOT NULL
       AND t.status != 'done'
       AND t.status != 'cancelled'\"\"\"
).fetchall()
conn.close()
now = datetime.now().isoformat()
found = False
for row in rows:
    if row[3] < now:
        found = True
        owner = row[4] if row[4] else 'unassigned'
        print(f'OVERDUE: [{row[0]}] {row[1]} ({row[2]}) due={row[3]} owner={owner}')
if not found:
    print('No overdue tasks.')
"
echo ""

error ">>> 'Fix' aplicado... pero solo en este script."
error ">>> En todo.py, notify_overdue() sigue excluyendo solo 'done'."
error ">>> Ahora hay DOS definiciones de 'tarea terminada':"
error ">>>   - notify_overdue() en todo.py:      status != 'done'"
error ">>>   - este parche:                       status != 'done' AND status != 'cancelled'"
error ">>> Ninguna está en el modelo. Las dos son hardcoded."
echo ""

# ─── Fix 4: tareas sin due_date ───
title "------------------------------------------"
title "  Fix 4: tareas sin due_date"
title "------------------------------------------"
echo ""

info "¿Qué pasa con las tareas que nunca tuvieron due_date?"
python -c "
import sqlite3
conn = sqlite3.connect('todo.db')
rows = conn.execute(
    \"SELECT id, title, status, due_date FROM tasks WHERE due_date IS NULL\"
).fetchall()
conn.close()
for row in rows:
    print(f'[{row[0]}] {row[1]} ({row[2]}) due_date=NULL')
if not rows:
    print('Todas las tareas tienen due_date.')
"
echo ""

error ">>> ERROR: Las tareas creadas antes de agregar due_date tienen NULL."
error ">>> ¿Son overdue? ¿Son válidas? ¿Se pueden notificar?"
error ">>> Nadie decidió qué hacer con las tareas legacy."
echo ""

# ─── El instructor para aquí ───
title "------------------------------------------"
title "  FIN — El instructor para aquí."
title "------------------------------------------"
echo ""
error "  No hay Fix 5. Cada fix introduce un problema nuevo."
error "  El sistema está en un estado donde cualquier cambio rompe algo."
echo ""

# ─── Resumen final ───
title "=========================================="
title "  AUTOPSIA: Decisiones implícitas"
title "=========================================="
echo ""
error "  | Decisión                        | ¿Quién decidió?                    | Consecuencia                         |"
error "  |---------------------------------|------------------------------------|--------------------------------------|"
error "  | Status como string libre        | Copilot (primera sugerencia)       | 'done' vs 'completed' coexisten      |"
error "  | user_id nullable                | Claude ('para no romper lo viejo') | Tareas huérfanas sin regla           |"
error "  | Priority como string            | Copilot (strings sin orden)        | Sort incorrecto, case-sensitive      |"
error "  | Estados terminales              | Nadie — está en 2+ lugares         | Loop infinito de fixes               |"
error "  | Visibilidad entre usuarios      | Claude (asumió acceso total)       | list() sin filtro                    |"
error "  | due_date en tareas existentes   | Claude (DEFAULT NULL)              | Tareas legacy sin fecha              |"
echo ""
title "  \"No podés evolucionar lo que no podés explicar.\""
echo ""
title "=========================================="
echo ""
