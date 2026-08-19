# SIGEVA

**Sistema de Gestión Electoral y Validación de Votos**

SIGEVA es una plataforma electoral digital. No es un formulario con contador. Es el recinto, el jurado, el tarjetón, la urna y el acta, convertidos en software.

Nació en el SENA para que los aprendices elijan representantes sin filas, sin papel y sin duda sobre quién ya votó. Se formula ahora, en etapa de **análisis**, para documentar lo que ya existe y convertirlo en un producto **multi-tenant**: la misma plataforma, muchas organizaciones, cada una con su censo, sus gestores y sus elecciones, sin mezclar un voto con el de otra.

Este archivo tiene dos partes:

1. **Qué es SIGEVA** — la explicación del producto. Léanla completa antes de llenar el Word.
2. **Texto para el FS-DOC** — las mismas ideas, en el orden exacto del formulario, listas para copiar.

---

# Parte 1 — Qué es SIGEVA

## La idea en una frase

**SIGEVA permite convocar una elección, habilitar quién puede votar, presentar candidatos, emitir un voto único verificado y publicar un resultado auditable, desde el navegador, a la escala de un centro, de toda una red institucional o, a futuro, de cualquier organización.**

Si una institución necesita elegir un representante, un vocero, un comité o una mesa, SIGEVA es el sistema que corre ese proceso de principio a fin.

## Por qué existe

Una elección institucional parece simple hasta que se hace en serio.

En el SENA el padrón no es una lista de diez nombres. Son aprendices distribuidos en regionales, centros de formación, fichas, programas y jornadas (mañana, tarde, noche). El que estudia de noche no puede hacer fila a las 10 a.m. El que está en práctica no está en el aula el día de la urna. El Excel del instructor no es un censo. El conteo en el tablero no es un acta. Y cuando alguien pregunta “¿ya votó fulano?” nadie tiene una respuesta que se pueda demostrar.

Eso no es un problema de “falta una página web”. Es un problema de **proceso electoral**:

| Lo que exige una elección real | Lo que pasa sin SIGEVA |
| --- | --- |
| Un censo cerrado y verificable | Listados impresos o hojas sueltas |
| Una ventana oficial de votación | “Voten cuando puedan” |
| Un tarjetón con candidatos identificables | Nombres en un grupo de WhatsApp |
| Un voto por persona, indelegable | Nadie impide el doble voto |
| Prueba de que quien vota es quien dice ser | Confianza ciega en el correo o en el compañero |
| Un resultado que se puede mostrar y defender | Conteo manual, empates opacos, actas tardías |

SIGEVA existe para cerrar esa brecha. El SENA fue el primer territorio. El producto no debería morir ahí: cualquier colegio, universidad, cooperativa o empresa que elija representación interna vive el mismo problema. Por eso el análisis de este proyecto no es “inventar una app de votos”. Es **entender el motor electoral que ya corre** y **diseñarlo como plataforma**, no como un desarrollo de un solo cliente.

## Qué tipo de sistema es

SIGEVA es un **sistema de información electoral de ciclo completo**.

Eso significa que no empieza cuando el votante hace clic. Empieza cuando un gestor construye el padrón y termina cuando un reporte dice quién ganó, con cuántos votos, y si hubo empate.

Tres capas mentales, que hay que explicar siempre en ese orden:

1. **Gobierno del proceso** — quién puede crear una elección, cargar personas y ver resultados. En el SENA: Administrador de plataforma y Funcionario de centro. En el rediseño: dueño del tenant y gestores de sede.
2. **Contienda** — la elección (nombre, circunscripción, jornada, apertura y cierre) y los candidatos (persona del censo, propuesta, foto, número de tarjetón único).
3. **Sufragio** — el votante autenticado ve solo lo que le corresponde, demuestra el correo con un OTP de un solo uso, elige y el sistema registra un voto que no se puede repetir.

Un Google Form cubre, mal, el punto 3. SIGEVA cubre los tres. Esa es la diferencia de producto.

## A quién le sirve (los tres mundos)

El sistema no tiene “usuarios”. Tiene **roles electorales**. Cada uno ve un producto distinto.

### El votante (hoy: Aprendiz)

Entra por la puerta pública, inicia sesión con su correo y ve **únicamente las elecciones abiertas de su centro y de su jornada**. No ve la red nacional. No ve el padrón. No administra nada.

