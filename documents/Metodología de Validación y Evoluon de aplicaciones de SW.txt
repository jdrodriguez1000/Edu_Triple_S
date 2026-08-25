# Metodología de Evolución y Construcción de una Aplicación de Software

## 1. Propósito

Esta metodología define un enfoque incremental para concebir, validar, construir y evolucionar aplicaciones de software.

Su propósito principal es reducir progresivamente el riesgo de inversión, evitando construir una solución completa antes de tener evidencia suficiente de que:

1. La solución propuesta tiene sentido para el usuario.
2. El usuario puede utilizarla.
3. El software construido entrega valor real.
4. Los usuarios adoptan y utilizan la solución.
5. Existe evidencia suficiente para continuar invirtiendo en su evolución.

La metodología se basa en seis conceptos principales:

- PROTOTIPO
- WSLT
- GRTH
- MVP
- EVOL
- RELEASE OBJETIVO

El modelo general es:

**PROTOTIPO → WSLT → GRTH → MVP → EVOL → RELEASE OBJETIVO**

El Release Objetivo no representa necesariamente el final de la vida del producto. Después de este puede continuar existiendo EVOL.

---

# 2. Filosofía general

La metodología parte de una premisa fundamental:

> **No debemos realizar una inversión mayor hasta obtener evidencia suficiente que justifique realizarla.**

Por esta razón, la inversión aumenta progresivamente:

**Prototipo → MVP → Evolución**

Cada etapa responde una pregunta diferente.

### Prototipo

> ¿La solución propuesta tiene sentido para el Actor Generador?

### MVP

> ¿La solución construida realmente es adoptada y utilizada por el Actor Generador?

### EVOL

> ¿Cómo aumentamos el valor de una solución que ya demostró adopción?

Esto permite que una iniciativa pueda detenerse tempranamente si la evidencia demuestra que no vale la pena continuar.

---

# 3. Principio del Actor Generador

La metodología comienza con el Actor Generador.

El Actor Generador es quien realiza la acción principal que da origen al proceso de la aplicación.

La razón es sencilla:

> **Si el Actor Generador no existe, no necesita la solución o no está dispuesto a utilizarla, no existe una razón fundamental para construir la aplicación.**

Por esta razón, el primer prototipo y el MVP se concentran normalmente en este actor.

---

# 4. Taxonomía de actores

La metodología utiliza seis tipos de actores.

## 4.1. Actor Generador

Es quien realiza la acción principal que da origen al proceso.

Ejemplo:

Un cliente que solicita una recolección de material reciclable.

---

## 4.2. Actor Coordinador

Es quien recibe las acciones o solicitudes generadas y coordina los recursos, personas y actividades necesarias para ejecutarlas.

Ejemplo:

Un analista de logística que recibe solicitudes y organiza las recogidas.

---

## 4.3. Actor Ejecutor

Es quien realiza directamente la actividad generada por el proceso.

Ejemplo:

Un conductor o recolector que realiza físicamente la recogida.

---

## 4.4. Actor Supervisor

Es quien utiliza la información generada por la aplicación para supervisar resultados, evaluar desempeño e intervenir en la toma de decisiones.

Ejemplo:

Un gerente de operaciones que analiza el comportamiento de las recogidas.

---

## 4.5. Actor Administrador de Plataforma

Es quien administra la plataforma desde el punto de vista técnico y operativo.

Puede administrar:

- usuarios;
- permisos;
- configuraciones;
- parámetros;
- catálogos;
- integraciones;
- elementos técnicos de la plataforma.

No necesariamente existe en todas las aplicaciones.

---

## 4.6. Actor Integrador

Es un sistema, plataforma o servicio externo que intercambia información o ejecuta acciones mediante una integración.

Ejemplos:

- ERP;
- sistemas contables;
- mapas;
- GPS;
- pasarelas de pago;
- servicios de correo;
- APIs externas.

---

# 5. Actor Invitado

"Actor Invitado" no forma parte de la taxonomía.

La condición de invitado describe una característica de acceso, no una función dentro del proceso.

Por ejemplo:

Un socio puede ser:

**Actor Supervisor + acceso temporal**

Por lo tanto, las características como:

- invitado;
- externo;
- temporal;
- interno;

deben tratarse mediante mecanismos de permisos, seguridad y control de acceso.

---

# 6. Diferencia entre tipo de actor y actor concreto

La metodología diferencia entre:

### Tipo de actor

Categoría funcional.

Ejemplo:

**Actor Generador**

### Actor concreto

Persona, rol, organización o sistema que desempeña esa función.

Ejemplo:

**Cliente**

Una misma aplicación puede tener:

| Tipo de actor | Actor concreto |
|---|---|
| Generador | Cliente |
| Coordinador | Analista de logística |
| Ejecutor | Conductor |
| Supervisor | Gerente de operaciones |
| Administrador de Plataforma | Administrador TI |
| Integrador | Sistema de mapas |

No todas las aplicaciones necesitan todos los tipos de actores.

---

# 7. Etapa 1 — PROTOTIPO

## 7.1. Propósito

El prototipo es un artefacto funcional, rápido, económico y descartable.

Normalmente puede ser un HTML cliqueable que representa el camino feliz del Actor Generador.

Su objetivo es:

> **Validar una hipótesis funcional antes de realizar una inversión significativa en software productivo.**

El prototipo no es una versión preliminar del producto.

No pretende representar:

- todos los actores;
- todos los casos de uso;
- todos los procesos;
- todas las reglas de negocio;
- todas las integraciones;
- ni el producto completo.

---

# 8. Alcance del prototipo

La regla general es:

