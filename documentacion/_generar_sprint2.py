# -*- coding: utf-8 -*-
"""Sprint 2 SIGEVA — 31 ago al 4 sep 2026. Excel de planificación y criterios."""
from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table, TableStyleInfo

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "entregables" / "sprint-2" / "SIGEVA-Sprint-2-31-ago-4-sep-2026.xlsx"

NAVY = "1B3A4B"
NAVY2 = "0F2A36"
GREEN = "1F7A4D"
SENA = "92D050"
GOLD = "9A6B2F"
RED = "8B1E3F"
WHITE = "FFFFFF"
MUTED = "667085"
LINE = "D0D5DD"
GRAY = "F2F4F7"
OK_BG = "E8F5EE"
OK_TX = "166534"
RUN_BG = "FEF3C7"
RUN_TX = "92400E"
TODO_BG = "E8EEF2"
TODO_TX = "1B3A4B"
NO_BG = "FEE2E2"
NO_TX = "991B1B"
LIGHT_GOLD = "F8F1E3"
LIGHT_SENA = "EAF7D8"

THIN = Border(
    left=Side(style="thin", color=LINE),
    right=Side(style="thin", color=LINE),
    top=Side(style="thin", color=LINE),
    bottom=Side(style="thin", color=LINE),
)
NONE = Border()


def fill(h):
    return PatternFill("solid", fgColor=h)


def font(size=10, bold=False, color=NAVY, italic=False):
    return Font(name="Arial", size=size, bold=bold, color=color, italic=italic)


def al(wrap=True, v="center", h="left"):
    return Alignment(wrap_text=wrap, vertical=v, horizontal=h)


def paint(cell, value=None, bg=None, fnt=None, align=None, border=THIN):
    if value is not None:
        cell.value = value
    if bg:
        cell.fill = fill(bg)
    cell.font = fnt or font()
    cell.alignment = align or al()
    cell.border = border
    return cell


def merge(ws, r1, c1, r2, c2):
    ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)


def widths(ws, xs):
    for i, x in enumerate(xs, 1):
        ws.column_dimensions[get_column_letter(i)].width = x


def page(ws, landscape=True, footer="Sprint 2  ·  31 ago – 4 sep 2026  ·  uso interno"):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.page_margins = PageMargins(left=0.45, right=0.45, top=0.55, bottom=0.45, header=0.22, footer=0.22)
    ws.sheet_view.showGridLines = False
    ws.oddHeader.left.text = "SIGEVA  ·  Sprint 2"
    ws.oddHeader.right.text = "&A"
    ws.oddFooter.left.text = footer
    ws.oddFooter.right.text = "Pág. &P de &N"


def banner(ws, cols, title, subtitle, height=32):
    for c in range(1, cols + 1):
        paint(ws.cell(1, c), "", NAVY, font(14, True, WHITE), al(False, "center", "center"), NONE)
    merge(ws, 1, 1, 1, cols)
    paint(ws.cell(1, 1), title, NAVY, font(16, True, WHITE), al(False, "center", "left"), NONE)
    ws.row_dimensions[1].height = height
    for c in range(1, cols + 1):
        paint(ws.cell(2, c), "", NAVY2, font(10, False, WHITE), al(True, "center", "center"), NONE)
    merge(ws, 2, 1, 2, cols)
    paint(ws.cell(2, 1), subtitle, NAVY2, font(10, False, WHITE), al(True, "center", "left"), NONE)
    ws.row_dimensions[2].height = 22


def header_row(ws, row, headers, bg=GREEN, fg=WHITE):
    for i, h in enumerate(headers, 1):
        paint(ws.cell(row, i), h, bg, font(10, True, fg), al(False, "center", "center"))
    ws.row_dimensions[row].height = 22


def add_table(ws, name, ref):
    tab = Table(displayName=name, ref=ref)
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False)
    ws.add_table(tab)


# ---------------------------------------------------------------------------
# Datos del sprint
# ---------------------------------------------------------------------------

SPRINT = {
    "nombre": "Sprint 2",
    "fechas": "lunes 31 de agosto al viernes 4 de septiembre de 2026",
    "kickoff": "lunes 31 ago 2026",
    "review": "viernes 4 sep 2026",
    "meta": (
        "Cerrar lo que ya se construyó y dejar documentado lo que faltaba: landing (Sofia), "
        "recuperar contraseña (Alex back + Maicol front), import Excel Sofia Plus sin jornada (Alex), "
        "prototipos de informe por jornada (Mebel) y de urna móvil (Paula), "
        "ojo y mensaje de credenciales en login (Maicol), criterios de una elección por día (Adrii), "
        "y Lucero escribe las HU que no estaban en el Excel de historias."
    ),
}