Su camino es deliberadamente corto: elecciones activas → tarjetón (candidato, foto, propuesta, número) → confirmación con código de 6 caracteres al correo → comprobante de voto emitido.

Eso no es un detalle de UI. Es la regla de una urna: el votante no debe poder explorar el sistema, solo ejercer el derecho.

Estados con los que el padrón decide si esa persona puede pedir OTP: `activo`, `en formacion`, `suspension`, `pendiente`, `condicionado`. Un aprendiz cancelado o retirado no entra a la urna.

### El gestor de sede (hoy: Funcionario)

Es el jurado digital de un centro de formación. Su mundo está acotado a **su** centro. No opera el país. Opera una sede.

Con él vive el día a día electoral:

- Carga el censo desde el Excel institucional de la ficha (el sistema lee grupo y programa, crea o actualiza aprendices, reporta insertados / actualizados / omitidos).
- Abre una elección: nombre, jornada, fecha y hora de inicio, fecha y hora de fin.
- Inscribe candidatos: toma a un aprendiz del padrón, le pone propuesta, foto (Cloudinary) y tarjetón. El tarjetón no se duplica dentro de la misma elección.
- Sigue el tablero: elecciones de su centro, votantes habilitados, votos del día.
- Baja el acta: totales por candidato, participación, ganador o empate, PDF.

### El administrador de red

Ve la institución completa. Crea funcionarios, asigna centro, carga padrones eligiendo sede, da de alta aprendices uno a uno. Es quien sostiene la red cuando SIGEVA corre a escala SENA: muchas regionales, muchos centros, muchos gestores.

En el rediseño multi-tenant este rol se parte en dos: **operador de la plataforma** (da de alta organizaciones) y **administrador del tenant** (gobierna su propia institución). Hoy esa separación aún no existe; el análisis debe diseñarlas.

## Cómo corre una elección de verdad (el viaje completo)

Imaginen el Centro de Biotecnología Agropecuaria, jornada noche, elección de vocero 2026.

**1. Se arma el padrón.**  
El funcionario sube el Excel de la ficha. SIGEVA no “importa una tabla”: interpreta un documento SENA (ficha en la celda C2, filas de aprendices desde la 5). Deduplica por documento y correo dentro del archivo y contra la base. Si el aprendiz ya existía, lo actualiza. Si es nuevo, lo crea con clave temporal. El centro no lo escribe el Excel: lo impone el usuario que importa. Un funcionario no puede cargar el padrón de otro centro. Eso es aislamiento territorial, el embrión del tenant.

**2. Se convoca.**  
Se crea la elección con una ventana real: no solo días, también horas. Una votación puede abrir el martes a las 18:00 y cerrar el jueves a las 21:00. El listado de “elecciones activas” no es un CRUD: es un filtro temporal. Si usted entra el lunes, la urna no existe. Si entra el viernes, ya cerró.

**3. Se arma el tarjetón.**  
Cada candidato es una persona del censo, no un nombre suelto. Tiene propuesta, fotografía y número de tarjetón. El tarjetón es único por elección: no puede haber dos “03”. Al mostrar candidatos al votante, el backend los desordena (`RANDOM()`): el primero de la lista no es “el de la administración”.

**4. Se vota.**  
El aprendiz autentica. El sistema le muestra solo lo abierto en **su centro** y **su jornada**. Pide un OTP. El backend comprueba: la persona existe, su estado lo habilita, la elección existe, centro del aprendiz = centro de la elección, y no hay un voto previo marcado `VOTED_`. Entonces genera un código de 6 caracteres, lo guarda, lo manda al correo y lo hace caducar (5 minutos por defecto). Validar el OTP no registra el voto: solo prueba el buzón. El voto es un segundo acto, protegido por un middleware que vuelve a preguntar: ¿esta persona ya sufragó en esta elección? Si sí, se detiene.

**5. Se escruta.**  
El reporte no “cuenta clics”. Cruza candidatos con votos, incluye a quien sacó cero, cuenta participantes distintos (no filas), toma el máximo y, si hay dos con el mismo tope, declara empate. El frontend arma un PDF con membrete, totales y resultado. Eso es el acta.

Ese ciclo es SIGEVA. Todo lo demás (dashboards, CRUD, Swagger) existe para que ese ciclo no se rompa.

## Qué lo hace un sistema electoral y no una encuesta

