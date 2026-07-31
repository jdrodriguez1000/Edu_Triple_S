---
nombre: cierre-de-ano
descripcion: La regla de valoración de fin de año -- con qué tasa se valoran
  los saldos al 31 de diciembre (que NO es la del día), la sección extra y el
  archivo aparte que lleva el cierre de diciembre, y el plazo de entrega. Úsala
  cuando la fecha sea diciembre o 31 de diciembre, o cuando hablen de cierre
  anual o valoración de saldos. El formato de las cinco secciones del reporte
  NO está aquí: está en reporte-mensual.
---

# Cierre de año

> ⚠️ **Reglas internas de una empresa ficticia**, inventadas para este curso.
> No son la norma contable colombiana ni una regla tributaria real.

## 🚨 Diciembre lleva DOS cierres, no uno

Es el error que se comete todos los años:

| | Qué es | Con qué tasa |
|---|---|---|
| **Cierre mensual** | el reporte normal del mes | la TRM de cada operación |
| **Valoración anual** | los **saldos** que quedan vivos al 31/12 | **una sola tasa para todos** |

Son dos cosas distintas en el mismo mes. **Diciembre necesita las dos**, y el
formato del reporte mensual está en la skill `reporte-mensual`.

## La tasa de valoración

> Los saldos al 31 de diciembre se valoran con la **TRM del último día hábil de
> diciembre**, no con la del 31 si ese día cae en fin de semana o festivo.

Se aplica **la misma tasa a todos los saldos**, sin importar en qué fecha se
originó cada uno. Esa es la diferencia de fondo con el reporte mensual, donde
cada operación lleva la tasa de su día.

**Cómo se consigue:** con `trm_en_fecha`, pidiendo el último día hábil de
diciembre. Si esa fecha cayó en festivo y la herramienta no devuelve nada,
retrocede un día hábil y **dilo en el reporte**. No uses la del 30 sin avisar,
y no la promedies con nada.

## La sección 6

El reporte de diciembre lleva las cinco secciones de siempre **más una sexta**,
al final, titulada `Valoracion anual`, con esta tabla:

```
Moneda | Saldo | Tasa de valoracion | Valor COP | Diferencia vs. registro
```

- La tasa de valoración es **la misma en todas las filas**. Si en tu tabla hay
  dos tasas distintas, está mal.
- La diferencia se redondea a **pesos completos**, y lleva signo: `+` o `-`.
- Si el saldo de una moneda es cero, la fila **no se pone**.

## El archivo aparte

Diciembre genera **dos** archivos, no uno:

```
cierre-2026-12.md      <- el mensual de siempre
cierre-anual-2026.md   <- solo la seccion 6, sola
```

El anual es una copia de la sección 6 como documento independiente, porque lo
pide contabilidad y no quiere leer el mes entero.

## Plazo

Antes del **15 de enero**. Si te lo piden después, hazlo igual, pero deja dicho
en el resumen que va fuera de plazo.

## Las tres equivocaciones de todos los años

1. **Usar la TRM del 31** cuando el 31 no fue hábil. Da una cifra distinta y
   nadie la revisa hasta la auditoría.
2. **Valorar cada saldo con la tasa de su fecha.** Eso es el reporte mensual,
   no la valoración anual.
3. **Entregar solo el mensual** y creer que diciembre ya quedó cerrado.