> **Un prototipo inicial y centrado exclusivamente en el Actor Generador.**

El prototipo valida el camino feliz.

No busca inicialmente validar:

- Coordinador;
- Ejecutor;
- Supervisor;
- Administrador de Plataforma;
- Integradores.

La pregunta principal es:

> **¿El Actor Generador entiende, puede ejecutar y considera válida la solución propuesta para resolver su necesidad principal?**

---

# 9. Duración del prototipo

El objetivo es que el prototipo se construya y valide en un período máximo aproximado de:

**3 a 4 semanas.**

La finalidad de este límite es mantener el prototipo como una inversión pequeña.

No se pretende perfeccionar el prototipo indefinidamente.

---

# 10. Evaluación del prototipo

El prototipo debe evaluarse principalmente mediante comportamiento observable.

No debe depender exclusivamente de preguntas como:

- "¿Te gusta?"
- "¿La utilizarías?"
- "¿Qué opinas?"

El usuario debe recibir una situación y una tarea.

Por ejemplo:

> "Imagina que tienes material reciclable en tu oficina y quieres solicitar que la empresa lo recoja. Utiliza esta aplicación para hacerlo."

El facilitador observa:

- dónde comienza;
- qué entiende;
- qué decisiones toma;
- dónde tiene dificultades;
- si completa la tarea;
- si necesita ayuda;
- qué comentarios realiza.

---

# 11. Principio de no sesgo

La evaluación debe minimizar la influencia sobre el usuario.

Por lo tanto:

1. No se debe explicar previamente cómo utilizar el prototipo.
2. Se debe presentar una tarea, no una secuencia de clics.
3. El usuario debe poder explorar.
4. Los errores no deben corregirse inmediatamente.
5. El facilitador debe intervenir lo mínimo posible.
6. El sponsor no debe enseñar al usuario cómo utilizar la solución.
7. Se debe registrar el comportamiento antes que las opiniones.
8. Las preguntas de opinión deben realizarse principalmente después de la tarea.
9. Los usuarios deben representar razonablemente al Actor Generador real.

---

# 12. Roles durante la evaluación

## Facilitador

Conduce la sesión y mantiene la neutralidad.

## Usuario

Interactúa con el prototipo y ejecuta la tarea.

## Observadores

Pueden ser miembros de la empresa dueña de la aplicación.

Pueden observar y tomar notas, pero no intervenir.

## Sponsor

Puede observar, pero no debe guiar al usuario durante la prueba.

---

# 13. Criterios de éxito del prototipo

El prototipo se considera exitoso cuando existe evidencia suficiente de que:

1. El usuario puede completar el camino feliz.
2. Puede hacerlo de forma autónoma.
3. Comprende lo que está haciendo.
4. El flujo representa una solución válida a su necesidad.
5. La empresa considera que el proceso representado es válido para el negocio.

El éxito del prototipo no significa que el producto esté validado.

Significa:

> **Existe suficiente evidencia para justificar la inversión en la construcción del MVP.**

---

# 14. Resultados posibles del prototipo

Cada tarea puede clasificarse como:

| Resultado | Descripción |
|---|---|
| Éxito autónomo | Completa la tarea sin ayuda. |
| Éxito con dudas | Completa sin ayuda pero presenta dudas importantes. |
| Éxito con ayuda | Completa con intervención del facilitador. |
| Fracaso | No logra completar la tarea. |

Como instrumento interno puede utilizarse:

- 3 = éxito autónomo;
- 2 = éxito con dudas;
- 1 = éxito con ayuda;
- 0 = fracaso.

La escala es un mecanismo de apoyo y no sustituye el análisis cualitativo.

---

# 15. Decisión posterior al prototipo

Si el prototipo fracasa:

- se revisa la hipótesis;
- se modifica la solución;
- se puede repetir la validación;
- se puede redefinir el problema;
- o se puede detener la iniciativa.

Si el prototipo es exitoso:

> **Se autoriza la construcción del MVP.**

---

# 16. Etapa 2 — WSLT

WSLT significa:

**Walking Skeleton**

Es la **Iteración 0** de construcción.

Su propósito es demostrar que existe un flujo técnico completo de punta a punta.

Por ejemplo:

**Interfaz → Backend → Lógica → Persistencia → Respuesta**

Dependiendo de la solución puede incluir:

- infraestructura;
- autenticación;
- APIs;
- base de datos;
- despliegue;
- servicios externos.

El WSLT no pretende tener todas las funcionalidades del MVP.

Su objetivo es:

> **Demostrar que el sistema puede caminar de punta a punta.**

---

# 17. Vertical Slices

La construcción se realiza utilizando Vertical Slices.

Cada Vertical Slice representa una capacidad funcional que atraviesa las capas necesarias para entregar un resultado completo.

El objetivo es evitar construir primero grandes bloques técnicos aislados.

En lugar de:

**Frontend → Backend → Base de datos → Integraciones**

se busca:

**Funcionalidad completa de extremo a extremo → siguiente funcionalidad → siguiente funcionalidad**

El WSLT constituye la primera demostración de esta estrategia.

---

# 18. Etapa 3 — GRTH

GRTH significa:

**Growth**

Las iteraciones GRTH hacen crecer progresivamente la solución desde el WSLT hasta alcanzar el MVP.

Puede existir:

**WSLT → GRTH-01 → MVP**

o:

**WSLT → GRTH-01 → GRTH-02 → GRTH-03 → MVP**

No existe un número fijo de iteraciones GRTH.

---

# 19. Propósito de GRTH

Cada GRTH incorpora capacidades adicionales necesarias para que el Actor Generador pueda utilizar progresivamente la solución.