HISTORIAS = [
    {
        "id": "HU-S2-026",
        "rf": "RF-NU-026",
        "cu": "CU-26",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Sofia",
        "capa": "Front landing",
        "rama": "sigevaFront · feat/landing",
        "titulo": "Landing page SIGEVA (producción)",
        "historia": (
            "Como visitante del SENA, quiero una landing clara y de confianza "
            "para entrar a votar o a gestionar, para no aterrizar en una pantalla que parece un contrato interno."
        ),
        "problema": "La home pública tiene que verse institucional: dos puertas (urna y gestión), identidad SENA, bien en escritorio y en celular.",
        "valor": "SIGEVA se puede mostrar. Es la puerta de todo el mundo que no está logueado.",
        "in_scope": [
            "Página Inicio de sigevaFront (ruta /). Desktop 1440 y móvil 375",
            "Dos CTA: Aprendiz (urna /login-aprendiz) y Gestión (/login)",
            "Paleta SENA (verde #39A900 / #92D050, navy). CTA visibles. Sin voto en la landing",
            "Enlace a Equipo si ya está (Paula lo prototipó). Sofia no reescribe Equipo.tsx",
        ],
        "out_scope": [
            "Urna, OTP, acta, form de elección, import Excel, recuperar contraseña",
            "Copiar el HomePage de sigeva-front/ (contrato de agente, no la web pública)",
            "Prototipos de urna móvil (eso es Paula HU-S2-033)",
        ],
        "listo": (
            "Network: / abre la landing. Los dos botones llegan a /login-aprendiz y /login. "
            "Se ve bien a 1440 y 375. No pide jornada ni documento en esa pantalla."
        ),
        "archivos": "sigevaFront/src/pages/Inicio.tsx · Inicio.css · App.tsx ruta /. No toca RecuperarContrasena ni urna.",
    },
    {
        "id": "HU-S2-027",
        "rf": "RF-NU-027",
        "cu": "CU-27",
        "sp": 2,
        "prio": "Debe tener",
        "persona": "Maicol",
        "capa": "Back",
        "rama": "sigevaBack · feat/elecciones-orden-reciente",
        "titulo": "Elecciones: la más reciente aparece primero",
        "historia": (
            "Como funcionario o admin de un centro, quiero ver primero la elección más reciente "
            "para no buscarla al final de la lista."
        ),
        "problema": "Hoy los GET de elección no ordenan: Eleccione.all() y los query por centro salen en orden de inserción (la vieja arriba).",
        "valor": "La mesa opera sobre la convocatoria actual, no sobre la del mes pasado.",
        "in_scope": [
            "Orden estable: fecha_inicio DESC, desempate ideleccion DESC",
            "Aplicarlo en TODOS los listados: traerEleccion, traerEleccionesActivas, traerPorCentroFormacion, traerPorCentroFormacionTodas, listarPorCentro, traerPorJornada, traerFiltrado",
            "El front pinta el array en el orden del JSON: no reordenar al revés",
        ],
        "out_scope": [
            "Filtros nuevos de búsqueda (texto, estado). Este HU es solo ORDEN",
            "Cambiar la regla de una elección global / jornada en candidato",
            "Acta, OTP, candidatos",
        ],
        "listo": (
            "Thunder: tres elecciones del mismo centro con fecha_inicio 20, 25 y 27 ago. "
            "El GET devuelve [27, 25, 20]. La primera fila del JSON es la del 27."
        ),
        "archivos": "app/controllers/eleccion_controller.ts · app/services/EleccionesServices.ts · app/services/FiltroJorElCen.ts",
    },
    {
        "id": "HU-S2-028",
        "rf": "RF-NU-028",
        "cu": "CU-28",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Sofia",
        "capa": "Front + Back padrón",
        "rama": "sigevaFront · feat/filtros-aprendices  +  sigevaBack · mismo nombre si toca el GET",
        "titulo": "Filtros de búsqueda en aprendices (centro, teléfono y los que faltan)",
        "historia": (
            "Como gestor de un centro, quiero filtrar el padrón por centro de formación, teléfono "
            "y el resto de campos útiles, para encontrar a alguien sin recorrerme toda la tabla."
        ),
        "problema": (
            "GET /api/aprendiz/listar no filtra. GET /api/aprendiz/centros/:idCentro busca nombres, "
            "apellidos, email y documento, pero NO celular. En pantalla faltan centro y teléfono."
        ),
        "valor": "El censo se puede operar. Encaja con admin_sistema (Alex) viendo solo su centro.",
        "in_scope": [
            "Filtro por centro de formación (combo; admin_sistema lo trae fijo de sesión y no elige otra sede)",
            "Filtro por teléfono = campo celular (contiene, dígitos)",
            "Completar los que faltan: documento, correo, nombres/apellidos, estado",
            "Query params combinables. Lista vacía = []. Nunca 404 por 'no hubo match'",
            "La respuesta NUNCA incluye password ni hash",
        ],
        "out_scope": [
            "Alta puntual / import Excel (HU-012 / HU-023 / HU-024)",
            "Que un admin_sistema o funcionario liste otra sede",
            "Editar aprendiz en masa",
        ],
        "listo": (
            "Network: GET con ?celular=300 y ?idcentro_formacion=X devuelve solo esos. "
            "Sin celular en el padrón, 0 filas. JSON sin password. UI: barra de filtros + vacío claro."
        ),
        "archivos": "app/controllers/aprendizs_controller.ts · start/routes/aprendiz.ts · pantalla Aprendices del front de producción",
    },
    {
        "id": "HU-S2-029",
        "rf": "RF-NU-029",
        "cu": "CU-29",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Adrii Eraso",
        "capa": "Back + criterio de producto",
        "rama": "sigevaBack · feat/eleccion-un-dia",
        "titulo": "Criterio de aceptación: una elección por centro el mismo día",
        "historia": (
            "Como funcionario, quiero que el sistema rechace una segunda elección el mismo día en mi centro "
            "para no duplicar la convocatoria (si ya hay una del 27 de agosto, no se crea otra ese día)."
        ),
        "problema": "crearEleccion no mira si ya existe una convocatoria con la misma fecha_inicio en ese centro.",
        "valor": "Cierra la regla de producto: una elección por centro Y no dos el mismo día.",
        "in_scope": [
            "Regla RN-S2-001: mismo idcentro_formacion + mismo día calendario de fecha_inicio (America/Bogota) = rechazo",
            "Vale para POST /api/eleccion/crear y para PUT /api/eleccionActualizar/:id si se mueve a un día ocupado",
            "Editar la MISMA elección (nombre, horas, fecha_fin) el mismo día SÍ se permite",
            "Otro centro, el mismo 27 de agosto, SÍ se permite",
            "Mensaje en español, HTTP 409. Mebel lo pinta en SweetAlert (HU-S2-031); el back no devuelve 500",
            "Criterios Gherkin de esta hoja son el contrato de Adrii: no se inventa otra regla",
        ],
        "out_scope": [
            "Prohibir ventanas que se solapan en días distintos (27-29 vs 28-30). No se pidió; no se implementa",
            "Unicidad por created_at (el día en que alguien pulsó Guardar). La regla es la fecha de la elección",
            "OTP, voto, acta, candidatos, jornada",
        ],
        "listo": (
            "Thunder: 1) POST 27 ago centro 1 = 201. 2) POST otra 27 ago centro 1 = 409 con el mensaje. "
            "3) POST 27 ago centro 2 = 201. 4) PUT de la primera cambiando nombre = 200. "
            "5) PUT de otra elección moviéndola al 27 = 409."
        ),
        "archivos": "app/controllers/eleccion_controller.ts (crear + actualizar) · validator si lo agrega. No toca candidatos ni FiltroJorElCen (eso es Maicol).",
    },
    {
        "id": "HU-S2-030",
        "rf": "RF-NU-030",
        "cu": "CU-30",
        "sp": 8,
        "prio": "Debe tener",
        "persona": "Alex",
        "capa": "Back + Front menú",
        "rama": "sigevaBack · feat/rol-admin-sistema  ·  sigevaFront menú",
        "titulo": "Rol admin_sistema: administra solo su centro de formación",
        "historia": (
            "Como admin_sistema, quiero entrar a gestión y ver/administrar únicamente las elecciones, "
            "aprendices y datos de MI centro de formación, para operar mi sede sin ver la red SENA ni otra mesa."
        ),
        "problema": (
            "Hoy hay Aprendiz, Funcionario (mesa) y Administrador (toda la red). Falta el administrador de UN centro: "
            "quien ve el padrón y las elecciones de su sede y no el tablero nacional."
        ),
        "valor": "Escala real del SENA: cada centro tiene un admin propio. El Administrador de red sigue viendo todo.",
        "in_scope": [
            "Nueva fila perfil.perfil = 'admin_sistema'. Usuario con idcentro_formacion OBLIGATORIO",
            "Login de gestión (misma puerta HU-010) devuelve perfil admin_sistema + centro",
            "Menú de gestión de centro: elecciones, aprendices, (lo que ya opera la mesa). SIN tablero de red",
            "Aislamiento: todo GET/POST de elecciones y aprendices usa el centro de la sesión, nunca el id del body/query si viene otro",
            "403/oculto: HU-020 tablero red, HU-024 import eligiendo centro, listar funcionarios de toda la red",
            "Contraste escrito: Funcionario = opera la mesa; admin_sistema = administra la sede; Administrador = red",
        ],
        "out_scope": [
            "JWT / SSO. El login as-is sigue sin token de API",
            "Tabla organizacion / multi-tenant de plataforma (análisis Sprint 1, no este código)",
            "Que admin_sistema vote",
            "Alta masiva de admin_sistema por Excel",
            "Que el Administrador de red 'se haga' admin_sistema de una sede como impersonación",
        ],
        "listo": (
            "Usuario admin_sistema del centro A: ve elecciones y aprendices de A. GET de centro B = vacío o 403, nunca filas de B. "
            "Tablero de red = no entra. Un Administrador de red SÍ sigue viendo A y B. JSON sin password."
        ),
        "archivos": "perfil (SQL) · app/models/perfil.ts · usuarios_controller login · gates en eleccion_controller y aprendizs_controller · menú front",
    },
    {
        "id": "HU-S2-031",
        "rf": "RF-NU-031",
        "cu": "CU-31",
        "sp": 3,
        "prio": "Debe tener",
        "persona": "Mebel",
        "capa": "Front UX",
        "rama": "sigevaFront · feat/swal-eleccion-creada",
        "titulo": "SweetAlert al crear una elección (rol funcionario)",
        "historia": (
            "Como funcionario, quiero ver un SweetAlert bonito cuando la elección se crea con éxito "
            "para no recibir el alert nativo del navegador («creadaeleccion exitosamente»)."
        ),
        "problema": "Hoy el alta de elección dispara window.alert / un aviso plano. Se ve de prototipo, no de producto SENA.",
        "valor": "El primer clic de la mesa (crear la convocatoria) se siente institucional. Encaja con el 409 de Adrii: el error también va en SweetAlert, no en alert().",
        "in_scope": [
            "Reemplazar el alert nativo del POST /api/eleccion/crear (201) por SweetAlert2",
            "Título: «Elección creada». Texto: «La elección se registró con éxito.» Icono success. Botón Entendido",
            "Paleta SENA: confirmButtonColor #1F7A4D (o #92D050). Español con tildes. Nada de «creadaeleccion exitosamente»",
            "Si el POST vuelve 409 (HU-S2-029), SweetAlert de error con el mensaje del back. No alert() nativo",
            "Solo el flujo crear elección logueado como Funcionario. No reescribir el formulario (eso sigue de Paula en el sprint anterior)",
        ],
        "out_scope": [
            "Rediseñar el form de campos (nombre, fechas). Paula no está en ese archivo esta semana; Mebel solo toca el feedback post-submit",
            "SweetAlert en urna, OTP, voto, acta, candidatos, login, import Excel",
            "Cambiar el JSON del back (el 201 sigue siendo Eleccion creada con exito; el texto lindo es del Swal)",
        ],
        "listo": (
            "Funcionario crea una elección válida: no sale alert() del browser; sale Swal verde «Elección creada». "
            "Segundo intento el mismo día (cuando Adrii esté): Swal rojo con el 409. Network del POST intacto (201/409)."
        ),
        "archivos": "sigevaFront · form crear elección (éxito/error del submit) · npm i sweetalert2 si no está. No toca eleccion_controller.ts.",
    },
    {
        "id": "HU-S2-032",
        "rf": "RF-NU-032",
        "cu": "CU-32",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Mebel",
        "capa": "UX prototipo",
        "rama": "Figma / entregables/sprint-2/informe-jornada/",
        "titulo": "Prototipo: informe de candidatos por jornada (quién va ganando)",
        "historia": (
            "Como funcionario, quiero ver un informe de candidatos partido por jornada "
            "(Mañana, Tarde, Noche) y quién va ganando en cada franja, para no mezclar las tres urnas en un solo total."
        ),
        "problema": "HU-018 es el acta global de la elección. No hay pantalla ni prototipo que corte votos por jornada del candidato. El daily pide ver 'quién va ganando' por franja.",
        "valor": "El review ve el diseño. Lucero escribe la HU-019 en el Excel de historias. El código del informe NO entra este sprint.",
        "in_scope": [
            "Prototipo escritorio + móvil: 3 bloques Mañana / Tarde / Noche",
            "En cada bloque: candidatos con votos, ceros incluidos, quién va primero o empate",
            "Grafía exacta: Mañana | Tarde | Noche (con ñ)",
            "Una elección del centro, no tres elecciones. El corte es de candidatos.jornada",
            "El aprendiz NO ve este informe (sigue HU-007)",
        ],
        "out_scope": [
            "Implementar API ni PDF este sprint (eso es HU-019, Lucero la escribe, código después)",
            "Cambiar el acta HU-018 (sigue existiendo el total de la elección)",
            "Landing, urna, OTP, import Excel, SweetAlert de crear elección (HU-S2-031 ya es suya si no cerró)",
        ],
        "listo": (
            "Hay Figma o HTML con las 3 jornadas y un ganador/empate por franja. El equipo lo ve el viernes. "
            "Cero PR de backend de totales."
        ),
        "archivos": "entregables/sprint-2/informe-jornada/ o Figma. No toca generacion_reporte_controller.ts.",
    },
    {
        "id": "HU-S2-033",
        "rf": "RF-NU-033",
        "cu": "CU-33",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Paula",
        "capa": "UX móvil",
        "rama": "Figma · urna aprendiz 375 px",
        "titulo": "Prototipos móvil del aprendiz (misma urna web, adaptada al celular)",
        "historia": (
            "Como aprendiz, quiero usar la urna en el celular igual que en la web "
            "(login, elegir jornada, votaciones, tarjetón, OTP, confirmar, comprobante) para votar desde el teléfono."
        ),
        "problema": "Las pantallas de urna están pensadas en escritorio. En 375 px se cortan o no se recorren.",
        "valor": "El SENA vota con el celular. Paula prototipa; no reescribe la urna en código este sprint.",
        "in_scope": [
            "Flujos de aprendiz a 375 px: login-aprendiz, recuperar contraseña, elegir jornada, votaciones, tarjetón, OTP, confirmar voto, comprobante",
            "Mismos campos y mismas URLs que la web. No inventar un app nativa",
            "Jornada: Mañana | Tarde | Noche. No picker inventado en el primer login distinto al de web",
        ],
        "out_scope": [
            "Código a develop de urna (Sofia ya tiene tarjetón web). Paula entrega prototipo",
            "Pantallas de funcionario / admin",
            "Landing (Sofia). Equipo.tsx ya lo hizo ella: no lo reabre salvo un ajuste móvil chico",
        ],
        "listo": "Figma o HTML recorrible: de login aprendiz hasta comprobante, en 375 px, mismos pasos que la web.",
        "archivos": "entregables/sprint-2/movil-aprendiz/ o Figma. No toca sigevaFront/src/pages/aprendiz salvo captura de referencia.",
    },
    {
        "id": "HU-S2-034",
        "rf": "RF-NU-034",
        "cu": "CU-34",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Maicol",
        "capa": "Front",
        "rama": "sigevaFront · feat/recuperar-password",
        "titulo": "Recuperar contraseña en el frontend (conectar el API)",
        "historia": (
            "Como aprendiz o gestor, quiero recuperar mi clave con el correo y un código de 6 caracteres "
            "para entrar de nuevo sin pedirle a Bienestar que me la cambie a mano."
        ),
        "problema": "RecuperarContrasena.tsx pide documento y llama rutas que el back no tiene. El back de Alex ya está: solicitar + confirmar.",
        "valor": "Los 4 roles usan un solo flujo. El paquete para copiar JSON está en para-companero/recuperar-password/.",
        "in_scope": [
            "Reescribir src/pages/RecuperarContrasena.tsx: 3 pasos (correo → código+clave → listo)",
            "POST /api/recuperar-password/solicitar { email } y POST .../confirmar { email, codigo, nueva_password }",
            "Código 6, clave mín 8, repetir clave solo en el form. Pintar message del back. Sin toast de éxito si falló",
            "Redirect: Aprendiz → /login-aprendiz. Staff → /login. Sin login automático",
            "Mantener Login.css y la ruta /recuperar-contrasena. No tocar App.tsx",
        ],
        "out_scope": [
            "Backend (Alex HU-S2-036). No crear otras URLs",
            "PUT /api/aprendiz/actualizar/contrasena (410)",
            "Landing, urna, elección, import",
        ],
        "listo": (
            "Network solicitar = { email } 200. Network confirmar = { email, codigo, nueva_password } 200. "
            "Ya no se pide documento. Login con la clave nueva funciona."
        ),
        "archivos": "sigevaFront/src/pages/RecuperarContrasena.tsx · contrato en para-companero/recuperar-password/README.md",
    },
    {
        "id": "HU-S2-035",
        "rf": "RF-NU-035",
        "cu": "CU-35",
        "sp": 2,
        "prio": "Debe tener",
        "persona": "Maicol",
        "capa": "Front login",
        "rama": "sigevaFront · feat/login-ojo-credenciales",
        "titulo": "Ojo para ver la clave y aviso si las credenciales no sirven",
        "historia": (
            "Como usuario en el login, quiero ver u ocultar lo que escribí en la contraseña "
            "y que me digan claro si el correo o la clave no coinciden, para no adivinar si me equivoqué."
        ),
        "problema": "El input es type=password sin ojo. El catch del login tira un toast genérico y a veces ignora el message del back.",
        "valor": "Menos tickets de 'no puedo entrar'. Misma pantalla de Login.tsx (gestión y aprendiz).",
        "in_scope": [
            "Botón de ojo (mostrar/ocultar) en login gestión y login aprendiz",
            "Pintar error.response.data.message cuando el login falle (401 / success false)",
            "Si las credenciales están bien, el flujo actual (navigate) no cambia",
        ],
        "out_scope": [
            "Recuperar contraseña (HU-S2-034). JWT. Cambiar endpoints de login",
            "Landing. Form de elección",
        ],
        "listo": "En /login y /login-aprendiz hay ojo. Clave mala = mensaje del API en pantalla, no un éxito falso.",
        "archivos": "sigevaFront/src/pages/Login.tsx · Login.css",
    },
    {
        "id": "HU-S2-036",
        "rf": "RF-NU-036",
        "cu": "CU-36",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Alex",
        "capa": "Back",
        "rama": "sigevaBack · feat/recuperar-password",
        "titulo": "Recuperar contraseña en el backend (OTP al correo, 4 roles)",
        "historia": (
            "Como cualquier rol con correo en SIGEVA, quiero pedir un código y dejar una clave nueva "
            "para recuperar el acceso sin un endpoint abierto de cambio de contraseña."
        ),
        "problema": "No había HU. El PUT /api/aprendiz/actualizar/contrasena era un hueco. El front pedía documento.",
        "valor": "Un solo par de endpoints. Tabla recuperacion_password. Caduca 5 min. bcrypt.",
        "in_scope": [
            "POST /api/recuperar-password/solicitar y POST /api/recuperar-password/confirmar",
            "Busca en usuarios y luego aprendiz. Código nanoid 6. Mail mismo SMTP que el OTP de voto",
            "410 en PUT /api/aprendiz/actualizar/contrasena",
            "Paquete para-companero/recuperar-password/ para Maicol",
        ],
        "out_scope": [
            "Front (Maicol HU-S2-034). JWT. Segunda cuenta de Gmail. OTP de votación",
        ],
        "listo": "Thunder solicitar 200 + mail. Confirmar 200 + login con la clave nueva. Correo inexistente 404. Código mal 400 OTP_INVALIDO.",
        "archivos": "app/controllers/recuperacion_password_controller.ts · start/routes/recuperar_password.ts · para-companero/recuperar-password/",
    },
    {
        "id": "HU-S2-037",
        "rf": "RF-NU-037",
        "cu": "CU-37",
        "sp": 8,
        "prio": "Debe tener",
        "persona": "Alex",
        "capa": "Back + Front",
        "rama": "sigevaBack + sigevaFront · import ficha",
        "titulo": "Cargar aprendices desde el Excel de Sofia Plus (mesa y red)",
        "historia": (
            "Como funcionario o administrador, quiero subir el Reporte de Aprendices de Sofia Plus "
            "para armar el padrón sin inventar otra plantilla y sin elegir jornada en la carga."
        ),
        "problema": "HU-012/024 existían en papel; el código no leía el xls real (C2 = ficha - programa). Pedían jornada en el form y eso saltaba el picker del aprendiz.",
        "valor": "Padrón real. Clave inicial = número de documento. Jornada la elige el aprendiz al entrar.",
        "in_scope": [
            "POST /api/aprendices/importarExcel. Parser C2 y filas desde 5. Todos los estados de Sofia Plus",
            "Password solo en insert = bcrypt(documento). No duplicar programa ni perfil Aprendiz",
            "Funcionario/admin_sistema: centro = sesión. Administrador: centroFormacionId obligatorio",
            "Front: /cargar-aprendices y /cargar-aprendices-admin. Sin combo de jornada. KPIs + SweetAlert de resultado",
        ],
        "out_scope": [
            "Acta. Recuperar clave (otra HU). Picker de jornada en el import",
        ],
        "listo": "Network del POST con el xls de ficha. Insertados/actualizados/omitidos. Reimport no duplica programa. Login con documento como clave. Grupo nuevo con jornada vacía.",
        "archivos": "app/services/import_ficha.ts · ImportController.ts · sigevaFront CargarAprendices.tsx y CargarAprendicesAdmin.tsx",
    },
    {
        "id": "HU-S2-038",
        "rf": "RF-NU-038",
        "cu": "CU-38",
        "sp": 3,
        "prio": "Debe tener",
        "persona": "Alex",
        "capa": "Back + Front",
        "rama": "ya en develop / ramas de import y elección",
        "titulo": "Quitar jornada de la elección y de la carga; el aprendiz la elige al entrar",
        "historia": (
            "Como mesa, quiero una sola elección por centro (sin jornada en la convocatoria) "
            "para que el aprendiz elija Mañana/Tarde/Noche cuando entra y la urna recorte candidatos con ?jornada=."
        ),
        "problema": "Si el import o el crear elección estampan jornada en el grupo, el login salta /elegir-jornada y la urna se descuadra.",
        "valor": "Cierra el paquete del 26-27 ago: jornada vive en el candidato y en la sesión del aprendiz, no en la elección.",
        "in_scope": [
            "POST/PUT elección sin jornada. Import no manda jornada. Grupo nuevo jornada = ''",
            "Login aprendiz: jornada vacía → /elegir-jornada. Urna ?jornada= de la sesión",
        ],
        "out_scope": [
            "Acta por jornada (eso es el prototipo de Mebel / HU-019 de Lucero)",
            "Form de candidato (Sofia sprint anterior, no reabrir)",
        ],
        "listo": "Crear elección 201 con jornada null. Import sin campo jornada. Aprendiz nuevo cae en elegir-jornada.",
        "archivos": "eleccion_controller · import_ficha.ts · CargarAprendices*.tsx · Login.tsx / ElegirJornadaPage.tsx",
    },
    {
        "id": "HU-S2-039",
        "rf": "RF-NU-039",
        "cu": "CU-39",
        "sp": 2,
        "prio": "Debería tener",
        "persona": "Paula",
        "capa": "Front",
        "rama": "sigevaFront · /equipo",
        "titulo": "Prototipo / página Equipo de desarrollo",
        "historia": (
            "Como visitante, quiero ver quién hizo SIGEVA "
            "para dar crédito al equipo de la Fábrica."
        ),
        "problema": "No había HU. Paula ya prototipó e implementó /equipo.",
        "valor": "La landing puede enlazar a personas reales. Lucero no inventa otra página: documenta esta.",
        "in_scope": [
            "Ruta /equipo. Layout de Login.css / Equipo.css. Fotos y roles del equipo",
        ],
        "out_scope": ["Urna", "Gestión", "Landing (Sofia solo enlaza)"],
        "listo": "GET /equipo pinta el equipo. Link desde la landing o el footer.",
        "archivos": "sigevaFront/src/pages/Equipo.tsx · App.tsx ruta /equipo",
    },
    {
        "id": "HU-S2-040",
        "rf": "RF-NU-040",
        "cu": "CU-40",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Lucero",
        "capa": "Documentación HU",
        "rama": "sigevaBack · documentacion + entregables/sprint-1",
        "titulo": "Escribir en el Excel de historias lo que ya se construyó y no estaba",
        "historia": (
            "Como analista, quiero que recuperar contraseña e informe por jornada "
            "queden como historias de usuario en el mismo Excel del Sprint 1, para que el cliente no vea huecos."
        ),
        "problema": "EP-SIG-001 dice 'fuera: recuperar contraseña'. HU-019 no existe. HU-013 todavía habla de jornada en la elección. HU-012 dice que el código pide jornada.",
        "valor": "El backlog coincide con el producto. Alex no reescribe las 22 HU a mano: Lucero las mete donde toca.",
        "in_scope": [
            "NUEVA HU-008 Recuperar contraseña (4 roles) — ver hoja 10-LUCERO, bloque A",
            "NUEVA HU-019 Informe de candidatos por jornada — hoja 10-LUCERO, bloque B",
            "ACTUALIZAR HU-012, HU-013, HU-016, HU-024 y épica EP-SIG-002 (jornada ya no va en la elección ni en el Excel) — bloque C",
            "Regenerar 04-Historias-de-Usuario.xlsx con python documentacion/_generar_entregables.py cuando los .py de datos estén",
        ],
        "out_scope": [
            "Código. Prototipos (Mebel/Paula). Inventar JWT, segunda vuelta, acta pública",
            "Renumerar HU-001 a 025. Las nuevas usan los huecos 008 y 019",
        ],
        "listo": (
            "04-Historias-de-Usuario.xlsx tiene HU-008 y HU-019. EP-SIG-001 ya no lista recuperar como fuera. "
            "HU-013 no pide jornada en la convocatoria. Criterios Gherkin en la hoja de esa HU."
        ),
        "archivos": "documentacion/_excel_senior_data_aprendiz.py (HU-008) · _excel_senior_data_funcionario.py (HU-019 + parches 012/013/016) · _excel_senior_data_epicas.py · hoja 10-LUCERO de ESTE Excel",
    },
]

