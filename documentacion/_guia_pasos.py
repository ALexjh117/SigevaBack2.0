# -*- coding: utf-8 -*-
"""Guía: una sección por persona, SQL único, trabajo en paralelo."""
from __future__ import annotations

from docx.shared import RGBColor

NAVY = RGBColor(0x1B, 0x3A, 0x4B)
GREEN = RGBColor(0x1F, 0x7A, 0x4D)
MUTED = RGBColor(0x4A, 0x55, 0x63)
SOFT_GREEN = "E8F5EE"
SOFT_RED = "FDECEC"
SOFT_NAVY = "E8EEF2"
SOFT_AMBER = "FEF3C7"
AMBER = RGBColor(0x92, 0x40, 0x0E)
ROJO = RGBColor(0x8B, 0x1E, 0x3F)


def escribir_pasos(doc, shots, H):
    add_p = H["add_p"]
    add_h = H["add_h"]
    add_table = H["add_table"]
    callout = H["callout"]
    photo = H["photo"]
    dicc = H["dicc"]
    cambio = H["cambio"]
    sql_block = H["sql_block"]
    banner = H["banner"]

    add_p(doc, "SIGEVA", size=12, bold=True, color=GREEN, space_after=2)
    add_p(doc, "Guía para trabajar TODOS A LA VEZ  ·  nadie espera a que el otro suba la base", size=11, color=MUTED, space_after=4)
    add_p(doc, "Elección global: tu sección, tu rama, tu listo", size=20, bold=True, color=NAVY, space_after=8)
    add_p(
        doc,
        "Lee primero el bloque TODOS (dónde está el proyecto + el SQL). "
        "Después salta a TU nombre. Cuando termines tu checklist, tu parte está lista. "
        "No tienes que esperar el merge de nadie para codear: cada uno corre el SQL en su PostgreSQL y abre su rama.",
        size=11,
        color=MUTED,
    )

    add_table(
        doc,
        ["Tú", "Tu sección", "Proyecto", "Rama sugerida"],
        [
            ["Alex", "Crear / editar elección sin jornada", "sigevaBack", "feat/eleccion-sin-jornada"],
            ["Maicol", "Jornada en el candidato + GET filtrado", "sigevaBack", "feat/candidatos-jornada"],
            ["Mebel", "Listar y filtrar elecciones", "sigevaBack", "feat/eleccion-listados"],
            ["Paula", "Form y listado de elección", "sigevaFront (React de producción)", "feat/form-eleccion-global"],
            ["Sofia", "Form candidato y tarjetón urna", "sigevaFront (gestión + urna)", "feat/tarjeton-jornada"],
        ],
        col_cm=[2.4, 6.2, 4.2, 4.0],
    )

    add_h(doc, "Cómo se lee una foto de código")
    add_table(
        doc,
        ["En la foto / en el recuadro", "Significa"],
        [
            ["CÓDIGO EXISTENTE — se modifica", "El archivo YA está. No lo crees. Abres y cambias lo que se indica."],
            ["CÓDIGO NUEVO — se agrega", "Esa línea, campo o índice no existía. Lo pegas."],
            ["Barra roja en la foto", "Eso ya está. Lo BORRAS."],
            ["Barra verde en la foto", "Eso lo PEGAS."],
            ["Foto negra con POST/PUT/GET", "Prueba en Thunder. Izquierda = lo que pegas. Derecha = lo que tiene que devolver. Abajo = cuándo marcas LISTO."],
            ["Foto Chrome DevTools · Network", "F12 en el navegador. Izquierda = el payload que salió. Abajo = cuándo marcas LISTO. Paula y Sofia se verifican así."],
            ["Foto de pantalla partida (rojo/verde)", "Izquierda = cómo se ve HOY. Derecha = cómo se ve cuando tu parte cerró."],
        ],
        col_cm=[6.2, 10.6],
    )

    # ========== TODOS ==========
    banner(
        doc,
        "TODOS — hagan esto primero (15 min) y después cada uno a su sección",
        "Carpetas + SQL + rama. Con esto ya no se esperan.",
    )

    add_h(doc, "1. Dónde está el proyecto (es un repo, no un script suelto)", 2)
    add_p(
        doc,
        "Hay DOS proyectos. El backend es AdonisJS y se llama sigevaBack (esta carpeta). "
        "El frontend de producción es sigevaFront (carpeta hermana: mismas pantallas de hoy, /elecciones, /votaciones). "
        "Paula y Sofia trabajan AHÍ, no en el React de contrato sigeva-front/. Si ves app/controllers, estás en el back. "
        "Si ves src/pages/funcionario, estás en el front de Paula/Sofia.",
    )
    add_table(
        doc,
        ["Carpeta (desde la raíz de sigevaBack)", "Qué hay ahí", "Quién entra"],
        [
            ["app/controllers/", "Recibe el HTTP. crearEleccion, store de candidatos.", "Alex, Maicol, Mebel"],
            ["app/models/", "Una clase = una tabla. eleccione.ts, candidatos.ts.", "Alex, Maicol"],
            ["app/services/", "La lógica. candidatos_service, FiltroJorElCen.", "Maicol, Mebel"],
            ["app/validators/", "Reglas del body (Vine). store_candidato_validator.", "Maicol"],
            ["start/routes/", "Las URLs. elecciones.ts, candidato.ts. NO creen rutas nuevas.", "Nadie toca, salvo mirar"],
            ["El otro repo / sigevaFront/", "Pantallas React de producción. Paula y Sofia trabajan AHÍ.", "Paula, Sofia"],
        ],
        col_cm=[5.4, 6.8, 4.6],
    )

    add_h(doc, "2. Git: cada uno en su rama (el back no se pisa)", 2)
    add_p(
        doc,
        "En sigevaBack: git checkout -b la-rama-de-arriba. Trabajan en archivos distintos (mira la tabla de tu sección). "
        "Alex y Mebel comparten eleccion_controller.ts pero NO el mismo método: Alex arriba (crear/actualizar), Mebel abajo (GET). "
        "Si no se meten en el método del otro, el merge sale. En sigevaFront: Paula form/listado de elección, Sofia candidato y urna. "
        "No reescriban App.tsx ni api.ts.",
    )
    callout(
        doc,
        "Por qué no se amarran entre sí",
        "La base vive en cada PC: por eso el SQL lo corre cada uno. El código vive en ramas distintas: por eso no se esperan un merge. "
        "El único momento juntos es el flujo de éxito al final (entrar a Elecciones y ver una convocatoria del centro).",
        fill=SOFT_NAVY,
        title_color=NAVY,
    )
    photo(
        doc,
        shots["carriles"],
        "Foto: cinco carriles. Cada quien baja hasta su LISTO. El de al lado no es un candado.",
    )

    add_h(doc, "3. PostgreSQL — un solo bloque, lo copia TODO el mundo", 2)
    add_p(
        doc,
        "Esto NO recrea la base de 0. NO borra elecciones ni candidatos. Solo suelta el NOT NULL de jornada en elecciones, "
        "agrega la columna jornada en candidatos, y crea un índice único para el tarjetón por jornada. "
        "Ábrelo en pgAdmin / DBeaver / psql, contra la misma base que usa tu .env, y ejecuta el bloque entero.",
    )
    sql_block(
        doc,
        """-- SIGEVA · pegar TODO · cada uno en SU PostgreSQL local
-- No recrea la base. Si una línea dice already exists, ignórala y sigue.

ALTER TABLE elecciones
  ALTER COLUMN jornada DROP NOT NULL;

ALTER TABLE candidatos
  ADD COLUMN IF NOT EXISTS jornada VARCHAR(20);

CREATE UNIQUE INDEX IF NOT EXISTS uq_candidatos_tarjeton_jornada
  ON candidatos (ideleccion, jornada, numero_tarjeton)
  WHERE jornada IS NOT NULL;""",
    )
    photo(doc, shots["sql_todos"], "Así se ve. Abajo está el texto para copiar; no dependas solo de la foto.")
    dicc(
        doc,
        [
            [
                "elecciones … DROP NOT NULL",
                "jornada de la elección puede quedar vacía.",
                "Las elecciones NUEVAS no llevan jornada. Las viejas siguen con el valor que ya tenían.",
                "El create de Alex truena: PostgreSQL exige un valor.",
            ],
            [
                "candidatos … ADD COLUMN jornada",
                "Campo nuevo en una tabla que YA existe.",
                "Ahí se guarda si el candidato es de Mañana, Tarde o Noche.",
                "El POST de Sofia / el create de Maicol no tienen dónde escribir.",
            ],
            [
                "UNIQUE INDEX … jornada",
                "Índice nuevo. No es una tabla nueva.",
                "Un 01 puede existir en mañana Y en tarde. No dos 01 en la misma jornada.",
                "Si solo lo validas en código, alguien puede colar duplicados por SQL.",
            ],
            [
                "WHERE jornada IS NOT NULL",
                "Las filas viejas sin jornada no rompen el índice.",
                "Puedes correr el SQL aunque ya haya candidatos.",
                "Sin el WHERE, filas null podrían pelearse el unique.",
            ],
        ],
    )
    callout(
        doc,
        "Si ADD COLUMN IF NOT EXISTS no te corre",
        "Tu PostgreSQL es viejo. Quita el IF NOT EXISTS y deja ADD COLUMN jornada VARCHAR(20); "
        "Si dice que la columna ya existe, esa línea ya está: sigue con el índice.",
        fill=SOFT_AMBER,
        title_color=AMBER,
    )

    add_h(doc, "4. En una frase, por qué hacemos esto", 2)
    add_p(
        doc,
        "Hoy hay que crear tres elecciones (mañana, tarde, noche). Queremos UNA por centro. "
        "La jornada se marca en cada candidato. El aprendiz ve solo su bloque. El voto sigue siendo uno, "
        "porque sigue habiendo una sola ideleccion. El picker de “elige jornada al entrar” NO va en este paquete.",
    )
    photo(doc, shots["flujo"], "Izquierda = hoy (tres urnas). Derecha = lo que armamos (una elección, tres bloques).")

    # ========== ALEX ==========
    banner(
        doc,
        "ESTA SECCIÓN ES TUYA — ALEX",
        "sigevaBack  ·  rama feat/eleccion-sin-jornada  ·  cuando el checklist esté, TÚ ya terminaste",
    )
    add_p(
        doc,
        "Tu carril es el POST y el PUT de la elección. Mebel usa el mismo archivo, pero la mitad de abajo (los GET). "
        "No es que ella te bloquee ni tú a ella: son dos mitades. Paula está en el otro repo, en el form.",
    )
    photo(
        doc,
        shots["archivo_split"],
        "Foto: eleccion_controller.ts partido. Arriba Alex (crear). Abajo Mebel (listar). Cada uno cierra su LISTO solo.",
    )
    add_table(
        doc,
        ["Archivo (desde sigevaBack)", "¿Nuevo o existente?", "Qué le haces"],
        [
            ["app/controllers/eleccion_controller.ts", "EXISTENTE — se modifica", "Métodos crearEleccion y actualizarEleccion. Quitar jornada."],
            ["app/models/eleccione.ts", "EXISTENTE — se modifica", "jornada pasa a string | null."],
            ["start/routes/elecciones.ts", "EXISTENTE — no se toca", "Las URLs siguen iguales. Solo míralo."],
        ],
        col_cm=[6.2, 5.0, 5.6],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/controllers/eleccion_controller.ts  →  crearEleccion",
        "El archivo existe. El método existe. No crees otro crear. Abre el que ya está (busca crearEleccion). "
        "Hoy lee 'jornada' y si no es Mañana/Tarde/Noche responde 400. ESE if es lo que obliga a tres elecciones. Lo borras. "
        "Dejas centro, fechas y horas: eso sí es de la convocatoria.",
    )
    photo(doc, shots["alex_antes"], "EXISTENTE. Lo rojo se borra. El if entero, no una línea.")
    dicc(
        doc,
        [
            [
                "'jornada' en request.only",
                "Saca jornada del body y la manda a la tabla.",
                "Hoy la elección “es de” una jornada.",
                "Lucid sigue guardándola y el form de Paula no cambia nada.",
            ],
            [
                "if Mañana/Tarde/Noche → 400",
                "Rechaza el POST si no hay jornada.",
                "Era la validación de la urna por franja.",
                "Paula manda el form nuevo y recibe 400. Tres elecciones otra vez.",
            ],
        ],
    )
    photo(doc, shots["alex_despues"], "Así queda el only. Debajo siguen TUS if de centro y fechas: esos no se tocan, ya existían.")
    dicc(
        doc,
        [
            [
                "idcentro_formacion",
                "De qué sede es la urna.",
                "El aislamiento sigue siendo el centro.",
                "Un funcionario podría crear en otra sede.",
            ],
            [
                "fechas y horas",
                "Cuándo abre y cierra.",
                "La ventana es de todo el centro, no de una jornada.",
                "No hay horario oficial.",
            ],
        ],
    )
    add_p(
        doc,
        "El método actualizarEleccion está más abajo en EL MISMO archivo. Es EXISTENTE. Hazle el mismo recorte: "
        "saca 'jornada' del only y borra el if. Si solo arreglas el crear, el PUT vuelve a forzar jornada.",
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/models/eleccione.ts",
        "El modelo ya existe. No crees otro. Cambia el tipo de jornada a string | null para que Lucid acepte el create vacío. "
        "La columna en PostgreSQL ya la soltaste con el SQL de TODOS.",
    )
    photo(doc, shots["alex_modelo"], "EXISTENTE. Solo cambia el tipo. No borres la columna del modelo.")
    dicc(
        doc,
        [
            [
                "string | null",
                "TypeScript admite vacío.",
                "Las elecciones nuevas no tienen jornada.",
                "Lucid puede quejarse al guardar null.",
            ],
        ],
    )
    add_h(doc, "LISTO — pruébalo en Thunder (fotos: JSON exacto)", 2)
    add_p(
        doc,
        "No es un texto suelto. Pegas lo de la izquierda. Si Thunder te devuelve lo de la derecha, tu sección acabó. "
        "Los GET de listado no los tocas: son de Mebel. Paula no entra en este checklist.",
    )
    photo(
        doc,
        shots["http_alex_post"],
        "CREAR. POST /api/eleccion/crear. Copia el JSON tal cual (cambia el idcentro_formacion por el tuyo). Tiene que salir 201, no 400.",
    )
    photo(
        doc,
        shots["http_alex_put"],
        "ACTUALIZAR. PUT /api/eleccionActualizar/12 — el 12 es el ideleccion que te devolvió el POST. Mismos campos, nombre o fechas pueden cambiar. 200.",
    )
    photo(
        doc,
        shots["http_alex_mal"],
        "Si SIN jornada te sigue saliendo 400 “La jornada no es válida”, el if viejo sigue. Eso NO es LISTO.",
    )

    # ========== MAICOL ==========
    banner(
        doc,
        "ESTA SECCIÓN ES TUYA — MAICOL",
        "sigevaBack  ·  rama feat/candidatos-jornada  ·  el SQL ya lo corriste TÚ, no esperas a Alex",
    )
    add_p(
        doc,
        "Tu carril son los archivos de candidatos. Alex no entra ahí. Mebel no entra ahí. "
        "Sofia pinta el select en el front a la vez: ella no necesita tu rama para dejar el JSX; "
        "el POST se prueba en el flujo de éxito, al final, juntos.",
    )
    add_table(
        doc,
        ["Archivo (desde sigevaBack)", "¿Nuevo o existente?", "Qué le haces"],
        [
            ["app/models/candidatos.ts", "EXISTENTE — se modifica", "Agregar el campo jornada (línea nueva en un archivo viejo)."],
            ["app/validators/store_candidato_validator.ts", "EXISTENTE — se modifica", "Agregar jornada al vine.object."],
            ["app/services/candidatos_service.ts", "EXISTENTE — se modifica", "DTO, unique, create, get, update."],
            ["app/controllers/candidatos_controller.ts", "EXISTENTE — se modifica", "store, update y getByEleccion leen jornada."],
            ["start/routes/candidato.ts", "EXISTENTE — no se toca", "La URL listar/:ideleccion se queda. Solo se le agrega query."],
        ],
        col_cm=[6.4, 5.0, 5.4],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/models/candidatos.ts",
        "El modelo YA existe. No crees candidatos2.ts. Abre el archivo y DEBAJO de numero_tarjeton PEGA el @column jornada. "
        "Eso sí es código nuevo: el campo no existía. El archivo no es nuevo.",
    )
    photo(doc, shots["maicol_modelo"], "Archivo existente. Las dos líneas verdes son NUEVAS.")
    dicc(
        doc,
        [
            [
                "@column() declare jornada",
                "Lucid lee/escribe la columna que agregó el SQL.",
                "Sin esto el create ignora jornada aunque la tabla ya la tenga.",
                "La fila nace vacía y el GET filtrado no encuentra a nadie.",
            ],
        ],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/validators/store_candidato_validator.ts",
        "El validator YA existe. Dentro del vine.object que ya está, AGREGAS una clave nueva: jornada. "
        "Las cadenas van CON eñe, iguales a las que usaba la elección.",
    )
    photo(doc, shots["maicol_val"], "Archivo existente. Solo la línea jornada es NUEVA.")
    dicc(
        doc,
        [
            [
                "vine.enum(['Mañana','Tarde','Noche'])",
                "Rechaza “manana”, “MADRUGADA”, vacío.",
                "Back y front hablan el mismo idioma.",
                "Alguien manda “tarde” y el where no pega.",
            ],
        ],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/services/candidatos_service.ts  →  checkDuplicateTarjeton",
        "La función YA existe. Hoy busca (elección + tarjetón). Eso impediría un 01 en mañana y un 01 en tarde. "
        "Le AGREGAS el parámetro jornada y un andWhere. El unique de PostgreSQL (SQL de TODOS) defiende lo mismo en la base.",
    )
    photo(doc, shots["maicol_unique_antes"], "EXISTENTE. Así está hoy. Eso hay que ampliar.")
    photo(doc, shots["maicol_unique"], "La firma gana un parámetro NUEVO. El andWhere jornada es NUEVO.")
    dicc(
        doc,
        [
            [
                "parámetro jornada",
                "El chequeo sabe la franja.",
                "No comparar un 01 de mañana con uno de tarde.",
                "El segundo POST (tarde) explota.",
            ],
            [
                "andWhere('jornada', jornada)",
                "Duplicado solo en esa franja.",
                "El 01 puede existir tres veces, una por bloque.",
                "Único por elección otra vez.",
            ],
        ],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/services/candidatos_service.ts  →  create + getAllCandidatosByIdEleccion",
        "createWithOptionalUpload YA existe: le pasas jornada al Candidatos.create (campo NUEVO en el objeto que ya se insertaba). "
        "getAllCandidatosByIdEleccion YA existe: le agregas un segundo argumento OPCIONAL y un if. "
        "Si viene jornada, recorta (urna). Si no, lista los tres (gestión). RANDOM() se queda: ya existía.",
    )
    photo(doc, shots["maicol_create"], "Objeto del create: jornada es NUEVO. El resto del create ya estaba.")
    dicc(
        doc,
        [
            [
                "jornada: data.jornada",
                "Escribe el campo en la fila.",
                "Es EL dato con el que después filtra la urna.",
                "GET ?jornada=Tarde devuelve [].",
            ],
        ],
    )
    photo(doc, shots["maicol_get"], "La función es EXISTENTE. jornada?: string e if (jornada) son NUEVOS.")
    dicc(
        doc,
        [
            [
                "jornada?: string",
                "Argumento opcional NUEVO.",
                "Gestión no lo manda. Urna sí.",
                "Si es obligatorio, se rompe el listado de gestión.",
            ],
            [
                "if (jornada) andWhere",
                "Recorta solo cuando hay query.",
                "Una función, dos pantallas.",
                "Si siempre filtras, gestión no ve los tres bloques.",
            ],
        ],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/controllers/candidatos_controller.ts",
        "El controller YA existe. store: pasa payload.jornada (NUEVO en el objeto). "
        "update: mete 'jornada' en el only (NUEVO en la lista). "
        "getByEleccion: lee request.qs().jornada (NUEVO) y se lo pasa al service. NO crees otra ruta.",
    )
    photo(doc, shots["maicol_store"], "store EXISTENTE. Solo se agrega jornada: payload.jornada.")
    photo(doc, shots["maicol_ctrl"], "getByEleccion EXISTENTE. Lo nuevo es qs().jornada. Misma URL.")
    dicc(
        doc,
        [
            [
                "request.qs().jornada",
                "Lee ?jornada=Tarde.",
                "Ahí Sofia manda la franja.",
                "El service siempre lista los tres.",
            ],
            [
                "No hay ruta nueva",
                "Sigue /api/candidatos/listar/:ideleccion",
                "El front ya la pega. Solo se le agrega query.",
                "Sofia tendría que cambiar de endpoint.",
            ],
        ],
    )
    add_p(
        doc,
        "En el type CreateCandidatoDTO (arriba del service, EXISTENTE) agrega jornada: string. "
        "En updateCandidatos, si llega jornada, asígnala y vuelve a correr el unique.",
    )
    add_h(doc, "LISTO — pruébalo en Thunder (fotos: JSON / form-data exacto)", 2)
    add_p(
        doc,
        "Haz los tres POST con tarjetón 01 (Mañana, Tarde, Noche) sobre la misma ideleccion. "
        "Después los dos GET. Sofia no entra en este checklist: ella pinta el select después.",
    )
    photo(
        doc,
        shots["http_maicol_post"],
        "CREAR. POST /api/candidatos/crear. Form-data, no JSON. Repite cambiando jornada y idaprendiz. Los tres = 201.",
    )
    photo(
        doc,
        shots["http_maicol_get_all"],
        "LISTAR SIN query. GET /api/candidatos/listar/12 — data trae 3 (las tres jornadas).",
    )
    photo(
        doc,
        shots["http_maicol_get_tarde"],
        "LISTAR CON query. GET /api/candidatos/listar/12?jornada=Tarde — data trae 1. Misma URL, no inventes otra.",
    )

    # ========== MEBEL ==========
    banner(
        doc,
        "ESTA SECCIÓN ES TUYA — MEBEL",
        "sigevaBack  ·  rama feat/eleccion-listados  ·  esto es código, no Word",
    )
    add_p(
        doc,
        "Tu carril: FiltroJorElCen.ts (ese archivo es solo tuyo) y los GET de abajo en eleccion_controller.ts. "
        "Alex está en la mitad de arriba del mismo controller (crear/actualizar). No es un semáforo: es un corte de archivo. "
        "La columna candidatos.jornada ya está en TU PostgreSQL porque corriste el SQL de TODOS.",
    )
    photo(
        doc,
        shots["archivo_split"],
        "La misma foto que vio Alex, leída al revés: tú eres el bloque verde de abajo. FiltroJorElCen ni siquiera está en ese archivo.",
    )
    add_table(
        doc,
        ["Archivo (desde sigevaBack)", "¿Nuevo o existente?", "Qué le haces"],
        [
            ["app/services/FiltroJorElCen.ts", "EXISTENTE — se modifica", "El where deja de ir a grupo y pasa a candidatos.jornada."],
            ["app/controllers/eleccion_controller.ts", "EXISTENTE — se modifica", "Solo los GET de abajo. Quitar jornada del JSON."],
            ["app/services/EleccionesServices.ts", "EXISTENTE — casi no se toca", "NO filtres eleccion.jornada."],
            ["start/swagger.ts", "EXISTENTE — opcional", "Quitar jornada del example de crear, si te alcanza."],
        ],
        col_cm=[6.4, 5.0, 5.4],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/services/FiltroJorElCen.ts",
        "El servicio YA existe. Hoy entra a aprendiz → grupo y filtra la ficha. Eso era “quién estudia de tarde”, no “quién se postula de tarde”. "
        "Dejas centro y fechas (eso ya estaba). CAMBIAS el preload: if jornada, where sobre candidatos.jornada (campo que agregó el SQL).",
    )
    photo(doc, shots["mebel_antes"], "EXISTENTE. Lo rojo se va: el filtro por grupo.")
    dicc(
        doc,
        [
            [
                "preload grupo + where jornada",
                "Filtra la ficha del aprendiz.",
                "El modelo viejo: la jornada vivía en el grupo.",
                "El tarjetón depende del Excel, no de lo que marcó el funcionario.",
            ],
        ],
    )
    photo(doc, shots["mebel_despues"], "El archivo es el mismo. El if + where candidatos.jornada es NUEVO. El preload aprendiz se queda.")
    dicc(
        doc,
        [
            [
                "where candidatos.jornada",
                "Recorta el tarjetón, no la elección.",
                "La urna pide ?jornada=Tarde y ve un bloque.",
                "Si filtras la elección, las nuevas (jornada null) desaparecen.",
            ],
        ],
    )

    cambio(
        doc,
        "SE MODIFICA",
        "app/controllers/eleccion_controller.ts  →  los GET, no el crear",
        "El controller YA existe. Alex modifica crear/actualizar. Tú modificas traerPorCentroFormacion, "
        "traerPorCentroFormacionTodas y traerPorJornada. En el push del JSON QUITAS jornada: eleccion.jornada. "
        "No inventes un GET nuevo. traerPorJornada cambia de significado: filtra candidatos, misma URL.",
    )
    photo(doc, shots["mebel_json"], "EXISTENTE. Este push sin jornada. Igual en Todas. No borres fechas ni centro.")
    dicc(
        doc,
        [
            [
                "Quitar jornada del JSON",
                "El listado ya no etiqueta la convocatoria.",
                "Paula pinta una card, no tres.",
                "El front sigue mostrando “Mañana”.",
            ],
        ],
    )
    photo(doc, shots["mebel_jornada"], "traerPorJornada EXISTENTE. El where en candidato es NUEVO. La URL no se toca.")
    dicc(
        doc,
        [
            [
                "Misma URL /api/eleccionJornada/listar",
                "La urna ya la pega.",
                "Sofia no cambia de endpoint.",
                "Si la renombras, el front viejo se cae.",
            ],
        ],
    )
    add_h(doc, "LISTO — pruébalo en Thunder (fotos: el JSON que tiene que volver)", 2)
    add_p(
        doc,
        "Tú no mandas body. Miras la respuesta. Si el objeto de la elección todavía trae “jornada”, no está LISTO. "
        "Paula puede pintar cuando quiera: no la esperas.",
    )
    photo(
        doc,
        shots["http_mebel_centro"],
        "GET /api/eleccionPorCentro/1 (o traerTodas). Una convocatoria. En el objeto NO aparece jornada. Igual en /api/eleccion/traerTodas/:id.",
    )
    photo(
        doc,
        shots["http_mebel_jornada"],
        "GET /api/eleccionJornada/listar?jornada=Tarde. Misma URL. candidato[] solo Tarde. Mensaje: Elecciones filtradas por jornada.",
    )

    # ========== PAULA ==========
    banner(
        doc,
        "ESTA SECCIÓN ES TUYA — PAULA",
        "sigevaFront  ·  rama feat/form-eleccion-global  ·  cuando Network y la pantalla coincidan, TÚ ya terminaste",
    )
    add_p(
        doc,
        "El React de producción ya existe (carpeta hermana sigevaFront). No copies sigeva-front ni armes rutas nuevas. "
        "Tus pantallas ya están: /elecciones, /nueva-eleccion, el modal de editar. "
        "Sofia no entra aquí. Alex ya dejó el POST/PUT sin jornada: tú solo dejas de mandarla y de pintarla.",
    )
    photo(
        doc,
        shots["paula_pantalla"],
        "Foto de TU pantalla. Izquierda = hoy (combo + tres filas). Derecha = LISTO (sin combo, una fila, sin columna Jornada).",
    )
    add_table(
        doc,
        ["Archivo (desde sigevaFront)", "¿Nuevo o existente?", "Qué le haces"],
        [
            ["src/pages/funcionario/FormEleccion.tsx", "EXISTENTE — se modifica", "Quitar el select y la clave jornada del POST."],
            ["src/components/EleccionEditarModal.tsx", "EXISTENTE — se modifica", "Quitar el select. El PUT SÍ lleva JSON, mismos campos que el crear."],
            ["src/pages/funcionario/EleccionesActivasPage.tsx", "EXISTENTE — se modifica", "Quitar la columna Jornada del DataTable."],
            ["src/components/EleccionDetalleModal.tsx", "EXISTENTE — se modifica", "No pintar <strong>Jornada</strong>."],
            ["src/components/EleccionCard.tsx", "EXISTENTE — si se usa", "No pintar jornada. El listado actual usa tabla, no esta card."],
        ],
        col_cm=[7.0, 4.6, 5.2],
    )
    callout(
        doc,
        "No toques",
        "Candidatos, urna, Login, App.tsx, api.ts, CargarAprendices, reportes/PDF. "
        "No armes combo de sedes: idcentro_formacion sale de user.centroFormacion.",
        fill=SOFT_RED,
        title_color=ROJO,
    )

    add_h(doc, "1. Crear — quitar jornada del form y del POST", 2)
    cambio(
        doc,
        "SE MODIFICA",
        "src/pages/funcionario/FormEleccion.tsx",
        "El archivo YA existe. Hoy tiene useState de jornada, un <Form.Select> “Selecciona la jornada” y el POST manda jornada. "
        "Borras el state, el combo entero y la clave del JSON. Dejas nombre, fechas, horas y el centro de la sesión. "
        "El formato de hora que ya usas (${fecha} ${hora}:00) se queda.",
    )
    photo(doc, shots["paula_antes"], "EXISTENTE. Lo rojo se borra: el combo y jornada en el POST.")
    dicc(
        doc,
        [
            [
                "useState jornada + Select",
                "Pide al funcionario una franja.",
                "Hoy cada urna “es de” una jornada.",
                "Siguen naciendo tres elecciones.",
            ],
            [
                "jornada en el POST",
                "Manda esa franja al back.",
                "Alex ya no la quiere en elecciones.",
                "Si el if viejo sigue, 400. Si no, guarda basura en la columna.",
            ],
        ],
    )
    photo(doc, shots["paula_despues"], "Así queda el POST. Sin jornada. El centro NO se elige: sale del login.")
    add_h(doc, "Cómo verificar el crear (F12, no a ojo)", 3)
    add_p(
        doc,
        "npm run dev. Login funcionario. Menú Elecciones → Crear Elección. Completa nombre, fechas y horas. "
        "NO debe aparecer el combo de jornada. Guardar. Abre F12 → Network → la petición POST /api/eleccion/crear.",
    )
    photo(
        doc,
        shots["net_paula_post"],
        "LISTO del crear: Payload = este JSON (cambia el centro por el de TU sesión) y status 201. Si ves jornada en el payload, foto de abajo.",
    )
    photo(
        doc,
        shots["http_alex_post"],
        "La respuesta tiene que ser esta (Thunder o la pestaña Response de Network). jornada: null. Message: Eleccion creada con exito.",
    )
    photo(
        doc,
        shots["net_paula_mal"],
        "Si el payload todavía lleva jornada, el form no está LISTO aunque el back responda 201.",
    )
    photo(
        doc,
        shots["http_alex_mal"],
        "Si SIN jornada te sale 400 “La jornada no es válida”, el back de Alex aún no está. Tu form igual NO manda jornada.",
    )

    add_h(doc, "2. Editar — el PUT sí lleva JSON, sin jornada", 2)
    cambio(
        doc,
        "SE MODIFICA",
        "src/components/EleccionEditarModal.tsx",
        "El modal YA existe (lápiz en el listado). Hoy manda jornada y muestra el combo. "
        "Quítaselo. El PUT no va vacío: lleva los MISMOS campos que el crear (centro de la sesión, nombre, fechas, horas). "
        "Puedes cambiar nombre o fechas. El :id es eleccion.ideleccion.",
    )
    photo(doc, shots["paula_edit_antes"], "EXISTENTE. Borra jornada del payload y el <Form.Select>.")
    photo(doc, shots["paula_edit_despues"], "El PUT con JSON completo. Status 200, no 201.")
    photo(
        doc,
        shots["net_paula_put"],
        "F12 al guardar el lápiz. URL /api/eleccionActualizar/12. 200 + “Eleccion actualizada con exito”.",
    )
    photo(
        doc,
        shots["http_alex_put"],
        "Misma foto que usa Alex. El 12 es el ideleccion del crear. Cambia el centro por el de la sesión.",
    )

    add_h(doc, "3. Listado — una fila, sin pintar jornada", 2)
    cambio(
        doc,
        "SE MODIFICA",
        "src/pages/funcionario/EleccionesActivasPage.tsx  +  EleccionDetalleModal.tsx",
        "El GET que ya tienes (/api/eleccion/traerTodas/:id o /api/eleccionPorCentro/:id) se queda. "
        "La lista viene en eleccionesActivas[]. Cada item usa titulo (no nombre). "
        "Borras la columna Jornada del DataTable. En el modal de detalle borras el <p> de Jornada. "
        "Si el JSON todavía trae jornada, Mebel no recortó el GET: tú igual no la muestres.",
    )
    photo(doc, shots["paula_tabla_antes"], "EXISTENTE. Esta columna se va.")
    photo(doc, shots["paula_tabla_despues"], "El GET no cambia. Lo que cambia es lo que pintas.")
    photo(doc, shots["paula_detalle"], "EleccionDetalleModal: borra el renglón Jornada.")
    photo(
        doc,
        shots["http_mebel_centro"],
        "Así vuelve el GET. Una convocatoria. Si aún trae jornada, no la pintes. Una fila en tu tabla = LISTO del listado.",
    )

    add_h(doc, "LISTO Paula — checklist", 2)
    add_table(
        doc,
        ["Qué miras", "Bien", "Mal"],
        [
            ["Form crear / editar", "No hay select Mañana/Tarde/Noche.", "Sigue el combo “Selecciona la jornada”."],
            ["Network POST /api/eleccion/crear", "JSON de la foto, sin clave jornada, 201.", "El payload lleva jornada, o 400 “La jornada no es válida” y tú la mandaste."],
            ["Network PUT /api/eleccionActualizar/:id", "Mismo JSON, 200, el nombre/fecha cambió.", "PUT vacío, o todavía manda jornada."],
            ["Listado /elecciones", "Una fila por convocatoria. Sin columna Jornada.", "Tres filas Mañana/Tarde/Noche, o “Sin jornada” en una columna."],
            ["Detalle / card", "Título + fechas. No dice Jornada.", "Sigue <strong>Jornada:</strong>."],
        ],
        col_cm=[4.4, 6.2, 6.2],
    )
    callout(
        doc,
        "Cuando eso cierra, tu carril acabó",
        "No esperes a Sofia ni a Mebel. No toques candidatos ni urna. El flujo de éxito se prueba al final, juntos.",
        fill=SOFT_GREEN,
        title_color=GREEN,
    )

    # ========== SOFIA ==========
    banner(
        doc,
        "ESTA SECCIÓN ES TUYA — SOFIA",
        "sigevaFront  ·  rama feat/tarjeton-jornada  ·  form + tres bloques + urna filtrada",
    )
    add_p(
        doc,
        "Trabajas en el React de producción (sigevaFront). No toques el form de crear/editar elección (eso es Paula). "
        "Tus rutas ya existen: /gestion-candidatos/:idEleccion, /votaciones, /seleccion/:id. "
        "La jornada se marca en el CANDIDATO. El aprendiz no elige jornada: la trae el login (grupo).",
    )
    photo(
        doc,
        shots["sofia_pantalla"],
        "Tres fotos en una. 1) Select en el form. 2) Gestión en tres bloques. 3) Urna con UNA elección y solo la franja del login.",
    )
    add_table(
        doc,
        ["Archivo (desde sigevaFront)", "¿Nuevo o existente?", "Qué le haces"],
        [
            ["src/components/candidatos/AgregarCandidatoModal.tsx", "EXISTENTE — se modifica", "Select required Mañana/Tarde/Noche + formData.append('jornada')."],
            ["src/components/candidatos/ModificarCandidatoModal.tsx", "EXISTENTE — se modifica", "Lo mismo en el PUT. No dejes el editar sin jornada."],
            ["src/pages/funcionario/GestionCandidatos.tsx", "EXISTENTE — se modifica", "GET /api/candidatos/listar/:ideleccion SIN query. Agrupar en tres bloques."],
            ["src/pages/aprendiz/VotacionesActivasPage.tsx", "EXISTENTE — se modifica", "QUITAR el filter por jornada de las elecciones."],
            ["src/components/aprendiz/VotacionCard.tsx", "EXISTENTE — se modifica", "No pintar jornada en la card de la convocatoria."],
            ["src/pages/aprendiz/SeleccionarCandidatoPage.tsx", "EXISTENTE — se modifica", "GET listar/:id?jornada=user.jornada. Sin modal de “elige jornada”."],
        ],
        col_cm=[7.4, 4.4, 5.0],
    )
    callout(
        doc,
        "No toques",
        "FormEleccion, EleccionEditarModal, Login (no armes picker), OTP, voto, import Excel, App.tsx. "
        "No renombres /api/candidatos/crear ni /api/candidatos/listar/:ideleccion.",
        fill=SOFT_RED,
        title_color=ROJO,
    )

    add_h(doc, "1. Form candidato — select + Form Data", 2)
    cambio(
        doc,
        "SE MODIFICA",
        "src/components/candidatos/AgregarCandidatoModal.tsx",
        "El modal YA existe (Agregar Candidato). Hoy el FormData manda nombres, ideleccion, idaprendiz, propuesta, numero_tarjeton, foto. "
        "AGREGAS jornada al state, un <Form.Select required> con exactamente Mañana, Tarde, Noche (con ñ), y data.append('jornada', formData.jornada). "
        "El POST sigue siendo multipart/form-data, no JSON puro. Igual en ModificarCandidatoModal.",
    )
    photo(doc, shots["sofia_form"], "PEGA el select y el append. Las tres cadenas van CON eñe, iguales al back.")
    dicc(
        doc,
        [
            [
                "select required",
                "El funcionario elige la franja del tarjetón.",
                "Ahí vive ahora la jornada, no en la elección.",
                "El POST sale sin jornada y Maicol no puede filtrar.",
            ],
            [
                "formData.append jornada",
                "La mete al multipart.",
                "Network tiene que mostrar esa línea.",
                "Si solo está en el JSX y no en el append, el back no la recibe.",
            ],
        ],
    )
    add_h(doc, "Cómo verificar el POST (F12 → Form Data)", 3)
    add_p(
        doc,
        "En ESA elección (la que creó Paula) inscribe tres aprendices distintos. Tarjetón 01 las tres veces. "
        "Uno Mañana, uno Tarde, uno Noche. F12 → Network → POST /api/candidatos/crear → Payload → Form Data.",
    )
    photo(
        doc,
        shots["net_sofia_post"],
        "LISTO del form: Form Data muestra jornada=Tarde (o Mañana/Noche) y 201. Repite tres veces, mismo 01.",
    )
    photo(
        doc,
        shots["http_maicol_post"],
        "Misma foto que Maicol. Si el segundo 01 falla, es el unique del back, no tu form.",
    )

    add_h(doc, "2. Gestión — GET sin query, tres bloques", 2)
    cambio(
        doc,
        "SE MODIFICA",
        "src/pages/funcionario/GestionCandidatos.tsx",
        "Hoy pides /api/candidatos/listar/cformacion/:centro y filtras en el cliente. "
        "Cámbialo a GET /api/candidatos/listar/:ideleccion SIN ?jornada=. data[] trae los tres. "
        "Agrupas en tres bloques (un <h5> Mañana / Tarde / Noche) y pintas los candidatos de cada uno. "
        "No inventes otra URL.",
    )
    photo(doc, shots["sofia_get_antes"], "EXISTENTE. Esta URL de cformacion se deja de usar en esta pantalla.")
    photo(doc, shots["sofia_get_despues"], "Misma ruta que la urna, pero SIN query. Tú agrupas.")
    photo(
        doc,
        shots["http_maicol_get_all"],
        "Thunder/Network del GET sin query: data.length = 3 (las tres franjas). En pantalla: tres bloques, no una tabla mezclada.",
    )

    add_h(doc, "3. Urna — UNA elección, recorte en candidatos", 2)
    add_p(
        doc,
        "Esto es lo que cierra el flujo del backend. Si no lo haces, el aprendiz de tarde no ve la convocatoria nueva "
        "(porque jornada de la elección ya viene null) o ve las tres franjas juntas.",
    )
    photo(
        doc,
        shots["urna_bug"],
        "Foto del bug. Izquierda = el filter de VotacionesActivasPage. Derecha = lo que tiene que quedar.",
    )
    cambio(
        doc,
        "SE MODIFICA",
        "src/pages/aprendiz/VotacionesActivasPage.tsx",
        "Hoy: votaciones.filter(val => val.jornada == user.jornada). Eso recortaba ELECCIONES. "
        "Con una elección global (jornada null) el filter tira la card y la urna queda vacía. "
        "QUITAS el filter. Pintas eleccionesActivas tal cual: una card por convocatoria del centro.",
    )
    photo(doc, shots["sofia_votaciones_antes"], "EXISTENTE. El filter se BORRA.")
    photo(doc, shots["sofia_votaciones_despues"], "Una card. El recorte no va aquí.")
    cambio(
        doc,
        "SE MODIFICA",
        "src/components/aprendiz/VotacionCard.tsx",
        "Quita el renglón “Jornada: …”. La convocatoria ya no es de una franja. El botón Participar sigue yendo a /seleccion/:ideleccion.",
    )
    photo(doc, shots["sofia_card"], "BORRA el texto Jornada. Título + centro + Participar.")
    cambio(
        doc,
        "SE MODIFICA",
        "src/pages/aprendiz/SeleccionarCandidatoPage.tsx",
        "Hoy: GET /api/candidatos/listar/${id} sin query → salen los tres bloques. "
        "AGREGAS params: { jornada: user.jornada } usando useAuth(). "
        "La jornada NO se pregunta: sale de data.jornada del login (ya viene del grupo). "
        "Si viene null, NO armes modal “elige tu jornada”. Eso es otro paquete: dejas el GET sin query.",
    )
    photo(doc, shots["sofia_urna"], "PEGA params jornada. F12 tiene que mostrar ?jornada=Tarde.")
    photo(
        doc,
        shots["http_login_aprendiz"],
        "El login YA devuelve data.jornada. No lo pidas otra vez. user.jornada en el context es ese campo.",
    )
    photo(
        doc,
        shots["net_sofia_urna"],
        "LISTO de la urna: Request URL lleva ?jornada=Tarde y en pantalla solo ese bloque.",
    )
    photo(
        doc,
        shots["http_maicol_get_tarde"],
        "La respuesta: data.length = 1. Ana (Mañana) y María (Noche) no salen.",
    )
    photo(
        doc,
        shots["net_sofia_mal"],
        "Si /seleccion llama listar/:id SIN query, el aprendiz ve las tres franjas. Eso NO es LISTO (en gestión sí va sin query).",
    )

    add_h(doc, "LISTO Sofia — checklist", 2)
    add_table(
        doc,
        ["Qué miras", "Bien", "Mal"],
        [
            ["Form agregar/editar candidato", "Select required Mañana | Tarde | Noche (con ñ).", "No hay select, o dice manana / MADRUGADA."],
            ["Network POST /api/candidatos/crear", "Form Data tiene jornada. 201 las tres veces (01 × 3).", "JSON puro, o Form Data sin jornada, o el 2º 01 falla y no es unique."],
            ["Gestión /gestion-candidatos/:id", "GET listar/:id SIN query. Tres bloques visibles.", "Sigue listar/cformacion. Una sola tabla mezclada."],
            ["/votaciones", "UNA card de la elección del centro. Sin texto Jornada.", "Cero cards (el filter viejo) o tres cards Mañana/Tarde/Noche."],
            ["/seleccion/:id Network", "GET …/listar/12?jornada=Tarde. Solo esa franja.", "GET sin query y salen las tres. O modal “elige tu jornada”."],
        ],
        col_cm=[4.6, 6.2, 6.0],
    )
    callout(
        doc,
        "Cuando eso cierra, tu carril acabó",
        "No toques el form de elección. No armes picker en el login. El flujo de éxito (los cinco) se prueba al final.",
        fill=SOFT_GREEN,
        title_color=GREEN,
    )

    banner(
        doc,
        "FLUJO DE ÉXITO — probar lo de todos, de punta a punta",
        "Cuando cada uno marcó LISTO. Entran a Elecciones. Crean UNA para todo el centro. Si el recorrido cierra, el paquete sirvió.",
    )
    add_p(
        doc,
        "Esto no es el checklist de una persona. Es el producto: el funcionario arma una convocatoria del centro "
        "y el aprendiz de tarde ve esa urna, no tres. No votan. No generan acta. Si este recorrido pasa, hay éxito.",
    )
    photo(
        doc,
        shots["exito"],
        "Foto del recorrido. Paso 6 verde = éxito. Si se rompe en el 2, es Alex/Paula. Si en el 3, Mebel. Si en el 4, Maicol/Sofia. Si en el 5–6, Sofia/Mebel.",
    )
    add_h(doc, "Recorrido en pantalla (háganlo juntos, 15 min)", 2)
    add_table(
        doc,
        ["Paso", "Quién se sienta", "Qué hacen", "Éxito se ve así"],
        [
            [
                "1. Entrar",
                "Paula",
                "Login funcionario. Menú Elecciones.",
                "Abre el módulo. No pide jornada para listar.",
            ],
            [
                "2. Crear para el centro",
                "Paula (Alex mira el POST)",
                "Nueva elección: nombre, fechas, horas. Centro el de la sesión. SIN campo jornada. Guardar.",
                "201. Quedó UNA convocatoria de ese centro, no tres.",
            ],
            [
                "3. Ver el listado",
                "Paula + Mebel",
                "Vuelven al listado del centro.",
                "Una sola card. No hay columnas Mañana / Tarde / Noche. No dice jornada en el título.",
            ],
            [
                "4. Cargar el tarjetón",
                "Sofia (Maicol mira el POST)",
                "En ESA elección inscriben tres aprendices. Tarjetón 01. Uno Mañana, uno Tarde, uno Noche.",
                "Los tres quedan. Gestión muestra tres bloques dentro de la misma elección.",
            ],
            [
                "5. Entrar a la urna",
                "Sofia",
                "Login de un aprendiz cuya jornada de login es Tarde (la que ya trae el grupo).",
                "Ve ESA elección (la del centro), no tres elecciones.",
            ],
            [
                "6. Éxito",
                "Los cinco miran",
                "Abren el tarjetón. F12: GET …/listar/:id?jornada=Tarde.",
                "Solo candidatos de Tarde. El de Mañana y el de Noche no salen. Ahí el paquete cumplió.",
            ],
        ],
        col_cm=[2.8, 3.4, 5.6, 5.0],
    )
    callout(
        doc,
        "Si algo falla, no se culpan en círculo",
        "Falla al guardar la elección → Alex/Paula. Sale tres veces en el listado o con etiqueta jornada → Mebel/Paula. "
        "No deja inscribir el segundo 01 → Maicol (unique). La urna muestra los tres bloques → Sofia no mandó ?jornada= o Mebel no filtró candidatos.",
        fill=SOFT_AMBER,
        title_color=AMBER,
    )

    add_h(doc, "¿Esto ya cubre todo?")
    add_p(
        doc,
        "Cubre la elección global y el tarjetón por jornada. "
        "NO cubre que el aprendiz ELIJA y GUARDE jornada la primera vez que entra. Eso es el último paquete.",
    )
    add_table(
        doc,
        ["Qué", "¿Cubre?", "Nota"],
        [
            ["Crear/editar/listar una elección por centro, sin jornada", "SÍ", "Alex, Paula, Mebel"],
            ["Candidatos de las tres jornadas en ESA elección", "SÍ", "Maicol, Sofia"],
            ["Urna con tarjetón recortado", "SÍ, con puente", "Usa jornada del login/grupo. Si viene null, no hay picker."],
            ["Un voto (no tres)", "SÍ, sin tocar voto", "Una ideleccion. Nadie abre votoxcandidato."],
            ["OTP", "SÍ, sin tocar", "Sigue atado a la elección."],
            ["Aprendiz elige jornada al entrar y se guarda", "NO", "Último paquete. Nadie lo arma ahora."],
            ["Acta / ganador por jornada", "NO", "Siguiente tanda. El PDF de hoy mezclaría franjas."],
        ],
        col_cm=[7.4, 2.8, 6.6],
    )
    callout(
        doc,
        "No se abre (ya cubierto o después)",
        "votoxcandidato, validarVoto, validacionVotoController, generacion_reporte_controller, "
        "ImportController, aprendizs_controller.login (sin picker), organizacion.ts, centros.",
        fill=SOFT_RED,
        title_color=ROJO,
    )
    add_p(
        doc,
        "Equipo SIGEVA · uso interno · 25 de agosto de 2026. Cada quien: SQL → su sección → checklist LISTO.",
        size=9,
        color=MUTED,
        italic=True,
        space_after=0,
    )