El objetivo es:

> **Construir progresivamente el mínimo necesario para entregar valor real al Generador.**

Las funcionalidades deben construirse mediante Vertical Slices.

Cada iteración debe producir un resultado demostrable.

---

# 20. Etapa 4 — MVP

El MVP representa la primera versión real y utilizable de la solución.

Definición:

> **El MVP es la versión mínima funcional que permite al Actor Generador utilizar la aplicación y obtener el valor principal que se pretende generar.**

El MVP no pretende ser una versión mínima de todos los actores.

Su alcance se concentra inicialmente en:

**Actor Generador**

---

# 21. Duración del MVP

A diferencia del prototipo, el MVP no tiene una duración fija.

Dependiendo de su tamaño y complejidad, puede requerir:

- 8 semanas;
- 12 semanas;
- 16 semanas;
- u otro período razonable.

Lo importante no es la cantidad exacta de semanas.

Lo importante es:

> **El MVP debe permanecer enfocado en entregar el mínimo valor real al Actor Generador.**

---

# 22. Operación híbrida del MVP

Los demás actores pueden continuar utilizando temporalmente los procesos existentes.

Por ejemplo:

**Generador**

Utiliza la nueva aplicación.

↓

La información puede llegar al:

**Coordinador**

mediante:

- Excel;
- Google Sheets;
- correo;
- software existente;
- procesos manuales.

El Coordinador puede continuar trabajando como lo hace actualmente.

El mismo principio puede aplicarse al Ejecutor y Supervisor.

Por lo tanto:

> **No es obligatorio digitalizar todo el ecosistema para lanzar el MVP.**

---

# 23. Condición de viabilidad de la operación híbrida

Aunque los demás actores no formen parte del MVP, debe evaluarse si los procesos existentes pueden absorber razonablemente el trabajo generado por la nueva aplicación.

No basta con decir:

> "El Coordinador seguirá utilizando Excel."

Debe preguntarse:

> **¿El proceso manual sigue siendo operacionalmente viable con el volumen generado por el MVP?**

Si la respuesta es no, puede ser necesario incorporar anticipadamente al Coordinador u otro actor.

---

# 24. El MVP también debe ser validado

El éxito del prototipo solamente autoriza construir el MVP.

No autoriza automáticamente iniciar EVOL.

Una vez construido el MVP debe evaluarse su comportamiento en condiciones reales.

La pregunta cambia:

### Prototipo

> "¿El usuario podría utilizar esta solución?"

### MVP

> **"¿El usuario realmente adopta y utiliza esta solución?"**

---

# 25. Criterio de éxito del MVP

El MVP se considera exitoso cuando existe evidencia suficiente de que:

1. El Actor Generador puede utilizar la aplicación.
2. El usuario logra realizar la actividad principal.
3. El usuario obtiene el valor esperado.
4. Existe adopción real.
5. Existe utilización real o recurrente.
6. La solución demuestra que vale la pena continuar invirtiendo en ella.

La métrica exacta de adopción dependerá de cada producto.

Puede incluir:

- usuarios activos;
- frecuencia de uso;
- cantidad de transacciones;
- porcentaje de usuarios que utilizan la solución;
- recurrencia;
- retención;
- reducción de trabajo;
- satisfacción;
- cumplimiento de objetivos.

---

# 26. Resultados posibles del MVP

Existen dos escenarios principales.

## MVP exitoso

Los usuarios adoptan y utilizan la solución.

Entonces:

**MVP → EVOL**

La inversión puede continuar.

---

## MVP no exitoso

Los usuarios no adoptan o no utilizan suficientemente la solución.

Entonces:

**MVP → detener / replantear / modificar**

Esto permite limitar la pérdida.

La filosofía es:

> **Es preferible descubrir después de invertir en un MVP que la solución no será utilizada, que descubrirlo después de haber construido todo el producto.**

---

# 27. La segunda barrera de inversión

La metodología tiene dos grandes filtros.

## Gate 1 — Prototipo

Pregunta:

> **¿Vale la pena construir?**

Resultado:

**Prototipo exitoso → construir MVP**

---

## Gate 2 — MVP

Pregunta:

> **¿Vale la pena continuar invirtiendo?**

Resultado:

**MVP exitoso → evolucionar**

Esta estructura permite reducir progresivamente el riesgo financiero y tecnológico.

---

# 28. Etapa 5 — EVOL

EVOL significa:

**Evolution**

Después de un MVP exitoso comienza la evolución del producto.

Puede existir:

**EVOL-01 → EVOL-02 → EVOL-03 → EVOL-N**

No existe un número predeterminado.

---

# 29. Objetivo de EVOL

Las iteraciones EVOL aumentan progresivamente el valor de una solución que ya demostró adopción.

Las funcionalidades pueden provenir principalmente de dos fuentes.

### Fuente 1 — Actor Generador

Los usuarios pueden solicitar:

- nuevas funcionalidades;
- mejoras;
- automatizaciones;
- nuevos casos de uso;
- nuevas opciones;
- información adicional.

### Fuente 2 — Otros actores

Progresivamente pueden incorporarse:

- Coordinador;
- Ejecutor;
- Supervisor;
- Administrador de Plataforma;
- Integradores.

---

# 30. La evolución como ciclo de retroalimentación

EVOL no debe entenderse únicamente como:

> "El equipo agrega funcionalidades."

Debe existir un ciclo:

**Usuarios → necesidades → producto → nueva funcionalidad → usuarios**

Esto genera una relación progresiva entre el producto y sus usuarios.

