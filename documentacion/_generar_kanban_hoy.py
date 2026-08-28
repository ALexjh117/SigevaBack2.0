# -*- coding: utf-8 -*-
"""Kanban del 26 ago 2026 — para el daily / sprint del 27."""
from __future__ import annotations

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table, TableStyleInfo
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "entregables" / "SIGEVA-Kanban-26-ago-2026.xlsx"

NAVY = "1B3A4B"
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
LIGHT_GOLD = "F8F1E3"
CARD_LINE = "D0D5DD"

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


def page(ws, landscape=True):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.paperSize = ws.PAPERSIZE_TABLOID
    ws.page_margins = PageMargins(left=0.45, right=0.45, top=0.55, bottom=0.45, header=0.22, footer=0.22)
    ws.sheet_view.showGridLines = False
    ws.oddHeader.left.text = "SIGEVA  ·  Kanban 26 ago 2026"
    ws.oddHeader.right.text = "&A"
    ws.oddFooter.left.text = "Daily / sprint 27 ago 2026  ·  uso interno"
    ws.oddFooter.right.text = "Pág. &P de &N"


# estado: Hecho | En curso | Por hacer
# cola: Backlog del daily (lo que se muestra) vs Siguiente tanda
TAREAS = [
    # —— HECHO hoy ——
    {
        "id": "T-01",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Back",
        "titulo": "Elección global: crear y editar sin jornada",
        "detalle": "POST /api/eleccion/crear y PUT /api/eleccionActualizar/:id ya no piden ni validan jornada. La columna queda null. Si el body trae jornada de más, se ignora.",
        "listo": "Thunder: 201 sin jornada. Ya no sale 400 “La jornada no es válida”.",
        "evidencia": "PR #1 mergeado · commit 9dd1da8 10:41 · rama feat/eleccion-sin-jornada",
        "hu": "HU-013 / HU-014",
    },
    {
        "id": "T-02",
        "estado": "Hecho",
        "persona": "Mebel",
        "capa": "Back",
        "titulo": "GET elecciones por centro: una convocatoria, no tres",
        "detalle": "traerPorCentroFormacion deja de pintar jornada de la elección (o va null). FiltroJorElCen deja de filtrar por grupo.jornada del aprendiz.",
        "listo": "GET por centro = una fila. El JSON de la elección no trae jornada de convocatoria.",
        "evidencia": "PR #2 mergeado · commit 8174bf7 10:59 · rama feat/eleccion-listados",
        "hu": "HU-015",
    },
    {
        "id": "T-03",
        "estado": "Hecho",
        "persona": "Alex (carril Maicol)",
        "capa": "Back",
        "titulo": "Jornada en el candidato + tarjetón único por franja",
        "detalle": "candidatos.jornada (Mañana | Tarde | Noche). Vine enum. Unique (elección, tarjetón, jornada): un 01 en cada franja. GET /api/candidatos/listar/:id?jornada=Tarde.",
        "listo": "Tres POST mismo 01, una jornada cada uno = 201. GET sin query = 3. GET ?jornada=Tarde = 1.",
        "evidencia": "commit 80926dc 11:42 “flujo jornada terminado” · develop",
        "hu": "HU-016",
    },
    {
        "id": "T-04",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Docs",
        "titulo": "Guía de código con fotos Thunder / Network y LISTO por persona",
        "detalle": "Word por carril (Alex, Maicol, Mebel, Paula, Sofia): archivo, qué borrar, JSON exacto, foto de éxito. SQL único para las cinco PCs. Flujo de éxito de 6 pasos al final.",
        "listo": "Cada quien salta a SU sección y marca el recuadro verde cuando Thunder/Network coincide con la foto.",
        "evidencia": "documentacion/SIGEVA-Guia-Codigo-Eleccion-Global.docx · commit f084dac",
        "hu": "—",
    },
    {
        "id": "T-05",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Docs",
        "titulo": "Plan de trabajo elección global (instructivo del daily de ayer)",
        "detalle": "Regla de producto, corte de archivos (Alex arriba / Mebel abajo del mismo controller), qué nadie toca (OTP, voto, acta).",
        "listo": "El equipo tiene un solo documento de “dónde ir”.",
        "evidencia": "documentacion/SIGEVA-Plan-Trabajo-Eleccion-Global.docx",
        "hu": "—",
    },
    {
        "id": "T-06",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Front / Docs",
        "titulo": "Brief Paula y Sofia (ramas, URLs, JSON, LISTO)",
        "detalle": "Paula: feat/form-eleccion-global — form y listado sin jornada. Sofia: feat/tarjeton-jornada — select jornada en candidato + urna ?jornada=. No se inventan URLs. Grafía Mañana | Tarde | Noche.",
        "listo": "El agente / la persona abre AGENTS.md y trabaja solo su carpeta.",
        "evidencia": "sigeva-front/AGENTS.md + guía Word (fotos Network)",
        "hu": "HU-013 a HU-016 · HU-002/003",
    },
    {
        "id": "T-07",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Docs",
        "titulo": "Entregables Sprint 1 versionados (RF, CU, HU, backlog)",
        "detalle": "01-Sprint, 02-Requerimientos, 03-Casos-de-Uso (plantilla SENA), 04-Historias, 05-Backlog. El Sprint 1 era especificar; ayer ya se tocó código encima.",
        "listo": "Carpeta entregables/sprint-1/ en el repo.",
        "evidencia": "commit 9dd1da8 (bloque documentación)",
        "hu": "EP-SIG-000",
    },
    {
        "id": "T-08",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Docs",
        "titulo": "Modelo multi-tenant para el PO (análisis, no código de urna)",
        "detalle": "Una base, columna de dueño. SENA = primer tenant. Word para PO, MD, DBML (dbdiagram), SQL Lucid, drawio.",
        "listo": "El PO puede ver el ERD. No se ejecutó DDL de organizacion en este paquete.",
        "evidencia": "documentacion/modelo-datos-multitenant.md · SIGEVA-Modelo-Multitenant-para-PO.docx",
        "hu": "análisis",
    },
    {
        "id": "T-09",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Front prod",
        "titulo": "Picker de jornada del aprendiz (una vez; queda guardada)",
        "detalle": "Al entrar elige Mañana / Tarde / Noche. Se guarda por id del aprendiz en el navegador. La próxima vez no se vuelve a preguntar. Paquete que el plan dejaba “para después”: se adelantó ayer en sigevaFront.",
        "listo": "Primera visita = modal. Segunda visita = entra directo a la elección del centro.",
        "evidencia": "sigevaFront · constants/jornada.ts · utils/jornadaAprendiz.ts · auth",
        "hu": "fuera del plan original · HU-002",
    },
    {
        "id": "T-10",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Front prod",
        "titulo": "Urna: solo candidatos de la jornada + vacío claro",
        "detalle": "GET /api/candidatos/listar/:id?jornada=Tarde. Si no hay de esa franja: “No hay candidatos para tu jornada”. La card de la elección ya no pinta “Jornada: Mañana” (la convocatoria es global).",
        "listo": "Aprendiz de Tarde no ve el bloque Mañana. Sin candidatos ≠ error mudo.",
        "evidencia": "sigevaFront · SeleccionarCandidatoPage · VotacionCard",
        "hu": "HU-003",
    },
    {
        "id": "T-11",
        "estado": "Hecho",
        "persona": "Alex",
        "capa": "Front prod",
        "titulo": "Página Equipo / Sobre nosotros (esta versión + crédito primera)",
        "detalle": "Bloque actual: Alex (Scrum Master / full stack), Mebel, Paula, Maicol, Sofia. Bloque de quienes armó la primera versión. Lightbox en fotos de esta versión, fondo negro, responsive.",
        "listo": "Ruta /equipo. Click en foto de esta versión abre grande. Avatares de la primera no se agrandan.",
        "evidencia": "sigevaFront · Equipo.tsx",
        "hu": "—",
    },
    # —— EN CURSO (el daily los mueve) ——
    {
        "id": "T-12",
        "estado": "En curso",
        "persona": "Paula",
        "capa": "Front prod",
        "titulo": "Form y listado de elección sin jornada",
        "detalle": "Quitar el select de jornada en crear/editar. POST/PUT sin jornada. idcentro_formacion de la sesión, no combo de sedes. Listado: una card, campo titulo, no pintar jornada.",
        "listo": "Network crear = 201 y JSON sin jornada. Editar = 200. Form sin combo. Una card por convocatoria.",
        "evidencia": "rama feat/form-eleccion-global · FormEleccion.tsx · EleccionesActivasPage.tsx",
        "hu": "HU-013 / HU-014 / HU-015",
    },
    {
        "id": "T-13",
        "estado": "En curso",
        "persona": "Sofia",
        "capa": "Front prod",
        "titulo": "Jornada en el form de candidato + tarjetón filtrado",
        "detalle": "Select required Mañana | Tarde | Noche en form-data del POST /api/candidatos/crear. Gestión: GET sin query, tres bloques. Urna: ?jornada= de la sesión, una elección del centro.",
        "listo": "Network del POST trae jornada. Gestión 3 bloques. Urna solo esa franja. No toca el form de elección.",
        "evidencia": "rama feat/tarjeton-jornada · AgregarCandidatoModal · GestionCandidatos · SeleccionarCandidatoPage",
        "hu": "HU-016 / HU-003",
    },
    {
        "id": "T-14",
        "estado": "En curso",
        "persona": "Todos",
        "capa": "Dev",
        "titulo": "SQL local en cada PostgreSQL (nadie espera el merge de la base)",
        "detalle": "ALTER elecciones.jornada DROP NOT NULL. ADD COLUMN candidatos.jornada. Índice único (ideleccion, numero_tarjeton, jornada). El texto está en la guía. Cada PC lo corre.",
        "listo": "El create de Alex no truena. El POST de Sofia tiene dónde escribir jornada.",
        "evidencia": "Guía · sección TODOS · foto sql-todos.png",
        "hu": "—",
    },
    {
        "id": "T-15",
        "estado": "En curso",
        "persona": "Equipo",
        "capa": "Front prod",
        "titulo": "Fotos de Maicol, Mebel, Paula y Sofia en Equipo",
        "detalle": "Hoy salen con inicial. Meter jpg en public/avatars. Solo se agrandan las de esta versión.",
        "listo": "Las cinco caras de esta versión tienen foto.",
        "evidencia": "sigevaFront/public/avatars/",
        "hu": "—",
    },
    {
        "id": "T-16",
        "estado": "En curso",
        "persona": "Maicol",
        "capa": "Back",
        "titulo": "Maicol toma el carril candidatos (ya está en develop)",
        "detalle": "Alex cerró el código ayer para no bloquear el daily. Maicol revisa modelo, Vine, unique y GET ?jornada=, abre su rama si hace falta y confirma el LISTO de Thunder.",
        "listo": "Tres 01, una jornada cada uno. GET sin query = 3. GET ?jornada=Tarde = 1. Si el segundo 01 falla, es el unique, no el form de Sofia.",
        "evidencia": "commit 80926dc · guía sección Maicol",
        "hu": "HU-016",
    },
    # —— POR HACER (sprint / siguiente) ——
    {
        "id": "T-17",
        "estado": "Por hacer",
        "persona": "Los cinco",
        "capa": "QA",
        "titulo": "Flujo de éxito juntos (15 min, nadie vota)",
        "detalle": "1) Entran a Elecciones. 2) Crean UNA para todo el centro. 3) Una card. 4) Tres candidatos (Mañana/Tarde/Noche), tarjetón 01. 5) Aprendiz de Tarde entra a la urna. 6) Solo ve Tarde = éxito.",
        "listo": "Paso 6 verde. Si se rompe: crear → Alex/Paula; listado → Mebel; tarjetón → Maicol/Sofia.",
        "evidencia": "Guía · flujo-exito.png · sección 10 del plan",
        "hu": "paquete elección global",
    },
    {
        "id": "T-18",
        "estado": "Por hacer",
        "persona": "Siguiente tanda",
        "capa": "Back",
        "titulo": "Acta / ganador partido por jornada",
        "detalle": "Con una elección global, un solo máximo mezclaría Mañana, Tarde y Noche. El PDF no se reescribe en este paquete. Quedó dicho para no pelearlo después.",
        "listo": "Fuera de este sprint. No abrir generacion_reporte_controller.",
        "evidencia": "Plan §2 y §9",
        "hu": "HU-018",
    },
    {
        "id": "T-19",
        "estado": "Por hacer",
        "persona": "Siguiente tanda",
        "capa": "Back / Front",
        "titulo": "OTP, voto y comprobante (URLs no se renombran)",
        "detalle": "validarVoto sigue siendo un aprendiz, una elección, un voto. OTP no sabe de jornada. No se toca en el daily de mañana.",
        "listo": "Fuera. Nadie abre votoxcandidato ni validacionVoto.",
        "evidencia": "Plan §9 · AGENTS.md “lo que nadie hace”",
        "hu": "HU-004 a HU-007",
    },
    {
        "id": "T-20",
        "estado": "Por hacer",
        "persona": "Siguiente tanda",
        "capa": "Back",
        "titulo": "Import Excel del padrón y jornada fiable en el grupo",
        "detalle": "El funcionario pone la jornada al inscribir al candidato porque el padrón aún no es fuente fiable. Import y grupo_controller no entran mañana.",
        "listo": "Fuera.",
        "evidencia": "Plan §5 y §9",
        "hu": "HU-012 / HU-024",
    },
    {
        "id": "T-21",
        "estado": "Por hacer",
        "persona": "Siguiente tanda",
        "capa": "Back",
        "titulo": "DDL multi-tenant (organizacion) — no se ejecuta aún",
        "detalle": "El análisis está. Una base, un esquema, dueño en las filas electorales. Este sprint no crea la tabla ni renombra aprendiz.",
        "listo": "Fuera. El aislamiento que sí corre hoy es por centro_formacion.",
        "evidencia": "modelo-multitenant.sql (propuesto) · Word PO",
        "hu": "análisis",
    },
]