TAREAS = [
    {"id": "T-S2-01", "hu": "HU-S2-026", "persona": "Sofia", "capa": "Front", "estado": "En curso",
     "titulo": "Landing page SIGEVA en producción",
     "detalle": "Pulir / de sigevaFront: dos puertas (urna y gestión), identidad SENA, desktop y 375 px. No reescribe Equipo.tsx (Paula). No toca urna.",
     "listo": "/ abre la landing. CTA a /login-aprendiz y /login. Se ve bien en celular."},
    {"id": "T-S2-02", "hu": "HU-S2-027", "persona": "Maicol", "capa": "Back", "estado": "Por hacer",
     "titulo": "Ordenar listados de elección: más reciente primero",
     "detalle": "orderBy fecha_inicio desc + ideleccion desc en todos los GET de elección. El front no invierte el array.",
     "listo": "Thunder: JSON [27 ago, 25 ago, 20 ago] en ese orden."},
    {"id": "T-S2-03", "hu": "HU-S2-028", "persona": "Sofia", "capa": "Front + Back", "estado": "Por hacer",
     "titulo": "Filtros de aprendices: centro, teléfono y los que faltan",
     "detalle": "Barra de filtros. Query: idcentro_formacion, celular, numero_documento, email, search (nombres/apellidos), estado. Combinables. Añadir celular al whereILike que hoy no lo tiene.",
     "listo": "Network con ?celular= y ?idcentro_formacion=. Vacío ≠ 404. Sin password en el JSON."},
    {"id": "T-S2-04", "hu": "HU-S2-029", "persona": "Adrii Eraso", "capa": "Back", "estado": "Por hacer",
     "titulo": "Una elección por centro el mismo día (criterios + guard)",
     "detalle": "Implementar RN-S2-001 en crear y actualizar. 409 + mensaje en español. No unique de created_at. No se pelea el solape de ventanas en días distintos.",
     "listo": "Los 5 disparos de Thunder de la hoja CRITERIOS en verde. El form muestra el 409."},
    {"id": "T-S2-05", "hu": "HU-S2-030", "persona": "Alex", "capa": "Back + menú", "estado": "Por hacer",
     "titulo": "Perfil admin_sistema aislado a su centro",
     "detalle": "INSERT perfil. Login devuelve el rol y el centro. Gates en elecciones y aprendices. 403 a rutas de red. Menú sin torre nacional. Usuario demo por centro para QA.",
     "listo": "Matriz de la hoja ROLES: las celdas de admin_sistema coinciden con Thunder."},
    {"id": "T-S2-06", "hu": "HU-S2-040", "persona": "Equipo", "capa": "Review", "estado": "Por hacer",
     "titulo": "Review viernes: demo de carriles + HU-008/019 de Lucero",
     "detalle": "Sofia landing. Paula urna móvil. Mebel informe por jornada. Maicol ojo login. Adrii 409. Lucero enseña HU-008 y HU-019 en el Excel de historias.",
     "listo": "Acta de 5 líneas: qué se vio, qué queda, Lucero dejó 008 y 019."},
    {"id": "T-S2-07", "hu": "HU-S2-031", "persona": "Mebel", "capa": "Front UX", "estado": "Por hacer",
     "titulo": "SweetAlert al crear elección (funcionario)",
     "detalle": "Quitar window.alert del éxito del POST crear. Swal.fire success: «Elección creada» / «La elección se registró con éxito.» Botón Entendido, verde SENA. El 409 de Adrii también va en Swal error, no en alert nativo.",
     "listo": "Crear como funcionario = Swal bonito. Cero alert() en esa pantalla. El JSON del back no se cambia."},
    {"id": "T-S2-08", "hu": "HU-S2-032", "persona": "Mebel", "capa": "UX", "estado": "En curso",
     "titulo": "Prototipo informe candidatos por jornada (quién va ganando)",
     "detalle": "Figma/HTML: 3 bloques Mañana/Tarde/Noche. En cada uno votos, ceros, ganador o empate. Una elección, corte por candidatos.jornada. El aprendiz no lo ve.",
     "listo": "Prototipo visto en review. Cero código de totales. Lucero usa esto para redactar HU-019."},
    {"id": "T-S2-09", "hu": "HU-S2-033", "persona": "Paula", "capa": "UX móvil", "estado": "En curso",
     "titulo": "Prototipos móvil de la urna del aprendiz",
     "detalle": "Mismos pasos que la web a 375 px: login aprendiz, recuperar, elegir jornada, votaciones, tarjetón, OTP, confirmar, comprobante. No app nativa.",
     "listo": "Recorrido Figma/HTML completo en celular. Grafía Mañana/Tarde/Noche."},
    {"id": "T-S2-10", "hu": "HU-S2-034", "persona": "Maicol", "capa": "Front", "estado": "Hecho",
     "titulo": "Conectar recuperar contraseña al API de Alex",
     "detalle": "Reescribir RecuperarContrasena.tsx. 3 pasos. POST solicitar y confirmar. JSON del paquete para-companero/recuperar-password/. Sin documento. Sin toast de éxito si falló.",
     "listo": "Network = las 2 rutas nuevas. Login con la clave nueva. Cero llamadas a las rutas viejas."},
    {"id": "T-S2-11", "hu": "HU-S2-035", "persona": "Maicol", "capa": "Front", "estado": "En curso",
     "titulo": "Ojo de contraseña y mensaje si las credenciales fallan",
     "detalle": "En Login.tsx (gestión y aprendiz): botón mostrar/ocultar clave. Si el POST de login falla, pintar el message del back (no un genérico que mienta).",
     "listo": "Ojo visible. Clave mala = texto del API. Clave buena = mismo navigate de hoy."},
    {"id": "T-S2-12", "hu": "HU-S2-036", "persona": "Alex", "capa": "Back", "estado": "Hecho",
     "titulo": "API recuperar contraseña (solicitar + confirmar)",
     "detalle": "Tabla recuperacion_password. OTP 6 al correo. 4 roles. 410 al PUT viejo. README + JSON para Maicol en para-companero/recuperar-password/.",
     "listo": "Thunder 200/404/400. Mail llega. Login con clave nueva."},
    {"id": "T-S2-13", "hu": "HU-S2-037", "persona": "Alex", "capa": "Back + Front", "estado": "Hecho",
     "titulo": "Import Excel Sofia Plus (funcionario y admin red)",
     "detalle": "Parser C2. Password=documento. Sin jornada en el form. KPIs + SweetAlert de resultado. Admin elige regional/centro.",
     "listo": "xls real importa. Reimport no duplica programa. Aprendiz entra con documento."},
    {"id": "T-S2-14", "hu": "HU-S2-038", "persona": "Alex", "capa": "Back + Front", "estado": "Hecho",
     "titulo": "Jornada fuera de la elección y de la carga",
     "detalle": "Elección global. Import deja grupo.jornada vacía. El aprendiz elige al entrar. Urna ?jornada=.",
     "listo": "201 crear sin jornada. Import sin combo. Picker /elegir-jornada en aprendiz nuevo."},
    {"id": "T-S2-15", "hu": "HU-S2-039", "persona": "Paula", "capa": "Front", "estado": "Hecho",
     "titulo": "Página Equipo de desarrollo",
     "detalle": "Ruta /equipo ya prototipada e implementada. Sofia solo enlaza desde la landing.",
     "listo": "/equipo pinta al equipo."},
    {"id": "T-S2-16", "hu": "HU-S2-040", "persona": "Lucero", "capa": "Docs", "estado": "Por hacer",
     "titulo": "Meter HU-008 y HU-019 en el Excel de historias (y parchar jornada)",
     "detalle": "Sigue la hoja 10-LUCERO al pie de la letra. No inventa IDs. Huecos 008 y 019. Actualiza HU-012/013/016/024 y EP-SIG-001/002.",
     "listo": "04-Historias-de-Usuario.xlsx regenerado con las dos HU nuevas y jornada corregida en convocatoria."},
    {"id": "T-S2-17", "hu": "HU-S2-029", "persona": "Adrii Eraso", "capa": "Back", "estado": "Por hacer",
     "titulo": "Cerrar los CA-029-* que YA están en 05-CRITERIOS (no inventar otros)",
     "detalle": "Adrii no escribe criterios nuevos: implementa RN-S2-001 contra CA-029-01 a CA-029-08. Thunder de los 5 disparos. 409 en español.",
     "listo": "Columna QA de CA-029-01 a 08 en sí. Mismos textos de 05-CRITERIOS."},
]