Hay cinco invariantes. Si alguna se pierde, SIGEVA deja de ser SIGEVA.

1. **Un ciudadano, un voto.** El padrón define quién existe. El middleware y la marca `VOTED_` impiden el segundo sufragio. No es un `UNIQUE` decorativo: es la urna.
2. **Identidad de dos factores débiles, suficientes para el dominio.** Usuario + contraseña demuestran “conozco la cuenta”. El OTP al correo demuestra “tengo el buzón que el censo registró”. No es biometría ni cédula con chip; es el nivel correcto para una elección institucional remota.
3. **Circunscripción.** Nadie vota en el centro de al lado. Nadie de la mañana entra a la urna de la noche. Territorio y jornada no son filtros de reporte: son la geometría del derecho al voto.
4. **Ventana oficial.** Fuera de fecha y hora no hay elección, aunque el registro siga en la base. Una urna que nunca cierra no es una urna.
5. **Resultado defendible.** Totales, participación, ganador o empate, documento descargable. El número que se publica tiene que poder reconstruirse desde los votos guardados.

Sobre esas cinco reglas se puede construir una plataforma. Sin ellas, se construye un Google Form con logo del SENA.

## El mapa del SENA por dentro

SIGEVA no nació genérico. Nació entendiendo cómo está armado el SENA, y por eso escala a nivel nacional en el primer cliente.

```text
País
 └── Departamento
      └── Municipio
           └── Regional SENA
                └── Centro de formación          ← hoy, el “tenant” implícito
                     ├── Funcionario (gestor)
                     ├── Aprendices (censo)
                     │     ├── Grupo / ficha
                     │     ├── Programa y nivel
                     │     └── Jornada
                     └── Elecciones de ese centro
                           ├── Candidatos (tarjetón + propuesta + foto)
                           ├── OTP de validación
                           └── Votos
```

El script `subida_centros_formacion.sql` no es un seeder de prueba: es el mapa real de centros (códigos, subdirectores, correos, municipios). SIGEVA está pensado para correr sobre esa red, no sobre “un colegio de ejemplo”.

Eso es una fortaleza y una trampa. Fortaleza: el producto ya habla el idioma del cliente más grande. Trampa: `aprendiz`, `regional` y `ficha` están pegados al núcleo. El análisis multi-tenant consiste en **separar el motor electoral de ese vocabulario**, no en borrar el SENA.

## La visión: de “app del SENA” a plataforma

Hoy el aislamiento es por centro de formación. Un funcionario no carga el padrón ajeno. Un aprendiz no vota en otra sede. Eso ya es multi-sede. **No es multi-tenant.**

Multi-tenant significa: el mismo código, la misma base (o el mismo esquema), **varias organizaciones dueñas de sus datos**, sin que el colegio X vea los votos de la universidad Y.

| Concepto SENA (as-is) | Concepto de plataforma (to-be) |
| --- | --- |
| SENA como único mundo | Organización (tenant) |
| Centro de formación | Sede / circunscripción |
| Aprendiz | Votante del censo |
| Funcionario | Gestor electoral |
| Administrador único | Operador de plataforma + admin del tenant |
| Excel de ficha SENA | Plantilla de importación del tenant (el Excel SENA queda como preset) |
| Jornada mañana/tarde/noche | Dimensión de circunscripción (el SENA la sigue usando; otro cliente puede no) |

El núcleo que **no cambia** es el valioso: censo, elección con ventana, tarjetón, OTP, voto único, acta. Lo que cambia es **quién es dueño** de ese núcleo.

Cuando eso esté diseñado, SIGEVA deja de ser “el sistemita de votos del SENA” y pasa a ser **infraestructura electoral para cualquier institución que necesite representación interna**. Ese es el salto de producto. Esa es la razón de volver a análisis.

## Cómo está construido (visión de arquitectura)

Dos repositorios, un solo sistema.

```text
  Navegador
     │
     │  React 19 + Vite + TypeScript
     │  sigevaFront
     │  (urna del votante | mesa del gestor | torre del admin)
     ▼
  API REST  AdonisJS 6
     │  sigevaBack   :3333
     │  Swagger /docs
     │
     ├── PostgreSQL     censo, elecciones, votos, auditoría OTP
     ├── SMTP           el OTP sale del servidor, no de la pantalla
     └── Cloudinary     fotos del tarjetón
```

