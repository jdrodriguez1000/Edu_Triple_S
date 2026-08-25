# Metodología de Prototipado, Taxonomía de Actores y Validación de Prototipos

## 1. Contexto

Al iniciar un proyecto de desarrollo de software, se construye inicialmente un **prototipo funcional, económico y totalmente descartable**.

El prototipo normalmente consiste en un HTML cliqueable que representa el **camino feliz del actor principal de la aplicación**.

Su propósito no es construir una versión reducida del producto final, sino **validar una hipótesis funcional antes de invertir recursos en la construcción del MVP**.

Este enfoque busca permitir que los principales supuestos funcionales sean evaluados de manera rápida y económica.

---

# 2. Problema que se busca resolver

Uno de los principales problemas durante la presentación de los prototipos es que el sponsor puede interpretar que:

> "El prototipo representa la aplicación que se va a construir."

Sin embargo, esa no es su finalidad.

El prototipo debe entenderse como:

> **Un artefacto de validación funcional, no como una versión preliminar del producto.**

El prototipo:

- Es barato.
- Es rápido de construir.
- Es descartable.
- No requiere arquitectura definitiva.
- No necesita contemplar todos los actores.
- No necesita implementar todos los casos de uso.
- No representa necesariamente el alcance completo de la aplicación.
- No debe ser evaluado con los mismos criterios de un MVP.

Su objetivo inicial es validar una pregunta concreta:

> **¿El camino feliz del actor generador funciona funcionalmente como esperamos?**

Si esta hipótesis es validada, se puede avanzar hacia la construcción del MVP.

---

# 3. Prototipo, MVP y producto

Es importante diferenciar claramente las tres etapas.

## Prototipo

Su objetivo es:

> **Validar una hipótesis funcional de manera rápida, económica y descartable.**

No pretende ser una solución completa.

## MVP

Su objetivo es:

> **Construir una versión real y utilizable que resuelva el problema principal, incorporando los actores y funcionalidades necesarias para operar.**

El MVP ya requiere software funcional, persistencia de información, reglas de negocio, seguridad, usuarios, etc., según corresponda al proyecto.

## Producto

Es la evolución del MVP hacia una solución completa y sostenible.

Puede incorporar:

- Nuevos actores.
- Nuevos procesos.
- Casos excepcionales.
- Integraciones.
- Reportes.
- Escalabilidad.
- Seguridad avanzada.
- Automatizaciones.
- Nuevas funcionalidades.

Por lo tanto:

**Prototipo → Validación**

**MVP → Operación**

**Producto → Evolución**

---

# 4. Concepto de actor

Un actor es una persona, rol, organización o sistema externo que interactúa con la aplicación y que tiene un propósito determinado dentro del proceso.

La taxonomía de actores no significa que todas las aplicaciones deban tener todos los tipos de actores.

Debe entenderse como un:

> **Catálogo de posibles tipos de actores que permite identificar y clasificar los actores reales de cada aplicación.**

Una aplicación puede tener solamente algunos de ellos.

Por ejemplo:

**Aplicación sencilla:**

Generador + Administrador de Plataforma

**Aplicación operativa:**

Generador + Coordinador + Ejecutor

**Aplicación empresarial:**

Generador + Coordinador + Ejecutor + Supervisor + Administrador de Plataforma + Integradores

---

# 5. Taxonomía de actores

La taxonomía definida hasta este punto está compuesta por seis tipos de actores:

1. Actor Generador
2. Actor Coordinador
3. Actor Ejecutor
4. Actor Supervisor
5. Actor Administrador de Plataforma
6. Actor Integrador

---

# 6. Actor Generador

## Definición

Es el actor que realiza la acción principal que da origen al proceso de la aplicación.

Una regla importante es:

> **Si el actor generador no existe o no utiliza la aplicación, no existe una razón fundamental para que la aplicación exista.**

El Generador es, por lo tanto, el punto de partida natural para analizar el flujo funcional principal.

## Ejemplo en una aplicación de reciclaje

El cliente solicita que se recoja material reciclable.

El flujo inicial podría ser:

**Cliente → Solicitar recolección**

En este caso:

**Cliente = Actor Generador**

---

# 7. Actor Coordinador

El concepto inicialmente denominado "Actor Operador" fue dividido porque el término Operador era demasiado amplio.

En una aplicación pueden existir personas que organizan el trabajo y personas que ejecutan físicamente ese trabajo.

## Definición

> **Es el actor que recibe las acciones o solicitudes generadas y coordina los recursos, personas y actividades necesarias para que sean ejecutadas.**

