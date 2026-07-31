# Nivel 2 — La conversación con memoria

En el nivel 1 descubriste que **la API no tiene memoria**. Aquí construyes la
memoria tú. Es tu primera pieza de harness de verdad.

Y descubres el primer problema serio de todo agente: esa memoria **crece**, y
crecer cuesta dinero y termina rompiéndose.

Antes de empezar, desde la raíz:

```powershell
.\.venv\Scripts\Activate.ps1
cd 02-conversacion
```

---

## 2.1 — El chat que recuerda

```powershell
python 01_chat.py
```

Habla con él unos 4 o 5 turnos. Prueba decirle tu nombre y luego preguntarle
cuál es.

### La idea completa cabe en una lista

```python
historial = []                                        # la memoria

historial.append({"role": "user", "content": entrada})      # lo que dices tú
respuesta = cliente.messages.create(messages=historial)      # se manda ENTERO
historial.append({"role": "assistant", "content": texto})    # lo que dijo Claude
```

Eso es todo. No hay nada más. Ese `append` de la última línea es la memoria:
si lo borras, el chat vuelve a ser amnésico.

**Analogía:** el modelo es un sabio con amnesia total, encerrado en un cuarto.
Cada vez que le hablas, le pasas por debajo de la puerta la transcripción
completa de todo lo que se han dicho hasta ahora. Él lee todo, responde una vez,
y olvida. La transcripción la guardas tú, afuera.

### La consecuencia incómoda

Si le pasas la transcripción completa cada vez... **pagas la transcripción
completa cada vez.** Mira la columna `entrada` que imprime el script: sube en
cada turno aunque tus mensajes sean igual de cortos.

---

## 2.1b — Lo que se midió de verdad (corrida real, 5 turnos)

| turno | entrada | salida |
|---|---|---|
| 1 | 61 | 99 |
| 2 | 185 | 149 |
| 3 | 362 | 180 |
| 4 | 570 | 217 |
| 5 | 808 | 180 |

### La fórmula sale de la resta

Cada turno paga lo del turno anterior, más lo que respondió Claude, más lo que
escribiste tú:

| turno | entrada | = entrada anterior | + salida anterior | + tu mensaje |
|---|---|---|---|---|
| 2 | 185 | 61 | 99 | ~25 |
| 3 | 362 | 185 | 149 | ~28 |
| 4 | 570 | 362 | 180 | ~28 |
| 5 | 808 | 570 | 217 | ~21 |

Cuadra en los cuatro saltos. **No hay cobro oculto: la entrada de un turno es
literalmente todo lo anterior sumado.**

### El dato inesperado: no eres tú quien llena el contexto

Mira la última columna. El usuario aportó ~25 tokens por turno. Claude aportó
entre 99 y 217.

**El historial crece sobre todo por lo que responde Claude.** De ahí una
consecuencia práctica: un `SYSTEM` que pida respuestas cortas no solo se lee
más rápido, te abarata **todos los turnos siguientes**.

### Resultado del ejercicio 1

Al comentar `historial.append({"role": "assistant", ...})`:

| | memoria completa | sin guardar las respuestas |
|---|---|---|
| entrada turno 1 | 61 | 58 |
| entrada turno 4 | **570** | **116** |
| crecimiento | ~230/turno | ~19/turno |

Cinco veces más barato. Pero fíjate en **lo que se rompe**, que no es lo obvio:

- Le preguntaron *"¿en qué ciudad vivo?"* y respondió **correcto**
- Y aun así saludó *"¡Hola Juan!"* **cuatro veces seguidas**
- Y repitió la misma recomendación en tres turnos distintos

No es amnesia total. Es un corte limpio:

> **Recuerda los datos** (lo que dijo el usuario, que sí sigue en la lista)
> **Olvida el diálogo** (que ya saludó, que ya respondió eso)

Te saluda de nuevo porque, desde donde él mira, acabas de llegar: él nunca ha
dicho nada.

### El bug del contador

Ese mismo ejercicio destapó un error en este script. El contador decía:

```python
f"[turno {len(historial) // 2} | ..."
```