CRITERIOS = [
    # Sofia landing
    {"hu": "HU-S2-026", "id": "CA-026-01", "tipo": "Feliz", "persona": "Sofia",
     "dado": "un visitante no logueado abre /",
     "cuando": "mira la landing",
     "entonces": "entiende qué es SIGEVA y ve dos CTA: votar (urna) y gestionar (mesa/admin)"},
    {"hu": "HU-S2-026", "id": "CA-026-02", "tipo": "UX", "persona": "Sofia",
     "dado": "la landing",
     "cuando": "se abre en 1440 px y en 375 px",
     "entonces": "CTA visibles, sin texto cortado, sin scroll horizontal"},
    {"hu": "HU-S2-026", "id": "CA-026-03", "tipo": "Feliz", "persona": "Sofia",
     "dado": "los dos botones",
     "cuando": "el visitante pulsa cada uno",
     "entonces": "urna va a /login-aprendiz y gestión a /login. No pide jornada ni documento en /"},
    {"hu": "HU-S2-026", "id": "CA-026-04", "tipo": "Fuera", "persona": "Sofia",
     "dado": "esta historia",
     "cuando": "se cierra",
     "entonces": "no se tocó urna, OTP, Equipo.tsx ni RecuperarContrasena"},
    # Maicol
    {"hu": "HU-S2-027", "id": "CA-027-01", "tipo": "Feliz", "persona": "Maicol",
     "dado": "un centro con 3 elecciones fecha_inicio 20, 25 y 27 de agosto 2026",
     "cuando": "GET por centro (todas) o GET listar",
     "entonces": "el array viene [27, 25, 20]. La posición 0 es la más reciente"},
    {"hu": "HU-S2-027", "id": "CA-027-02", "tipo": "Feliz", "persona": "Maicol",
     "dado": "dos elecciones del mismo día de inicio (no debería pasar tras HU-S2-029; si hay datos viejos)",
     "cuando": "empatan en fecha_inicio",
     "entonces": "gana la de mayor ideleccion (la creada después)"},
    {"hu": "HU-S2-027", "id": "CA-027-03", "tipo": "Permiso", "persona": "Maicol",
     "dado": "el orden",
     "cuando": "el front pinta el listado",
     "entonces": "no se hace .reverse() ni se ordena por nombre. El JSON manda"},
    {"hu": "HU-S2-027", "id": "CA-027-04", "tipo": "Fuera", "persona": "Maicol",
     "dado": "esta historia",
     "cuando": "se cierra",
     "entonces": "no se agregaron filtros de texto ni se tocó candidatos, OTP ni acta"},
    # Sofia
    {"hu": "HU-S2-028", "id": "CA-028-01", "tipo": "Feliz", "persona": "Sofia",
     "dado": "padrón con varios centros",
     "cuando": "filtra por centro de formación X",
     "entonces": "solo salen aprendices de X"},
    {"hu": "HU-S2-028", "id": "CA-028-02", "tipo": "Feliz", "persona": "Sofia",
     "dado": "aprendices con celular 3001112233 y 3109998877",
     "cuando": "filtra teléfono 300",
     "entonces": "sale el del 300, no el del 310"},
    {"hu": "HU-S2-028", "id": "CA-028-03", "tipo": "Feliz", "persona": "Sofia",
     "dado": "la barra de filtros",
     "cuando": "usa documento, correo, nombres/apellidos o estado (los que faltaban en UI)",
     "entonces": "cada uno recorta el listado. Se pueden combinar (centro + teléfono + estado)"},
    {"hu": "HU-S2-028", "id": "CA-028-04", "tipo": "Excepción", "persona": "Sofia",
     "dado": "filtros que no matchean a nadie",
     "cuando": "busca",
     "entonces": "lista vacía y mensaje claro. HTTP 200. No 404"},
    {"hu": "HU-S2-028", "id": "CA-028-05", "tipo": "Seguridad", "persona": "Sofia",
     "dado": "cualquier respuesta de esta consulta",
     "cuando": "se inspecciona el JSON",
     "entonces": "no viaja password ni hash"},
    {"hu": "HU-S2-028", "id": "CA-028-06", "tipo": "Permiso", "persona": "Sofia",
     "dado": "un admin_sistema o funcionario del centro A",
     "cuando": "intenta filtrar centro B",
     "entonces": "el sistema ignora B y no lista el padrón ajeno (Alex pone el gate; Sofia no pinta combo de sedes a ese rol)"},
    # Adrii — el bloque más cerrado a propósito
    {"hu": "HU-S2-029", "id": "CA-029-01", "tipo": "Feliz", "persona": "Adrii Eraso",
     "dado": "centro 1 sin elección el 27 de agosto de 2026",
     "cuando": "POST /api/eleccion/crear con fecha_inicio 2026-08-27 e idcentro_formacion 1",
     "entonces": "201 y queda creada"},
    {"hu": "HU-S2-029", "id": "CA-029-02", "tipo": "Excepción", "persona": "Adrii Eraso",
     "dado": "ya existe una elección del centro 1 con fecha_inicio el 27 de agosto de 2026",
     "cuando": "POST otra con fecha_inicio 2026-08-27 e idcentro 1 (aunque el nombre sea distinto)",
     "entonces": "409. Mensaje: «Ya existe una elección para este centro el 27 de agosto. No se puede crear otra el mismo día.» No se inserta fila"},
    {"hu": "HU-S2-029", "id": "CA-029-03", "tipo": "Feliz", "persona": "Adrii Eraso",
     "dado": "la elección del 27 en el centro 1",
     "cuando": "POST con fecha_inicio 2026-08-27 pero idcentro_formacion 2",
     "entonces": "201. La regla es por centro, no mundial"},
    {"hu": "HU-S2-029", "id": "CA-029-04", "tipo": "Feliz", "persona": "Adrii Eraso",
     "dado": "la elección del 27 en el centro 1",
     "cuando": "POST con fecha_inicio 2026-08-28 e idcentro 1",
     "entonces": "201. Otro día, misma sede, sí"},
    {"hu": "HU-S2-029", "id": "CA-029-05", "tipo": "Feliz", "persona": "Adrii Eraso",
     "dado": "la elección del 27 (id E1)",
     "cuando": "PUT /api/eleccionActualizar/E1 cambiando nombre u horas, sin cambiar el día",
     "entonces": "200. Editar la misma no viola la regla"},
    {"hu": "HU-S2-029", "id": "CA-029-06", "tipo": "Excepción", "persona": "Adrii Eraso",
     "dado": "E1 el 27 y E2 el 28, mismo centro",
     "cuando": "PUT de E2 con fecha_inicio 2026-08-27",
     "entonces": "409. No se «mueve» al día ocupado"},
    {"hu": "HU-S2-029", "id": "CA-029-07", "tipo": "Validación", "persona": "Adrii Eraso",
     "dado": "el día calendario",
     "cuando": "se compara fecha_inicio",
     "entonces": "se usa el día en America/Bogota, no el instante UTC que cruce medianoche"},
    {"hu": "HU-S2-029", "id": "CA-029-08", "tipo": "Fuera", "persona": "Adrii Eraso",
     "dado": "una elección 27–29 y otra 28–30",
     "cuando": "las ventanas se solapan pero fecha_inicio es distinta",
     "entonces": "NO se rechaza en este sprint. Queda nota, no código"},
    # Alex
    {"hu": "HU-S2-030", "id": "CA-030-01", "tipo": "Feliz", "persona": "Alex",
     "dado": "existe el perfil admin_sistema y un usuario activo con centro A",
     "cuando": "hace login de gestión con su correo",
     "entonces": "200. data.perfil = 'admin_sistema' y data.centroFormacion = A. No viaja password"},
    {"hu": "HU-S2-030", "id": "CA-030-02", "tipo": "Feliz", "persona": "Alex",
     "dado": "ese admin_sistema autenticado",
     "cuando": "lista elecciones o aprendices",
     "entonces": "solo ve filas del centro A"},
    {"hu": "HU-S2-030", "id": "CA-030-03", "tipo": "Permiso", "persona": "Alex",
     "dado": "admin_sistema del centro A",
     "cuando": "manda idcentro_formacion de B en el body, query o URL",
     "entonces": "no crea ni lista en B. O se ignora el id y se usa la sesión, o 403. Nunca filas de B"},
    {"hu": "HU-S2-030", "id": "CA-030-04", "tipo": "Permiso", "persona": "Alex",
     "dado": "admin_sistema",
     "cuando": "pide tablero de red, import eligiendo centro, o listado de funcionarios de toda la red",
     "entonces": "no entra (403 u oculto en menú)"},
    {"hu": "HU-S2-030", "id": "CA-030-05", "tipo": "Permiso", "persona": "Alex",
     "dado": "un Administrador de red",
     "cuando": "lista censo o elecciones",
     "entonces": "sigue viendo toda la red. Este HU no le recorta la torre"},
    {"hu": "HU-S2-030", "id": "CA-030-06", "tipo": "Permiso", "persona": "Alex",
     "dado": "un aprendiz",
     "cuando": "pide menú o APIs de admin_sistema",
     "entonces": "no se le sirve"},
    {"hu": "HU-S2-030", "id": "CA-030-07", "tipo": "Validación", "persona": "Alex",
     "dado": "el alta de un admin_sistema",
     "cuando": "no trae idcentro_formacion",
     "entonces": "no se crea. El centro es obligatorio para este perfil, no para el Administrador de red"},
    {"hu": "HU-S2-030", "id": "CA-030-08", "tipo": "Fuera", "persona": "Alex",
     "dado": "este sprint",
     "cuando": "se cierra el HU",
     "entonces": "no hay JWT nuevo, no se crea tabla organizacion, admin_sistema no vota"},
    # Mebel
    {"hu": "HU-S2-031", "id": "CA-031-01", "tipo": "Feliz", "persona": "Mebel",
     "dado": "un funcionario autenticado en el form de nueva elección, con datos válidos",
     "cuando": "envía y el POST /api/eleccion/crear responde 201",
     "entonces": "aparece un SweetAlert (no el alert nativo) con icono success, título «Elección creada» y texto «La elección se registró con éxito.»"},
    {"hu": "HU-S2-031", "id": "CA-031-02", "tipo": "UX", "persona": "Mebel",
     "dado": "ese SweetAlert de éxito",
     "cuando": "se mira el botón y el color",
     "entonces": "el botón dice Entendido, el color es verde SENA (#1F7A4D o #92D050), el español lleva tildes. No dice «creadaeleccion exitosamente»"},
    {"hu": "HU-S2-031", "id": "CA-031-03", "tipo": "Excepción", "persona": "Mebel",
     "dado": "el mismo form y un 409 de Adrii (ya hay elección ese día)",
     "cuando": "el POST falla",
     "entonces": "SweetAlert de error con el mensaje del back. Tampoco hay window.alert"},
    {"hu": "HU-S2-031", "id": "CA-031-04", "tipo": "Permiso", "persona": "Mebel",
     "dado": "esta pantalla",
     "cuando": "se inspecciona el código",
     "entonces": "no queda ningún alert( ni confirm( en el flujo crear elección"},
    {"hu": "HU-S2-031", "id": "CA-031-05", "tipo": "Fuera", "persona": "Mebel",
     "dado": "esta historia",
     "cuando": "se cierra",
     "entonces": "no se rediseñó el form, no se tocó urna/OTP/acta, no se cambió el JSON del 201"},
    # Mebel informe
    {"hu": "HU-S2-032", "id": "CA-032-01", "tipo": "Feliz", "persona": "Mebel",
     "dado": "una elección con candidatos en Mañana, Tarde y Noche",
     "cuando": "se mira el prototipo de informe",
     "entonces": "hay tres bloques, uno por jornada, con votos (ceros incluidos) y quién va primero o empate en ESA franja"},
    {"hu": "HU-S2-032", "id": "CA-032-02", "tipo": "UX", "persona": "Mebel",
     "dado": "las etiquetas de jornada",
     "cuando": "se leen",
     "entonces": "dicen Mañana, Tarde, Noche (con ñ). No manana ni 3 elecciones distintas"},
    {"hu": "HU-S2-032", "id": "CA-032-03", "tipo": "Fuera", "persona": "Mebel",
     "dado": "el aprendiz",
     "cuando": "abre urna",
     "entonces": "no ve este informe (HU-007). El prototipo es de funcionario"},
    {"hu": "HU-S2-032", "id": "CA-032-04", "tipo": "Fuera", "persona": "Mebel",
     "dado": "este sprint",
     "cuando": "se cierra el prototipo",
     "entonces": "no hay PR de generacion_reporte_controller ni PDF nuevo"},
    # Paula móvil
    {"hu": "HU-S2-033", "id": "CA-033-01", "tipo": "Feliz", "persona": "Paula",
     "dado": "un aprendiz en celular 375 px",
     "cuando": "recorre el prototipo de urna",
     "entonces": "puede hacer login, elegir jornada, ver votaciones, tarjetón, OTP, confirmar y comprobante — los mismos pasos que la web"},
    {"hu": "HU-S2-033", "id": "CA-033-02", "tipo": "UX", "persona": "Paula",
     "dado": "cada pantalla del prototipo",
     "cuando": "se abre a 375 px",
     "entonces": "CTA visibles, sin scroll horizontal, sin campos que la web no tenga"},
    {"hu": "HU-S2-033", "id": "CA-033-03", "tipo": "Fuera", "persona": "Paula",
     "dado": "esta historia",
     "cuando": "se cierra",
     "entonces": "no hay merge de código de urna a develop. No se prototipó gestión de funcionario"},
    # Maicol recuperar
    {"hu": "HU-S2-034", "id": "CA-034-01", "tipo": "Feliz", "persona": "Maicol",
     "dado": "un correo que existe en usuarios o aprendiz",
     "cuando": "POST /api/recuperar-password/solicitar con { email }",
     "entonces": "200. Pasa al paso código. Network solo manda email. Ya no se pide documento"},
    {"hu": "HU-S2-034", "id": "CA-034-02", "tipo": "Feliz", "persona": "Maicol",
     "dado": "el código de 6 y una clave ≥ 8 (y repetir igual)",
     "cuando": "POST /api/recuperar-password/confirmar",
     "entonces": "200. Redirect /login-aprendiz si perfil Aprendiz, /login si staff. No llama login() del auth"},
    {"hu": "HU-S2-034", "id": "CA-034-03", "tipo": "Excepción", "persona": "Maicol",
     "dado": "correo inexistente o código mal",
     "cuando": "falla el API",
     "entonces": "se pinta message del back. No hay toast de éxito en el catch"},
    {"hu": "HU-S2-034", "id": "CA-034-04", "tipo": "Fuera", "persona": "Maicol",
     "dado": "esta pantalla",
     "cuando": "se inspecciona Network",
     "entonces": "cero llamadas a /api/usuarios/recuperar-contrasena, /api/aprendiz/recuperar-contrasena o PUT actualizar/contrasena"},
    # Maicol ojo
    {"hu": "HU-S2-035", "id": "CA-035-01", "tipo": "Feliz", "persona": "Maicol",
     "dado": "login gestión o login aprendiz",
     "cuando": "pulsa el ojo",
     "entonces": "la clave se ve; al pulsar otra vez se oculta"},
    {"hu": "HU-S2-035", "id": "CA-035-02", "tipo": "Excepción", "persona": "Maicol",
     "dado": "correo o clave incorrectos",
     "cuando": "envía el login",
     "entonces": "aparece el message del back (o success:false). No entra. No dice que salió bien"},
    {"hu": "HU-S2-035", "id": "CA-035-03", "tipo": "Feliz", "persona": "Maicol",
     "dado": "credenciales correctas y usuario activo",
     "cuando": "envía",
     "entonces": "el navigate actual no cambia (urna o dashboard según perfil)"},
    # Alex recuperar back
    {"hu": "HU-S2-036", "id": "CA-036-01", "tipo": "Feliz", "persona": "Alex",
     "dado": "un correo de aprendiz o staff",
     "cuando": "POST solicitar",
     "entonces": "200, mail con código 6, en desarrollo viene codigo_otp_temporal"},
    {"hu": "HU-S2-036", "id": "CA-036-02", "tipo": "Feliz", "persona": "Alex",
     "dado": "ese código vigente",
     "cuando": "POST confirmar con nueva_password ≥ 8",
     "entonces": "200, data.perfil y data.login. La clave vieja ya no entra"},
    {"hu": "HU-S2-036", "id": "CA-036-03", "tipo": "Excepción", "persona": "Alex",
     "dado": "correo que no existe / código mal / código de más de 5 min",
     "cuando": "solicitar o confirmar",
     "entonces": "404 CUENTA_NO_ENCONTRADA o 400 OTP_INVALIDO / OTP_EXPIRADO"},
    {"hu": "HU-S2-036", "id": "CA-036-04", "tipo": "Seguridad", "persona": "Alex",
     "dado": "PUT /api/aprendiz/actualizar/contrasena",
     "cuando": "alguien lo llama",
     "entonces": "410 y el mensaje de usar solicitar/confirmar"},
    # Alex excel
    {"hu": "HU-S2-037", "id": "CA-037-01", "tipo": "Feliz", "persona": "Alex",
     "dado": "un xls Reporte de Aprendices Sofia Plus (C2 = ficha - programa)",
     "cuando": "funcionario POST /api/aprendices/importarExcel",
     "entonces": "inserted/updated/skipped. Centro = sesión. Clave inicial = documento. Sin jornada en el FormData"},
    {"hu": "HU-S2-037", "id": "CA-037-02", "tipo": "Feliz", "persona": "Alex",
     "dado": "Administrador de red",
     "cuando": "importa eligiendo regional y centro",
     "entonces": "mismo parser. centroFormacionId obligatorio. El funcionario no ve ese combo"},
    {"hu": "HU-S2-037", "id": "CA-037-03", "tipo": "Feliz", "persona": "Alex",
     "dado": "el mismo archivo otra vez",
     "cuando": "reimporta",
     "entonces": "0 insertados extra de programa. Updates no pisan la clave"},
    {"hu": "HU-S2-037", "id": "CA-037-04", "tipo": "UX", "persona": "Alex",
     "dado": "la carga terminó",
     "cuando": "el front responde",
     "entonces": "SweetAlert de importación + KPIs Insertados/Actualizados/Omitidos. Vista previa con scroll. Botón Subir al lado del archivo"},
    # Alex jornada
    {"hu": "HU-S2-038", "id": "CA-038-01", "tipo": "Feliz", "persona": "Alex",
     "dado": "POST /api/eleccion/crear",
     "cuando": "el body no trae jornada",
     "entonces": "201. eleccion.jornada null. No 400 «jornada no válida»"},
    {"hu": "HU-S2-038", "id": "CA-038-02", "tipo": "Feliz", "persona": "Alex",
     "dado": "un aprendiz recién importado",
     "cuando": "hace login",
     "entonces": "jornada vacía/null y cae en /elegir-jornada. Después la urna llama ?jornada="},
    # Paula equipo
    {"hu": "HU-S2-039", "id": "CA-039-01", "tipo": "Feliz", "persona": "Paula",
     "dado": "un visitante",
     "cuando": "abre /equipo",
     "entonces": "ve al equipo de desarrollo. La ruta ya existe en App.tsx"},
    # Lucero
    {"hu": "HU-S2-040", "id": "CA-040-01", "tipo": "Feliz", "persona": "Lucero",
     "dado": "el Excel 04-Historias-de-Usuario.xlsx",
     "cuando": "termina su carril",
     "entonces": "existe HU-008 Recuperar contraseña (4 roles) con Como/quiero/para, sí entra, no entra y criterios Gherkin"},
    {"hu": "HU-S2-040", "id": "CA-040-02", "tipo": "Feliz", "persona": "Lucero",
     "dado": "el mismo Excel",
     "cuando": "se busca el informe por jornada",
     "entonces": "existe HU-019 después de HU-018. No se fusionó con el acta global. Grafía Mañana/Tarde/Noche"},
    {"hu": "HU-S2-040", "id": "CA-040-03", "tipo": "Validación", "persona": "Lucero",
     "dado": "HU-012, HU-013, HU-016, HU-024 y EP-SIG-001 / 002",
     "cuando": "se leen",
     "entonces": "ya no dicen que la elección o el Excel piden jornada. EP-SIG-001 ya no lista recuperar contraseña en fuera"},
    {"hu": "HU-S2-040", "id": "CA-040-04", "tipo": "Fuera", "persona": "Lucero",
     "dado": "esta historia",
     "cuando": "se cierra",
     "entonces": "no se tocó código. No se renumeraron HU-001 a 025. Los IDs nuevos son 008 y 019"},
]