def n_estado(nombre):
    return sum(1 for t in TAREAS if t["estado"] == nombre)


def sheet_kanban(wb):
    ws = wb.active
    ws.title = "KANBAN"
    page(ws)
    ws.sheet_properties.tabColor = SENA
    widths(ws, [3.2, 28, 28, 28, 2.2, 28, 28, 28, 2.2, 28, 28, 28, 3.2])

    # franja
    for c in range(1, 14):
        paint(ws.cell(1, c), "", NAVY, font(11, True, WHITE), al(False, "center", "center"), NONE)
    merge(ws, 1, 1, 1, 13)
    paint(
        ws.cell(1, 1),
        "SIGEVA   ·   Kanban del 26 de agosto de 2026   ·   para el daily / sprint del 27",
        NAVY,
        font(16, True, WHITE),
        al(False, "center", "center"),
        NONE,
    )
    ws.row_dimensions[1].height = 32

    for c in range(1, 14):
        paint(ws.cell(2, c), "", "0F2A36", font(10, False, WHITE), al(True, "center", "center"), NONE)
    merge(ws, 2, 1, 2, 13)
    paint(
        ws.cell(2, 1),
        "Regla de producto: una elección por centro. La jornada vive en el candidato (Mañana | Tarde | Noche). "
        "El aprendiz ve solo su franja. Notion cobró: este Excel es el tablero.",
        "0F2A36",
        font(10, False, WHITE),
        al(True, "center", "center"),
        NONE,
    )
    ws.row_dimensions[2].height = 22

    # KPIs
    kpis = [
        (2, 4, f"{n_estado('Hecho')}  HECHO", "Cerrado ayer. Se muestra al backlog.", GREEN, WHITE),
        (6, 8, f"{n_estado('En curso')}  EN CURSO", "Se mueve en el daily de mañana.", GOLD, WHITE),
        (10, 12, f"{n_estado('Por hacer')}  POR HACER", "Cierre del paquete + siguiente tanda.", NAVY, WHITE),
    ]
    ws.row_dimensions[3].height = 8
    ws.row_dimensions[4].height = 36
    ws.row_dimensions[5].height = 18
    for c1, c2, title, sub, bg, fg in kpis:
        merge(ws, 4, c1, 4, c2)
        paint(ws.cell(4, c1), title, bg, font(14, True, fg), al(False, "center", "center"))
        merge(ws, 5, c1, 5, c2)
        paint(ws.cell(5, c1), sub, bg, font(9, False, fg), al(False, "center", "center"))
        for c in range(c1, c2 + 1):
            ws.cell(4, c).fill = fill(bg)
            ws.cell(4, c).border = THIN
            ws.cell(5, c).fill = fill(bg)
            ws.cell(5, c).border = THIN

    ws.row_dimensions[6].height = 10

    cols = [
        ("Por hacer", 2, TODO_BG, NAVY, [t for t in TAREAS if t["estado"] == "Por hacer"]),
        ("En curso", 6, RUN_BG, RUN_TX, [t for t in TAREAS if t["estado"] == "En curso"]),
        ("Hecho", 10, OK_BG, OK_TX, [t for t in TAREAS if t["estado"] == "Hecho"]),
    ]

    header_row = 7
    ws.row_dimensions[header_row].height = 26
    header_color = {"Por hacer": NAVY, "En curso": GOLD, "Hecho": GREEN}
    for nombre, c1, bg, fg, _items in cols:
        hc = header_color[nombre]
        merge(ws, header_row, c1, header_row, c1 + 2)
        paint(
            ws.cell(header_row, c1),
            nombre.upper(),
            hc,
            font(12, True, WHITE),
            al(False, "center", "center"),
        )
        for c in range(c1 + 1, c1 + 3):
            ws.cell(header_row, c).fill = fill(hc)
            ws.cell(header_row, c).border = THIN

    max_cards = max(len(c[4]) for c in cols)
    start = 8
    card_h = 78

    for i in range(max_cards):
        r = start + i
        ws.row_dimensions[r].height = card_h
        for nombre, c1, bg, fg, items in cols:
            merge(ws, r, c1, r, c1 + 2)
            if i < len(items):
                t = items[i]
                text = (
                    f"{t['id']}   ·   {t['capa']}\n"
                    f"{t['titulo']}\n"
                    f"{t['persona']}\n"
                    f"{t['evidencia']}"
                )
                if nombre == "Hecho":
                    card_bg, card_fg, title_fg = OK_BG, MUTED, OK_TX
                elif nombre == "En curso":
                    card_bg, card_fg, title_fg = RUN_BG, MUTED, RUN_TX
                else:
                    card_bg, card_fg, title_fg = TODO_BG, MUTED, NAVY
                paint(ws.cell(r, c1), text, card_bg, font(9, False, card_fg), al(True, "top", "left"))
                ws.cell(r, c1).font = font(10, True, title_fg)
                # keep wrap; title emphasis is the first lines via the string itself
                ws.cell(r, c1).font = font(9, False, NAVY)
                for c in range(c1, c1 + 3):
                    ws.cell(r, c).fill = fill(card_bg)
                    ws.cell(r, c).border = THIN
            else:
                paint(ws.cell(r, c1), "", GRAY, font(), al(), NONE)
                for c in range(c1, c1 + 3):
                    ws.cell(r, c).fill = fill("F7F8FA")
                    ws.cell(r, c).border = NONE

    # nota pie
    foot = start + max_cards + 1
    merge(ws, foot, 2, foot, 12)
    paint(
        ws.cell(foot, 2),
        "Cómo presentarlo: 1) la regla de producto (franja de arriba). 2) columna HECHO = lo que el back ya mergeó + docs + adelanto de urna/equipo. "
        "3) EN CURSO = Paula, Sofia, SQL local, Maicol confirma candidatos, fotos. 4) POR HACER = humo de 15 min juntos; acta/OTP/import/multi-tenant no se reparte mañana.",
        GRAY,
        font(9, False, MUTED),
        al(True, "center", "left"),
        NONE,
    )
    ws.row_dimensions[foot].height = 36
    ws.freeze_panes = "A8"
    ws.print_title_rows = "1:7"
    ws.sheet_view.zoomScale = 90