El frontend no “tiene la verdad”. La verdad está en la API: reglas de centro, de jornada, de OTP, de voto único, de ganador. El cliente pinta el recinto. El servidor es el jurado.

Stack, dicho en una línea: TypeScript de punta a punta, Lucid/PostgreSQL, bcrypt, VineJS, Excel (`xlsx`), correo institucional, PDF de acta (`jsPDF`). Es un stack de producto, no de taller.

## Qué hay que decirle a un instructor o a un compañero nuevo

Usen este párrafo, de memoria:

> SIGEVA es la plataforma con la que una institución corre una elección interna de principio a fin. En el SENA, el funcionario de un centro carga el padrón de aprendices, abre la votación por jornada, arma el tarjetón de candidatos y el aprendiz vota desde su casa con un código que le llega al correo. El sistema garantiza un solo voto, no deja votar en otro centro ni fuera de horario, y entrega un acta con ganador o empate. El proyecto ahora se analiza para sacar ese motor del molde SENA y convertirlo en multi-tenant: que un colegio, una universidad o una empresa puedan usar la misma plataforma, cada uno en su propia urna.

Si después de eso alguien pregunta “¿entonces es un login y un CRUD?”, la respuesta es no. Es un **proceso electoral implementado**.

---

# Parte 2 — Contenido para el formulario FS-DOC

Copiar en el mismo orden del Word. `[POR COMPLETAR]` lo llena el equipo (firmas, patrocinador, URL de producción).

## Portada

| Campo | Texto |
| --- | --- |
| Nombre del proyecto | SIGEVA — Sistema de Gestión Electoral y Validación de Votos |
| Fecha | 19/08/2026 |

## Historial de versiones *(del documento, no del software)*

| Fecha | Versión | Autor | Descripción |
| --- | --- | --- | --- |
| 19/08/2026 | 1.0 | Equipo SIGEVA — Fábrica de Software | Primera formulación: producto reconstruido desde el código y visión multi-tenant |
| `[POR COMPLETAR]` | | | |

## Información del proyecto

| Campo | Texto |
| --- | --- |
| Empresa / Organización | Servicio Nacional de Aprendizaje — SENA. Área: Fábrica de Software |
| Proyecto | SIGEVA (Sistema de Gestión Electoral y Validación de Votos) |
| Fecha de preparación | 19/08/2026 |
| Cliente | Actual: SENA, centros de formación a nivel nacional. Objetivo del rediseño: cualquier institución u organización que requiera elecciones internas digitales |
| Patrocinador principal | `[POR COMPLETAR: p. ej. Henry Bastidas — Product Owner / Coordinación Fábrica de Software]` |

## Aprobaciones

Dejar la tabla del Word para firmas. Referencia de roles (página *Sobre nosotros* del frontend):

| Nombre | Rol | Cargo sugerido |
| --- | --- | --- |
| Henry Bastidas | Product Owner | Patrocinador / PO |
| Alexandra Guevara Muñoz | Supervisora | Supervisión académica |
| Jorge Enrique Porras | Scrum Master | Líder técnico / SM |
| Equipo de desarrollo | Construcción | Analistas / desarrolladores |

## 1. Título del proyecto

Metodología P.O.P. del formato:

- **P**roceso: análisis, diseño, desarrollo e implantación
- **O**bjeto: un sistema de gestión electoral y validación de votos
- **P**articularidad: SIGEVA, plataforma multi-tenant para instituciones educativas y organizaciones

**Título (copiar tal cual):**

> Análisis, diseño, desarrollo e implantación de SIGEVA: sistema de gestión electoral y validación de votos, con arquitectura multi-tenant para instituciones educativas y organizaciones.

**Variante corta:**

> Análisis, diseño, desarrollo e implantación de un sistema de votación digital multi-tenant (SIGEVA) para el SENA y otras organizaciones.

## 2. Planteamiento del problema, necesidad u oportunidad

Las elecciones internas del SENA —voceros y representantes de aprendices— se han resuelto como un acto presencial: padron en papel o Excel, urna física, conteo a mano. Ese modelo no soporta la geometría real de la institución. Hay regionales, cientos de centros, fichas, programas y tres jornadas. El aprendiz de noche, el de práctica y el de un centro distante no llegan a la mesa. El listado impreso no dice quién ya votó. El tablero no es un acta. El doble voto no se puede demostrar ni impedir. La desconfianza no es un rumor: es el resultado natural de un proceso que no deja huella.

