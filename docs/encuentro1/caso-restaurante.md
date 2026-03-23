# El restaurante sin receta

Analogía para explicar por qué el sistema se rompe sin decisiones explícitas.

---

## La historia

**Día 1** — Un cliente pide una milanesa. El chef la hace con pan rallado fino. Funciona.

**Día 2** — Contratan otro chef. Hace la milanesa con pan rallado grueso. También funciona.

**Día 3** — El dueño dice "agreguen milanesa napolitana al menú". El chef 1 pone la salsa encima del pan fino. El chef 2 pone la salsa abajo del pan grueso. Los dos dicen que "la milanesa" es la base.

**Día 4** — Un cliente se queja: "esta no es la milanesa que pedí la semana pasada". Nadie sabe cuál es "la correcta" porque **nunca escribieron la receta**.

**Día 5** — Intentan estandarizar. Pero cada plato del menú que usa "milanesa" como base depende de una versión distinta. Cada fix rompe otro plato.

---

## Ahora en código

```
Día 1:  status = "done"        ← funciona
Día 2:  status = "completed"   ← también funciona
Día 3:  notify_overdue() pregunta: ¿está terminada?
        → busca "done"
        → "completed" no es "done"
        → tarea terminada aparece como vencida
Día 4:  fix: reemplazar "completed" → "done"
        → pero "cancelled" también es terminada
        → nadie lo escribió
Día 5:  cada fix rompe algo porque no hay receta
```

---

## El problema real

El problema nunca fue la milanesa. El problema es que **no hay receta**.

En código, la receta es una decisión explícita:

```
Estados terminales: done, cancelled.
Definido en: un solo lugar.
Regla: ninguna tarea en estado terminal puede modificarse.
```

Sin esa decisión, cada persona (o cada IA) inventa su propia versión. Y cuando las versiones chocan, empieza el loop infinito de fixes.

---

> "No podés evolucionar lo que no podés explicar."