def sheet_tabla(wb):
    ws = wb.create_sheet("TABLA")
    page(ws)
    ws.sheet_properties.tabColor = NAVY
    headers = [
        "ID",
        "Estado",
        "Persona",
        "Capa",
        "Tarea",
        "Qué se hizo / qué falta",
        "Criterio LISTO",
        "Evidencia",
        "HU / CU",
        "Fecha",
    ]
    widths(ws, [8, 14, 20, 14, 42, 58, 46, 48, 22, 14])

    for c in range(1, 11):
        paint(ws.cell(1, c), "", NAVY, font(12, True, WHITE), al(False, "center", "center"), NONE)
    merge(ws, 1, 1, 1, 10)
    paint(
        ws.cell(1, 1),
        "Backlog filtrable  ·  mismas tarjetas del Kanban  ·  26 ago 2026",
        NAVY,
        font(14, True, WHITE),
        al(False, "center", "left"),
        NONE,
    )
    ws.row_dimensions[1].height = 28

    for i, h in enumerate(headers, 1):
        paint(ws.cell(2, i), h, GREEN, font(10, True, WHITE), al(False, "center", "center"))
    ws.row_dimensions[2].height = 22

    estado_fill = {
        "Hecho": (OK_BG, OK_TX),
        "En curso": (RUN_BG, RUN_TX),
        "Por hacer": (TODO_BG, TODO_TX),
    }

    for i, t in enumerate(TAREAS, 3):
        bg, fg = estado_fill[t["estado"]]
        vals = [
            t["id"],
            t["estado"],
            t["persona"],
            t["capa"],
            t["titulo"],
            t["detalle"],
            t["listo"],
            t["evidencia"],
            t["hu"],
            "26-ago-2026" if t["estado"] == "Hecho" else "27-ago-2026",
        ]
        ws.row_dimensions[i].height = 64
        for c, v in enumerate(vals, 1):
            cell_bg = bg if c == 2 else WHITE
            cell_fg = fg if c == 2 else NAVY
            bold = c in (1, 2, 5)
            paint(ws.cell(i, c), v, cell_bg, font(9, bold, cell_fg), al(True, "top", "left"))
            if c == 2:
                ws.cell(i, c).alignment = al(False, "center", "center")
                ws.cell(i, c).font = font(9, True, fg)

    last = 2 + len(TAREAS)
    tab = Table(displayName="KanbanHoy", ref=f"A2:J{last}")
    tab.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False)
    ws.add_table(tab)
    ws.freeze_panes = "A3"

    # data bars / note
    note = last + 2
    merge(ws, note, 1, note, 10)
    paint(
        ws.cell(note, 1),
        "Filtros: Estado (Hecho / En curso / Por hacer)  ·  Persona  ·  Capa. "
        "Esto es lo que se proyecta si piden “el backlog en tabla”. El Kanban es la hoja 1.",
        GRAY,
        font(9, False, MUTED),
        al(True, "center", "left"),
        NONE,
    )
    ws.row_dimensions[note].height = 22