Ese `// 2` asume que **cada turno mete 2 mensajes**. Al dejar de guardar las
respuestas entra 1 por turno, y el contador imprimió `0, 1, 1, 2`. No falló:
**calculó mal con toda confianza.**

> **Regla:** si quieres contar turnos, cuenta turnos. No deduzcas un dato de la
> forma de una estructura que puede cambiar.

---

## 2.2 — La cuenta que crece sola

```powershell
python 02_ventana.py
```

Seis preguntas, todas cortas, todas parecidas. Esto se midió de verdad
(**corrida A**; más abajo se compara con una segunda corrida):

| turno | tokens de entrada |
|---|---|
| 1 | 43 |
| 2 | 122 |
| 3 | 212 |
| 4 | 302 |
| 5 | 376 |
| 6 | 469 |

**Once veces más caro el turno 6 que el turno 1**, preguntando lo mismo de largo.

El motivo es que cada turno paga por todos los anteriores:

```
turno 1 paga:  P1
turno 2 paga:  P1 + R1 + P2
turno 3 paga:  P1 + R1 + P2 + R2 + P3
```

### Dos corridas del mismo script

El estudiante lo corrió aparte y dio otros números. Comparar las dos enseña más
que cualquiera de las dos sola:

| | corrida A | corrida B |
|---|---|---|
| entrada turno 1 | 43 | **43** |
| entrada total | 1.524 | 1.669 |
| salida total | 455 | 482 |

**El turno 1 es idéntico** porque la entrada es determinista: es texto que ya
existe (system + pregunta 1). Contarlo da siempre lo mismo. Lo que varía es la
salida — y como la salida de hoy es la entrada de mañana, la diferencia se
propaga hacia adelante.

### Cada token de salida se paga muchas veces

Mira las dos últimas filas. Claude generó **27 tokens de más** en la corrida B.
Eso costó **145 tokens de entrada de más**. Un factor de ~5x.

Lógico: un token generado en el turno 1 se reenvía en los turnos 2, 3, 4, 5 y 6.

> Por eso un `SYSTEM` que pida respuestas cortas no ahorra una vez.
> **Ahorra en cada turno que venga después.**

### La forma del crecimiento depende de las respuestas

Los incrementos de entrada por turno fueron: 99, 101, 81, 82, 105. **Planos.**
Aquí la entrada crece en *línea recta*, no acelerando.

Y sin embargo en `01_chat.py` los incrementos fueron 124, 177, 208, 238 —
cada vez más altos. ¿Por qué la diferencia?

| | `01_chat.py` | `02_ventana.py` |
|---|---|---|
| SYSTEM | sin límite de largo | *"máximo 2 frases"* |
| respuestas | 99 → 217, crecen | ~71–93, planas |
| escalones | cada vez más altos | iguales |

**El escalón mide lo que mida la respuesta anterior.** Si las respuestas se
alargan, la entrada se dispara; si se mantienen, crece recto.

En los dos casos el **acumulado** crece más rápido que los turnos, porque cada
turno paga por todos los anteriores.

> Esta versión corrige una que estaba en el script y decía que la entrada
> "crece como una escalera cada vez más alta" siempre. Era una generalización
> hecha desde un solo caso (`01_chat.py`). Los datos de las dos corridas de
> `02_ventana.py` la desmienten.

### Y hay un límite más duro que el dinero: la ventana de contexto

La **ventana de contexto** es cuánto texto cabe en una sola llamada. Es un techo
físico, no una recomendación.

| Modelo | Ventana |
|---|---|
| `claude-opus-5` | 1.000.000 tokens |
| `claude-sonnet-5` | 1.000.000 tokens |
| `claude-haiku-4-5` | 200.000 tokens |

Cuando el historial pasa ese número, la API **no responde: falla**. No hay
degradación suave. Por eso todo agente que corre mucho rato necesita una
política para recortar.

---

## 2.3 — Las tres políticas para recortar

```powershell
python 03_recortar.py
```

Compara tres formas de meter el mismo historial en la llamada. Casi todo el
script es **gratis**: usa `count_tokens`, que cuenta sin generar.