No necesariamente significa que construya un "plan".

Puede:

- Organizar.
- Asignar.
- Priorizar.
- Distribuir.
- Reasignar.
- Coordinar recursos.
- Coordinar personas.
- Supervisar la ejecución operativa.

## Ejemplo en una aplicación de reciclaje

El analista de logística recibe las solicitudes de recolección y organiza:

- rutas;
- vehículos;
- conductores;
- prioridades;
- horarios.

En este caso:

**Analista de logística = Actor Coordinador**

---

# 8. Actor Ejecutor

El Actor Ejecutor representa a quien realiza directamente el trabajo.

## Definición

> **Es el actor que ejecuta física o directamente la acción que debe realizarse como consecuencia del proceso iniciado en la aplicación.**

## Ejemplo en una aplicación de reciclaje

El conductor o recolector:

- consulta sus recogidas;
- se desplaza al lugar;
- realiza la recolección;
- registra novedades;
- confirma que el material fue recogido.

En este caso:

**Conductor/Recollector = Actor Ejecutor**

La diferencia fundamental entre Coordinador y Ejecutor es:

> **El Coordinador organiza el trabajo; el Ejecutor realiza el trabajo.**

---

# 9. Actor Supervisor

Inicialmente se utilizó el concepto de "Actor Gerencial", pero se decidió cambiarlo porque no seguía la lógica de los otros nombres.

Los términos:

- Generador
- Coordinador
- Ejecutor

describen acciones.

Por esa razón, "Gerencial" resultaba inconsistente al ser un adjetivo asociado a un nivel jerárquico.

Se seleccionó:

**Actor Supervisor**

## Definición

> **Es el actor que utiliza la información generada por la aplicación para supervisar resultados, evaluar desempeño, identificar comportamientos y apoyar la toma de decisiones.**

No necesariamente tiene que ser un gerente.

Puede ser:

- Gerente general.
- Gerente de operaciones.
- Director.
- Jefe de área.
- Socio.
- Responsable de un área.

Lo importante no es el cargo de la persona, sino la función que desempeña dentro de la aplicación.

## Ejemplo

El gerente de operaciones consulta:

- cantidad de recolecciones;
- cumplimiento de rutas;
- productividad;
- materiales recogidos;
- desempeño de vehículos;
- comportamiento por zonas.

En este caso:

**Gerente de operaciones = Actor Supervisor**

---

# 10. Actor Administrador de Plataforma

El Administrador de Plataforma tiene una función diferente a los actores de negocio.

Su objetivo principal no es ejecutar el proceso de negocio, sino garantizar la correcta administración de la plataforma.

## Definición

> **Es el actor responsable de administrar el funcionamiento de la plataforma, incluyendo usuarios, permisos, configuraciones y otros elementos necesarios para su operación.**

Puede ser:

- Personal interno de TI.
- Administrador de sistemas.
- Proveedor externo.
- Personal técnico especializado.

Entre sus posibles actividades están:

- Crear y administrar usuarios.
- Administrar roles.
- Configurar permisos.
- Administrar parámetros.
- Gestionar configuraciones.
- Administrar catálogos.
- Revisar problemas de la plataforma.
- Administrar integraciones.

Este actor **no necesariamente existe en todas las aplicaciones**.

---

# 11. Actor Integrador

El Actor Integrador es diferente porque no necesariamente es una persona.

Puede ser un sistema, plataforma o servicio externo.

## Definición

> **Es un sistema, plataforma o servicio externo que intercambia información o ejecuta acciones mediante una integración con la aplicación.**

Ejemplos:

- Sistemas ERP.
- Sistemas contables.
- Pasarelas de pago.
- Sistemas de mapas.
- Sistemas GPS.
- Servicios de correo.
- WhatsApp.
- Sistemas de autenticación.
- APIs externas.

## Ejemplo en reciclaje

La aplicación podría integrarse con un servicio de mapas para calcular rutas.

En ese caso:

**Servicio de mapas = Actor Integrador**

---

# 12. Por qué "Actor Invitado" no forma parte de la taxonomía

Inicialmente se consideró:

**Actor Invitado**

como una categoría.

Sin embargo, se concluyó que "Invitado" no describe realmente el comportamiento del actor.

Describe principalmente una **condición de acceso**.

Por ejemplo, un socio puede tener acceso temporal a determinados informes.

Pero ese socio podría clasificarse funcionalmente como:

**Actor Supervisor + acceso temporal**

De la misma manera, un auditor externo podría ser:

**Actor Supervisor + usuario externo**

Por lo tanto:

> **"Invitado" no se considera un tipo de actor dentro de la taxonomía.**

La condición de invitado, temporal, externo, etc., deberá tratarse posteriormente como una característica de acceso, permisos o seguridad.

---

# 13. Diferencia entre tipo de actor y actor concreto

Es importante distinguir ambos conceptos.

## Tipo de actor

Es la categoría funcional.

Ejemplo:

**Actor Generador**

## Actor concreto

Es la persona, rol o sistema que desempeña esa función dentro de una aplicación específica.

Ejemplo:

**Cliente**

Por lo tanto:

| Tipo de actor | Actor concreto en reciclaje |
|---|---|
| Generador | Cliente |
| Coordinador | Analista de logística |
| Ejecutor | Conductor/Recollector |
| Supervisor | Gerente de operaciones |
| Administrador de Plataforma | Administrador de TI |
| Integrador | Servicio de mapas |

Esta separación permite que la taxonomía sea reutilizable en diferentes proyectos y empresas.

---

# 14. Ejemplo completo: aplicación de recolección de reciclaje

La aplicación permite que una persona, empresa u organización solicite la recolección de material reciclable.

El material puede variar desde una pequeña bolsa hasta una cantidad que requiera un camión.

El proceso puede involucrar diferentes actores.

### Generador

El cliente:

**Solicita la recolección.**

↓

### Coordinador

El analista de logística:

**Recibe y coordina las solicitudes.**

↓

### Ejecutor

El conductor/recolector:

**Realiza la recolección y confirma el resultado.**

↓

### Supervisor

El gerente:

**Consulta información y supervisa el desempeño de la operación.**

↓

### Administrador de Plataforma

El administrador:

**Administra usuarios, permisos y configuración de la plataforma.**

↓

### Integrador

Los sistemas externos:

**Intercambian información o ejecutan acciones integradas con la aplicación.**

---

# 15. Principio fundamental de la taxonomía

La clasificación no debe construirse a partir de los cargos organizacionales de una empresa.

Debe construirse a partir de:

> **La función que el actor desempeña dentro de la aplicación.**

Por ejemplo, "Gerente de Operaciones" no debería ser una categoría de actor.

La categoría debe ser:

**Actor Supervisor**

y "Gerente de Operaciones" es el actor concreto que desempeña ese papel.

De esta forma, la taxonomía puede utilizarse independientemente de la estructura organizacional de cada empresa.

---

# 16. Taxonomía cerrada hasta este punto

La taxonomía actualmente definida es:

### Actores de negocio

1. **Actor Generador**  
   Genera la acción o proceso principal.

2. **Actor Coordinador**  
   Coordina el trabajo generado.

3. **Actor Ejecutor**  
   Ejecuta el trabajo.

4. **Actor Supervisor**  
   Supervisa resultados y utiliza información para tomar decisiones.

### Actor de plataforma

5. **Actor Administrador de Plataforma**  
   Administra la plataforma y sus configuraciones.

### Actor externo

6. **Actor Integrador**  
   Interactúa con la aplicación mediante integraciones externas.

---

# 17. Evaluación del prototipo

Una vez construido el prototipo, es necesario determinar si realmente logró su objetivo.

El propósito de la evaluación no debe ser determinar si al usuario "le gusta" el prototipo.

El objetivo debe ser:

> **Determinar si el Actor que se está evaluando puede comprender y ejecutar correctamente el camino feliz que el prototipo pretende validar.**

Por lo tanto, la evaluación debe basarse principalmente en **comportamiento observable**, no en opiniones.

---

# 18. Problema del enfoque tradicional de evaluación

Un enfoque tradicional podría ser:

**Construir prototipo → mostrarlo al usuario → pedir su opinión → recoger observaciones.**

Este enfoque presenta varios riesgos.

El usuario puede:

- sentirse comprometido con la empresa;
- querer agradar al sponsor;
- sentirse evaluado;
- aceptar la solución aunque no la entienda;
- sugerir funcionalidades que no son necesarias;
- afirmar que utilizaría la solución sin haber demostrado que puede utilizarla.

Además, cuando la prueba se realiza en las instalaciones de la empresa y con representantes de la empresa presentes, existe un riesgo adicional de influencia.

Por esta razón:

> **La evaluación debe pasar de "preguntar qué piensa el usuario" a "observar cómo se comporta el usuario frente a una tarea".**

---

# 19. Principio de evaluación