def sheet_hoy(wb):
    ws = wb.create_sheet("PARA DECIR EN EL DAILY")
    page(ws, landscape=True)
    ws.sheet_properties.tabColor = GOLD
    widths(ws, [4, 28, 88, 4])

    for c in range(1, 5):
        paint(ws.cell(1, c), "", NAVY, font(14, True, WHITE), al(False, "center", "center"), NONE)
    merge(ws, 1, 1, 1, 4)
    paint(
        ws.cell(1, 1),
        "Guion de 3 minutos  ·  Scrum Master  ·  27 ago 2026",
        NAVY,
        font(16, True, WHITE),
        al(False, "center", "left"),
        NONE,
    )
    ws.row_dimensions[1].height = 30

    bloques = [
        (
            "1. Qué cambió de producto (30 s)",
            "Antes el funcionario armaba tres elecciones (Mañana, Tarde, Noche) para el mismo centro y el mismo cargo. "
            "Ayer cortamos eso: una elección por centro. La jornada se marca en cada candidato. "
            "El aprendiz, al votar, solo ve su franja. Mañana, tarde y noche corren en la misma urna.",
        ),
        (
            "2. Qué cerró el back (45 s)",
            "Alex: POST y PUT de elección ya no piden jornada (PR #1, merge a develop). "
            "Mebel: GET por centro devuelve una convocatoria, sin jornada de la elección (PR #2). "
            "Jornada en candidatos + unique por (elección, tarjetón, jornada) + GET ?jornada=Tarde: código en develop "
            "(commit “flujo jornada terminado”). Maicol confirma Thunder en el daily: tres 01, una jornada cada uno.",
        ),
        (
            "3. Qué adelantó el front (45 s)",
            "Paula y Sofia tienen brief (AGENTS.md + fotos Network en el Word): ella form/listado de elección, ella candidato y urna. "
            "Eso sigue EN CURSO — no se asignaron las dos personas al mismo PR. "
            "Alex adelantó en sigevaFront: el aprendiz elige jornada una vez y queda guardada; la urna filtra candidatos; "
            "si no hay de su franja, el mensaje es claro; la card de la elección ya no dice “Jornada: Mañana”. "
            "También quedó la página Equipo (esta versión + crédito a la primera).",
        ),
        (
            "4. Qué pedimos hoy (30 s)",
            "Paula marca LISTO de form/listado (Network 201/200 sin jornada, una card). "
            "Sofia marca LISTO de form candidato + tres bloques + urna ?jornada=. "
            "Cada PC corre el SQL de la guía. "
            "Los cinco: 15 minutos de humo (flujo de éxito). Nadie vota. Nadie genera acta.",
        ),
        (
            "5. Qué no entra (15 s)",
            "Acta / ganador por jornada. OTP y voto. Import Excel. Picker no se vuelve a diseñar: ya está adelantado. "
            "No se renombran URLs. No se crea la tabla organizacion. Multi-tenant queda en análisis.",
        ),
        (
            "Si preguntan “¿y Maicol?”",
            "El carril era suyo. Para no frenar el daily, el código de candidatos quedó ayer en develop. "
            "Hoy él valida el LISTO de Thunder y se queda de dueño de esos archivos. Sofia no espera otro merge para pintar el select.",
        ),
        (
            "Si preguntan “¿y el Sprint 1 de papeles?”",
            "Sigue en entregables/sprint-1/ (RF, CU, HU, backlog). Ayer no se tiró: se versionó y encima se tocó el código del paquete elección global.",
        ),
    ]

    r = 3
    for titulo, cuerpo in bloques:
        merge(ws, r, 2, r, 3)
        paint(ws.cell(r, 2), titulo, GREEN, font(11, True, WHITE), al(False, "center", "left"))
        ws.cell(r, 3).fill = fill(GREEN)
        ws.cell(r, 3).border = THIN
        ws.row_dimensions[r].height = 20
        r += 1
        merge(ws, r, 2, r, 3)
        paint(ws.cell(r, 2), cuerpo, WHITE, font(10, False, NAVY), al(True, "top", "left"))
        ws.cell(r, 3).fill = fill(WHITE)
        ws.cell(r, 3).border = THIN
        ws.row_dimensions[r].height = 52
        r += 1

    merge(ws, r, 2, r, 3)
    paint(
        ws.cell(r, 2),
        "Commits de ayer (sigevaBack): 9dd1da8 elecciones sin jornada  ·  8174bf7 traer elecciones por centro (Mebel)  ·  "
        "80926dc flujo jornada terminado  ·  f084dac documents global. PRs #1 y #2 mergeados a develop.",
        LIGHT_GOLD,
        font(9, False, GOLD),
        al(True, "center", "left"),
        NONE,
    )
    ws.row_dimensions[r].height = 32
    ws.freeze_panes = "A3"