Una característica importante de esta metodología es que los usuarios pueden percibir:

> **"La aplicación está creciendo."**

Y además:

> **"La aplicación está creciendo con base en lo que nosotros hemos solicitado."**

Esto puede favorecer:

- confianza;
- adopción;
- apropiación;
- participación;
- percepción de evolución;
- relación de largo plazo con el producto.

---

# 31. Incorporación progresiva de otros actores

La evolución puede ampliar progresivamente el alcance.

Por ejemplo:

**MVP**

Generador utiliza la aplicación.

↓

**EVOL-01**

Nuevas funcionalidades del Generador.

↓

**EVOL-02**

El Coordinador comienza a utilizar la aplicación.

↓

**EVOL-03**

El Ejecutor comienza a utilizar la aplicación.

↓

**EVOL-04**

El Supervisor obtiene información y dashboards.

↓

**EVOL-05**

Se incorporan funcionalidades del Administrador de Plataforma.

↓

**EVOL-06**

Se incorporan Integradores.

Esta secuencia es solamente ilustrativa.

Los actores deben incorporarse según las necesidades y prioridades reales del producto.

---

# 32. No existe una etapa FINAL

Se elimina el concepto de:

**FINAL**

como etapa obligatoria.

La razón es que un producto de software normalmente no tiene un verdadero punto final.

En su lugar se utiliza:

> **RELEASE OBJETIVO**

---

# 33. Release Objetivo

Un Release Objetivo representa una versión que alcanza un alcance específico definido por:

- proyecto;
- contrato;
- estrategia;
- negocio;
- cliente;
- objetivo de producto.

Por ejemplo:

**MVP → EVOL-01 → EVOL-02 → EVOL-03**

Si EVOL-03 alcanza el alcance definido:

**EVOL-03 = Release Objetivo**

Pero esto no significa que el producto deje de evolucionar.

Posteriormente pueden existir:

**EVOL-04 → EVOL-05 → EVOL-06...**

---

# 34. Modelo completo

El modelo queda definido como:

