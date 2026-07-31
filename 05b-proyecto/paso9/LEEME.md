# `paso9/` — la evidencia de una medición terminada

Estos cuatro archivos son las bitácoras de las corridas del **paso 9** (sesiones
15 y 16). Están aquí archivados, no borrados, por una razón concreta:

> **La tabla de comparación de los tres modelos que está en `PROGRESO.md` sale
> de estos archivos.** Sin ellos, esos números dejan de estar *medidos* y pasan
> a estar *recordados* — que es exactamente la diferencia que enseña este nivel.

## Qué es cada uno

| Archivo | Qué es | Gasto |
|---|---|---|
| `registro.jsonl` | La corrida de la **sesión 15**, el paso 8 | $0,14956 |
| `registro_claude-opus-5.jsonl` | **Copia byte a byte** del anterior | $0,14956 |
| `registro_claude-sonnet-5.jsonl` | Corrida real de la sesión 16 | $0,089436 |
| `registro_claude-haiku-4-5.jsonl` | Corrida real de la sesión 16 | $0,028357 |

Las cuatro son las mismas **tres preguntas** y las mismas **7 vueltas**.

## Por qué hay dos archivos idénticos

`registro.jsonl` es el original de la sesión 15, y **su línea 13 está citada por
nombre en `PROGRESO.md`** como la evidencia del defecto del permiso:

```json
{"evento": "permiso", "herramienta": "convertir", "concedido": true}
```

A nadie le preguntaron por `convertir` —es "libre"—, así que ese `true` era una
afirmación falsa. De ahí nació el campo `motivo`.

Cuando la sesión 16 empezó a nombrar los registros por modelo, ese archivo se
**copió** en vez de renombrarse, para no romper la cita.

## ⚠️ Lo que le falta al de opus, y hay que saberlo

Mira la primera línea de cada uno:

```
opus-5     precio_entrada: None    precio_salida: None
sonnet-5   precio_entrada: 3.0     precio_salida: 15.0
haiku-4-5  precio_entrada: 1.0     precio_salida: 5.0
```

**El archivo de opus no sabe con qué precios se calculó su propio costo.** Es
anterior al `anotar("inicio")` que guarda los precios, y se copió después.

No invalida el $0,14956 —los tokens están, línea por línea, y la cuenta se
rehace a mano—, pero conviene decirlo: **dos de las tres filas de la tabla
pueden demostrar su aritmética; la de opus hay que creérsela.**

Es justo el agujero que el `CATALOGO` vino a tapar, sobreviviendo en el único
archivo que se **copió** en vez de generarse.

## Por qué se archivaron

Porque `anotar()` abre en modo **añadir**. Con MODELO en `claude-haiku-4-5`, un
`python agente.py` le habría pegado 23 líneas nuevas al archivo de haiku,
debajo de las del paso 9, **sin error y sin aviso**. La medición habría quedado
mezclada con otra corrida y ya no se podría separar con confianza.

> **Un artefacto cerrado se guarda donde nadie lo pise.** Nombrar el archivo por
> modelo resolvió *quién* corrió; nunca resolvió *cuándo*.