def sheet_demo(wb):
    ws = wb.create_sheet("FLUJO DE EXITO")
    page(ws)
    ws.sheet_properties.tabColor = GREEN
    widths(ws, [6, 38, 22, 42, 42, 4])

    for c in range(1, 7):
        paint(ws.cell(1, c), "", NAVY, font(14, True, WHITE), al(False, "center", "center"), NONE)
    merge(ws, 1, 1, 1, 6)
    paint(
        ws.cell(1, 1),
        "Humo de 15 minutos  ·  los cinco  ·  si el paso 6 cierra, el paquete sirvió",
        NAVY,
        font(16, True, WHITE),
        al(False, "center", "left"),
        NONE,
    )
    ws.row_dimensions[1].height = 30

    headers = ["Paso", "Qué hacer", "Quién dispara", "Si se rompe, de quién es", "Se ve así cuando está bien"]
    for i, h in enumerate(headers, 1):
        paint(ws.cell(3, i), h, GREEN, font(10, True, WHITE), al(False, "center", "center"))
    ws.row_dimensions[3].height = 22

    pasos = [
        ("1", "Entran a Elecciones (gestión).", "Paula", "Login / menú del funcionario.", "Pantalla de listado del centro."),
        ("2", "Crean UNA elección para todo el centro. Sin jornada.", "Paula + Alex", "Alex (POST) o Paula (el form todavía manda jornada).", "201. Body sin jornada. eleccion.jornada = null."),
        ("3", "El listado muestra una sola card. No pinta jornada.", "Paula + Mebel", "Mebel (GET aún manda jornada) o Paula (la pinta).", "Una convocatoria. Campo titulo."),
        ("4", "Tres candidatos, tarjetón 01, una jornada cada uno.", "Sofia + Maicol", "Maicol si el segundo 01 truena (unique). Sofia si el FormData no lleva jornada.", "201 × 3. GET sin query = 3."),
        ("5", "Aprendiz de Tarde entra a la urna (jornada ya elegida o guardada).", "Sofia / Alex", "Picker o sesión sin jornada.", "Ve la elección del centro, no tres menús."),
        ("6", "El tarjetón pide ?jornada=Tarde y solo muestra ese bloque.", "Sofia", "Sofia no mandó query, o Mebel no filtró candidatos.jornada.", "Un bloque. Si no hay: “No hay candidatos para tu jornada”."),
    ]
    for i, row in enumerate(pasos, 4):
        ws.row_dimensions[i].height = 48
        bg = WHITE if i % 2 == 0 else GRAY
        for c, v in enumerate(row, 1):
            paint(ws.cell(i, c), v, GREEN if c == 1 else bg, font(10, c == 1, WHITE if c == 1 else NAVY), al(True, "center" if c == 1 else "top", "center" if c == 1 else "left"))

    merge(ws, 11, 1, 11, 5)
    paint(
        ws.cell(11, 1),
        "Nadie vota. Nadie genera acta. OTP no se abre. Si el paso 6 está verde, mañana se puede decir “el paquete elección global cerró”.",
        OK_BG,
        font(10, True, OK_TX),
        al(True, "center", "left"),
    )
    ws.row_dimensions[11].height = 28

    merge(ws, 13, 1, 13, 5)
    paint(ws.cell(13, 1), "Lo que nadie hace en este humo (para que no se desvíe el daily)", NAVY, font(11, True, WHITE), al(False, "center", "left"))
    ws.cell(13, 2).fill = fill(NAVY)
    ws.row_dimensions[13].height = 20

    fuera = [
        "Picker de jornada: ya está adelantado; no se rediseña en la reunión.",
        "Acta / ganador por jornada: siguiente tanda (un solo máximo mezclaría las tres franjas).",
        "OTP, voto, comprobante: mismas URLs, no se tocan.",
        "Import Excel / grupo: el funcionario pone la jornada al inscribir.",
        "Renombrar /api/eleccion/crear, /api/eleccionActualizar/:id, /api/candidatos/crear, /api/candidatos/listar/:id.",
    ]
    for i, line in enumerate(fuera, 14):
        merge(ws, i, 1, i, 5)
        paint(ws.cell(i, 1), line, WHITE, font(10, False, NAVY), al(True, "center", "left"))
        ws.row_dimensions[i].height = 20


