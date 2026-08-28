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
        "Dejar el producto presentable y gobernable por centro: landing con 3 prototipos a elegir, "
        "listados de elección con lo más reciente arriba, padrón de aprendices filtrable, "
        "una sola elección por centro el mismo día, el rol admin_sistema aislado a su sede, "
        "y al crear una elección como funcionario un SweetAlert en vez del alert nativo."
    ),
}

HISTORIAS = [
    {
        "id": "HU-S2-026",
        "rf": "RF-NU-026",
        "cu": "CU-26",
        "sp": 5,
        "prio": "Debe tener",
        "persona": "Paula",
        "capa": "UX / Front",
        "rama": "sigevaFront · feat/landing-prototipos",
        "titulo": "Tres prototipos nuevos de landing page",
        "historia": (
            "Como visitante del SENA, quiero una landing clara y de confianza "
            "para entrar a votar o a gestionar, para no aterrizar en una pantalla que parece un contrato interno."
        ),
        "problema": "La landing actual se ve horrible: no parece un producto electoral institucional.",
        "valor": "El review del viernes elige UNA dirección. Sprint 3 implementa. Sin esto, SIGEVA no se puede mostrar.",
        "in_scope": [
            "Tres prototipos distintos (A institucional SENA, B urna/confianza, C centro de formación)",
            "Cada uno en escritorio 1440 px y móvil 375 px",
            "Dos puertas: Aprendiz (urna) y Gestión (funcionario / admin_sistema / administrador)",
            "Paleta e identidad SENA (verde 92D050, navy). Tipografía legible. CTA visibles",
            "Estados: visitante no logueado. No se pide voto en la landing",
            "Presentación de 10 min el viernes con recomendación de cuál llevar a código",
        ],
        "out_scope": [
            "Implementar la ganadora en producción (eso es Sprint 3)",
            "Rediseñar urna, OTP, acta o formularios de elección",
            "Copiar el HomePage de sigeva-front (ese React es contrato de agente, no la web pública)",
        ],
        "listo": (
            "Hay 3 archivos o links (Figma / HTML) con desktop + móvil. El equipo marca uno como ganador en el review. "
            "Nadie mergea CSS a develop este sprint."
        ),
        "archivos": "prototipos en entregables/sprint-2/landing/ o Figma. No toca app/ ni urna.",
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
]

TAREAS = [
    {"id": "T-S2-01", "hu": "HU-S2-026", "persona": "Paula", "capa": "UX", "estado": "Por hacer",
     "titulo": "Brief y 3 direcciones de landing",
     "detalle": "A = institucional SENA (hero, dos puertas). B = urna/confianza (voto seguro, sin totales). C = centro de formación (sede, convocatoria). Cada una desktop 1440 y móvil 375.",
     "listo": "3 prototipos entregados. El viernes el equipo elige 1. No hay PR de CSS a develop."},
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
    {"id": "T-S2-06", "hu": "HU-S2-026", "persona": "Equipo", "capa": "Review", "estado": "Por hacer",
     "titulo": "Review viernes: elegir prototipo ganador",
     "detalle": "10 min Paula. Voto del equipo. Se anota en esta hoja el ganador (A, B o C). Implementación = Sprint 3.",
     "listo": "Acta de 3 líneas: ganador + por qué + qué no se copia de los perdedores."},
    {"id": "T-S2-07", "hu": "HU-S2-031", "persona": "Mebel", "capa": "Front UX", "estado": "Por hacer",
     "titulo": "SweetAlert al crear elección (funcionario)",
     "detalle": "Quitar window.alert del éxito del POST crear. Swal.fire success: «Elección creada» / «La elección se registró con éxito.» Botón Entendido, verde SENA. El 409 de Adrii también va en Swal error, no en alert nativo.",
     "listo": "Crear como funcionario = Swal bonito. Cero alert() en esa pantalla. El JSON del back no se cambia."},
]

CRITERIOS = [
    # Paula
    {"hu": "HU-S2-026", "id": "CA-026-01", "tipo": "Feliz", "persona": "Paula",
     "dado": "un visitante abre la landing (no logueado)",
     "cuando": "mira cualquiera de los 3 prototipos",
     "entonces": "entiende en menos de 5 segundos qué es SIGEVA y ve dos CTA: votar (urna) y gestionar (mesa/admin)"},
    {"hu": "HU-S2-026", "id": "CA-026-02", "tipo": "UX", "persona": "Paula",
     "dado": "los 3 prototipos",
     "cuando": "se comparan lado a lado",
     "entonces": "son direcciones distintas (no el mismo layout con otro color). A institucional, B urna/confianza, C centro"},
    {"hu": "HU-S2-026", "id": "CA-026-03", "tipo": "UX", "persona": "Paula",
     "dado": "cada prototipo",
     "cuando": "se abre en 1440 px y en 375 px",
     "entonces": "CTA visibles, sin texto cortado, sin scroll horizontal"},
    {"hu": "HU-S2-026", "id": "CA-026-04", "tipo": "Fuera", "persona": "Paula",
     "dado": "el review del viernes",
     "cuando": "se elige un ganador",
     "entonces": "NO se mergea a develop este sprint. Queda acta para Sprint 3"},
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
]

ROLES = [
    ("Entrar a la urna y votar", "Sí", "No", "No", "No"),
    ("Entrar a gestión (misma puerta HU-010)", "No", "Sí", "Sí", "Sí"),
    ("Centro obligatorio en el usuario", "El del censo", "Sí", "Sí", "No (opera la red)"),
    ("Ver elecciones de SU centro", "Solo urna filtrada", "Sí", "Sí", "Sí"),
    ("Ver elecciones de OTRO centro", "No", "No", "No", "Sí"),
    ("Crear / editar elección de SU centro", "No", "Sí", "Sí", "No en este sprint (P10)"),
    ("Crear segunda elección el mismo día", "—", "409 (Adrii)", "409 (Adrii)", "—"),
    ("Aviso al crear elección con éxito", "—", "SweetAlert (Mebel)", "Mismo Swal si crea", "—"),
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
    ("Paula", "UX / Front landing", "HU-S2-026", "5",
     "3 prototipos (A/B/C) desktop+móvil. Presenta el viernes.",
     "Código de urna, OTP, form de elección, CSS a develop.",
     "sigevaFront · feat/landing-prototipos  ·  entregables/sprint-2/landing/"),
    ("Maicol", "Back listados elección", "HU-S2-027", "2",
     "orderBy fecha_inicio DESC en todos los GET de elección. Thunder [reciente → vieja].",
     "La regla de un día (eso es Adrii). Filtros de aprendices. Candidatos.",
     "sigevaBack · feat/elecciones-orden-reciente"),
    ("Sofia", "Front + GET padrón", "HU-S2-028", "5",
     "Barra de filtros: centro, celular, documento, email, nombre, estado. API combinable.",
     "Form de candidato / urna (cerrado en sprint anterior). Elección un-día.",
     "sigevaFront · feat/filtros-aprendices  ·  aprendizs_controller.ts"),
    ("Adrii Eraso", "Back regla de elección", "HU-S2-029", "5",
     "Guard 409 en crear y actualizar. Mensaje en español. 5 disparos Thunder de CRITERIOS.",
     "Orden del listado (Maicol). OTP, voto, acta, candidatos. Solape de ventanas.",
     "sigevaBack · feat/eleccion-un-dia  ·  eleccion_controller.ts arriba (crear/actualizar)"),
    ("Alex", "SM + rol admin_sistema", "HU-S2-030", "8",
     "Perfil, login, gates por centro, 403 a red, menú, usuario demo. Facilita el review.",
     "JWT, tabla organizacion, que el admin vote, implementar la landing ganadora.",
     "sigevaBack · feat/rol-admin-sistema"),
    ("Mebel", "Front UX crear elección", "HU-S2-031", "3",
     "SweetAlert2 en el 201 del funcionario. Cero alert() nativo. El 409 de Adrii también en Swal error.",
     "GET de elección (Maicol). Guard del día (Adrii). Campos del form. Landing de Paula. OTP/urna.",
     "sigevaFront · feat/swal-eleccion-creada"),
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
        "Meta: landing presentable (3 prototipos), listados con lo reciente arriba, padrón filtrable, "
        "una elección por centro el mismo día, rol admin_sistema aislado a su sede, SweetAlert al crear.",
    )

    kpis = [
        (1, 2, "6  HISTORIAS", "Una por persona con carril.", GREEN, WHITE),
        (3, 4, "28  PUNTOS", "5+2+5+5+8+3. Cabe en 5 días.", GOLD, WHITE),
        (5, 6, "5  DÍAS", "Lun 31 ago → vie 4 sep.", NAVY, WHITE),
        (7, 8, "0  EN CURSO", "Arranca todo en Por hacer.", MUTED, WHITE),
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
        ("Equipo", "Paula, Maicol, Sofia, Adrii Eraso, Alex y Mebel. Seis carriles."),
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
    chart.y_axis.scaling.max = 10
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
        "Kanban del Sprint 2   ·   seis carriles   ·   nadie espera el merge del otro",
        "Arranca todo en POR HACER. En el daily se mueve la tarjeta (cambia el estado en 03-TAREAS). "
        "Fila de arriba: Paula · Maicol · Sofia. Fila de abajo: Adrii · Alex · Mebel.",
    )

    colores = ["92D050", GOLD, "3B6FA0", RED, NAVY, "6B4C9A"]
    fondos_titulo = [LIGHT_SENA, TODO_BG, "E8F0F8", NO_BG, LIGHT_GOLD, "F3E8FF"]
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

    bloque(4, [0, 1, 2])
    bloque(12, [3, 4, 5])

    merge(ws, 20, 2, 20, 9)
    paint(
        ws.cell(20, 2),
        "Cómo usarlo en el daily: cada quien dice SU carril (30 s). Si está bloqueado, se pinta la tarjeta de 03-TAREAS como En curso. "
        "Paula no espera API. Maicol no espera a Adrii. Mebel no espera a Adrii para el Swal de éxito (el 409 sí, cuando el back exista). "
        "Sofia coordina el combo de centro con Alex. Adrii solo toca crear/actualizar. Alex no reabre OTP. Mebel no toca GET ni el guard del día.",
        GRAY, font(9, False, MUTED), al(True, "center", "left"), NONE,
    )
    ws.row_dimensions[20].height = 40
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
        "T-S2-01": "4-sep (review)",
        "T-S2-02": "1-sep",
        "T-S2-03": "3-sep",
        "T-S2-04": "2-sep",
        "T-S2-05": "4-sep",
        "T-S2-06": "4-sep review",
        "T-S2-07": "2-sep",
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
    banner(ws, 14, "Historias de usuario del Sprint 2   ·   una por carril",
           "Prioridad en español. Una historia = un RF = un CU (CU-26 a CU-30). Los criterios Gherkin van en la hoja 05.")
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
        ("1", "Criterios de SU historia en 05-CRITERIOS = sí", "Thunder o Network pegado en Evidencia, o link Figma para Paula", "Dueño del carril"),
        ("2", "Rama feat/… publicada, PR abierto a develop", "URL del PR. Un carril = un PR. No se mezclan landing + rol + 409", "Dueño"),
        ("3", "No se rompió el paquete elección global del 26-27 ago", "Sigue: una elección por centro, jornada en el candidato, urna ?jornada=", "Alex en review"),
        ("4", "JSON de aprendices sin password/hash", "Inspección del body", "Sofia + Alex"),
        ("5", "admin_sistema no ve centro B", "CA-030-03 en sí", "Alex"),
        ("6", "Segundo POST el mismo día = 409, no 500", "CA-029-02 en sí. El form muestra el texto en español", "Adrii"),
        ("7", "GET elecciones [reciente → vieja]", "CA-027-01 en sí", "Maicol"),
        ("8", "3 prototipos vistos en review y ganador anotado", "CA-026-04. No hay commit de CSS a develop", "Paula + equipo"),
        ("9", "Crear elección = SweetAlert, cero alert() nativo", "CA-031-01 y CA-031-04 en sí", "Mebel"),
        ("10", "Nadie abrió OTP / voto / acta", "Diff del PR sin esos archivos", "Alex (SM)"),
        ("11", "SQL local documentado si hay INSERT de perfil", "Una línea en el PR de Alex: el INSERT de admin_sistema. Cada PC lo corre", "Alex"),
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
        "Implementar en producción el prototipo ganador de landing (Sprint 3).",
        "Solape de ventanas en días distintos (27–29 vs 28–30).",
        "Acta / ganador partido por jornada. OTP, voto, comprobante. Import Excel.",
        "JWT, tabla organizacion, multi-tenant de plataforma.",
        "Que admin_sistema vote o impersonar una mesa desde el Administrador de red.",
        "Fotos de equipo, picker de jornada, unique de tarjetón: ya se cerró o no es de esta semana.",
        "SweetAlert en urna, OTP, voto, acta o login: Mebel solo toca el crear elección del funcionario.",
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
         "No es otro sprint de papeles. Se construye. Al viernes: Paula trajo 3 landings y el equipo eligió una; "
         "Maicol dejó lo reciente arriba; Sofia filtró el padrón por centro y teléfono; Adrii impide dos elecciones el mismo día; "
         "Alex dejó vivo el rol admin_sistema, que solo ve su centro; Mebel cambió el alert nativo de crear elección por un SweetAlert."),
        ("2. Regla nueva de producto (45 s) — para Adrii, en voz alta",
         "Si en el centro X ya hay una elección del 27 de agosto, no se puede crear otra ese mismo día en X. "
         "Otro centro el 27 sí. Cambiarle el nombre a la del 27 sí. Mover una del 28 al 27, no. "
         "El día es fecha_inicio en hora Colombia, no el momento en que alguien pulsó Guardar. "
         "No estamos prohibiendo que se solapen ventanas de varios días: eso no entra."),
        ("3. Qué es admin_sistema (45 s) — para el equipo",
         "No es el Administrador de la red. Es el administrador de UN centro de formación: ve elecciones y aprendices de su sede y nada más. "
         "El funcionario sigue operando la mesa. El Administrador de red sigue viendo todo. El aprendiz sigue sin administrar."),
        ("4. Carriles y archivos (60 s)",
         "Paula: prototipos, cero código a develop. "
         "Maicol: GET de elección, orderBy. "
         "Sofia: pantalla aprendices + query celular/centro. "
         "Adrii: crear y actualizar elección (el 409). "
         "Alex: perfil + gates. "
         "Mebel: SweetAlert al crear (funcionario). Cero alert() nativo. "
         "Nadie abre OTP, voto, acta."),
        ("5. Qué pedimos cada día (30 s)",
         "Lunes Maicol puede cerrar. Martes Adrii y Mebel (éxito Swal). Miércoles Sofia se alinea con Alex en el combo de centro. "
         "Jueves Alex deja el usuario demo. Viernes Paula presenta y se vota el prototipo."),
        ("6. Qué no entra (15 s)",
         "Landing a producción. JWT. organizacion. Solape de ventanas. Import Excel. Segunda vuelta. Fotos del equipo."),
        ("Si preguntan “¿y el Sprint 1?”",
         "Sigue en entregables/sprint-1/. Este paquete es entregables/sprint-2/. Las HU nuevas son HU-S2-026 a 031 (CU-26 a 31). No se renumeran las 001–025."),
        ("Si preguntan “¿Paula implementa la web?”",
         "No esta semana. Tres prototipos y el equipo elige. Implementar es Sprint 3. Si mergea CSS ahora, se revierte."),
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
    banner(ws, 2, "Cómo leer este Excel   ·   Sprint 2 SIGEVA",
           "Un archivo. Nueve hojas. La verdad del daily está en 03-TAREAS (columna Estado). Los criterios no se improvisan: están en 05.")
    filas = [
        ("00-COMO LEER", "Esta hoja."),
        ("01-SPRINT", "Portada: fechas, meta, 28 puntos, gráfico, compromiso."),
        ("02-KANBAN", "Seis carriles (2 filas × 3). Se proyecta en el daily."),
        ("03-TAREAS", "Tabla filtrable. Ahí se mueve Por hacer → En curso → Hecho. Desplegable en Estado."),
        ("04-HISTORIAS", "Las seis HU (026–031) con sí entra / no entra / LISTO."),
        ("05-CRITERIOS", "Gherkin. Contrato de QA. Adrii vive en CA-029-*. Mebel en CA-031-*. Columna QA se tacha sí/no."),
        ("06-ROLES", "Qué ve cada perfil. Definición de admin_sistema. Alex implementa esta matriz."),
        ("07-POR PERSONA", "Corte de archivos y dependencias reales (no inventadas)."),
        ("08-LISTO", "DoD del sprint + lo que queda fuera."),
        ("09-KICKOFF", "Guion de 8 minutos para el lunes 31."),
        ("IDs", "HU-S2-026…031 · RF-NU-026…031 · CU-26…31 · T-S2-01…07. No se pisan las HU-001 a 025 del Sprint 1."),
        ("RN-S2-001", "Un centro + un día de fecha_inicio = una elección. Zona America/Bogota."),
        ("Repos", "Back: este repo. Front de producción: sigevaFront (Paula landing, Sofia padrón, Mebel Swal). sigeva-front/ es contrato de agente, no la landing pública."),
        ("Regenerar", "python documentacion/_generar_sprint2.py  →  sobreescribe este xlsx. No editar a mano las historias; editar el .py."),
    ]
    r = 4
    for k, v in filas:
        paint(ws.cell(r, 1), k, LIGHT_SENA, font(10, True, NAVY))
        paint(ws.cell(r, 2), v, WHITE, font(10))
        ws.row_dimensions[r].height = 32
        r += 1
    ws.freeze_panes = "A4"


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
    # orden de pestañas
    order = [
        "00-COMO LEER", "01-SPRINT", "02-KANBAN", "03-TAREAS", "04-HISTORIAS",
        "05-CRITERIOS", "06-ROLES", "07-POR PERSONA", "08-LISTO", "09-KICKOFF",
    ]
    for i, name in enumerate(order):
        wb.move_sheet(name, offset=i - wb.sheetnames.index(name))
    wb.save(OUT)
    print(f"OK {OUT}")


if __name__ == "__main__":
    build()