ROLES = [
    ("Entrar a la urna y votar", "Sí", "No", "No", "No"),
    ("Entrar a gestión (misma puerta HU-010)", "No", "Sí", "Sí", "Sí"),
    ("Centro obligatorio en el usuario", "El del censo", "Sí", "Sí", "No (opera la red)"),
    ("Ver elecciones de SU centro", "Solo urna filtrada", "Sí", "Sí", "Sí"),
    ("Ver elecciones de OTRO centro", "No", "No", "No", "Sí"),
    ("Crear / editar elección de SU centro", "No", "Sí", "Sí", "No en este sprint (P10)"),
    ("Crear segunda elección el mismo día", "—", "409 (Adrii)", "409 (Adrii)", "—"),
    ("Recuperar contraseña (correo + código)", "Sí (Maicol/Alex)", "Sí", "Sí", "Sí"),
    ("Ver padrón de SU centro", "No", "Sí (mesa)", "Sí", "Sí"),
    ("Filtrar padrón por teléfono / documento", "No", "Sí (Sofia)", "Sí, solo su centro", "Sí, eligiendo centro"),
    ("Ver padrón de toda la red", "No", "No", "No", "Sí"),
    ("Import Excel de SU centro (HU-012)", "No", "Sí", "Sí (mismo centro de sesión)", "No: usa HU-024"),
    ("Import eligiendo cualquier centro (HU-024)", "No", "No", "No", "Sí"),
    ("Tablero institucional de red (HU-020)", "No", "No", "No", "Sí"),
    ("Crear funcionarios de cualquier sede (HU-021)", "No", "No", "No", "Sí"),
    ("Ver menú de urna (votar)", "Sí", "No", "No", "No"),
]

PERSONAS = [
    ("Sofia", "Front landing", "HU-S2-026", "5",
     "Landing / en producción: dos puertas, SENA, desktop+móvil. El filtro de padrón (028) si da tiempo.",
     "Equipo.tsx (Paula). Recuperar contraseña (Maicol). Urna código. Informe por jornada (Mebel).",
     "sigevaFront · Inicio.tsx"),
    ("Maicol", "Front acceso", "HU-S2-034 + 035", "7",
     "Recuperar contraseña conectado al API (Hecho). Ojo + mensaje de credenciales en login. GET elecciones reciente-primero (027) si no cerró.",
     "Backend de recuperar (Alex). Landing. Import Excel.",
     "sigevaFront · RecuperarContrasena.tsx · Login.tsx"),
    ("Paula", "UX móvil + equipo", "HU-S2-033 + 039", "7",
     "Prototipos 375 px de TODA la urna del aprendiz (igual que web). Equipo /equipo ya Hecho.",
     "Landing (Sofia). Código de urna. Form crear elección.",
     "Figma móvil aprendiz  ·  Equipo.tsx"),
    ("Adrii Eraso", "Back regla de elección", "HU-S2-029", "5",
     "Implementar los criterios CA-029-01 a 08 que YA están en 05-CRITERIOS. No inventa otra regla. Thunder 409.",
     "Orden del listado (Maicol). OTP, voto, acta, candidatos. Solape de ventanas.",
     "sigevaBack · feat/eleccion-un-dia  ·  eleccion_controller.ts crear/actualizar"),
    ("Alex", "SM + back/front ya entregado", "HU-S2-036/037/038 + 030", "8+",
     "Hecho: recuperar back, import Excel, quitar jornada. Sigue admin_sistema si no cerró. Facilita a Lucero y a Maicol.",
     "JWT, tabla organizacion, implementar informe por jornada, prototipos de Paula/Mebel.",
     "sigevaBack · recuperar_password · import_ficha · CargarAprendices*.tsx"),
    ("Mebel", "UX informe + Swal", "HU-S2-032 + 031", "8",
     "Prototipo quién va ganando por jornada (3 bloques). SweetAlert al crear elección si no lo cerró.",
     "API de totales. Landing. Recuperar clave. Import.",
     "Figma informe-jornada  ·  form crear elección"),
    ("Lucero", "Historias de usuario", "HU-S2-040", "5",
     "Escribe HU-008 (recuperar clave) y HU-019 (informe por jornada) donde dice la hoja 10-LUCERO. Parcha jornada en 012/013/016/024.",
     "Código. Figma. Renumerar HU viejas. Inventar JWT o segunda vuelta.",
     "documentacion/_excel_senior_data_*.py  ·  entregables/sprint-1/04-Historias-de-Usuario.xlsx"),
]

TIPO_BG = {
    "Feliz": (OK_BG, OK_TX),
    "UX": (LIGHT_SENA, NAVY),
    "Validación": (RUN_BG, RUN_TX),
    "Excepción": (NO_BG, NO_TX),
    "Permiso": (NO_BG, NO_TX),
    "Seguridad": (NO_BG, NO_TX),
    "Fuera": (GRAY, MUTED),
}

PRIO_BG = {"Debe tener": (SENA, "000000"), "Debería tener": (GOLD, WHITE)}


def sheet_portada(wb):
    ws = wb.active
    ws.title = "01-SPRINT"
    page(ws)
    ws.sheet_properties.tabColor = SENA
    widths(ws, [28, 22, 18, 18, 18, 18, 22, 22])

    banner(
        ws, 8,
        "SIGEVA   ·   Sprint 2   ·   31 ago – 4 sep 2026",
        "Meta: landing (Sofia), recuperar clave (Alex+Maicol), import Excel sin jornada (Alex), "
        "informe por jornada (Mebel), urna móvil (Paula), criterios un-día (Adrii), HU faltantes (Lucero).",
    )

    n_hu = len(HISTORIAS)
    n_sp = sum(int(h["sp"]) if str(h["sp"]).isdigit() else 5 for h in HISTORIAS)
    kpis = [
        (1, 2, f"{n_hu}  HISTORIAS", "Carriles + lo ya construido.", GREEN, WHITE),
        (3, 4, f"{n_sp}  PUNTOS", "Varias Hecho (Alex, Maicol, Paula equipo).", GOLD, WHITE),
        (5, 6, "5  DÍAS", "Lun 31 ago → vie 4 sep.", NAVY, WHITE),
        (7, 8, "7  PERSONAS", "Entra Lucero. Adrii sigue en 029.", MUTED, WHITE),
    ]
    ws.row_dimensions[4].height = 36
    ws.row_dimensions[5].height = 20
    for c1, c2, title, sub, bg, fg in kpis:
        merge(ws, 4, c1, 4, c2)
        merge(ws, 5, c1, 5, c2)
        paint(ws.cell(4, c1), title, bg, font(14, True, fg), al(False, "center", "center"))
        paint(ws.cell(5, c1), sub, bg, font(9, False, fg), al(False, "center", "center"))
        for c in range(c1, c2 + 1):
            ws.cell(4, c).fill = fill(bg)
            ws.cell(4, c).border = THIN
            ws.cell(5, c).fill = fill(bg)
            ws.cell(5, c).border = THIN

    pares = [
        ("Producto", "SIGEVA — Sistema de Gestión Electoral y Validación de Votos"),
        ("Sprint", SPRINT["nombre"] + "  ·  " + SPRINT["fechas"]),
        ("Kickoff / Review", SPRINT["kickoff"] + "  ·  review " + SPRINT["review"]),
        ("Qué se hace", "Construir. El Sprint 1 fue especificar (RF/CU/HU). Este sprint toca código y prototipos."),
        ("Meta en una frase", SPRINT["meta"]),
        ("Quién acepta en review", "El equipo + Henry/Jorge si se convoca. Scrum Master: Alex"),
        ("Equipo", "Sofia, Maicol, Paula, Adrii Eraso, Alex, Mebel y Lucero (historias de usuario). Scrum Master: Alex"),
        ("Regla de producto que se suma", "Ya vige: una elección por centro (jornada en el candidato). Se suma RN-S2-001: no dos elecciones el mismo día (fecha_inicio) en el mismo centro."),
        ("Idioma / DoD", "Español. LISTO = criterios de la hoja 05-CRITERIOS en verde + Thunder/Network. Nadie toca OTP, voto ni acta."),
        ("Notion", "Sigue cobrando. Este Excel es el tablero del sprint."),
    ]
    r = 7
    for label, value in pares:
        paint(ws.cell(r, 1), label, LIGHT_SENA, font(10, True, NAVY))
        merge(ws, r, 2, r, 8)
        paint(ws.cell(r, 2), value, WHITE, font(10))
        for c in range(3, 9):
            ws.cell(r, c).border = THIN
            ws.cell(r, c).fill = fill(WHITE)
        ws.row_dimensions[r].height = 36
        r += 1

    r += 1
    merge(ws, r, 1, r, 8)
    paint(ws.cell(r, 1), "Compromiso (una fila = una persona = una historia)", GREEN, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 9):
        ws.cell(r, c).fill = fill(GREEN)
        ws.cell(r, c).border = THIN
    r += 1
    header_row(ws, r, ["Persona", "Historia", "Título", "SP", "Capa", "Rama", "Criterio LISTO (corto)", "No toca"])
    start = r
    for i, h in enumerate(HISTORIAS, r + 1):
        vals = [h["persona"], h["id"], h["titulo"], h["sp"], h["capa"], h["rama"], h["listo"], "; ".join(h["out_scope"][:2])]
        bg = WHITE if i % 2 else GRAY
        ws.row_dimensions[i].height = 52
        for c, v in enumerate(vals, 1):
            paint(ws.cell(i, c), v, bg, font(9, c in (1, 2), NAVY), al(True, "top", "left"))
        ws.cell(i, 4).alignment = al(False, "center", "center")
        last = i

    # datos para el gráfico (columna oculta a la derecha)
    chart_row = last + 2
    paint(ws.cell(chart_row, 1), "Carga por persona (puntos)", NAVY, font(11, True, WHITE), al(False, "center", "left"))
    merge(ws, chart_row, 1, chart_row, 3)
    for c in range(2, 4):
        ws.cell(chart_row, c).fill = fill(NAVY)
    header_row(ws, chart_row + 1, ["Persona", "SP", "Historia"], NAVY, WHITE)
    for i, h in enumerate(HISTORIAS):
        rr = chart_row + 2 + i
        paint(ws.cell(rr, 1), h["persona"], WHITE, font(10, True))
        paint(ws.cell(rr, 2), h["sp"], WHITE, font(10))
        paint(ws.cell(rr, 3), h["id"], WHITE, font(10))
        ws.cell(rr, 2).alignment = al(False, "center", "center")
    chart = BarChart()
    chart.type = "col"
    chart.title = "Puntos por persona"
    chart.y_axis.title = "SP"
    chart.style = 10
    data = Reference(ws, min_col=2, min_row=chart_row + 1, max_row=chart_row + 1 + len(HISTORIAS))
    cats = Reference(ws, min_col=1, min_row=chart_row + 2, max_row=chart_row + 1 + len(HISTORIAS))
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(cats)
    chart.shape = 4
    chart.legend = None
    chart.y_axis.scaling.min = 0
    chart.y_axis.scaling.max = 16
    chart.width = 15
    chart.height = 7
    ws.add_chart(chart, "E" + str(chart_row + 1))

    ws.freeze_panes = "A7"
    ws.sheet_view.zoomScale = 95