```text
                    PROTOTIPO
                        │
                        │
              Validación funcional
                        │
                        ▼
                      WSLT
                 Walking Skeleton
                  Iteración 0
                        │
                        ▼
                     GRTH-01
                        │
                        ▼
                     GRTH-02
                        │
                        ▼
                       ...
                        │
                        ▼
                       MVP
                        │
                        │
                 Validación real
                    de adopción
                   /            \
                 NO              SÍ
                 │                │
                 ▼                ▼
             Detener /         EVOL-01
             replantear           │
                                  ▼
                               EVOL-02
                                  │
                                  ▼
                                 ...
                                  │
                                  ▼
                          RELEASE OBJETIVO
                                  │
                                  ▼
                               EVOL-N
                                  │
                                  ▼
                                 …



35. Ventajas de la metodología

35.1. Reduce el riesgo inicial
La primera inversión es pequeña y está orientada a validar la hipótesis.
Evita construir grandes cantidades de software antes de saber si la solución tiene sentido.

35.2. Evita construir correctamente algo que nadie necesita
El prototipo permite descubrir problemas antes de realizar una inversión significativa.

35.3. Evita el "MVP monstruoso"
El MVP no intenta construir una versión pequeña de toda la aplicación.
Se concentra en entregar valor al Generador.

35.4. Permite entregar valor rápidamente
El usuario puede comenzar a utilizar una solución real antes de que todos los procesos de la empresa hayan sido digitalizados.

35.5. Permite aprovechar procesos existentes
La operación híbrida permite que:
Nueva aplicación + procesos existentes
convivan temporalmente.
Esto puede reducir considerablemente el tiempo de lanzamiento.

35.6. Reduce el alcance inicial
La cantidad de funcionalidades iniciales se limita deliberadamente.
Esto facilita:
- planificación;
- construcción;
- pruebas;
- aprendizaje;
- control de costos.

35.7. Facilita la construcción mediante Vertical Slices
WSLT y GRTH permiten demostrar progresivamente capacidades funcionales completas.

35.8. Permite detener la inversión
Si el prototipo fracasa, se evita construir el MVP.
Si el MVP fracasa en adopción, se evita invertir en una evolución extensa.
Por lo tanto:
La inversión aumenta solamente cuando la evidencia justifica continuar.

35.9. Favorece la participación de los usuarios
Los usuarios pueden ver cómo el producto evoluciona y cómo sus necesidades influyen en las nuevas funcionalidades.

35.10. Facilita la evolución progresiva de actores
No es necesario construir desde el inicio funcionalidades para todos los actores.
Se incorporan progresivamente cuando existe evidencia de necesidad.


36. Riesgos de la metodología

36.1. Optimización excesiva para el Generador
El principal riesgo es construir una solución excelente para el Generador pero difícil de extender hacia:
- Coordinador;
- Ejecutor;
- Supervisor;
- Administrador;
- Integradores.
Mitigación
No construir funcionalidades futuras, pero evitar decisiones estructurales que impidan su futura incorporación.


37. No construir no significa no diseñar
El hecho de que un actor no esté dentro del MVP no significa que pueda ignorarse completamente.
Debe existir conciencia sobre:
- información;
- estados;
- entidades;
- relaciones;
- trazabilidad;
- permisos;
- extensibilidad.
La regla es:
No construir funcionalidades futuras innecesariamente, pero tampoco tomar decisiones que imposibiliten su futura construcción.


38. Riesgo operacional
La operación híbrida puede funcionar inicialmente y dejar de ser viable cuando aumente el volumen.
Por ejemplo:
20 solicitudes → Excel funciona
pero:
5.000 solicitudes → Excel puede ser inviable
Por eso debe evaluarse periódicamente la capacidad de los procesos existentes.


39. Riesgo de validar solamente el Happy Path
El prototipo no valida necesariamente:
- errores;
- excepciones;
- cancelaciones;
- datos incorrectos;
- duplicados;
- falta de disponibilidad;
- problemas de conectividad;
- situaciones extraordinarias.
Esto debe quedar explícito.
El éxito del prototipo no significa que todo el comportamiento del producto haya sido validado.


40. Riesgo de interpretar el éxito del prototipo como éxito del producto
Un prototipo exitoso solamente demuestra:
Existe evidencia suficiente para construir el MVP.

No demuestra:
El producto tendrá adopción.

La adopción se valida posteriormente mediante el MVP.


41. Riesgo de que GRTH se convierta en Waterfall
GRTH debe mantener la filosofía incremental.
Cada iteración debería entregar una capacidad demostrable.
No debe convertirse en:
"Primero definimos todo el MVP y luego construimos todo."

La evolución debe mantenerse basada en Vertical Slices.


42. Riesgo de expansión prematura
Durante la construcción pueden aparecer solicitudes como:
- dashboards;
- módulos administrativos;
- funcionalidades del Supervisor;
- funcionalidades del Coordinador;
- integraciones.
Estas solicitudes no deben entrar automáticamente al MVP.
Debe evaluarse si realmente son necesarias para que el Generador obtenga el valor principal.


43. Riesgo de expansión tardía
El riesgo contrario también existe.
Si otros actores son indispensables para que el producto funcione, esperar hasta EVOL puede ser un error.
Por esta razón la metodología necesita excepciones.


44. Límites de la metodología
La metodología funciona mejor cuando:
- existe un Actor Generador claramente identificable;
- el valor principal puede comenzar en ese actor;
- los demás actores pueden continuar temporalmente con procesos existentes;
- existe posibilidad de operación híbrida;
- el producto puede evolucionar progresivamente.


45. Cuándo debe extenderse el prototipo
La regla general es:
Prototipo → Generador
Pero debe ampliarse a otros actores cuando el valor de la hipótesis dependa necesariamente de ellos.
Por ejemplo:
Si el Generador solamente obtiene valor cuando un Coordinador procesa inmediatamente su solicitud, podría ser necesario validar también al Coordinador.


46. Cuándo debe extenderse el MVP
El MVP normalmente se concentra en el Generador.
Sin embargo, otro actor debe incorporarse anticipadamente cuando:
1. El producto no puede entregar valor sin él.
2. La operación existente no puede absorber el nuevo volumen.
3. Existe una dependencia técnica crítica.
4. Existe una obligación regulatoria.
5. Existe una integración indispensable.
6. La propuesta de valor depende de varios actores simultáneamente.


47. Aplicaciones donde la metodología puede requerir adaptación
Debe evaluarse cuidadosamente en:
- sistemas altamente regulados;
- sistemas críticos;
- sistemas donde varios actores generan valor conjuntamente;
- marketplaces;
- sistemas con fuertes dependencias externas;
- sistemas donde el proceso completo debe estar digitalizado desde el inicio;
- soluciones donde una operación manual temporal no sea viable.
En estos casos puede ser necesario ampliar el alcance del prototipo o del MVP.


48. Principio de excepción
La metodología no debe convertirse en una regla rígida.
El principio general es:
Comenzar por el Generador y minimizar el alcance inicial.

La excepción es:
Incorporar otros actores cuando exista una razón crítica que haga imposible validar, operar o entregar el valor del producto sin ellos.


49. Principios fundamentales
1. El prototipo es descartable.
2. El prototipo valida; no construye el producto.
3. El primer prototipo se concentra en el Actor Generador.
4. El prototipo valida el camino feliz.
5. El comportamiento observable tiene prioridad sobre la opinión.
6. La validación del usuario y la validación del negocio son diferentes.
7. Un prototipo exitoso autoriza construir el MVP.
8. El WSLT es la Iteración 0.
9. WSLT demuestra el flujo técnico de punta a punta.
10. La construcción utiliza Vertical Slices.
11. GRTH hace crecer la solución hasta alcanzar el MVP.
12. El MVP se concentra inicialmente en el Actor Generador.
13. El tamaño del MVP depende de su alcance y complejidad.
14. El MVP debe validarse en condiciones reales.
15. La adopción real es el principal indicador de éxito del MVP.
16. Un MVP exitoso autoriza la evolución.
17. Un MVP no exitoso puede llevar a detener o replantear la iniciativa.
18. EVOL incrementa progresivamente el valor del producto.
19. EVOL puede incorporar nuevas necesidades del Generador.
20. EVOL puede incorporar progresivamente otros actores.
21. Los usuarios deben poder percibir que el producto evoluciona.
22. Las nuevas funcionalidades deben responder, cuando sea posible, a necesidades reales de los usuarios.
23. No construir una funcionalidad futura no significa ignorar la futura extensibilidad.
24. La operación híbrida es válida cuando sea operacionalmente sostenible.
25. La metodología debe adaptarse cuando otros actores sean indispensables.
26. No existe una etapa FINAL obligatoria.
27. Un Release Objetivo representa un punto formal de alcance, no el final de la vida del producto.
28. El producto puede continuar evolucionando después del Release Objetivo.


50. Modelo conceptual definitivo
La metodología puede resumirse en seis preguntas:
PROTOTIPO
¿Vale la pena construir?

WSLT
¿Podemos hacer que la solución funcione de punta a punta?

GRTH
¿Podemos hacer crecer la solución hasta entregar el mínimo valor necesario?

MVP
¿Los usuarios realmente adoptan y utilizan la solución?

EVOL
¿Cómo aumentamos progresivamente el valor de una solución que ya funciona?

RELEASE OBJETIVO
¿Hemos alcanzado el alcance definido para este objetivo del producto?

Y después:
El producto continúa evolucionando cuando exista una razón para hacerlo.


51. Filosofía final
La metodología puede resumirse en una frase:
Validar antes de construir, construir antes de expandir, demostrar adopción antes de continuar invirtiendo y evolucionar el producto junto con sus usuarios.

El objetivo no es construir la aplicación completa lo más rápido posible.
El objetivo es:
Reducir progresivamente la incertidumbre y aumentar progresivamente la inversión a medida que aumenta la evidencia de valor.

El flujo completo es:
Hipótesis → Prototipo → Validación → WSLT → GRTH → MVP → Adopción → EVOL → Release Objetivo → Evolución continua




# ANEXO — PROTOTIPO DE EVOLUCIÓN

## 1. Propósito

El Prototipo de Evolución es un mecanismo de validación utilizado durante la etapa EVOL para reducir la incertidumbre antes de construir una nueva funcionalidad, modificar significativamente una funcionalidad existente o incorporar capacidades para un nuevo actor.

A diferencia del Prototipo Inicial, el Prototipo de Evolución no busca determinar si vale la pena construir el producto.

Su propósito es:

> **Determinar si una nueva capacidad o cambio debe construirse y, en caso afirmativo, cuál es la forma funcional más adecuada de construirlo.**

El Prototipo de Evolución puede utilizarse con cualquier actor de la aplicación:

- Generador;
- Coordinador;
- Ejecutor;
- Supervisor;
- Administrador de Plataforma;
- Integrador.

---

# 2. Principio fundamental

El prototipo no está asociado exclusivamente a un actor.

El criterio para decidir si se prototipa debe ser:

> **El nivel de incertidumbre y el impacto potencial de equivocarse.**

Por lo tanto:

**Nueva funcionalidad ≠ necesariamente nuevo prototipo.**

La pregunta correcta es:

> **¿Existe suficiente incertidumbre funcional o riesgo como para que sea conveniente validar antes de construir?**

---

# 3. Diferencia entre Prototipo Inicial y Prototipo de Evolución

## Prototipo Inicial

Se realiza al comienzo del proyecto.

Su objetivo es validar la hipótesis fundamental del producto.

Pregunta principal:

> **¿La solución propuesta tiene sentido para el Actor Generador?**

Resultado:

**Prototipo exitoso → autorización para construir MVP.**

---

## Prototipo de Evolución

Se realiza durante la evolución del producto cuando aparece una nueva necesidad o una modificación con suficiente incertidumbre.

Pregunta principal:

> **¿Esta nueva capacidad resuelve correctamente la necesidad del usuario y cuál es la mejor forma de implementarla?**

Resultado:

**Prototipo exitoso → autorización para construir la funcionalidad.**

---

# 4. El Prototipo de Evolución no constituye una nueva etapa del ciclo

El Prototipo de Evolución no reemplaza ni modifica:

- WSLT;
- GRTH;
- MVP;
- EVOL.

Es una herramienta que puede utilizarse dentro de EVOL cuando sea necesario.

El flujo puede ser:

```text
EVOL
 │
 ├── Nueva funcionalidad
 │       │
 │       ├── Baja incertidumbre
 │       │       ↓
 │       │    Construcción
 │       │
 │       └── Alta incertidumbre
 │               ↓
 │        Prototipo de Evolución
 │               ↓
 │          Validación
 │               ↓
 │          Construcción
 │
 └── Continúa EVOL


