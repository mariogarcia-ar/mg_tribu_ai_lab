# MG TRIBU AI Lab

Laboratorio práctico sobre desarrollo asistido por AI, diseñado para mostrar la diferencia entre generar código rápido y construir sistemas gobernados.

## Objetivo

Demostrar que el problema del desarrollo con AI no es la velocidad — es la falta de gobierno. A través de dos encuentros de live coding, los participantes experimentan cómo las decisiones implícitas de la AI generan deuda técnica invisible, y cómo un modelo System-Centric elimina ese problema.

## Estructura

El laboratorio se divide en dos encuentros que construyen el mismo sistema (una TODO app que escala a multi-usuario), pero con procesos radicalmente distintos.

### [Encuentro 1 — "Cómo se rompe un sistema aunque parezca que funciona"](docs/encuentro1/readme.md)

Enfoque **Code-Centric**: se genera código con Claude y GitHub Copilot sin decisiones previas. El sistema funciona al principio, pero cada feature nueva introduce inconsistencias hasta llegar a un loop infinito de fixes.

**Etapas:**
1. TODO básico funcional
2. Módulo de usuarios (primer escalamiento)
3. Múltiples usuarios con ambigüedades
4. El loop infinito — cada fix rompe algo nuevo

### [Encuentro 2 — "El mismo sistema. Sin el loop."](docs/encuentro2/readme.md)

Enfoque **System-Centric**: se recorre el mismo camino, pero aplicando el framework **Think / Decide / Execute / Verify** en cada etapa. Las decisiones se documentan antes de escribir código.

| Fase | Quién | Qué produce |
|---|---|---|
| **Think** | Humano | Preguntas sin responder |
| **Decide** | Humano | Reglas explícitas documentadas |
| **Execute** | AI dentro del marco definido | Código que respeta las reglas |
| **Verify** | Humano | Confirmación de que el código cumple lo decidido |

## Stack

- **Lenguaje:** Python
- **Herramientas AI:** Claude + GitHub Copilot
- **Modalidad:** Live coding
- **Dependencias:** sqlite3, argparse (sin dependencias externas)

## Audiencia

- **Product owners / decisores:** observar cuándo el instructor frena y qué pregunta — entender el valor de las decisiones explícitas.
- **Desarrolladores senior:** observar qué cambia en el código como resultado de cada decisión documentada.

## Idea central

> "La ventaja no está en usar AI. Está en usarla sin perder el control."
