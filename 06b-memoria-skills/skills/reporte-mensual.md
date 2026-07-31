---
nombre: reporte-mensual
descripcion: El formato obligatorio del reporte de cierre de mes -- las cinco
  secciones, en qué orden van, cómo se redondea cada cifra, cómo se nombra el
  archivo y qué nota al pie es obligatoria. Úsala cuando pidan armar, guardar o
  revisar el cierre de un mes. NO cubre el cierre de año, que usa otra tasa y
  agrega una sección: eso está en cierre-de-ano.
---

# Reporte de cierre mensual

> ⚠️ **Reglas internas de una empresa ficticia**, inventadas para este curso.
> No son la normativa colombiana ni la práctica de ninguna empresa real.

## La regla que manda sobre todas

El reporte **se guarda en un archivo** con `guardar_reporte`. **Nunca** se pega
completo en la conversación. Al usuario se le responde con un resumen de máximo
tres líneas y el nombre del archivo donde quedó.

## Nombre del archivo

```
cierre-AAAA-MM.md
```

Todo en minúsculas, mes con dos dígitos: `cierre-2026-07.md`.
Si el archivo ya existe, **no lo sobrescribas**: avisa y pide confirmación.

## Las cinco secciones, en este orden

El orden no es sugerencia. Quien lo lee lo lee siempre igual.

| # | Sección | Qué va |
|---|---|---|
| 1 | **Encabezado** | Mes y año en letras, y la fecha en que se generó |
| 2 | **Resumen** | **Una sola frase.** Cuántas operaciones y por cuánto en total |
| 3 | **Operaciones** | La tabla. Ver abajo |
| 4 | **Tasa de referencia** | Qué TRM se usó, de qué fecha, y si es oficial o de mercado |
| 5 | **Nota al pie** | El texto fijo. Ver abajo |

## La tabla de la sección 3

Columnas, en este orden: `Fecha | Moneda | Monto origen | Tasa | Monto COP`.

- Se ordena por **monto COP, de mayor a menor**. Nunca por fecha.
- La última fila es el **total**, y solo tiene la columna `Monto COP` llena.

## Redondeo

| Qué | Cómo |
|---|---|
| Montos en COP | **sin decimales**, con punto de miles: `4.318.900` |
| Montos en moneda extranjera | **2 decimales**: `1.250,00` |
| Tasas | **2 decimales**: `4.102,55` |
| Porcentajes | **1 decimal**: `3,4 %` |

## Datos que faltan

Si no tienes una cifra, escribe **`sin dato`** en la celda.

- Nunca dejes una celda vacía: parece un error de formato y nadie sabe si faltó
  el dato o falló el reporte.
- Nunca la estimes ni la deduzcas de las otras filas. Un reporte con una cifra
  inventada es peor que un reporte incompleto, porque no se nota.

## La nota al pie (texto exacto, sección 5)

```
Cifras calculadas con la TRM indicada en la seccion 4. Documento interno de
control. No constituye una cotizacion en firme ni un comprobante contable.
```

Va siempre, aunque el reporte tenga una sola operación.

## Antes de guardar, revisa estas cuatro

1. ¿Están las cinco secciones, en orden?
2. ¿La tabla está ordenada por monto COP descendente, con fila de total?
3. ¿La sección 4 dice **fecha** y **fuente** de la tasa, no solo el número?
4. ¿Está la nota al pie, palabra por palabra?

Si alguna falla, arréglala antes de llamar a `guardar_reporte`. Un reporte mal
formado ya guardado hay que volverlo a hacer entero.