def sheet_kanban(wb):
    ws = wb.create_sheet("02-KANBAN")
    page(ws)
    ws.sheet_properties.tabColor = GOLD
    widths(ws, [2.4, 28, 28, 2.2, 28, 28, 2.2, 28, 28, 2.4])
    banner(
        ws, 10,
        "Kanban del Sprint 2   ·   siete personas   ·   Lucero documenta, Adrii no cambia de criterios",
        "Fila 1: Sofia landing · Maicol recuperar clave · Paula urna móvil. "
        "Fila 2: Adrii un-día (CA-029) · Alex Excel/API (Hecho) · Mebel informe por jornada. "
        "Fila 3: Lucero HU-008/019 · Maicol ojo login · Alex admin_sistema.",
    )

    colores = [
        "92D050", GOLD, "3B6FA0", RED, NAVY, "6B4C9A",
        "1F7A4D", "9A6B2F", "0E5C63", "5A6560", "39A900",
        "0B3D2E", "8B1E3F", "3B6FA0", "6B4C9A",
    ]
    fondos_titulo = [
        LIGHT_SENA, TODO_BG, "E8F0F8", NO_BG, LIGHT_GOLD, "F3E8FF",
        OK_BG, LIGHT_GOLD, "E8F0F8", GRAY, LIGHT_SENA,
        TODO_BG, NO_BG, "F3E8FF", LIGHT_GOLD,
    ]
    cols_lane = [2, 5, 8]

    def card(r, c1, title, body, bg, h=78):
        merge(ws, r, c1, r, c1 + 1)
        paint(ws.cell(r, c1), title + "\n" + body, bg, font(9, False, NAVY), al(True, "top", "left"))
        ws.cell(r, c1 + 1).fill = fill(bg)
        ws.cell(r, c1 + 1).border = THIN
        ws.row_dimensions[r].height = h

    def bloque(start_row, historias_idx):
        ws.row_dimensions[start_row].height = 26
        ws.row_dimensions[start_row + 1].height = 22
        for i, hi in enumerate(historias_idx):
            h = HISTORIAS[hi]
            c1 = cols_lane[i]
            color = colores[hi]
            merge(ws, start_row, c1, start_row, c1 + 1)
            paint(
                ws.cell(start_row, c1),
                f"{h['persona'].upper()}   ·   {h['id']}",
                color, font(11, True, WHITE), al(False, "center", "center"),
            )
            ws.cell(start_row, c1 + 1).fill = fill(color)
            ws.cell(start_row, c1 + 1).border = THIN
            merge(ws, start_row + 1, c1, start_row + 1, c1 + 1)
            paint(
                ws.cell(start_row + 1, c1),
                f"{h['capa']}   ·   {h['sp']} SP   ·   Por hacer",
                TODO_BG, font(9, True, NAVY), al(False, "center", "center"),
            )
            ws.cell(start_row + 1, c1 + 1).fill = fill(TODO_BG)
            ws.cell(start_row + 1, c1 + 1).border = THIN
            card(start_row + 2, c1, h["titulo"], h["historia"], fondos_titulo[hi], 88)
            card(start_row + 3, c1, "LISTO", h["listo"], WHITE, 88)
            card(start_row + 4, c1, "SÍ ENTRA", " · ".join(h["in_scope"][:3]), OK_BG, 80)
            card(start_row + 5, c1, "NO TOCA", " · ".join(h["out_scope"]), GRAY, 64)
            card(start_row + 6, c1, "RAMA / ENTREGA", h["rama"], WHITE, 40)

    bloque(4, [0, 8, 7])
    bloque(12, [3, 11, 6])
    bloque(20, [14, 9, 4])

    merge(ws, 28, 2, 28, 9)
    paint(
        ws.cell(28, 2),
        "Daily: cada quien su carril (30 s). Adrii SOLO implementa CA-029-* (no reescribe criterios). "
        "Lucero no pide API: escribe en entregables/sprint-1/04-Historias-de-Usuario.xlsx donde dice la hoja 10-LUCERO. "
        "Mebel prototipa el informe; no pica totales. Paula prototipa móvil; no mergea urna. "
        "Maicol no toca el back de recuperar. Alex ya entregó Excel + OTP de clave.",
        GRAY, font(9, False, MUTED), al(True, "center", "left"), NONE,
    )
    ws.row_dimensions[28].height = 44
    ws.sheet_view.zoomScale = 85


def sheet_tareas(wb):
    ws = wb.create_sheet("03-TAREAS")
    page(ws)
    ws.sheet_properties.tabColor = NAVY
    headers = ["ID", "HU", "Estado", "Persona", "Capa", "Tarea", "Qué se hace", "Criterio LISTO", "Fecha objetivo"]
    widths(ws, [12, 14, 14, 16, 16, 42, 62, 52, 16])
    banner(ws, 9, "Backlog filtrable del Sprint 2   ·   misma verdad que el Kanban",
           "Filtros: Estado · Persona · HU. El daily solo mueve la columna Estado (Por hacer / En curso / Hecho / Bloqueado).")
    header_row(ws, 3, headers)
    fechas = {
        "T-S2-01": "4-sep",
        "T-S2-02": "1-sep",
        "T-S2-03": "3-sep",
        "T-S2-04": "2-sep",
        "T-S2-05": "4-sep",
        "T-S2-06": "4-sep review",
        "T-S2-07": "2-sep",
        "T-S2-08": "4-sep",
        "T-S2-09": "4-sep",
        "T-S2-10": "31-ago",
        "T-S2-11": "2-sep",
        "T-S2-12": "31-ago",
        "T-S2-13": "31-ago",
        "T-S2-14": "31-ago",
        "T-S2-15": "31-ago",
        "T-S2-16": "3-sep",
        "T-S2-17": "2-sep",
    }
    estado_fill = {"Por hacer": (TODO_BG, TODO_TX), "En curso": (RUN_BG, RUN_TX), "Hecho": (OK_BG, OK_TX), "Bloqueado": (NO_BG, NO_TX)}
    for i, t in enumerate(TAREAS, 4):
        vals = [t["id"], t["hu"], t["estado"], t["persona"], t["capa"], t["titulo"], t["detalle"], t["listo"], fechas[t["id"]]]
        ws.row_dimensions[i].height = 68
        bg_e, fg_e = estado_fill[t["estado"]]
        for c, v in enumerate(vals, 1):
            if c == 3:
                paint(ws.cell(i, c), v, bg_e, font(9, True, fg_e), al(False, "center", "center"))
            else:
                paint(ws.cell(i, c), v, WHITE, font(9, c in (1, 6), NAVY), al(True, "top", "left"))
    last = 3 + len(TAREAS)
    add_table(ws, "TareasSprint2", f"A3:I{last}")
    dv = DataValidation(type="list", formula1='"Por hacer,En curso,Hecho,Bloqueado"', allow_blank=False)
    dv.error = "Use el desplegable"
    dv.errorTitle = "Estado"
    dv.prompt = "Mover en el daily"
    dv.promptTitle = "Estado"
    ws.add_data_validation(dv)
    dv.add(f"C4:C{last}")
    for col, ok_val in (("C", "Hecho"),):
        ws.conditional_formatting.add(
            f"{col}4:{col}{last}",
            CellIsRule(operator="equal", formula=['"Hecho"'], fill=fill(OK_BG), font=font(9, True, OK_TX)),
        )
        ws.conditional_formatting.add(
            f"{col}4:{col}{last}",
            CellIsRule(operator="equal", formula=['"En curso"'], fill=fill(RUN_BG), font=font(9, True, RUN_TX)),
        )
        ws.conditional_formatting.add(
            f"{col}4:{col}{last}",
            CellIsRule(operator="equal", formula=['"Bloqueado"'], fill=fill(NO_BG), font=font(9, True, NO_TX)),
        )
    note = last + 2
    merge(ws, note, 1, note, 9)
    paint(ws.cell(note, 1),
          "T-S2-06 es del equipo (review). No cuenta puntos extra: está dentro de HU-S2-026. "
          "T-S2-07 es Mebel (SweetAlert). Puede cerrar el martes sin esperar el 409: el Swal de éxito no depende de Adrii. "
          "Si Adrii termina el martes, Maicol ya puede haber mergeado el orden el lunes: no se pisan archivos si Adrii solo toca crear/actualizar y Maicol los GET.",
          GRAY, font(9, False, MUTED), al(True, "center", "left"), NONE)
    ws.row_dimensions[note].height = 28
    ws.freeze_panes = "A4"


def sheet_historias(wb):
    ws = wb.create_sheet("04-HISTORIAS")
    page(ws)
    ws.sheet_properties.tabColor = GREEN
    headers = [
        "ID", "RF", "CU", "Persona", "SP", "Prioridad", "Título",
        "Como / quiero / para", "Problema", "Valor", "Sí entra", "No entra", "LISTO", "Archivos / rama",
    ]
    widths(ws, [12, 12, 10, 14, 8, 14, 32, 40, 36, 32, 40, 36, 40, 36])
    banner(ws, 14, "Historias de usuario del Sprint 2   ·   carriles + lo construido esta semana",
           "Prioridad en español. HU-S2-026 a 040 (CU-26 a 40). Adrii: HU-S2-029 / CA-029-* no se reescriben. Lucero escribe HU-008 y HU-019 en el Excel del Sprint 1 (hoja 10-LUCERO).")
    header_row(ws, 3, headers)
    for i, h in enumerate(HISTORIAS, 4):
        pbg, pfg = PRIO_BG[h["prio"]]
        vals = [
            h["id"], h["rf"], h["cu"], h["persona"], h["sp"], h["prio"], h["titulo"],
            h["historia"], h["problema"], h["valor"],
            "\n".join(f"• {x}" for x in h["in_scope"]),
            "\n".join(f"• {x}" for x in h["out_scope"]),
            h["listo"], h["archivos"],
        ]
        ws.row_dimensions[i].height = 120
        for c, v in enumerate(vals, 1):
            if c == 6:
                paint(ws.cell(i, c), v, pbg, font(9, True, pfg), al(False, "center", "center"))
            else:
                paint(ws.cell(i, c), v, WHITE, font(9, c in (1, 7), NAVY), al(True, "top", "left"))
        ws.cell(i, 5).alignment = al(False, "center", "center")
    add_table(ws, "HistoriasSprint2", f"A3:N{3 + len(HISTORIAS)}")
    ws.freeze_panes = "E4"


