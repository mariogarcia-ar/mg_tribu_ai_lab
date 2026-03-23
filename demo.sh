#!/usr/bin/env bash
set -e

echo "=== TODO App Demo ==="
echo ""

# Clean start
rm -f todo.db

echo "--- Crear tareas ---"
python todo.py add "Comprar café"
python todo.py add "Preparar presentación"
python todo.py add "Revisar código"
echo ""

echo "--- Listar tareas ---"
python todo.py list
echo ""

echo "--- Marcar tarea 1 como done ---"
python todo.py update 1 done
echo ""

echo "--- Listar tareas ---"
python todo.py list
echo ""

echo "--- Eliminar tarea 1 ---"
python todo.py delete 1
echo ""

echo "--- Crear usuarios ---"
python todo.py create-user "Ana" "ana@example.com"
python todo.py create-user "Luis" "luis@example.com"
echo ""

echo "--- Asignar tareas a usuarios ---"
python todo.py assign 2 1
python todo.py assign 3 2
echo ""

echo "--- Tareas de Ana ---"
python todo.py list-user 1
echo ""

echo "--- Tareas de Luis ---"
python todo.py list-user 2
echo ""

echo "--- Lista completa ---"
python todo.py list
echo ""

echo "=== Demo finalizada ==="