La pregunta que el sistema de información debe responder es precisa: **¿cómo garantizar que cada persona habilitada vote una sola vez, en la circunscripción que le corresponde, dentro de una ventana oficial, y que el resultado se pueda mostrar el mismo día?**

SIGEVA es la respuesta que ya está en código. El funcionario carga el censo, abre la elección, arma el tarjetón; el aprendiz autentica, confirma el correo con OTP y sufragia; el sistema bloquea el segundo voto y emite totales, participación y ganador o empate. No es un requerimiento nuevo en blanco. Es un **producto construido a contrarreloj, sin artefactos de análisis**, que ahora hay que entender, documentar y decidir.

Esa ausencia de análisis es parte del problema. Sin documento no hay alcance, no hay onboarding de compañeros, no hay criterio para decir qué es núcleo y qué es accidente SENA. El código existe (`sigevaBack`, `sigevaFront`); la definición de producto, no.

La oportunidad de esta etapa es doble:

1. **Estabilizar el as-is.** Roles (Administrador, Funcionario, Aprendiz), árbol territorial SENA, importación de fichas, elecciones con fecha y hora, OTP, voto único, reportes PDF. Eso ya opera y hay que tratarlo como activo, no como prototipo desechable.
2. **Abrir el to-be multi-tenant.** Hoy el mundo es el SENA y el aislamiento es el centro de formación. Un colegio, una universidad o una empresa no tienen “aprendiz” ni “regional”. El análisis debe extraer el motor (censo, contienda, urna, acta) y ponerle dueño: una organización. El SENA queda como el primer tenant, no como el único universo posible.

Lo que se quiere solucionar: **elecciones internas íntegras, remotas y defendibles, primero en el SENA y después en cualquier organización, sobre un mismo producto parametrizable.**

## 3. Justificación del proyecto

### Diagnóstico

El SENA es un país electoral pequeño: muchas sedes, mucho padrón, poco tiempo de urna. Un software genérico de encuestas no conoce ficha, jornada ni centro. Un SaaS extranjero cobra por votante y se lleva los datos. Un desarrollo “solo SENA” eterniza el acoplamiento. El camino correcto es el que ya empezó el equipo: un motor propio, nacido en el dominio real, que se documenta y se generaliza.

### ¿Qué se va a hacer?

Analizar, diseñar, desarrollar e implantar SIGEVA como plataforma de votación digital de ciclo completo, partiendo del sistema actual y evolucionándola a multi-tenant.

### ¿Por qué se va a hacer?

Porque el voto presencial excluye, el conteo manual no se defiende, y el código existente no se puede mantener ni ofrecer a otro cliente mientras el SENA esté soldado al núcleo.

### ¿Para qué se va a hacer?

Para que un dueño de organización configure su urna, un gestor arme censo y contienda, y un votante ejerza un derecho único, verificado y acotado, con un acta el mismo día.

### ¿Cómo se va a hacer?

Ciclo de vida de software: ingeniería inversa del producto actual (pantallas, API, reglas), diseño de arquitectura multi-tenant, desarrollo incremental sobre AdonisJS y React, pruebas de las cinco invariantes electorales, implantación y guía de alta de una nueva organización.

### ¿Quién lo va a hacer?

Fábrica de Software del SENA: Product Owner, Scrum Master, backend, frontend, móvil, UI/UX, con supervisión académica.

### Beneficios

- Participación remota real: la urna viaja al votante, no al revés.
- Integridad: un voto, un correo verificado, una circunscripción, una ventana.
- Operación institucional: Excel de fichas, tarjetón con foto, acta PDF, dashboards por rol.
- Escala SENA: la red de centros ya está modelada, no es un demo.
- Palanca de producto: el mismo motor, muchos clientes, sin reescribir la urna.

## 4. Objetivo general

Analizar, diseñar, desarrollar e implantar SIGEVA, un sistema de información web para la gestión de procesos electorales digitales con censo, contienda, validación de identidad del votante, voto único y resultados auditables, evolucionando la solución actual del SENA hacia una arquitectura multi-tenant utilizable por cualquier organización.

Medible (módulos y tenant configurables), alcanzable (parte de un backend y un frontend ya construidos), verificable (prueba de extremo a extremo y de aislamiento entre organizaciones) y acotado (no incluye biometría ni urna física).

## 5. Objetivos específicos