```python
cliente.messages.count_tokens(model=..., system=..., messages=...).input_tokens
```

> Guárdate ese método. Sirve para saber cuánto vas a pagar **antes** de pagarlo.

**Por qué es gratis:** generar texto es trabajo de GPU token a token — eso es lo
caro. Contar es partir el texto según un diccionario fijo, sin modelo pensando.
Pesar el paquete es gratis; enviarlo se paga por peso.

Tres letras pequeñas, verificadas en la documentación oficial:

- **Gratis ≠ ilimitado.** Tope de 2.000 peticiones/minuto en el nivel inicial,
  con un límite propio, independiente del de `messages.create`
- **Es un estimado.** El conteo real "puede diferir en una cantidad pequeña"
- **Solo cuenta la entrada.** Los tokens de salida no existen hasta que el
  modelo responde — por eso en `02_ventana.py` la entrada coincidió entre
  corridas y la salida nunca

### Resultados reales de la corrida

| Estrategia | Mensajes | Tokens | ¿Recuerda el turno 1? |
|---|---|---|---|
| Historial completo | 19 | 418 | ✅ sí |
| Ventana deslizante (últimos 4) | 5 | 127 | ❌ **no** |
| Resumen + últimos 4 | 7 | 308 | ✅ sí |

La prueba de fuego fue preguntarle un dato que solo aparecía en el primer turno
(el nombre de la usuaria). La ventana deslizante contestó:

> *"No tengo esa información. Es la primera vez que conversamos en esta sesión."*

No se equivocó ni alucinó. Simplemente **ese turno ya no se le estaba
mandando**. Olvidar no es un bug del modelo: es una decisión de tu código.

### Otra vez: lo determinista coincide, lo generado no

Dos corridas del script en máquinas distintas:

| estrategia | corrida A | corrida B |
|---|---|---|
| 1. completo | **418** | **418** |
| 2. ventana deslizante | **127** | **127** |
| 3. resumen + recientes | 308 | 293 |

Las dos primeras coinciden **al token**: son texto que ya existía. La tercera
varía porque el resumen lo genera el modelo. Tercer script del nivel donde
aparece lo mismo — ya no es casualidad, es una propiedad del sistema.

### El modelo te recita su propia ventana

Al preguntarle a la estrategia 2 quién era Marta:

> *"No tengo esa información. En esta conversación solo me has preguntado sobre
> errores de sintaxis y cómo leer mensajes de error."*

Ve a mirar los últimos 4 mensajes del historial en el script. Son exactamente
esos dos temas.

No está confundido ni alucinando: **está describiendo con precisión la lista que
recibió.** Su memoria *es* esa lista, y nada más.

### Lo que la tabla no muestra: el resumen cuesta

La columna "ahorro" compara tokens de entrada, pero **la estrategia 3 necesita
una llamada extra** para generar el resumen, y esa llamada no aparece en ninguna
columna. El script ahora la mide:

| | |
|---|---|
| Costo de generar el resumen | $0.001077 |
| Ahorro por turno | $0.000117 |
| **Se paga solo en** | **~9 turnos** |

Generar el resumen cuesta **9 veces lo que ahorra en un turno**. Si la
conversación termina en el turno 3, resumir fue tirar dinero. Si llega al 50,
fue la mejor decisión del harness.

> Eso convierte una intuición ("resumir ahorra") en una pregunta de ingeniería:
> **¿cuánto va a durar esta conversación?** Si no lo sabes, no sabes si tu
> optimización es una optimización.

Y es un **techo**: como el historial completo sigue creciendo, el ahorro real
por turno también crece. En la práctica se paga antes de los 9.

---

> Existe una **cuarta estrategia**, la que apareció sola en el ejercicio 1:
> guardar únicamente los mensajes del usuario (sección 2.1b). Este script no la
> mide, así que no lleva fila en la tabla. Si quieres su número exacto, añádela
> tú — es el ejercicio 6.

### El detalle que casi te engaña