5. ¿Cuándo utilizar un Prototipo de Evolución?
Debe considerarse cuando exista una o varias de las siguientes condiciones.

5.1. Nueva funcionalidad con comportamiento desconocido
Cuando no está claro cómo debería funcionar para el usuario.
Ejemplo:
El Generador solicita una recogida y ahora se quiere permitir cancelar la solicitud.
No está claro:
- cuándo puede cancelar;
- qué ocurre si ya fue asignada;
- qué ocurre si el vehículo está en camino;
- qué información debe recibir.
La incertidumbre justifica prototipar.

5.2. Existen varias alternativas funcionales
Si existen diferentes formas razonables de resolver una necesidad, puede ser conveniente prototiparlas antes de construir.
Ejemplo:
El Coordinador debe organizar las recogidas.
Alternativas:
- lista;
- tablero;
- mapa;
- calendario;
- combinación de mapa y lista.
El prototipo permite comparar alternativas antes de realizar el desarrollo.

5.3. La funcionalidad cambia significativamente el comportamiento del usuario
Si una funcionalidad modifica un proceso que los usuarios ya conocen, debe considerarse prototiparla.
Ejemplo:
El Generador actualmente solicita una recogida en tres pasos y se pretende convertirla en un proceso completamente diferente.

5.4. Existe riesgo elevado de rechazo
Si existe una posibilidad significativa de que los usuarios no acepten la nueva funcionalidad, es preferible validar antes de construir.

5.5. La funcionalidad es crítica para el negocio
Cuando una funcionalidad tiene un impacto importante sobre:
- ingresos;
- costos;
- operación;
- experiencia del usuario;
- cumplimiento;
- seguridad;
- productividad;
puede ser conveniente realizar una validación previa.