Alineados al ciclo de vida y a una entrega que se pueda señalar con el dedo.

1. **Analizar** el proceso electoral (padrón, convocatoria, sufragio, escrutinio) y el software existente, para fijar actores, invariantes, acoplamientos SENA y requisitos del tenant.
2. **Diseñar** arquitectura, modelo de datos (organización, sede, censo, elección, candidato, voto, auditoría) e interfaces por rol, con el núcleo electoral independiente de la nomenclatura SENA.
3. **Desarrollar** autenticación por perfil, censo (alta e importación), elecciones, tarjetón, OTP, voto único y actas.
4. **Verificar** las invariantes: un votante no vota dos veces, el OTP caduca, nadie cruza de circunscripción, el acta reconstruye los votos.
5. **Implantar** la plataforma, parametrizar el tenant SENA y dejar el procedimiento para dar de alta una organización nueva.

## 6. Alcance y viabilidad

### Producto

- **sigevaFront:** React 19, Vite, TypeScript, Bootstrap. Puerta pública, urna del aprendiz, mesa del funcionario, torre del administrador, PDF de acta.
- **sigevaBack:** API REST AdonisJS 6, PostgreSQL, SMTP (OTP), Cloudinary (fotos), Swagger en `/docs`.

**Dentro de alcance**

| Módulo | Hoy | Multi-tenant |
| --- | --- | --- |
| Identidad y perfiles | Administrador, Funcionario, Aprendiz | Operador de plataforma, admin del tenant, gestor, votante |
| Territorio | Departamento → municipio → regional → centro | Tenant → sedes (el árbol SENA es el preset del primer cliente) |
| Censo | Aprendices, ficha, programa, jornada; Excel institucional | Censo del tenant; plantilla configurable |
| Elección | Nombre, centro, jornada, fecha y hora de apertura/cierre | Elección de una circunscripción del tenant |
| Tarjetón | Aprendiz + propuesta + foto + número único | Candidato del censo, sin exigir “aprendiz” |
| OTP | 6 caracteres al correo; caducidad; marcas USED_ / VOTED_ | Servicio transversal |
| Voto | `votoxcandidato` + middleware de unicidad | Igual, aislado por tenant |
| Acta | Totales, participantes, ganador o empate, PDF | Acta con identidad de la organización |

**Fuera de alcance**

- Biometría, urna física, lectura de cédula con hardware.
- Integración con Registraduría o censo nacional.
- Voto criptográfico tipo Helios (línea futura, no este ciclo).
- App móvil nativa como entrega obligatoria (hay rol en el equipo; el núcleo es web).
- Campaña, foros o redes de candidatos.
- Sistemas misionales del SENA ajenos a la elección.

### Proceso de uso

1. Se crea la organización (o se usa el SENA como primer tenant) y sus gestores.
2. Se carga el censo.
3. Se abre la elección (ventana y circunscripción).
4. Se arma el tarjetón.
5. El votante entra, recibe OTP, elige, confirma.
6. El sistema sella el voto único y emite el acta.

### Contexto

Implantación primera: red de centros SENA (`subida_centros_formacion.sql`). Destino: cualquier organización con padrón y contienda interna.

### Viabilidad

| Recurso | Lectura |
| --- | --- |
| Tiempo | El núcleo existe. El ciclo de análisis + rediseño de tenant + endurecimiento cabe en un proyecto de fábrica; no se parte de cero. |
| Dinero | Node, PostgreSQL, SMTP, Cloudinary. Sin licencia de motor electoral comercial. |
| Gente | Equipo ya armado (PO, SM, backend, frontend, móvil, UI/UX). El riesgo era la falta de documento; este archivo lo ataca. |
| Material | Servidor Node/PostgreSQL, correo, almacenamiento de imágenes, navegador en el votante. |

**Veredicto:** viable. Se reutiliza un producto en marcha, el dominio está aprendido, y el salto multi-tenant es de modelo y autorización, no de tipo de sistema.

## 7. Resumen del proyecto *(máximo 100 palabras)*

SIGEVA es una plataforma para correr elecciones internas de principio a fin: arma el censo, abre la urna, presenta candidatos y permite un voto remoto único, verificado con OTP, con acta de ganador o empate. En el SENA, los aprendices eligen representantes por centro y jornada sin papel. El proyecto documenta esa solución —construida sin análisis formal— y la convierte en multi-tenant, para que cualquier institución configure su organización y sus comicios sobre el mismo motor electoral.

