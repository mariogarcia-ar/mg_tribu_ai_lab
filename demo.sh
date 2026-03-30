#!/usr/bin/env bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

error() { echo -e "${RED}$1${NC}"; }
ok()    { echo -e "${GREEN}$1${NC}"; }
info()  { echo -e "${CYAN}$1${NC}"; }
title() { echo -e "${BOLD}${YELLOW}$1${NC}"; }

# Clean start
rm -f todo.db

echo ""
title "=========================================="
title "  TODO App Demo — Encuentro 2"
title "  System-Centric: Think/Decide/Execute/Verify"
title "=========================================="

# ══════════════════════════════════════════
#  SETUP
# ══════════════════════════════════════════
echo ""
title "--- Setup: crear usuarios y tareas ---"
python todo.py create-user "Ana" "ana@example.com"
python todo.py create-user "Luis" "luis@example.com"
python todo.py add "Diseñar API" 1
python todo.py add "Escribir tests" 1
python todo.py add "Deploy a producción" 2
python todo.py add "Revisar PR de Luis" 1
python todo.py assign 1 1 1
python todo.py assign 2 1 1
python todo.py assign 3 2 2
python todo.py assign 4 1 1

echo ""
ok "Setup completo."

# ══════════════════════════════════════════
#  PROTECCIÓN 1: No existe list_all
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 1: No existe list_all"
title "=========================================="
echo ""

info "Tareas de Ana (user 1) — solo ve las suyas:"
python todo.py list-user 1
echo ""

info "Tareas de Luis (user 2) — solo ve las suyas:"
python todo.py list-user 2
echo ""

ok ">>> En E1, list() devolvía TODAS las tareas sin filtro."
ok ">>> En E2, list_all no existe. Siempre se requiere user_id."

# ══════════════════════════════════════════
#  PROTECCIÓN 2: Status es un Enum
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 2: Status es un Enum"
title "=========================================="
echo ""

info "Intentar setear un status inválido ('completed'):"
python todo.py update 1 completed 1
echo ""

info "Intentar setear un status inválido ('Done' con mayúscula):"
python todo.py update 1 Done 1
echo ""

info "Status válido ('done'):"
python todo.py update 1 done 1
echo ""

ok ">>> En E1, 'completed' se podía insertar vía DB directa."
ok ">>> En E2, el Enum rechaza cualquier valor que no esté definido."

# ══════════════════════════════════════════
#  PROTECCIÓN 3: Estados terminales
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 3: Estados terminales bloqueados"
title "=========================================="
echo ""

info "Tarea 1 está en 'done'. Intentar cambiarla a 'pending':"
python todo.py update 1 pending 1
echo ""

info "Intentar cambiar prioridad de tarea terminada:"
python todo.py set-priority 1 urgent 1
echo ""

info "Intentar setear due date en tarea terminada:"
python todo.py set-due 1 2026-04-01 1
echo ""

ok ">>> En E1, no había protección. Se podía modificar una tarea terminada."
ok ">>> En E2, TaskStatus.terminal_states() bloquea cualquier modificación."

# ══════════════════════════════════════════
#  PROTECCIÓN 4: Prioridad con valor entero
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 4: Prioridad ordena correctamente"
title "=========================================="
echo ""

info "Seteamos prioridades:"
python todo.py set-priority 2 high 1
python todo.py set-priority 3 urgent 2
python todo.py set-priority 4 low 1
echo ""

info "Listar por prioridad (Ana, user 1):"
python todo.py list-by-priority 1
echo ""

ok ">>> En E1, ORDER BY priority DESC ordenaba alfabéticamente: urgent > medium > low > high."
ok ">>> En E2, ORDER BY priority_value DESC ordena por valor: URGENT(4) > HIGH(3) > MEDIUM(2) > LOW(1)."

# ══════════════════════════════════════════
#  PROTECCIÓN 5: Prioridad inválida rechazada
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 5: Prioridad inválida rechazada"
title "=========================================="
echo ""

info "Intentar setear prioridad 'critical' (no existe en el Enum):"
python todo.py set-priority 2 critical 1
echo ""

ok ">>> En E1, set_priority aceptaba cualquier string sin validación."
ok ">>> En E2, TaskPriority rechaza valores no definidos."

# ══════════════════════════════════════════
#  PROTECCIÓN 6: Permisos obligatorios
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 6: Permisos obligatorios"
title "=========================================="
echo ""

info "Luis (user 2) intenta modificar tarea de Ana (tarea 2):"
python todo.py update 2 in_progress 2
echo ""

info "Luis (user 2) intenta eliminar tarea de Ana (tarea 4):"
python todo.py delete 4 2
echo ""

ok ">>> En E1, update() y delete() no verificaban permisos."
ok ">>> En E2, TODA operación requiere user_id y valida acceso."

# ══════════════════════════════════════════
#  PROTECCIÓN 7: Overdue usa terminal_states()
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  PROTECCIÓN 7: Overdue usa terminal_states()"
title "=========================================="
echo ""

info "Setear due dates:"
python todo.py set-due 2 2025-01-01 1
python todo.py set-due 3 2025-06-15 2
echo ""

info "Notificaciones de overdue:"
python todo.py notify-overdue
echo ""

info "Cancelar tarea 2 y verificar que ya no aparece como overdue:"
python todo.py update 2 cancelled 1
echo ""

info "Notificaciones de overdue después de cancelar:"
python todo.py notify-overdue
echo ""

ok ">>> En E1, notify_overdue solo excluía status != 'done'. 'cancelled' seguía apareciendo."
ok ">>> En E2, terminal_states() incluye DONE y CANCELLED. Una sola fuente de verdad."

# ══════════════════════════════════════════
#  RESUMEN
# ══════════════════════════════════════════
echo ""
title "=========================================="
title "  RESUMEN COMPARATIVO"
title "=========================================="
echo ""
echo -e "${BOLD}| Bug del E1                        | Protección en E2                           |${NC}"
echo -e "| --------------------------------- | ------------------------------------------ |"
echo -e "| Status como string libre          | TaskStatus Enum — rechaza valores inválidos |"
echo -e "| 'done' hardcodeado en overdue     | TaskStatus.terminal_states()                |"
echo -e "| Priority sort alfabético          | IntEnum con valor numérico                 |"
echo -e "| list_all sin filtro               | Solo list_tasks_for_user(user_id)          |"
echo -e "| update/delete sin permisos        | Toda operación requiere user_id            |"
echo -e "| Tareas terminadas modificables    | Terminal state guard en toda operación     |"
echo -e "| Sharing sin modelo de permisos    | Decisión explícita: no implementar         |"
echo ""
echo -e "${BOLD}${GREEN}Tiempo en debugging: 0${NC}"
echo ""
echo -e "${BOLD}\"La ventaja no está en usar AI."
echo -e "Está en usarla sin perder el control.\"${NC}"
echo ""