En esa tabla el resumen ahorra *menos* que la ventana (26% vs 70%). Parece que
la estrategia elegante es la peor. No lo es: la conversación es de 8 turnos, y
el resumen pesa casi lo mismo que lo que resume.

La diferencia está en cómo crecen:

- el historial completo crece **sin techo**
- el resumen se mantiene **más o menos del mismo tamaño**

Con 8 turnos no se nota. Con 80, es la diferencia entre funcionar y fallar.

Y el resumen **no es gratis**: cuesta una llamada extra cada vez que recortas.
Pagas tokens hoy para no pagar la conversación entera mañana.

### Esto ya lo has visto

Cuando Claude Code dice *"compactando conversación"*, está haciendo la
estrategia 3. Es el mismo mecanismo que acabas de escribir a mano.

---

## Ejercicios (haz al menos 2 antes de seguir)

1. ✅ **Hecho** — En `01_chat.py`, comenta la línea que hace
   `historial.append({"role": "assistant", ...})`. Habla 3 turnos.
   Predice primero si la entrada seguirá creciendo, y luego compruébalo.
   Resultado y análisis en la sección **2.1b**. (Acuérdate de descomentarla
   después.)
2. En `01_chat.py`, cambia `MODELO` a `"claude-opus-5"` y ten la misma
   conversación de 4 turnos. Compara los tokens de salida contra Haiku.
3. En `03_recortar.py`, cambia `ultimos=4` a `ultimos=2` y a `ultimos=10`.
   ¿En qué punto la ventana deslizante deja de recordar a Marta?
4. En `03_recortar.py`, empeora a propósito el prompt de `resumir()`: pídele
   solo *"lista los temas"*. Vuelve a correr. ¿Sigue sabiendo quién es Marta?
   Esto te enseña que **la calidad del resumen es parte del harness**.
5. Usa `count_tokens` solo, en un script de 5 líneas, para medir cuántos tokens
   pesa el `README.md` de este nivel. No cuesta nada.
6. En `03_recortar.py`, agrega la **cuarta estrategia** a la comparación: filtra
   el historial dejando solo los mensajes con `role == "user"`. Mídela con
   `count_tokens` (gratis) y ponla en la tabla. ¿Cuánto ahorra de verdad?
   ¿Responde bien la pregunta sobre Marta?

---

## Lo que ya sabes

- La memoria de un chat es **una lista que tú administras**, no algo del modelo
- Cada turno reenvía todo, así que el acumulado crece más rápido que los turnos
- La forma de ese crecimiento **depende del largo de las respuestas**: planas →
  la entrada crece recto; cada vez más largas → se dispara
- La **ventana de contexto** es un techo duro; pasarlo es un error, no una molestia
- `count_tokens` mide el costo **antes** de pagarlo, gratis
- El historial crece sobre todo **por lo que responde el modelo**, no por lo que
  escribes tú
- **La entrada es determinista; la salida no.** Dos corridas del mismo script dan
  el mismo turno 1 y se separan a partir del turno 2
- **Un token de salida se vuelve a pagar como entrada en cada turno siguiente.**
  Medido: 27 tokens de salida de más costaron 145 de entrada de más
- **Resumir cuesta una llamada extra que tarda ~9 turnos en pagarse sola.** Si
  no sabes cuánto va a durar la conversación, no sabes si te conviene
- Una tabla de comparación puede ser correcta y **engañosa a la vez** si deja
  fuera un costo. Pregunta siempre qué columna falta
- Recortar el historial es una decisión de diseño con tres opciones clásicas:
  completo, ventana deslizante, resumen — y ninguna es gratis
- Hay una cuarta, que descubriste sin querer en el ejercicio 1: **guardar solo
  los mensajes del usuario.** Baratísima, conserva los hechos, y destruye la
  coherencia del diálogo
- Un contador mal derivado **no lanza error: miente**. Los bugs que no fallan
  son los más caros de encontrar

**Siguiente:** nivel 3 — el primer agente de verdad. Le vas a dar a Claude una
herramienta que **tu código ejecuta**, y vas a construir el bucle agéntico
completo. Ahí empieza lo bueno.