5.6. Se incorpora un nuevo actor
Cuando una funcionalidad requiere incorporar por primera vez a un actor que todavía no utiliza la aplicación, normalmente se recomienda realizar un Prototipo de Evolución.
Ejemplo:
El MVP funciona únicamente para el Generador.
Durante EVOL se decide incorporar al Coordinador.
Antes de construir su módulo completo:
Prototipo de Evolución → Coordinador → Validación → Construcción.

5.7. Existe incertidumbre sobre el flujo de interacción
Cuando sabemos qué queremos lograr, pero no sabemos cómo debería interactuar el usuario con la solución.

5.8. Existe una dependencia entre varios actores
Cuando una funcionalidad requiere interacción entre dos o más actores y todavía no está claro cómo debe funcionar el proceso completo.
Ejemplo:
Generador → Coordinador → Ejecutor
El prototipo puede representar únicamente la interacción necesaria para validar ese nuevo flujo.


6. ¿Cuándo NO utilizar un Prototipo de Evolución?
No toda funcionalidad necesita ser prototipada.
No debería utilizarse cuando:

6.1. La funcionalidad es simple y evidente
Ejemplo:
Agregar un campo claramente definido a un formulario existente.

6.2. Es una modificación menor
Ejemplo:
- cambiar un texto;
- modificar una etiqueta;
- agregar una opción sencilla;
- cambiar una validación evidente.

6.3. La solución funcional ya está validada
Si una funcionalidad ya fue validada previamente y solamente requiere una implementación equivalente, no necesariamente requiere un nuevo prototipo.

6.4. Existe baja incertidumbre
Si:
- el problema está claramente entendido;
- la solución es conocida;
- el usuario ya validó el comportamiento;
- no existen alternativas relevantes;
puede pasarse directamente a construcción.

6.5. El costo del prototipado supera su beneficio
El prototipo también representa una inversión.
No tiene sentido crear un prototipo complejo para una funcionalidad cuyo costo de equivocarse es mínimo.


7. Matriz de decisión
Puede utilizarse una matriz sencilla para decidir si prototipar.
Incertidumbre	Impacto de equivocarse	Decisión
Baja	Bajo	Construir directamente
Baja	Alto	Evaluar cuidadosamente
Alta	Bajo	Prototipo opcional
Alta	Alto	Prototipo recomendado
Muy alta	Muy alto	Prototipo altamente recomendado


La decisión final debe considerar el contexto del producto.


8. El tamaño del Prototipo de Evolución
El Prototipo de Evolución debe ser:
Tan pequeño como sea necesario para responder la pregunta que genera la incertidumbre.

No debe convertirse en una mini-versión de la funcionalidad productiva.
Puede ser:
- un boceto;
- wireframes;
- un flujo;
- HTML cliqueable;
- una simulación;
- un mockup;
- una demostración funcional;
- una combinación de varias de estas técnicas.
La tecnología utilizada no es lo importante.
Lo importante es:
Reducir la incertidumbre antes de invertir en construcción.


9. El Prototipo de Evolución debe tener una pregunta de validación
Antes de construirlo debe existir una pregunta concreta.
Ejemplo:
"¿El Coordinador puede organizar eficientemente las solicitudes mediante un tablero?"

No debería construirse simplemente porque:
"Queremos prototipar el módulo del Coordinador."

El prototipo debe responder una pregunta.


10. Ejemplos de preguntas de validación
Generador
¿El Generador entiende el nuevo proceso para cancelar una solicitud?

Coordinador
¿El Coordinador puede organizar las solicitudes mediante un tablero?

Ejecutor
¿El Ejecutor puede identificar fácilmente cuál es su siguiente recogida?

Supervisor
¿El Supervisor encuentra la información necesaria para evaluar el desempeño?

Administrador
¿El Administrador puede configurar el parámetro sin asistencia técnica?

Integrador
¿El flujo de información entre ambos sistemas representa correctamente el proceso requerido?


11. Alcance del Prototipo de Evolución
El prototipo debe incluir únicamente aquello necesario para responder la pregunta de validación.
No debe incorporar:
- funcionalidades no relacionadas;
- administración completa;
- seguridad productiva;
- infraestructura definitiva;
- integraciones completas;
- todos los casos excepcionales;
- funcionalidades futuras.
Su naturaleza sigue siendo:
rápida, económica y descartable.


12. Participantes
Los participantes deben corresponder principalmente al actor afectado por la nueva funcionalidad.
Si la funcionalidad afecta a varios actores, deben participar los actores necesarios para validar la interacción.
Ejemplo:
Una nueva funcionalidad involucra:
Generador + Coordinador
La evaluación puede requerir usuarios de ambos roles.


13. Evaluación
La evaluación debe mantener los principios utilizados para el Prototipo Inicial:
- tareas concretas;
- comportamiento observable;
- mínima intervención del facilitador;
- ausencia de instrucciones sobre cómo utilizarlo;
- registro de dificultades;
- registro de comentarios;
- identificación de comportamientos inesperados.
La evaluación debe buscar responder:
1. ¿El usuario entiende la funcionalidad?
2. ¿Puede utilizarla?
3. ¿La funcionalidad resuelve su necesidad?
4. ¿El flujo resulta razonable?
5. ¿Existen alternativas mejores?
6. ¿Qué debe modificarse antes de construir?


14. Resultado del Prototipo de Evolución
El resultado puede ser:
APROBADO
La funcionalidad está suficientemente validada para iniciar construcción.
APROBADO CON AJUSTES
La hipótesis es correcta, pero deben realizarse modificaciones antes de construir.
NO APROBADO
La solución propuesta no resuelve adecuadamente la necesidad.
REPLANTEAR
La necesidad es válida, pero la solución debe replantearse.