El usuario no debe recibir una explicación detallada de cómo utilizar el prototipo.

Debe recibir un **contexto y una tarea**.

Por ejemplo, para el Actor Generador de la aplicación de reciclaje:

En lugar de decir:

> "Haz clic en Solicitar recolección y después selecciona la fecha."

Se debería decir:

> **"Imagina que tienes varias bolsas de material reciclable en tu oficina y quieres solicitar que la empresa las recoja. Utiliza esta aplicación para hacerlo."**

A partir de ese momento, el facilitador debe observar.

Esto permite evaluar si el usuario realmente entiende cómo utilizar la solución.

---

# 20. La prueba debe centrarse en una tarea

La evaluación debe utilizar tareas concretas.

Ejemplo:

> **"Solicita una recolección para mañana en tu oficina, indicando que tienes aproximadamente 10 bolsas de material reciclable."**

Durante la tarea se puede observar:

- ¿Entiende dónde comenzar?
- ¿Encuentra la opción correcta?
- ¿Comprende los campos?
- ¿Sabe qué información introducir?
- ¿Comprende las opciones disponibles?
- ¿Puede completar el proceso?
- ¿Comete errores?
- ¿Se queda bloqueado?
- ¿Necesita ayuda?

---

# 21. El éxito no significa solamente llegar al final

Es necesario registrar cómo llegó el usuario al resultado.

Se pueden considerar cuatro estados:

### Éxito autónomo

El usuario completa la tarea sin ayuda.

**Resultado ideal.**

### Éxito con dudas

El usuario completa la tarea sin ayuda, pero manifiesta dudas importantes.

**Debe analizarse.**

### Éxito con ayuda

El usuario completa la tarea, pero el facilitador tuvo que intervenir.

**No debería considerarse un éxito completo.**

### Fracaso

El usuario no logra completar la tarea.

**El flujo necesita revisión.**

Como instrumento interno puede utilizarse una escala:

| Resultado | Valor |
|---|---:|
| Completa sin ayuda | 3 |
| Completa con dudas pero sin ayuda | 2 |
| Completa con ayuda | 1 |
| No completa | 0 |

La escala es solamente un mecanismo de apoyo. Lo importante es identificar patrones y entender las causas.

---

# 22. Organización de la sesión de evaluación

La sesión debería tener roles claramente definidos.

## Facilitador

Una persona conduce la sesión.

Sus responsabilidades son:

- Explicar el ejercicio.
- Entregar la tarea.
- Hacer preguntas neutrales.
- Observar.
- Registrar resultados.
- Evitar enseñar la solución.

El facilitador debe intervenir lo mínimo posible.

## Observadores

Representantes de la empresa dueña de la aplicación pueden participar como observadores.

Pueden:

- Observar.
- Tomar notas.
- Registrar comportamientos.
- Escuchar comentarios.

Pero:

> **No deben intervenir durante la interacción del usuario con el prototipo.**

## Usuario

Realiza la tarea utilizando el prototipo.

## Sponsor

Puede observar, pero no debería responder las preguntas del usuario durante la prueba.

Por ejemplo, si el usuario pregunta:

> "¿Aquí debo poner la dirección?"

El sponsor no debería responder:

> "Sí."

El facilitador debería mantener la neutralidad y permitir que el usuario tome su propia decisión.

---

# 23. Selección de usuarios

No deberían seleccionarse únicamente usuarios que sean fáciles de conseguir o que tengan una relación favorable con la empresa.

Idealmente, antes de la prueba se debe definir:

> **¿Qué características debe tener un usuario real del Actor que estamos evaluando?**

Por ejemplo:

- Experiencia baja.
- Experiencia media.
- Experiencia alta.
- Tipo de cliente.
- Frecuencia de uso del proceso.
- Contexto operativo.
- Tipo de necesidad.

El objetivo es que los participantes representen razonablemente al Actor real.

---

# 24. Preguntas posteriores a la tarea

Después de completar la tarea se pueden realizar preguntas, pero deben ser neutrales.

## Comprensión

> "¿Qué creías que iba a pasar cuando hiciste clic aquí?"

## Dificultad

> "¿Hubo algún momento en el que no supieras qué hacer?"

## Expectativa

> "¿Esperabas encontrar alguna otra opción?"

## Necesidad

> "¿Qué información necesitarías realmente para completar esta solicitud?"

## Proceso actual

> "¿Cómo haces esto actualmente?"

Esta última pregunta es especialmente importante porque permite comparar la solución propuesta con el comportamiento real.

---

# 25. No preguntar inicialmente "¿Te gustó?"

