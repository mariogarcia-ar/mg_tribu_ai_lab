# Quickstart — TODO CLI App

## Requisitos

- Python 3.8+
- No requiere dependencias externas

## Instalación

```bash
git clone <repo-url>
cd mg_tribu_ai_lab
git checkout encuentro1
```

## Uso

### Crear una tarea

```bash
python todo.py add "Comprar café"
```

### Listar tareas

```bash
python todo.py list
```

Salida esperada:

```
[1] Comprar café (pending) - 2026-03-23T10:00:00
```

### Marcar como done

```bash
python todo.py update 1 done
```

### Volver a pending

```bash
python todo.py update 1 pending
```

### Eliminar una tarea

```bash
python todo.py delete 1
```

## Base de datos

La app crea automáticamente un archivo `todo.db` (SQLite) en el directorio actual la primera vez que se ejecuta. No se necesita configuración previa.

## Estructura de una tarea

| Campo       | Tipo   | Descripción                        |
|-------------|--------|------------------------------------|
| id          | int    | Autoincremental                    |
| title       | text   | Título de la tarea                 |
| status      | text   | `pending` o `done`                 |
| created_at  | text   | Fecha de creación (ISO 8601)       |