15. Prototipo exitoso no significa funcionalidad terminada
El éxito del Prototipo de Evolución significa:
Existe suficiente evidencia para iniciar la construcción de la funcionalidad.

No significa:
- que la funcionalidad esté completamente definida;
- que no existan errores;
- que todos los casos excepcionales estén resueltos;
- que la implementación técnica esté terminada.
La validación funcional y la construcción continúan siendo actividades diferentes.


16. Relación con EVOL
El Prototipo de Evolución puede aparecer múltiples veces durante la vida del producto.
Ejemplo:
MVP
 │
 ▼
EVOL-01
 │
 ├── Nueva necesidad Generador
 │        ↓
 │   Prototipo Evolución
 │        ↓
 │   Construcción
 │
 ▼
EVOL-02
 │
 ├── Nueva funcionalidad Coordinador
 │        ↓
 │   Prototipo Evolución
 │        ↓
 │   Construcción
 │
 ▼
EVOL-03
 │
 └── Nueva funcionalidad simple
          ↓
       Construcción directa
Por lo tanto:
EVOL no implica necesariamente prototipar todo.

El prototipado se activa cuando existe suficiente incertidumbre.


17. Prototipar una nueva funcionalidad del Generador
Una nueva funcionalidad del Actor Generador también puede requerir un Prototipo de Evolución.
El hecho de que el actor ya utilice la aplicación no elimina la incertidumbre.
Ejemplo:
El Generador ya puede solicitar una recogida.
Se quiere agregar:
"Programar una recogida recurrente."

Puede existir incertidumbre sobre:
- frecuencia;
- fechas;
- cantidades;
- modificaciones;
- cancelaciones;
- excepciones.
Por lo tanto:
Nueva funcionalidad Generador → Prototipo de Evolución → Validación → EVOL


18. Prototipar una funcionalidad para un actor nuevo
Cuando se incorpora un actor que nunca ha utilizado la aplicación, el Prototipo de Evolución puede utilizarse para descubrir:
- necesidades;
- lenguaje;
- flujo de trabajo;
- información requerida;
- decisiones;
- excepciones;
- interacción con otros actores.
Esto reduce el riesgo de construir una solución basada únicamente en las suposiciones del equipo de desarrollo o del sponsor.


19. Prototipos que involucran varios actores
Una nueva funcionalidad puede requerir validar un flujo completo entre varios actores.
Ejemplo:
Generador
    ↓
Solicitud
    ↓
Coordinador
    ↓
Asignación
    ↓
Ejecutor
    ↓
Confirmación
No necesariamente se deben prototipar todas las funcionalidades de cada actor.
Se prototipa únicamente el segmento necesario para validar la nueva hipótesis.


20. Principio de proporcionalidad
El nivel de prototipado debe ser proporcional a:
incertidumbre + impacto + complejidad + costo de equivocarse
Cuanto mayor sea la combinación de estos factores, mayor debe ser el esfuerzo de validación.
No se debe convertir el prototipado en burocracia.


21. Principio de descartabilidad
El Prototipo de Evolución debe considerarse descartable.
No debe existir presión para reutilizar su código en producción.
Esto permite:
- experimentar;
- equivocarse;
- comparar alternativas;
- cambiar rápidamente;
- priorizar la validación sobre la calidad técnica.
La calidad técnica corresponde a la etapa de construcción.


22. Principio de independencia tecnológica
El prototipo no tiene que utilizar necesariamente la misma tecnología del producto.
Puede utilizar:
- HTML;
- herramientas de prototipado;
- simulaciones;
- datos ficticios;
- interfaces simplificadas.
La tecnología se selecciona en función de la pregunta que debe responder.


23. Regla general
La metodología adopta la siguiente regla:
No se prototipa por actor, ni se prototipa por obligación. Se prototipa cuando existe incertidumbre suficiente para justificar una validación antes de construir.

Por esta razón:
- una nueva funcionalidad del Generador puede requerir prototipo;
- una nueva funcionalidad del Coordinador puede requerir prototipo;
- una nueva funcionalidad del Ejecutor puede requerir prototipo;
- una nueva funcionalidad del Supervisor puede requerir prototipo;
- una nueva funcionalidad del Administrador puede requerir prototipo;
- una integración puede requerir prototipo.
Pero ninguna de ellas necesariamente lo requiere.


24. Principio final
El Prototipo Inicial y el Prototipo de Evolución comparten una misma filosofía:
Prototipar es una herramienta para reducir incertidumbre antes de realizar una inversión mayor.

La diferencia está en el momento y en la pregunta que responden.
Prototipo Inicial:
¿Vale la pena construir esta solución?

Prototipo de Evolución:
¿Vale la pena construir esta nueva capacidad y cuál es la mejor forma funcional de hacerlo?

De esta manera, el prototipado acompaña al producto durante toda su evolución sin convertirse en una etapa obligatoria para cada funcionalidad.


25. Modelo conceptual
                    PRODUCTO
                       │
                       ▼
                    EVOL
                       │
              Nueva necesidad
                       │
                       ▼
              ¿Hay incertidumbre?
                  /          \
                NO            SÍ
                │              │
                ▼              ▼
          Construcción     PROTOTIPO
                              │
                              ▼
                         Validación
                              │
                  ┌───────────┴───────────┐
                  │                       │
                NO                       SÍ
                  │                       │
                  ▼                       ▼
             Replantear             Construcción
                                          │
                                          ▼
                                        EVOL
                                          │
                                          ▼
                                Nueva necesidad...

Principio rector
La metodología no busca prototipar todo. Busca evitar construir aquello que todavía no entendemos suficientemente bien.