Las preguntas de opinión tienen un valor limitado.

Por ejemplo:

> "¿Te gusta la aplicación?"

o:

> "¿La utilizarías?"

pueden producir respuestas positivas que no necesariamente demuestran que la solución funciona.

La evidencia principal debe provenir de:

> **Lo que el usuario hace.**

La opinión del usuario es complementaria.

---

# 26. Cuatro dimensiones de validación

La evaluación del prototipo debe considerar al menos cuatro dimensiones.

## A. Ejecución

> **¿Puede el usuario completar la tarea?**

## B. Comprensión

> **¿Comprende lo que está haciendo y el significado de las opciones que utiliza?**

## C. Validación de la necesidad

> **¿El flujo representa una forma válida de resolver la necesidad real del usuario?**

## D. Validación del negocio

> **¿El flujo representa correctamente el proceso de negocio que la empresa quiere implementar?**

Las dos últimas dimensiones deben mantenerse diferenciadas.

---

# 27. Validación del usuario vs. validación del negocio

El usuario valida principalmente:

> **"Esto representa correctamente cómo yo realizaría esta tarea."**

La empresa o sponsor valida:

> **"Este flujo es compatible con el proceso de negocio que queremos implementar."**

No deben mezclarse ambas validaciones.

Es posible que:

- El usuario entienda y pueda utilizar el flujo.
- Pero el sponsor descubra que el proceso no es compatible con una regla interna de la empresa.

También puede ocurrir lo contrario:

- El proceso de negocio sea correcto.
- Pero los usuarios no puedan utilizarlo fácilmente.

Ambas dimensiones deben ser satisfactorias.

---

# 28. Las observaciones no son automáticamente requisitos

Durante la evaluación los usuarios probablemente realizarán comentarios como:

> "Sería bueno que también pudiera hacer X."

Esto no significa automáticamente que:

> "El prototipo fracasó porque no tiene X."

Las observaciones deben clasificarse posteriormente como:

- Problema funcional.
- Problema de comprensión.
- Problema de usabilidad.
- Necesidad no contemplada.
- Sugerencia.
- Nueva funcionalidad potencial.
- Caso excepcional.
- Requisito de negocio.
- Idea para una fase posterior.

Por lo tanto:

> **Una observación del usuario no se convierte automáticamente en un requisito del MVP.**

---

# 29. Definición preliminar de éxito del prototipo

A partir de lo discutido hasta este momento, se propone la siguiente definición:

> **Un prototipo es exitoso cuando usuarios representativos del Actor que se está evaluando pueden completar de manera autónoma el camino feliz definido, comprenden lo que están haciendo y confirman que el flujo representa una forma válida de resolver la necesidad que la aplicación pretende atender.**

Adicionalmente:

> **El proceso de negocio representado por el prototipo debe ser considerado válido por la empresa dueña de la aplicación.**

Por lo tanto, el éxito tiene dos perspectivas principales:

**Usuario**

→ Puede hacerlo y entiende lo que está haciendo.

**Empresa**

→ El proceso representado es correcto y válido para el negocio.

---

# 30. Principio de no sesgo

La evaluación debe buscar minimizar cualquier influencia externa sobre el comportamiento del usuario.

Principios:

1. No explicar previamente cómo utilizar el prototipo.
2. Presentar una tarea, no una secuencia de clics.
3. Permitir que el usuario explore.
4. No corregir inmediatamente los errores.
5. No responder preguntas de manera que revele la solución.
6. Evitar que el sponsor intervenga.
7. Registrar el comportamiento antes que las opiniones.
8. Preguntar después de la interacción.
9. Utilizar usuarios representativos.
10. Separar las observaciones del usuario de las decisiones del negocio.

---

# 31. Estado actual de la metodología

Hasta este punto se han definido dos componentes importantes.

## Componente 1 — Taxonomía de actores

- Actor Generador.
- Actor Coordinador.
- Actor Ejecutor.
- Actor Supervisor.
- Actor Administrador de Plataforma.
- Actor Integrador.

## Componente 2 — Evaluación del prototipo

El prototipo debe:

- Tener un objetivo funcional concreto.
- Evaluarse mediante tareas.
- Ser probado con usuarios representativos.
- Priorizar la observación sobre la opinión.
- Minimizar el sesgo.
- Separar la validación del usuario de la validación del negocio.
- Determinar si el camino feliz puede ser ejecutado de forma autónoma.
- Clasificar las observaciones sin convertirlas automáticamente en requisitos.

---

