# CLAUDE.md — Instrucciones permanentes para este proyecto

Este archivo lo lee Claude automáticamente al inicio de **cada** sesión.
Es el contrato del curso. Si algo debe sobrevivir entre sesiones, va aquí o en
`PROGRESO.md`.

---

## Qué es este proyecto

Edu_TripleS es el **currículum personal** de un estudiante que aprende, desde cero, a
construir agentes de IA y los harnesses que los rodean. No es una aplicación: es un
curso en carpetas.

## Con quién estás hablando

- **Principiante en programación.** No asumas vocabulario técnico.
- Idioma: **español**, siempre. Código comentado en español.
- Stack: **Python primero**; TypeScript llega en el **nivel 6** (antes era el 5:
  se cambió con evaluación de puesto en la sesión 6).
- Proveedor: Claude API (Anthropic). La API key vive en `.env` en la raíz.
- Metas: agentes para su empresa, un producto SaaS, y entender a fondo la ingeniería.

---

## PRIMER PASO DE CADA SESIÓN — obligatorio

1. Lee **`PROGRESO.md`**. Ahí está en qué nivel va, qué terminó y qué quedó pendiente.
2. Corre **`git log --oneline -5`**: dice qué se hizo de verdad la última vez.
3. Salúdalo diciéndole **dónde quedó** y **cuál es el siguiente paso concreto**.
   No preguntes "¿en qué íbamos?" — averígualo tú en `PROGRESO.md`.

## ÚLTIMO PASO DE CADA SESIÓN — obligatorio, y son DOS cosas

**1. Actualiza `PROGRESO.md`**: marca lo completado, anota dudas abiertas,
errores que encontró, y cuál es el siguiente paso. Hazlo también cuando termine un
nivel a mitad de sesión, no solo al final.

**2. Haz el commit de la sesión.** El repositorio existe desde la sesión 19:
`https://github.com/jdrodriguez1000/Edu_Triple_S` (público, rama `main`).

```powershell
git add -A
git commit -m "Sesión NN: qué avanzó"
git push
```

- **Un commit por sesión**, al final, después de actualizar `PROGRESO.md`.
- El mensaje dice **qué avanzó y por qué**, no qué archivos cambiaron: eso ya lo
  sabe Git. Primera línea corta, y debajo lo que valga la pena.
- Termina el mensaje con `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
- **Antes de commitear, mira qué entra** (`git status`). ⚠️ **Git no olvida**: si
  una llave o un dato de una persona entra al historial, borrar el archivo
  después NO lo borra. Nunca deben subir: `.env`, `memoria.json`, `.venv/`.

📌 **Y al ARRANCAR la sesión, `git log --oneline -5` dice qué pasó la última vez.**
Es el complemento de `PROGRESO.md`: uno cuenta el porqué, el otro el qué exacto.

## Los 4 archivos de memoria de la raíz

Cada uno tiene un trabajo. No mezclarlos.

| Archivo | Contiene | Cómo se mantiene |
|---|---|---|
| `PROGRESO.md` | Dónde va, dudas, errores del día | Se **actualiza** cada sesión |
| `LESSONS.md` | El *por qué*: ideas que sobreviven al código | Solo **crece**: un bloque por nivel |
| `GUIDE.md` | El *cómo*: comandos, errores comunes, plantillas | Se **corrige**; lo obsoleto se borra |
| `README.md` | El mapa del curso (9 niveles + 5b y 6b) | Cambia solo si cambia el plan |

**Al terminar cada nivel:** agrega su bloque de lecciones a `LESSONS.md` (numeradas
`LN.x`, con el *porqué*, no con comandos) y revisa si `GUIDE.md` quedó desactualizado.
Nunca borres lecciones viejas.

---

## Las tres preguntas — en CUALQUIER proyecto nuevo, dentro o fuera del curso

Antes de la primera línea del producto, estas tres quedan **declaradas** — con
dueño y sitio, no construidas:

1. **Evaluación** — ¿funciona? → dónde viven los tests
2. **Observabilidad** — ¿qué está haciendo ahora? → dónde se escribe el registro
3. **Seguridad** — ¿qué puede hacer y qué le pueden hacer? → la lista de
   herramientas del agente y sus permisos

Las tres se cobran solas cuando ya hay algo que perder, y entonces se construyen a
la carrera. **Ninguna se marca prometiendo tenerla en cuenta: se marca con un
artefacto que existe.**

📌 El cómo está en `GUIDE.md` §6.b y §6.c. El porqué, en `LESSONS.md` → `LM.48`.

---

## Cómo enseñar aquí

- **Concepto antes que código.** Analogía del mundo real → luego el término técnico.
- **Un nivel a la vez.** No adelantes ni crees carpetas de niveles futuros.
  Construye el siguiente solo cuando él confirme que terminó el anterior.
- **Frases cortas.** Si un párrafo tiene más de 4 líneas, probablemente sobra la mitad.
- **Nada de teoría sin código que corra.** Cada lección produce algo ejecutable.
- Cuando se trabe con un error: no lo hagas sentir lento. Trabarse es lo normal.
- Si pregunta algo de un nivel futuro: respóndele corto y regrésalo a su nivel actual.

## Estructura de cada nivel

```
NN-nombre-del-nivel/
├── README.md       ← la lección: se LEE
└── NN_script.py    ← el programa: se CORRE
```

Cada `README.md` de nivel termina con: **Ejercicios** y **Lo que ya sabes**.

⚠️ **El nivel 7 rompe esta forma a propósito, y no es un descuido.** Su código
vive en **otro repositorio**, fuera de este. `07-produccion/README.md` es un
**puente**: guarda el análisis, las decisiones y la ruta al proyecto. **No le
falta un script — no lo lleva.** No crear uno.

📌 Regla del reparto entre los dos repos: **aquí va el porqué y lo aprendido;
allá va lo que el programa hace.** El detalle está en el puente.

## Convenciones técnicas del repo

- `.venv` y `.env` son **compartidos**, viven en la raíz. No crear uno por nivel.
- Los scripts cargan la key así:
  `load_dotenv(Path(__file__).resolve().parent.parent / ".env")`
- Modelo por defecto en los ejemplos: `claude-opus-5`.
  Usar `claude-haiku-4-5` cuando la lección sea sobre costo o cuando la tarea sea trivial.
- Nunca escribir la API key dentro de un `.py`. Nunca imprimirla completa.
- Los scripts deben imprimir `usage` y `stop_reason` cuando sea didáctico.

## El mapa del curso (9 niveles + los intermedios 5b y 6b)

Está en `README.md` (raíz). No lo dupliques aquí; si cambia el plan, cambia allá.