*(99 palabras)*

## 8. Glosario

| Término | Significado en SIGEVA |
| --- | --- |
| SIGEVA | Sistema de Gestión Electoral y Validación de Votos. La plataforma. |
| Motor electoral | Núcleo reutilizable: censo, elección, tarjetón, OTP, voto único, acta. |
| Tenant | Organización dueña de sus datos. Hoy, de forma imperfecta, el centro de formación. Mañana, el cliente (SENA, colegio, empresa). |
| Multi-tenant | Un solo software, muchas organizaciones aisladas, sin copiar el código por cliente. |
| Circunscripción | Quién puede votar en una elección. Hoy: centro + jornada. |
| Censo / padrón | Personas habilitadas. Hoy: aprendices de un centro. |
| Aprendiz | Votante en el modelo SENA. |
| Funcionario | Gestor electoral de una sede. |
| Administrador | Gobierna la red de centros y funcionarios. |
| Elección | Contienda con nombre, circunscripción y ventana de fechas/horas. |
| Jornada | Mañana, tarde o noche. Dimensión SENA del derecho al voto. |
| Tarjetón | Número único del candidato en una elección. |
| OTP | Código de un solo uso al correo; prueba el buzón del censo. Caduca. |
| Voto único | Invariante: una persona, una elección, un sufragio. |
| Acta | Resultado defendible: totales, participación, ganador o empate, PDF. |
| Regional / centro | Geografía SENA. El centro es la urna territorial actual. |
| Ficha / grupo | Cohorte del aprendiz; entra por el Excel institucional. |
| Invariante | Regla que, si se rompe, el sistema deja de ser electoral. |

## 9. Investigación tecnológica / antecedentes / vigilancia tecnológica

No se busca “apps parecidas”. Se busca **quién ya resolvió elecciones internas**, qué se puede aprender y por qué SIGEVA no se reemplaza con una licencia.

### 9.1 SIGEVA (línea base)

| Campo | Valor |
| --- | --- |
| Nombre | SIGEVA |
| Tipo | Web (API + SPA). Capacidad móvil en el equipo; el núcleo es web |
| Características | Ciclo completo: censo, contienda, urna OTP, voto único, acta. Roles, árbol SENA, Excel de fichas, Cloudinary, PDF |
| País / región | Colombia, red de centros SENA |
| URL | API local `http://localhost:3333` (`/docs`). Producción: `[POR COMPLETAR]` |
| Licencia | Código del proyecto (`UNLICENSED`). Uso institucional |

### 9.2 EVS para universidades en Colombia

| Campo | Valor |
| --- | --- |
| Nombre | Electronic Voting System for Universities in Colombia |
| Tipo | Web institucional (investigación) |
| Características | Padrón, fórmulas, jurados, votación, reportes; se apoya en la Ley 892 de 2004 |
| País / región | Colombia |
| URL | https://www.scitepress.org/Papers/2019/79291/79291.pdf |
| Licencia | Publicación académica; no es un producto adoptable |

### 9.3 Voto electrónico ETITC

| Campo | Valor |
| --- | --- |
| Nombre | Voto electrónico — Escuela Tecnológica Instituto Técnico Central |
| Tipo | Módulo del sistema académico institucional |
| Características | Voto secreto con cuenta personal, comité de transparencia, respaldo de BD al abrir la jornada |
| País / región | Colombia (Bogotá) |
| URL | https://etitc.edu.co/archives/acuerdo042021.pdf |
| Licencia | Uso interno; no reutilizable |

### 9.4 Helios Voting

| Campo | Valor |
| --- | --- |
| Nombre | Helios Voting |
| Tipo | Web, voto verificable criptográficamente |
| Características | Cifrado, verificación de extremo a extremo, referente académico mundial |
| País / región | Internacional |
| URL | https://heliosvoting.org |
| Licencia | Código abierto |
| Lectura | Excelente criptografía; pésima operación SENA (fichas, jornadas, red de centros). Complejidad de más para el primer usuario institucional. Línea futura, no sustituto |

### 9.5 Simply Voting / ElectionBuddy

