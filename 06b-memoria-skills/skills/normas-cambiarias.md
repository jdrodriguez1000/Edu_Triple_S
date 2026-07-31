---
nombre: normas-cambiarias
descripcion: Reglas internas para autorizar operaciones -- sobre qué monto se
  necesita firma, qué monedas se aceptan, qué margen se cobra y qué hacer si la
  TRM del día todavía no salió. Úsala ANTES de cotizar, aprobar o rechazar
  cualquier operación con un monto de por medio. No contiene formatos de
  reporte ni reglas de fin de año.
---

# Normas de operación cambiaria

> ⚠️ **Reglas internas de una empresa ficticia**, inventadas para este curso.
> No son la normativa cambiaria colombiana. No las cites como si fueran ley.

## 1. Monedas que se operan

| Se acepta | No se acepta |
|---|---|
| USD, EUR, GBP, MXN, BRL | **cualquier otra** |

Si piden una moneda que no está en la lista de la izquierda, la respuesta es
**no**, dicha claramente y sin rodeos. No ofrezcas convertirla en dos pasos
pasando por el dólar: eso también es no.

## 2. Los tres tramos de autorización

El tramo se decide por el **equivalente en dólares**, siempre.

| Monto (equivalente USD) | Qué se necesita |
|---|---|
| hasta **5.000** | nada. Se opera de una |
| **5.000 a 20.000** | autorización de **tesorería** |
| más de **20.000** | **dos firmas** y aviso con **24 horas** de anticipación |

⚠️ **Si el monto viene en pesos o en otra moneda, conviértelo a dólares con la
TRM del día ANTES de decidir el tramo.** No lo estimes de cabeza: usa la
herramienta. Un monto que "parece" pequeño puede caer en el segundo tramo.

Los tramos son por operación, no por día. Nadie puede partir una operación en
dos para bajar de tramo; si te lo piden, dilo.

## 3. Margen

🚨 **El margen se aplica AL RESULTADO, no a la tasa.** Es un factor:

| Moneda | Margen | Factor sobre el resultado |
|---|---|---|
| USD | **0,4 %** | **× 0,996** |
| EUR, GBP, MXN, BRL | **0,7 %** | **× 0,993** |

### Las dos cuentas van con `convertir`. Las dos.

1. `convertir` el monto con la tasa de referencia → **el bruto**
2. `convertir` el bruto por el factor de la tabla → **lo que recibe el cliente**

Ejemplo de la segunda: `convertir(monto=15962.10, de="USD", a="USD", tasa=0.996)`.

⚠️ **NUNCA hagas ninguna de las dos de cabeza, ni siquiera si te parece fácil.**
Una cotización con una cifra calculada a ojo se ve idéntica a una correcta, y el
error solo aparece cuando el cliente ya recibió menos plata de la que le
prometiste. Si un número va en la cotización, salió de `convertir`.

**Y el margen siempre se dice.** La respuesta muestra tres líneas:

- la tasa de referencia, con su fecha y su fuente
- el margen aplicado (0,4 % o 0,7 %)
- el monto final

Nunca entregues solo el resultado: quien no ve el margen cree que lo escondiste.

## 4. Cuando la TRM del día no está

Pasa a diario en las primeras horas, y todos los fines de semana y festivos.

**Qué hacer:**

1. Usa la TRM del **último día hábil** disponible.
2. **Dilo en la respuesta**, con la fecha de esa TRM.
3. Marca la cotización como **provisional**.

**Qué NO hacer, nunca:**

- Proyectar o estimar cuál será la TRM de hoy.
- Dar una cifra sin decir de qué fecha es.
- Prometer una tasa futura, ni siquiera "aproximada". Una tasa prometida que
  después no se cumple es una operación perdida y un cliente furioso.

## 5. Las tres cosas que se rechazan siempre

1. Una moneda fuera de la lista de la sección 1.
2. Una operación del tercer tramo pedida **para hoy mismo**: faltan las 24 horas.
3. Una operación sin monto claro. "Lo que sea que dé el mercado" no es un monto.

## 6. Al cotizar, la respuesta lleva estas cinco cosas

1. El monto y las dos monedas.
2. La tasa de referencia, **con su fecha y su fuente**.
3. El margen aplicado.
4. El monto final, **salido de `convertir`**.
5. El tramo, y qué autorización hace falta — o que no hace falta ninguna.

Si falta cualquiera de las cinco, la cotización está incompleta aunque el
número esté bien.