def sheet_criterios(wb):
    ws = wb.create_sheet("05-CRITERIOS")
    page(ws)
    ws.sheet_properties.tabColor = RED
    headers = ["HU", "ID", "Tipo", "Persona", "Dado", "Cuando", "Entonces", "QA (sí/no)", "Evidencia"]
    widths(ws, [12, 12, 14, 14, 42, 42, 52, 12, 28])
    banner(
        ws, 9,
        "Criterios de aceptación   ·   contrato de LISTO   ·   Adrii: esta hoja ES tu trabajo de producto",
        "RN-S2-001 (CA-029-*): si creaste una elección del 27 de agosto en un centro, no puedes crear otra ese mismo día en ese centro. "
        "Otro centro el 27 sí. Editar la misma sí. Mover otra al 27 = 409. No se pisa solape de ventanas. "
        "Mebel (CA-031-*): el 201 y el 409 se ven en SweetAlert, nunca en el alert() del navegador.",
    )
    header_row(ws, 3, headers, RED, WHITE)
    for i, c in enumerate(CRITERIOS, 4):
        bg, fg = TIPO_BG.get(c["tipo"], (WHITE, NAVY))
        vals = [c["hu"], c["id"], c["tipo"], c["persona"], c["dado"], c["cuando"], c["entonces"], "", ""]
        ws.row_dimensions[i].height = 58
        for col, v in enumerate(vals, 1):
            if col == 3:
                paint(ws.cell(i, col), v, bg, font(9, True, fg), al(False, "center", "center"))
            else:
                paint(ws.cell(i, col), v, WHITE, font(9, col in (1, 2), NAVY), al(True, "top", "left"))
    last = 3 + len(CRITERIOS)
    add_table(ws, "CriteriosSprint2", f"A3:I{last}")
    dv = DataValidation(type="list", formula1='"sí,no,n/a"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H4:H{last}")
    note = last + 2
    merge(ws, note, 1, note, 9)
    paint(
        ws.cell(note, 1),
        "Cómo marcar LISTO: la columna QA se llena en el review o cuando Thunder/Network coincide. "
        "Adrii no cierra HU-S2-029 si CA-029-02 (segundo POST el mismo día) no está en sí. "
        "Alex no cierra HU-S2-030 si CA-030-03 (idcentro ajeno) no está en sí. "
        "Mebel no cierra HU-S2-031 si sigue existiendo un alert() nativo al crear. "
        "Paula marca CA-026-04 en sí cuando el equipo eligió y NO se mergeó CSS.",
        LIGHT_GOLD, font(9, False, GOLD), al(True, "center", "left"), NONE,
    )
    ws.row_dimensions[note].height = 36
    ws.freeze_panes = "E4"


def sheet_roles(wb):
    ws = wb.create_sheet("06-ROLES")
    page(ws)
    ws.sheet_properties.tabColor = "3B6FA0"
    widths(ws, [44, 22, 22, 28, 28])
    banner(
        ws, 5,
        "Matriz de roles   ·   acá se entiende admin_sistema   ·   Alex implementa las celdas, QA las tacha",
        "admin_sistema ≠ Administrador de red. admin_sistema ≠ Funcionario, aunque los dos viven en UN centro. "
        "Él administra y ve la información de SU centro (elecciones, aprendices, etc.). No ve la red.",
    )
    header_row(ws, 3, ["Capacidad", "Aprendiz", "Funcionario (mesa)", "admin_sistema (este sprint)", "Administrador (red)"], NAVY, WHITE)
    for i, row in enumerate(ROLES, 4):
        ws.row_dimensions[i].height = 28
        for c, v in enumerate(row, 1):
            cell_bg, cell_fg = WHITE, NAVY
            text = str(v)
            if c > 1:
                if text.startswith("Sí"):
                    cell_bg, cell_fg = OK_BG, OK_TX
                elif text.startswith("No") or text == "—":
                    cell_bg, cell_fg = NO_BG, NO_TX
                elif "409" in text:
                    cell_bg, cell_fg = RUN_BG, RUN_TX
            paint(ws.cell(i, c), v, cell_bg, font(9, c == 1 or text.startswith("Sí") or text.startswith("No"), cell_fg), al(True, "center" if c > 1 else "center", "left" if c == 1 else "center"))
    last = 3 + len(ROLES)
    add_table(ws, "RolesSprint2", f"A3:E{last}")

    r = last + 2
    merge(ws, r, 1, r, 5)
    paint(ws.cell(r, 1), "Definiciones que Alex deja por escrito en código (comentario + README de la rama)", NAVY, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 6):
        ws.cell(r, c).fill = fill(NAVY)
        ws.cell(r, c).border = THIN
    defs = [
        ("Aprendiz", "Vota en la urna de su centro y jornada. No administra. Puerta distinta (login urna)."),
        ("Funcionario", "Jurado digital de UNA mesa. Crea la elección, arma tarjetón, genera acta de SU centro. No ve otras sedes ni la torre nacional."),
        ("admin_sistema", "Administrador de UN centro de formación. Ve y administra elecciones, padrón de aprendices y lo operativo de SU sede. Centro obligatorio. No ve tablero de red, no importa eligiendo otra sede, no lista funcionarios de toda la red, no vota."),
        ("Administrador", "Gobierno de la red SENA (HU-020 a HU-025). Ve todas las sedes. No se recorta en este sprint."),
        ("Perfil en BD", "INSERT INTO perfil (perfil) VALUES ('admin_sistema'); El string es exacto: admin_sistema. El login ya devuelve perfil.perfil: el front ramifica con ese valor."),
        ("Fuente del centro", "Sesión (idcentro_formacion del usuario). Nunca el body. Igual que el funcionario en crear elección. Si el cliente manda otro id, se ignora o 403."),
    ]
    for i, (k, v) in enumerate(defs, r + 1):
        paint(ws.cell(i, 1), k, LIGHT_SENA, font(10, True, NAVY))
        merge(ws, i, 2, i, 5)
        paint(ws.cell(i, 2), v, WHITE, font(10))
        for c in range(3, 6):
            ws.cell(i, c).border = THIN
            ws.cell(i, c).fill = fill(WHITE)
        ws.row_dimensions[i].height = 36
    ws.freeze_panes = "B4"


def sheet_personas(wb):
    ws = wb.create_sheet("07-POR PERSONA")
    page(ws)
    ws.sheet_properties.tabColor = GOLD
    widths(ws, [16, 24, 14, 8, 48, 44, 44])
    banner(ws, 7, "Carriles   ·   corte de archivos   ·   nadie espera el merge del otro",
           "Alex y Adrii se parten eleccion_controller.ts: Adrii solo crear/actualizar (el guard del día). Maicol solo los GET (el orderBy). Mebel no abre ese archivo: ella pinta el Swal en el front.")
    header_row(ws, 3, ["Persona", "Rol esta semana", "HU", "SP", "Qué lleva al daily / review", "Qué NO abre", "Repo / rama"])
    for i, row in enumerate(PERSONAS, 4):
        ws.row_dimensions[i].height = 72
        for c, v in enumerate(row, 1):
            paint(ws.cell(i, c), v, WHITE, font(10, c == 1, NAVY), al(True, "top", "left"))
            if c == 4:
                ws.cell(i, c).alignment = al(False, "center", "center")
    add_table(ws, "PersonasSprint2", f"A3:G{3 + len(PERSONAS)}")
    r = 3 + len(PERSONAS) + 2
    merge(ws, r, 1, r, 7)
    paint(ws.cell(r, 1), "Dependencias (para no inventar bloqueos)", GREEN, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 8):
        ws.cell(r, c).fill = fill(GREEN)
        ws.cell(r, c).border = THIN
    deps = [
        "Paula no depende de nadie. Puede cerrar el jueves y solo aparece el viernes a presentar.",
        "Maicol no depende de Adrii. Ordenar GET no choca con el 409 del POST. Si hay datos viejos con dos elecciones el mismo día, ordena por ideleccion (CA-027-02).",
        "Adrii no depende de Maicol. Si mergean el mismo día, un rebase de 5 minutos: él no toca los query de listar.",
        "Sofia SÍ se alinea con Alex el miércoles: el combo de centro NO se muestra a admin_sistema ni a funcionario. El Administrador de red sí elige centro.",
        "Alex no espera la landing. El menú de admin_sistema es el de gestión de centro, no la home pública.",
        "Mebel no espera a Adrii para el Swal de éxito (CA-031-01). El Swal de error 409 (CA-031-03) sí espera el mensaje del back.",
        "Nadie reabre OTP, votoxcandidato, validacionVoto, generacion_reporte_controller.",
    ]
    for i, line in enumerate(deps, r + 1):
        merge(ws, i, 1, i, 7)
        paint(ws.cell(i, 1), line, WHITE if i % 2 == 0 else GRAY, font(10), al(True, "center", "left"))
        ws.row_dimensions[i].height = 22
    ws.freeze_panes = "A4"


def sheet_dod(wb):
    ws = wb.create_sheet("08-LISTO")
    page(ws, landscape=True)
    ws.sheet_properties.tabColor = GREEN
    widths(ws, [8, 36, 70, 40])
    banner(ws, 4, "Definition of Done del Sprint 2   ·   si falta una casilla, no está Hecho",
           "No se mergea a develop con criterios en blanco. El review del viernes es la demo, no el momento de descubrir el 409.")
    header_row(ws, 3, ["#", "Casilla", "Cómo se demuestra", "Quién la marca"])
    rows = [
        ("1", "Criterios de SU historia en 05-CRITERIOS = sí", "Thunder, Network o link Figma en Evidencia", "Dueño del carril"),
        ("2", "Adrii: CA-029-01 a 08 en sí (no criterios nuevos)", "Thunder del 409 el mismo día", "Adrii"),
        ("3", "Lucero: HU-008 y HU-019 en 04-Historias-de-Usuario.xlsx", "IDs 008 y 019 visibles. Jornada parchada en 012/013", "Lucero"),
        ("4", "Landing / con dos puertas", "CA-026 en sí", "Sofia"),
        ("5", "Recuperar clave: Network solicitar+confirmar", "CA-034 y CA-036", "Maicol + Alex"),
        ("6", "Import Excel Sofia Plus sin jornada", "CA-037", "Alex"),
        ("7", "Prototipo informe por jornada (3 bloques)", "CA-032. Cero PR de totales", "Mebel"),
        ("8", "Prototipo urna móvil 375 px", "CA-033", "Paula"),
        ("9", "Ojo de clave + error de login claro", "CA-035", "Maicol"),
        ("10", "Paquete elección global intacto", "jornada en candidato, urna ?jornada=, import sin jornada", "Alex en review"),
        ("11", "Nadie reabre OTP de VOTO / votoxcandidato", "Diff sin esos archivos (recuperar clave SÍ usa OTP propio)", "Alex (SM)"),
    ]
    for i, row in enumerate(rows, 4):
        ws.row_dimensions[i].height = 36
        bg = WHITE if i % 2 == 0 else GRAY
        for c, v in enumerate(row, 1):
            paint(ws.cell(i, c), v, GREEN if c == 1 else bg, font(10, c == 1, WHITE if c == 1 else NAVY), al(True, "center" if c == 1 else "top", "center" if c == 1 else "left"))
    r = 4 + len(rows) + 2
    merge(ws, r, 1, r, 4)
    paint(ws.cell(r, 1), "Fuera de este sprint (si sale en el daily, se anota y se pospone)", NAVY, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 5):
        ws.cell(r, c).fill = fill(NAVY)
        ws.cell(r, c).border = THIN
    fuera = [
        "Código del informe/acta partido por jornada (Mebel prototipa; Lucero escribe HU-019; implementar es después).",
        "App nativa. Paula solo prototipa la urna web a 375 px.",
        "Solape de ventanas en días distintos (27–29 vs 28–30).",
        "JWT, tabla organizacion, multi-tenant de plataforma.",
        "Que admin_sistema vote. Segunda vuelta / sorteo.",
        "OTP de votación, votoxcandidato, comprobante: no se reabren.",
    ]
    for i, line in enumerate(fuera, r + 1):
        merge(ws, i, 1, i, 4)
        paint(ws.cell(i, 1), "•  " + line, WHITE, font(10), al(True, "center", "left"))
        ws.row_dimensions[i].height = 20
    ws.freeze_panes = "A4"


def sheet_daily(wb):
    ws = wb.create_sheet("09-KICKOFF")
    page(ws)
    ws.sheet_properties.tabColor = SENA
    widths(ws, [4, 32, 90, 4])
    banner(ws, 4, "Guion de kickoff  ·  lunes 31 ago 2026  ·  8 minutos  ·  Scrum Master",
           "Se proyecta la hoja 02-KANBAN. Luego 06-ROLES si preguntan qué es admin_sistema. Los criterios de Adrii se leen en voz alta (el ejemplo del 27 de agosto).")
    bloques = [
        ("1. Meta de la semana (45 s)",
         "Sofia deja la landing presentable. Maicol conectó recuperar clave (front) y pone el ojo en el login. "
         "Paula prototipa la urna en celular (la página Equipo ya está). Mebel prototipa quién va ganando por jornada. "
         "Alex ya entregó el back de recuperar, el Excel de Sofia Plus y quitar jornada. "
         "Adrii implementa UNA elección por centro el mismo día — con los criterios que YA están en la hoja 05. "
         "Lucero escribe las HU que faltaban: recuperar clave (HU-008) e informe por jornada (HU-019)."),
        ("2. Adrii — los criterios no se reescriben (45 s)",
         "Si en el centro X ya hay una elección del 27 de agosto, no se puede crear otra ese mismo día en X. "
         "Otro centro el 27 sí. Cambiarle el nombre a la del 27 sí. Mover una del 28 al 27, no. "
         "Eso es CA-029-01 a 08. Adrii los implementa; no inventa otra regla ni otra hoja."),
        ("3. Lucero — dónde escribe (45 s)",
         "Hoja 10-LUCERO. Recuperar contraseña = HU-008 en el Excel de historias del Sprint 1 "
         "(entregables/sprint-1/04-Historias-de-Usuario.xlsx), épica Acceso. "
         "Informe por jornada = HU-019, justo después del acta HU-018. "
         "También parcha HU-012/013/016 porque todavía dicen que la elección pide jornada."),
        ("4. Carriles (60 s)",
         "Sofia: Inicio.tsx. Maicol: RecuperarContrasena + Login ojo. Paula: Figma 375 px aprendiz. "
         "Adrii: crear/actualizar elección 409. Alex: ya entregó; sigue admin_sistema si falta. "
         "Mebel: Figma informe 3 jornadas + Swal crear si no cerró. Lucero: _excel_senior_data_*.py. "
         "Nadie reabre OTP de VOTO ni votoxcandidato."),
        ("5. Qué ya está Hecho (30 s)",
         "Alex: API recuperar, import Excel, jornada fuera de elección/carga. "
         "Maicol: front recuperar. Paula: /equipo. El daily no los vuelve a repartir."),
        ("6. Qué no entra (15 s)",
         "Código del acta por jornada. App nativa. JWT. Solape de ventanas. Segunda vuelta."),
        ("Si preguntan “¿y el Sprint 1?”",
         "Sigue en entregables/sprint-1/. Este archivo es entregables/sprint-2/. "
         "Lucero mete 008 y 019 en el Excel del 1. No se renumeran 001–025. El Sprint 2 usa HU-S2-026 a 040."),
    ]
    r = 4
    for titulo, cuerpo in bloques:
        merge(ws, r, 2, r, 3)
        paint(ws.cell(r, 2), titulo, GREEN, font(11, True, WHITE), al(False, "center", "left"))
        ws.cell(r, 3).fill = fill(GREEN)
        ws.cell(r, 3).border = THIN
        ws.row_dimensions[r].height = 20
        r += 1
        merge(ws, r, 2, r, 3)
        paint(ws.cell(r, 2), cuerpo, WHITE, font(10), al(True, "top", "left"))
        ws.cell(r, 3).fill = fill(WHITE)
        ws.cell(r, 3).border = THIN
        ws.row_dimensions[r].height = 56
        r += 1
    ws.freeze_panes = "A4"


def sheet_como_leer(wb):
    ws = wb.create_sheet("00-COMO LEER", 0)
    page(ws, landscape=False)
    ws.sheet_properties.tabColor = MUTED
    widths(ws, [28, 72])
    banner(ws, 2, "Cómo leer este Excel   ·   Sprint 2 SIGEVA (actualizado 31 ago)",
           "Un archivo. La verdad del daily está en 03-TAREAS (columna Estado). Adrii: criterios en 05, no se inventan. Lucero: hoja 10-LUCERO.")
    filas = [
        ("00-COMO LEER", "Esta hoja."),
        ("01-SPRINT", "Portada: fechas, meta, puntos, gráfico, compromiso."),
        ("02-KANBAN", "7 personas. 3 filas × 3. Se proyecta en el daily."),
        ("03-TAREAS", "Tabla filtrable. Estado: Por hacer / En curso / Hecho / Bloqueado. Varias ya Hecho (Alex, Maicol recuperar, Paula equipo)."),
        ("04-HISTORIAS", "HU-S2-026 a 040. Las del Sprint 1 (001–025) NO se renumeran."),
        ("05-CRITERIOS", "Gherkin. Adrii = CA-029-* (ya escritos: los implementa). Lucero = CA-040-*."),
        ("06-ROLES", "Qué ve cada perfil. admin_sistema."),
        ("07-POR PERSONA", "Carril, qué no abre, repo."),
        ("08-LISTO", "DoD + huecos de documentación (para Lucero y el SM)."),
        ("09-KICKOFF", "Guion corto del lunes."),
        ("10-LUCERO", "DÓNDE escribir HU-008 recuperar clave y HU-019 informe por jornada. Archivos y IDs fijos."),
        ("IDs Sprint 2", "HU-S2-026…040 · T-S2-01…17. Huecos del Sprint 1 que Lucero usa: HU-008 y HU-019."),
        ("Repos", "Back: este repo. Front: sigevaFront. Contrato recuperar: para-companero/recuperar-password/."),
        ("Regenerar", "python documentacion/_generar_sprint2.py  →  sobreescribe el xlsx. Editar el .py, no el Excel a mano."),
    ]
    r = 4
    for k, v in filas:
        paint(ws.cell(r, 1), k, LIGHT_SENA, font(10, True, NAVY))
        paint(ws.cell(r, 2), v, WHITE, font(10))
        ws.row_dimensions[r].height = 32
        r += 1
    ws.freeze_panes = "A4"


def sheet_lucero(wb):
    ws = wb.create_sheet("10-LUCERO")
    page(ws)
    ws.sheet_properties.tabColor = "6B4C9A"
    widths(ws, [14, 18, 28, 52, 52])
    banner(
        ws, 5,
        "Lucero   ·   dónde va cada historia   ·   no inventes IDs   ·   no toques código",
        "El Excel de producto es entregables/sprint-1/04-Historias-de-Usuario.xlsx (se regenera desde documentacion/_excel_senior_data_*.py). "
        "Los huecos libres del Sprint 1 son HU-008 y HU-019. No renumeres 001–007 ni 010–018 ni 020–025.",
    )
    r = 4
    merge(ws, r, 1, r, 5)
    paint(ws.cell(r, 1), "A — Recuperar contraseña  →  HU-008 (NUEVA)", GREEN, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 6):
        ws.cell(r, c).fill = fill(GREEN)
        ws.cell(r, c).border = THIN
    r += 1
    header_row(ws, r, ["Qué", "ID a usar", "Archivo que editas", "Dónde / cómo", "Contrato de producto"], GREEN, WHITE)
    filas_a = [
        ("Nueva historia", "HU-008 · RF-NU-008 · CU-8",
         "documentacion/_excel_senior_data_aprendiz.py (al final, o un bloque 'acceso')",
         "Como aprendiz O gestor, quiero recuperar mi clave con el correo y un código de 6, para entrar de nuevo. UN solo flujo para Aprendiz, Funcionario, admin_sistema y Administrador. No pregunta el rol.",
         "API: POST /api/recuperar-password/solicitar {email} y POST .../confirmar {email, codigo, nueva_password}. Paquete: para-companero/recuperar-password/README.md"),
        ("Épica", "EP-SIG-001 Acceso",
         "documentacion/_excel_senior_data_epicas.py",
         "Quita «recuperar contraseña» de la lista fuera. Agrégalo al alcance y a historias: HU-001 · HU-008 · HU-010.",
         "Hoy el campo fuera dice explícitamente que recuperar NO tiene HU. Ese es el hueco."),
        ("Criterios mínimos", "CA-008-01…",
         "La misma entrada de HU-008, lista cp/ca",
         "Feliz: correo existe → 200 y mail. Feliz: código+clave≥8 → 200 y perfil. Excepción: 404 CUENTA_NO_ENCONTRADA. Excepción: 400 OTP_INVALIDO / OTP_EXPIRADO. Fuera: no login automático.",
         "Copia los JSON de para-companero/recuperar-password/json/"),
        ("No pongas esto", "—",
         "No crees HU-026 de producto (026 ya es del Sprint 2, landing)",
         "No hagas una HU de aprendiz y otra de funcionario: el back es el mismo.",
         "No documentes PUT /api/aprendiz/actualizar/contrasena: está en 410."),
    ]
    for i, row in enumerate(filas_a, r + 1):
        ws.row_dimensions[i].height = 72
        for c, v in enumerate(row, 1):
            paint(ws.cell(i, c), v, WHITE, font(9, c == 1, NAVY), al(True, "top", "left"))
    r = r + 1 + len(filas_a) + 1
    merge(ws, r, 1, r, 5)
    paint(ws.cell(r, 1), "B — Informe de candidatos por jornada (quién va ganando)  →  HU-019 (NUEVA)", GOLD, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 6):
        ws.cell(r, c).fill = fill(GOLD)
        ws.cell(r, c).border = THIN
    r += 1
    header_row(ws, r, ["Qué", "ID a usar", "Archivo que editas", "Dónde / cómo", "Contrato de producto"], GOLD, WHITE)
    filas_b = [
        ("Nueva historia", "HU-019 · RF-NU-019 · CU-19",
         "documentacion/_excel_senior_data_funcionario.py  DESPUÉS de HU-018 (acta)",
         "Como funcionario, quiero el informe de candidatos partido por Mañana / Tarde / Noche y ver quién va ganando en cada franja. NO fusionar con HU-018 (el acta global sigue).",
         "El corte es candidatos.jornada, no tres elecciones. Grafía con ñ. El aprendiz no lo ve (HU-007)."),
        ("Épica", "EP-SIG-004 Acta",
         "_excel_senior_data_epicas.py",
         "Alcance: HU-018 (acta global) + HU-019 (corte por jornada). Fuera: aprendiz ve totales, segunda vuelta.",
         "Mebel prototipa (HU-S2-032). Lucero escribe. El código del informe NO es de Lucero."),
        ("Criterios mínimos", "CA-019-01…",
         "En la HU-019",
         "Feliz: 3 bloques. Ceros incluidos. Un máximo = ganando; empate declarado. Fuera: no se implementa API en el mismo commit de la HU.",
         "Usa el prototipo de Mebel cuando exista. Si aún no, deja el Gherkin igual."),
        ("No pongas esto", "—",
         "No uses HU-S2-032 como ID de producto",
         "HU-S2-032 es la tarea de prototipo de ESTA semana. La historia de producto permanente es HU-019.",
         "No pidas jornada en la elección (eso ya se quitó)."),
    ]
    for i, row in enumerate(filas_b, r + 1):
        ws.row_dimensions[i].height = 72
        for c, v in enumerate(row, 1):
            paint(ws.cell(i, c), v, WHITE, font(9, c == 1, NAVY), al(True, "top", "left"))
    r = r + 1 + len(filas_b) + 1
    merge(ws, r, 1, r, 5)
    paint(ws.cell(r, 1), "C — Parches (historias VIEJAS que ya no coinciden con el código)", RED, font(11, True, WHITE), al(False, "center", "left"))
    for c in range(2, 6):
        ws.cell(r, c).fill = fill(RED)
        ws.cell(r, c).border = THIN
    r += 1
    header_row(ws, r, ["HU / épica", "Qué tiene hoy (mal)", "Qué debe decir", "Archivo", "Por qué"], RED, WHITE)
    filas_c = [
        ("HU-013 / HU-014 crear-editar elección",
         "La épica 002 dice «elección con jornada Mañana/Tarde/Noche».",
         "Una elección por centro, SIN jornada en la convocatoria. Jornada vive en el candidato y la elige el aprendiz al entrar.",
         "_excel_senior_data_funcionario.py · _excel_senior_data_epicas.py EP-SIG-002",
         "Paquete 26-27 ago + HU-S2-038 de Alex."),
        ("HU-012 y HU-024 import Excel",
         "«el código pide jornada». Plantilla genérica.",
         "Reporte de Aprendices Sofia Plus: C2 = ficha - programa, filas desde 5. Password = documento. NO se elige jornada en la carga. Informe insertados/actualizados/omitidos.",
         "_excel_senior_data_funcionario.py HU-012 · _excel_senior_data_admin.py HU-024",
         "Alex ya lo construyó (HU-S2-037)."),
        ("HU-016 candidato",
         "Puede no mencionar jornada del candidato.",
         "Select obligatorio Mañana|Tarde|Noche en el candidato. Unique tarjetón+jornada. Urna GET ?jornada=.",
         "_excel_senior_data_funcionario.py HU-016",
         "Ya era el paquete de Sofia/Maicol; el Excel de producto se quedó atrás."),
        ("EP-SIG-001 Acceso",
         "fuera: recuperar contraseña · no hay HU",
         "Alcance incluye HU-008. Fuera ya no lista recuperar.",
         "_excel_senior_data_epicas.py",
         "Maicol front + Alex back ya existen."),
        ("No hay HU de Equipo ni de landing ni de ojo de login",
         "Páginas / y /equipo y el ojo del password no están en el backlog de 22.",
         "Opcional este sprint: nota en épica de acceso o HU-009 (ojo login) si te alcanza. Landing = HU-S2-026 (sprint 2, no la muevas al 1).",
         "Si da tiempo: HU-009 «ver/ocultar clave y error de credenciales» ligado a Maicol HU-S2-035.",
         "Prioridad: primero 008 y 019. Luego los parches de jornada. Luego HU-009 si sobra el miércoles."),
    ]
    for i, row in enumerate(filas_c, r + 1):
        ws.row_dimensions[i].height = 64
        for c, v in enumerate(row, 1):
            paint(ws.cell(i, c), v, WHITE, font(9, c == 1, NAVY), al(True, "top", "left"))
    r = r + 1 + len(filas_c) + 1
    merge(ws, r, 1, r, 5)
    paint(
        ws.cell(r, 1),
        "Cómo entregar: 1) edita los .py de documentacion/_excel_senior_data_*.py  2) corre python documentacion/_generar_entregables.py  "
        "3) abre entregables/sprint-1/04-Historias-de-Usuario.xlsx y enseña HU-008 y HU-019 en el daily. "
        "No edites el xlsx a mano: se pisa al regenerar. Criterios de Adrii (CA-029) NO se tocan.",
        LIGHT_GOLD, font(9, False, GOLD), al(True, "center", "left"), NONE,
    )
    ws.row_dimensions[r].height = 48
    ws.freeze_panes = "A5"


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    sheet_portada(wb)
    sheet_como_leer(wb)
    sheet_kanban(wb)
    sheet_tareas(wb)
    sheet_historias(wb)
    sheet_criterios(wb)
    sheet_roles(wb)
    sheet_personas(wb)
    sheet_dod(wb)
    sheet_daily(wb)
    sheet_lucero(wb)
    order = [
        "00-COMO LEER", "01-SPRINT", "02-KANBAN", "03-TAREAS", "04-HISTORIAS",
        "05-CRITERIOS", "06-ROLES", "07-POR PERSONA", "08-LISTO", "09-KICKOFF", "10-LUCERO",
    ]
    for i, name in enumerate(order):
        wb.move_sheet(name, offset=i - wb.sheetnames.index(name))
    dest = OUT
    try:
        wb.save(dest)
    except PermissionError:
        dest = OUT.with_name(OUT.stem + "-actualizado.xlsx")
        wb.save(dest)
        print(f"AVISO el xlsx original esta abierto. Guarde y cierre. Este archivo: {dest}")
        return
    print(f"OK {dest}")


if __name__ == "__main__":
    build()