def sheet_equipo(wb):
    ws = wb.create_sheet("POR PERSONA")
    page(ws)
    ws.sheet_properties.tabColor = "1B3A4B"
    widths(ws, [16, 14, 16, 48, 48, 22])

    for c in range(1, 7):
        paint(ws.cell(1, c), "", NAVY, font(14, True, WHITE), al(False, "center", "center"), NONE)
    merge(ws, 1, 1, 1, 6)
    paint(
        ws.cell(1, 1),
        "Carriles  ·  nadie espera el merge del otro  ·  26 → 27 ago",
        NAVY,
        font(16, True, WHITE),
        al(False, "center", "left"),
        NONE,
    )
    ws.row_dimensions[1].height = 30

    headers = ["Persona", "Rol ayer", "Estado", "Qué cerró / qué tiene", "Qué lleva al daily", "Repo / rama"]
    for i, h in enumerate(headers, 1):
        paint(ws.cell(3, i), h, GREEN, font(10, True, WHITE), al(False, "center", "center"))
    ws.row_dimensions[3].height = 22

    filas = [
        (
            "Alex",
            "Back + SM",
            "Hecho + adelanto",
            "POST/PUT sin jornada. Código de candidatos en develop. Guía, plan, brief. Urna (picker + filtro). Página Equipo.",
            "Facilita el humo. No reabre OTP/acta. Si Maicol confirma Thunder, el carril candidatos queda de él.",
            "sigevaBack · feat/eleccion-sin-jornada\nsigevaFront",
        ),
        (
            "Mebel",
            "Back listados",
            "Hecho",
            "GET por centro. Filtro sin grupo.jornada. PR #2 mergeado.",
            "En el humo: el listado es una card. Si aún sale jornada en el JSON, recortar.",
            "sigevaBack · feat/eleccion-listados",
        ),
        (
            "Maicol",
            "Back candidatos",
            "En curso",
            "El código del carril ya está (Alex, 11:42). Falta su LISTO de Thunder y dueño de los archivos.",
            "Tres POST 01. GET sin query = 3. GET ?jornada=Tarde = 1.",
            "sigevaBack · feat/candidatos-jornada (o develop)",
        ),
        (
            "Paula",
            "Front elección",
            "En curso",
            "Brief listo. Form/listado de producción aún es su LISTO: sin select, una card, Network 201/200.",
            "No toca candidatos ni urna. idcentro de la sesión.",
            "sigevaFront · feat/form-eleccion-global",
        ),
        (
            "Sofia",
            "Front tarjetón",
            "En curso",
            "Brief listo. Select jornada en form-data. Tres bloques en gestión. Urna con ?jornada=.",
            "No toca el form de crear elección. Si el segundo 01 falla, es unique de Maicol.",
            "sigevaFront · feat/tarjeton-jornada",
        ),
    ]
    estado_bg = {
        "Hecho": (OK_BG, OK_TX),
        "En curso": (RUN_BG, RUN_TX),
        "Hecho + adelanto": (OK_BG, OK_TX),
    }
    for i, row in enumerate(filas, 4):
        ws.row_dimensions[i].height = 72
        bg_e, fg_e = estado_bg[row[2]]
        for c, v in enumerate(row, 1):
            if c == 3:
                paint(ws.cell(i, c), v, bg_e, font(10, True, fg_e), al(True, "center", "center"))
            else:
                paint(ws.cell(i, c), v, WHITE, font(10, c == 1, NAVY), al(True, "top", "left"))

    merge(ws, 10, 1, 10, 6)
    paint(
        ws.cell(10, 1),
        "Corte de archivos: Alex y Mebel se parten eleccion_controller.ts por método (él crear/actualizar, ella GET). "
        "Maicol es dueño de modelo / validator / service / controller de candidatos. Paula carpeta eleccion. Sofia carpeta candidatos + urna. "
        "types.ts, client.ts, jornada.ts y layouts no se reescriben.",
        GRAY,
        font(9, False, MUTED),
        al(True, "center", "left"),
        NONE,
    )
    ws.row_dimensions[10].height = 40


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    sheet_kanban(wb)
    sheet_tabla(wb)
    sheet_hoy(wb)
    sheet_demo(wb)
    sheet_equipo(wb)
    wb.save(OUT)
    print(f"OK {OUT}")


if __name__ == "__main__":
    build()
