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
title "  TODO App Demo — Encuentro 1, Etapa 3"
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

# ─── Resumen ───
title "=========================================="
title "  RESUMEN: Decisiones implícitas"
title "=========================================="
echo ""
error "  1. Status como string libre       → 'done' vs 'completed' coexisten"
error "  2. Priority como string libre      → 'high' != 'High', sort incorrecto"
error "  3. list() sin filtro de usuario    → Visibilidad total, permisos ignorados"
error "  4. Dos caminos para update/delete  → Con y sin permisos en el mismo sistema"
echo ""
error "  Nadie decidió estas cosas. El sistema las decidió por nosotros."
echo ""
title "=========================================="
echo ""