| Campo | Simply Voting | ElectionBuddy |
| --- | --- | --- |
| Tipo | SaaS web | SaaS web |
| Características | Censo, boletas, correo, resultados, modelo multi-organización | Igual, enfocado en juntas y asociaciones |
| País / región | Internacional | Internacional |
| URL | https://www.simplyvoting.com | https://electionbuddy.com |
| Licencia | Comercial, cobro por votante |
| Lectura | Son el espejo del to-be (tenant, onboarding, UX de urna). No conocen el Excel de fichas ni la jerarquía SENA. Llevar el padrón a un tercero es un no institucional |

### 9.6 Google Forms / Microsoft Forms

El anti-patrón. No hay circunscripción, no hay voto único demostrable, no hay ventana de urna, no hay acta. Es lo que SIGEVA viene a matar.

### Lectura de vigilancia

La Ley 892 de 2004 habla del voto electrónico ciudadano. SIGEVA **no** sustituye a la Registraduría. Compite en **elecciones internas**. Las universidades colombianas construyen software propio. Los SaaS internacionales ya son multi-tenant y cobran por ello. La decisión de producto es nítida: **conservar el dominio SENA ya pagado en código y absorber de los SaaS el modelo de organización aislada**, en vez de comprar una urna que no entiende qué es una ficha.

---

# Anexo para el equipo *(no va en el Word)*

## Repositorios

| Capa | Repo | Qué es |
| --- | --- | --- |
| API | `sigevaBack` | El jurado. AdonisJS 6, PostgreSQL, `/docs` |
| Web | `sigevaFront` | El recinto. React 19, Vite |

## Invariantes (contrato de calidad)

1. Un votante, una elección, un voto.
2. OTP al correo del censo; caduca; validar ≠ votar.
3. Nadie vota fuera de su centro ni de su jornada.
4. Fuera de la ventana no hay urna.
5. El acta se reconstruye desde los votos.

## Flujo técnico del sufragio

1. Login aprendiz (bcrypt).
2. Listado de elecciones activas del centro, filtradas por ahora y por jornada.
3. `POST /api/validaciones/generarOtp` — estado habilitado, mismo centro, sin `VOTED_`, limpia OTP viejos, envía correo.
4. `POST /api/validaciones/validarOtp` — no expirado → marca `USED_`.
5. `POST /api/votoXCandidato/crear` — middleware de voto único → inserta.
6. `GET /api/reporte/eleccion/:id` — totales, participantes distintos, ganador o empate.

## Entidades actuales

`perfil` · `usuarios` · `aprendiz` · `grupo` · `programa_formacion` · `nivel_formacion` · `departamento` · `municipio` · `regional` · `centro_formacion` · `elecciones` · `candidatos` · `validacionvoto` · `votoxcandidato`

El tenant implícito es `centro_formacion`. No hay tabla `organizacion`. Eso es exactamente lo que el análisis debe diseñar.

## Arranque del backend

```bash
cp .env.example .env
npm install
node ace serve --hmr
```

Necesarios: `APP_KEY`, `DB_*`. Para OTP real: `SMTP_*`, `MAIL_FROM_ADDRESS`, `OTP_EXPIRATION_MINUTES`. Fotos: `CLOUDINARY_*`.

## Deuda que el análisis debe nombrar (con honestidad de senior)

El producto es real y el dominio está bien visto. El código se hizo rápido. Eso se nota: login sin token de API, algo de validación horaria comentada en OTP (el listado de activas sí filtra tiempo), nombres de columna heredados, multi-tenant aún no existe. Ninguna de esas deudas anula el valor. Todas son trabajo de las fases que siguen al FS-DOC. Mentirlas en el formulario sería peor que no haber documentado.

## Equipo (frontend, página Equipo)

**Manejo:** Henry Bastidas (PO), Alexandra Guevara Muñoz (supervisión).

**Construcción:** Jorge Enrique Porras (SM), Fernanda Gonzalez, Alex Jhoan Chaguendo, Dovin Richard Hoyos, Bryan Andrés Hurtado, Mariana Cifuentes Zuñiga, Víctor Manuel Mosquera, Andrés Santiago Arias, Jeison Reyes Ruiz, Camilo Hurtado, Daniela Paredes, David Santiago Rengifo.

## Lo que hay que escribir a mano en el Word

1. Patrocinador (nombre y cargo).
2. Tabla de aprobaciones (firma y fecha).
3. URL de producción, si ya hay.
4. Título P.O.P. si el instructor pide otra redacción.
5. Cliente, si oficialmente no es “SENA / Fábrica de Software”.
