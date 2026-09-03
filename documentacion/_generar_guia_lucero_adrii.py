# -*- coding: utf-8 -*-
"""Word para Lucero y Adrii: cada cuadro de la historia, listo para copiar y pegar."""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "entregables" / "sprint-2" / "PARA-LUCERO-Y-ADRII-Historias-copiar-pegar.docx"

NAVY = RGBColor(0x1B, 0x3A, 0x4B)
GREEN = RGBColor(0x1F, 0x7A, 0x4D)
SENA = RGBColor(0x00, 0x73, 0x32)
MUTED = RGBColor(0x4A, 0x55, 0x63)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0x92, 0x40, 0x0E)
PURPLE = RGBColor(0x5B, 0x3A, 0x8C)

NAVY_HEX = "1B3A4B"
GREEN_HEX = "1F7A4D"
SENA_HEX = "92D050"
ROW_HEX = "F2F4F7"
SOFT_GREEN = "E8F5EE"
SOFT_AMBER = "FEF3C7"
SOFT_NAVY = "E8EEF2"
SOFT_PURPLE = "F3EEF9"
SOFT_RED = "FDECEC"
LABEL_HEX = "1B3A4B"


def set_run(run, size=11, bold=False, color=BLACK, italic=False):
    run.font.name = "Arial"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    r_pr = run._element.get_or_add_rPr()
    r_fonts = r_pr.find(qn("w:rFonts"))
    if r_fonts is None:
        r_fonts = OxmlElement("w:rFonts")
        r_pr.append(r_fonts)
    for key in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        r_fonts.set(qn(key), "Arial")


def shade(cell, hex_color):
    tc_pr = cell._tc.get_or_add_tcPr()
    for old in tc_pr.findall(qn("w:shd")):
        tc_pr.remove(old)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), hex_color)
    shd.set(qn("w:val"), "clear")
    tc_pr.append(shd)


def set_cell_margins(cell, **sides):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement("w:tcMar")
    for side, cm in sides.items():
        node = OxmlElement(f"w:{side}")
        node.set(qn("w:w"), str(int(cm * 567)))
        node.set(qn("w:type"), "dxa")
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def cell_text(cell, text, *, bold=False, color=BLACK, size=10, fill=None, align="left"):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.line_spacing = 1.08
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run(run, size=size, bold=bold, color=color)
    if fill:
        shade(cell, fill)
    set_cell_margins(cell, top=0.08, bottom=0.08, left=0.12, right=0.12)


def add_p(doc, text, *, size=11, bold=False, color=BLACK, space_after=8, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    set_run(run, size=size, bold=bold, color=color, italic=italic)
    return p


def add_h(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    size = {1: 16, 2: 13, 3: 12}.get(level, 12)
    color = {1: NAVY, 2: GREEN, 3: PURPLE}.get(level, NAVY)
    for run in p.runs:
        set_run(run, size=size, bold=True, color=color)
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(6)
    return p


def banner(doc, title, subtitle, fill=NAVY_HEX):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    shade(cell, fill)
    set_cell_margins(cell, top=0.28, bottom=0.28, left=0.35, right=0.35)
    cell.text = ""
    p1 = cell.paragraphs[0]
    r1 = p1.add_run(title)
    set_run(r1, size=16, bold=True, color=WHITE)
    p2 = cell.add_paragraph()
    r2 = p2.add_run(subtitle)
    set_run(r2, size=10, color=WHITE)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def callout(doc, title, body, fill=SOFT_AMBER, title_color=AMBER):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    shade(cell, fill)
    set_cell_margins(cell, top=0.18, bottom=0.18, left=0.28, right=0.28)
    cell.text = ""
    p1 = cell.paragraphs[0]
    r1 = p1.add_run(title)
    set_run(r1, size=11, bold=True, color=title_color)
    p2 = cell.add_paragraph()
    r2 = p2.add_run(body)
    set_run(r2, size=10, color=BLACK)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def pegar_tabla(doc, filas, header_fill=GREEN_HEX):
    """filas = lista de (cuadro, texto)."""
    table = doc.add_table(rows=1 + len(filas), cols=2)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_text(table.rows[0].cells[0], "Cuadro (columna del Excel)", bold=True, color=WHITE, fill=header_fill, size=10, align="center")
    cell_text(table.rows[0].cells[1], "Copiar y pegar esto — no cambien ni una coma", bold=True, color=WHITE, fill=header_fill, size=10, align="center")
    for i, (cuadro, texto) in enumerate(filas):
        bg_l = LABEL_HEX
        bg_r = ROW_HEX if i % 2 == 0 else "FFFFFF"
        cell_text(table.rows[i + 1].cells[0], cuadro, bold=True, color=WHITE, fill=bg_l, size=9)
        cell_text(table.rows[i + 1].cells[1], texto, fill=bg_r, size=9)
        table.rows[i + 1].cells[0].width = Cm(4.4)
        table.rows[i + 1].cells[1].width = Cm(12.6)
    table.rows[0].cells[0].width = Cm(4.4)
    table.rows[0].cells[1].width = Cm(12.6)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(10)
    return table


def add_table(doc, headers, rows, header_fill=NAVY_HEX):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, header in enumerate(headers):
        cell_text(table.rows[0].cells[i], header, bold=True, color=WHITE, fill=header_fill, size=10, align="center")
    for r_i, row in enumerate(rows):
        bg = ROW_HEX if r_i % 2 == 0 else "FFFFFF"
        for c_i, val in enumerate(row):
            cell_text(table.rows[r_i + 1].cells[c_i], val, fill=bg, size=9)
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(8)
    return table


HU008 = [
    ("ID", "HU-SIG-008"),
    ("Título", "Recuperar contraseña (correo + código de 6)"),
    ("Historia", "Como aprendiz o gestor, quiero recuperar mi clave con el correo y un código de 6 caracteres, para entrar de nuevo sin pedirle a Bienestar que me la cambie a mano."),
    ("Como (si el cuadro va separado)", "aprendiz o gestor (Aprendiz, Funcionario, admin_sistema o Administrador — un solo flujo, el sistema no pregunta el rol)"),
    ("Quiero (si el cuadro va separado)", "recuperar mi clave con el correo y un código de 6 caracteres"),
    ("Para (si el cuadro va separado)", "entrar de nuevo sin pedirle a Bienestar que me la cambie a mano"),
    ("Actor", "Aprendiz, Funcionario, admin_sistema y Administrador (misma historia, mismo flujo)"),
    ("Producto", "Urna + Gestión"),
    ("Épica", "EP-SIG-001 Accesos"),
    ("RF", "RF-NU-008"),
    ("CU", "CU-08"),
    ("Prioridad", "Debe tener"),
    ("Puntos", "5"),
    ("Sprint", "Sprint 2 — 31 ago al 4 sep 2026"),
    ("Sí entra", "• Un solo flujo para los 4 roles: el usuario solo escribe el correo; el sistema no pregunta si es aprendiz o funcionario.\n"
                 "• Paso 1: POST /api/recuperar-password/solicitar con { email }. Código de 6 al correo. Caduca en 5 minutos.\n"
                 "• Paso 2: POST /api/recuperar-password/confirmar con { email, codigo, nueva_password }. Clave mínima 8 caracteres.\n"
                 "• Reenviar código = volver a llamar solicitar. El código anterior se invalida.\n"
                 "• Redirect: Aprendiz → /login-aprendiz. Staff → /login. No hay login automático.\n"
                 "• Pintar el message del back si falla. Sin toast de éxito cuando falló."),
    ("No entra", "• No pedir número de documento.\n"
                 "• No preguntar el rol ni la jornada.\n"
                 "• No usar PUT /api/aprendiz/actualizar/contrasena (responde 410).\n"
                 "• No usar /api/usuarios/recuperar-contrasena ni /api/aprendiz/recuperar-contrasena (esas rutas no existen).\n"
                 "• No JWT. No OTP de votación. No dos historias (una de aprendiz y otra de funcionario)."),
    ("Criterios de aceptación",
     "CA-008-01\n"
     "Dado un correo que existe en usuarios o en aprendiz\n"
     "Cuando POST /api/recuperar-password/solicitar con { email }\n"
     "Entonces 200, se envía el código de 6 al correo y Network solo manda email. Ya no se pide documento.\n\n"
     "CA-008-02\n"
     "Dado el código vigente de 6 y una clave de 8 o más caracteres (y repetir igual)\n"
     "Cuando POST /api/recuperar-password/confirmar con { email, codigo, nueva_password }\n"
     "Entonces 200. Redirect /login-aprendiz si el perfil es Aprendiz, /login si es staff. No llama login() solo. La clave vieja ya no entra.\n\n"
     "CA-008-03\n"
     "Dado un correo que no existe\n"
     "Cuando POST solicitar\n"
     "Entonces 404. codigo_error CUENTA_NO_ENCONTRADA. Mensaje: No hay una cuenta con ese correo. No se pasa al paso 2.\n\n"
     "CA-008-04\n"
     "Dado un código mal escrito o un código de más de 5 minutos\n"
     "Cuando POST confirmar\n"
     "Entonces 400. OTP_INVALIDO o OTP_EXPIRADO. Se pinta el message del back. No hay toast de éxito.\n\n"
     "CA-008-05\n"
     "Dado PUT /api/aprendiz/actualizar/contrasena\n"
     "Cuando alguien lo llama\n"
     "Entonces 410 y el mensaje de usar solicitar/confirmar.\n\n"
     "CA-008-06\n"
     "Dado esta historia\n"
     "Cuando se cierra\n"
     "Entonces no hay login automático, no se preguntó el rol, no se pidió documento ni jornada."),
    ("Depende de", "HU-SIG-001-AP (login urna) y HU-SIG-010-GE (login gestión). El usuario ya existe en censo o en usuarios."),
    ("Responsable", "Lucero (documenta) · Alex back · Maicol front"),
]

HU019 = [
    ("ID", "HU-SIG-019-FU"),
    ("Título", "Informe de candidatos por jornada (quién va ganando)"),
    ("Historia", "Como funcionario, quiero ver el informe de candidatos partido por jornada (Mañana, Tarde, Noche) y quién va ganando en cada franja, para no mezclar las tres urnas en un solo total."),
    ("Como (si el cuadro va separado)", "Funcionario"),
    ("Quiero (si el cuadro va separado)", "ver el informe de candidatos partido por jornada (Mañana, Tarde, Noche) y quién va ganando en cada franja"),
    ("Para (si el cuadro va separado)", "no mezclar las tres urnas en un solo total"),
    ("Actor", "Funcionario"),
    ("Producto", "Mesa"),
    ("Épica", "EP-SIG-004 Acta"),
    ("RF", "RF-NU-019"),
    ("CU", "CU-19"),
    ("Prioridad", "Debe tener"),
    ("Puntos", "5"),
    ("Sprint", "Sprint 2 — 31 ago al 4 sep 2026 (prototipo Mebel; la HU de producto la escribe Lucero)"),
    ("Sí entra", "• Una sola elección del centro, cortada por candidatos.jornada. NO son tres elecciones.\n"
                 "• Tres bloques: Mañana / Tarde / Noche (con ñ, nunca “manana”).\n"
                 "• En cada bloque: candidatos con votos, ceros incluidos, quién va primero o empate en ESA franja.\n"
                 "• El acta global HU-018 sigue existiendo. Esta historia NO la reemplaza ni se fusiona con ella.\n"
                 "• El aprendiz no ve este informe (sigue HU-007)."),
    ("No entra", "• Implementar API ni PDF en el mismo commit de esta HU de documentación (el prototipo es de Mebel; el código del informe es después).\n"
                 "• Pedir jornada en la elección (la jornada vive en el candidato, no en la convocatoria).\n"
                 "• Que el aprendiz vea totales o ganador.\n"
                 "• Segunda vuelta o sorteo.\n"
                 "• Usar el ID HU-S2-032: ese es el prototipo de ESTA semana. La historia permanente de producto es HU-019."),
    ("Criterios de aceptación",
     "CA-019-01\n"
     "Dado una elección con candidatos en Mañana, Tarde y Noche\n"
     "Cuando se mira el informe de candidatos por jornada\n"
     "Entonces hay tres bloques, uno por jornada, con votos (ceros incluidos) y quién va primero o empate en ESA franja.\n\n"
     "CA-019-02\n"
     "Dado las etiquetas de jornada\n"
     "Cuando se leen\n"
     "Entonces dicen Mañana, Tarde, Noche (con ñ). No manana ni tres elecciones distintas.\n\n"
     "CA-019-03\n"
     "Dado un máximo único en una franja\n"
     "Cuando se calcula el resultado de esa jornada\n"
     "Entonces se declara quién va ganando en esa franja.\n\n"
     "CA-019-04\n"
     "Dado dos o más candidatos que comparten el máximo en una franja\n"
     "Cuando se calcula el resultado de esa jornada\n"
     "Entonces se declara empate en esa franja. No se inventa un único ganador ni una segunda vuelta.\n\n"
     "CA-019-05\n"
     "Dado un aprendiz autenticado\n"
     "Cuando abre urna o pide este informe\n"
     "Entonces no se le sirve (HU-007). El informe es de funcionario.\n\n"
     "CA-019-06\n"
     "Dado el acta HU-018\n"
     "Cuando existe HU-019\n"
     "Entonces el acta global sigue. No se fusionaron las dos historias."),
    ("Depende de", "HU-SIG-016-FU (candidatos con jornada) · HU-SIG-018-FU (acta global, no se borra) · prototipo Mebel HU-S2-032"),
    ("Responsable", "Lucero (documenta) · Mebel (prototipo)"),
]

ADRII_HU = [
    ("ID", "HU-S2-029"),
    ("Título", "Una elección por centro el mismo día"),
    ("Historia", "Como funcionario, quiero que el sistema rechace una segunda elección el mismo día en mi centro, para no duplicar la convocatoria (si ya hay una del 27 de agosto, no se crea otra ese día)."),
    ("Como (si el cuadro va separado)", "Funcionario"),
    ("Quiero (si el cuadro va separado)", "que el sistema rechace una segunda elección el mismo día en mi centro"),
    ("Para (si el cuadro va separado)", "no duplicar la convocatoria (si ya hay una del 27 de agosto, no se crea otra ese día)"),
    ("Actor", "Funcionario"),
    ("Producto", "Mesa"),
    ("Épica", "EP-SIG-002 Censo y convocatoria"),
    ("RF", "RF-NU-029"),
    ("CU", "CU-29"),
    ("Prioridad", "Debe tener"),
    ("Puntos", "5"),
    ("Sprint", "Sprint 2 — 31 ago al 4 sep 2026"),
    ("Sí entra", "• Regla RN-S2-001: mismo idcentro_formacion + mismo día calendario de fecha_inicio (America/Bogota) = rechazo.\n"
                 "• Vale para POST /api/eleccion/crear y para PUT /api/eleccionActualizar/:id si se mueve a un día ocupado.\n"
                 "• Editar la MISMA elección (nombre, horas, fecha_fin) el mismo día SÍ se permite.\n"
                 "• Otro centro, el mismo 27 de agosto, SÍ se permite.\n"
                 "• Mensaje en español, HTTP 409. El front lo pinta en SweetAlert (eso es de Mebel). El back no devuelve 500."),
    ("No entra", "• Prohibir ventanas que se solapan en días distintos (27-29 vs 28-30). No se pidió; no se implementa.\n"
                 "• Unicidad por created_at (el día en que alguien pulsó Guardar). La regla es la fecha de la elección.\n"
                 "• OTP, voto, acta, candidatos, jornada.\n"
                 "• Inventar otros criterios. Los únicos válidos son CA-029-01 a CA-029-08."),
    ("Criterios de aceptación",
     "CA-029-01\n"
     "Dado centro 1 sin elección el 27 de agosto de 2026\n"
     "Cuando POST /api/eleccion/crear con fecha_inicio 2026-08-27 e idcentro_formacion 1\n"
     "Entonces 201 y queda creada.\n\n"
     "CA-029-02\n"
     "Dado ya existe una elección del centro 1 con fecha_inicio el 27 de agosto de 2026\n"
     "Cuando POST otra con fecha_inicio 2026-08-27 e idcentro 1 (aunque el nombre sea distinto)\n"
     "Entonces 409. Mensaje: «Ya existe una elección para este centro el 27 de agosto. No se puede crear otra el mismo día.» No se inserta fila.\n\n"
     "CA-029-03\n"
     "Dado la elección del 27 en el centro 1\n"
     "Cuando POST con fecha_inicio 2026-08-27 pero idcentro_formacion 2\n"
     "Entonces 201. La regla es por centro, no mundial.\n\n"
     "CA-029-04\n"
     "Dado la elección del 27 en el centro 1\n"
     "Cuando POST con fecha_inicio 2026-08-28 e idcentro 1\n"
     "Entonces 201. Otro día, misma sede, sí.\n\n"
     "CA-029-05\n"
     "Dado la elección del 27 (id E1)\n"
     "Cuando PUT /api/eleccionActualizar/E1 cambiando nombre u horas, sin cambiar el día\n"
     "Entonces 200. Editar la misma no viola la regla.\n\n"
     "CA-029-06\n"
     "Dado E1 el 27 y E2 el 28, mismo centro\n"
     "Cuando PUT de E2 con fecha_inicio 2026-08-27\n"
     "Entonces 409. No se «mueve» al día ocupado.\n\n"
     "CA-029-07\n"
     "Dado el día calendario\n"
     "Cuando se compara fecha_inicio\n"
     "Entonces se usa el día en America/Bogota, no el instante UTC que cruce medianoche.\n\n"
     "CA-029-08\n"
     "Dado una elección 27–29 y otra 28–30\n"
     "Cuando las ventanas se solapan pero fecha_inicio es distinta\n"
     "Entonces NO se rechaza en este sprint. Queda nota, no código."),
    ("Depende de", "HU-SIG-013-FU (crear elección) · HU-SIG-014-FU (actualizar elección)"),
    ("Responsable", "Adrii Eraso"),
]

ADRII_VIÑETA_SI = (
    "• Una sola elección por centro el mismo día de fecha_inicio (America/Bogota). "
    "La segunda el mismo día responde 409 con el mensaje en español."
)
ADRII_VIÑETA_NO = (
    "• No se prohibe que dos elecciones se solapen en días distintos (27-29 vs 28-30). Eso no entra este sprint."
)


def build():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(1.6)
    section.right_margin = Cm(1.6)
    section.top_margin = Cm(1.4)
    section.bottom_margin = Cm(1.4)
    section.different_first_page_header_footer = False
    header = section.header.paragraphs[0]
    header.text = "SIGEVA  ·  Sprint 2  ·  Historias de usuario para copiar y pegar  ·  Lucero y Adrii"
    for run in header.runs:
        set_run(run, size=8, color=MUTED)
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fr = footer.add_run("No inventen IDs  ·  No toquen código  ·  Pegar tal cual")
    set_run(fr, size=8, color=MUTED)

    banner(
        doc,
        "SIGEVA · Sprint 2 · 31 ago – 4 sep 2026",
        "Para Lucero y Adrii  ·  qué pegar en cada cuadro de las historias de usuario  ·  solo copiar y pegar",
    )
    callout(
        doc,
        "Léanlo 2 minutos y después solo pegan. No hay que redactar.",
        "Archivo: entregables/sprint-1/04-Historias-de-Usuario.xlsx\n"
        "Hoja: Historias  (un cuadro = una columna de la fila).\n"
        "También existe la hoja Épicas, Lucero corrige 3 textos ahí.\n"
        "No editen el Excel del Sprint 2 para inventar IDs. Los huecos libres del Sprint 1 son 008 y 019. Adrii usa HU-S2-029 (no 008, no 019, no 009).",
        SOFT_GREEN,
        GREEN,
    )

    add_h(doc, "1. Quién hace qué", 1)
    add_table(
        doc,
        ["Quién", "Qué pega", "Dónde", "Qué NO hace"],
        [
            [
                "Lucero",
                "1) Fila NUEVA HU-008 Recuperar contraseña.\n2) Fila NUEVA HU-019 Informe por jornada.\n3) Parches de épicas y de HU viejas (jornada).",
                "Hoja Historias: insertar 2 filas.\nHoja Épicas: corregir EP-SIG-001, 002 y 004.\nFilas ya existentes HU-012, 013, 014, 016, 024: cambiar el texto que habla de jornada.",
                "No toca código.\nNo renumera 001–007 ni 010–018 ni 020–025.\nNo usa HU-S2-032 como ID de producto.\nNo inventa JWT ni segunda vuelta.",
            ],
            [
                "Adrii Eraso",
                "1) En HU-013, pegar al FINAL del cuadro Criterios los 8 CA-029 (sin borrar lo que ya está).\n2) Una viñeta en Sí entra y una en No entra de HU-013.\n3) Si el instructor pide una historia aparte: la fila completa HU-S2-029 (está al final de su sección).",
                "Misma hoja Historias, fila HU-SIG-013-FU (Crear una elección de mi centro).\nSi piden HU aparte: insertar una fila nueva con ID HU-S2-029.",
                "NO inventa otros criterios.\nNO cambia CA-029-01 a 08 ni una coma.\nNO usa los IDs 008, 009 ni 019.\nNO pisa el solape de ventanas (eso es CA-029-08: no se implementa).",
            ],
        ],
        NAVY_HEX,
    )

    add_h(doc, "2. Cómo insertar una fila (las dos)", 1)
    add_p(
        doc,
        "1. Abrir 04-Historias-de-Usuario.xlsx. Ir a la hoja Historias. Activar el filtro si está apagado. "
        "2. Lucero: insertar una fila debajo de HU-007 (queda HU-008) y otra debajo de HU-018 (queda HU-019). "
        "3. Adrii: NO inserta fila salvo que el instructor pida la HU aparte; primero trabaja sobre la fila de HU-013. "
        "4. Cada tabla de este Word tiene a la izquierda el nombre EXACTO de la columna. Copian la celda de la derecha y la pegan en esa columna. "
        "5. Si el formulario del instructor separa Como / Quiero / Para, usen esas tres filas de la tabla. Si el Excel tiene una sola columna Historia, usen esa.",
        size=10,
    )

    # ---------- LUCERO ----------
    add_h(doc, "3. LUCERO — Historia nueva 1 de 2", 1)
    callout(
        doc,
        "Insertar fila nueva  ·  ID HU-SIG-008  ·  Recuperar contraseña",
        "Va en la hoja Historias, después de HU-007 (comprobante) y antes de HU-010 (login gestión). "
        "Épica EP-SIG-001 Accesos. Un solo flujo para los 4 roles. Alex y Maicol ya lo construyeron; Lucero solo lo deja escrito.",
        SOFT_PURPLE,
        PURPLE,
    )
    pegar_tabla(doc, HU008, "6B4C9A")

    add_h(doc, "4. LUCERO — Historia nueva 2 de 2", 1)
    callout(
        doc,
        "Insertar fila nueva  ·  ID HU-SIG-019-FU  ·  Informe por jornada",
        "Va en la hoja Historias, JUSTO DESPUÉS de HU-018 (acta global). No se fusiona con el acta. "
        "Mebel prototipa (HU-S2-032). Lucero escribe HU-019. El código del informe no es de Lucero.",
        SOFT_AMBER,
        AMBER,
    )
    pegar_tabla(doc, HU019, "9A6B2F")

    add_h(doc, "5. LUCERO — Parches (historias y épicas que ya existen)", 1)
    add_p(
        doc,
        "No crean filas nuevas aquí. Buscan la fila por el ID y CAMBIAN solo el cuadro que se indica. "
        "Si un cuadro no se nombra, lo dejan igual.",
        size=10,
        italic=True,
    )

    add_h(doc, "5.1 Hoja Épicas · EP-SIG-001 Accesos", 2)
    add_table(
        doc,
        ["Cuadro", "Tiene hoy (borrar / quitar)", "Dejar pegado esto"],
        [
            [
                "Historias",
                "HU-SIG-001-AP · HU-SIG-010-GE",
                "HU-SIG-001-AP · HU-SIG-008 · HU-SIG-010-GE",
            ],
            [
                "No entra / Fuera",
                "Quitar de la lista: recuperar contraseña · cerrar sesión (huecos de journey; no hay HU)",
                "JWT / SSO / 2FA extra · cerrar sesión (hueco de journey; no hay HU) · login duplicado de administrador · que el administrador vote.\n(Recuperar contraseña YA NO va en fuera: ahora es HU-008.)",
            ],
            [
                "Sí entra / Alcance",
                "Login de urna (HU-001) · login único de gestión (HU-010) · …",
                "Login de urna (HU-001) · recuperar contraseña correo + código de 6 (HU-008) · login único de gestión (HU-010) · menú por perfil · centro atado a la sesión del funcionario · rechazo de inactivo · error genérico de credenciales · bcrypt.",
            ],
        ],
        "6B4C9A",
    )

    add_h(doc, "5.2 Hoja Épicas · EP-SIG-002 Censo y convocatoria", 2)
    add_table(
        doc,
        ["Cuadro", "Tiene hoy (mal)", "Dejar pegado esto"],
        [
            [
                "Éxito / en una frase",
                "Crea una elección con jornada Mañana/Tarde/Noche y ventana fecha-hora.",
                "Crea UNA elección por centro, SIN jornada en la convocatoria, con ventana fecha-hora. La jornada (Mañana/Tarde/Noche) vive en el candidato y la elige el aprendiz al entrar.",
            ],
        ],
        "C0392B",
    )

    add_h(doc, "5.3 Hoja Épicas · EP-SIG-004 Acta", 2)
    add_table(
        doc,
        ["Cuadro", "Tiene hoy", "Dejar pegado esto"],
        [
            [
                "Historias",
                "HU-SIG-018-FU",
                "HU-SIG-018-FU · HU-SIG-019-FU",
            ],
            [
                "Sí entra / Alcance",
                "Reporte + PDF (HU-018). Ceros incluidos. Empate declarado.",
                "Reporte + PDF global (HU-018). Informe de candidatos partido por jornada Mañana/Tarde/Noche y quién va ganando en cada franja (HU-019). Ceros incluidos. Empate declarado por franja y en el acta global.",
            ],
            [
                "No entra / Fuera",
                "(dejar lo de aprendiz / segunda vuelta)",
                "El aprendiz ve el acta o el informe por jornada · publicación pública · recuento biométrico · segunda vuelta / sorteo · historia de administrador descargando actas de toda la red.",
            ],
        ],
        "9A6B2F",
    )

    add_h(doc, "5.4 Hoja Historias · HU-013 Crear una elección", 2)
    add_p(doc, "Adrii también pega criterios en esta misma fila. Lucero solo quita la jornada de la convocatoria. No se pisan: Lucero cambia Título / Historia / Sí entra viejo; Adrii AGREGA al final de Criterios.", size=10, italic=True)
    add_table(
        doc,
        ["Cuadro", "Quitar / ya no decir", "Dejar pegado esto"],
        [
            [
                "Título",
                "Crear una elección de mi centro  (si dice «con jornada», quitarlo)",
                "Crear una elección de mi centro",
            ],
            [
                "Historia",
                "Como funcionario, quiero crear una elección con jornada y ventana de fecha y hora, para convocar la urna oficial de mi centro, no un 'voten cuando puedan'.",
                "Como funcionario, quiero crear una elección con ventana de fecha y hora (sin jornada en la convocatoria), para convocar la urna oficial de mi centro, no un “voten cuando puedan”.",
            ],
            [
                "Sí entra  (reemplazar la viñeta de jornada)",
                "Alta de elección: nombre, jornada, fecha_inicio, hora_inicio, fecha_fin, hora_fin",
                "• Alta de elección: nombre, fecha_inicio, hora_inicio, fecha_fin, hora_fin. SIN campo jornada en la convocatoria.\n• Centro = sesión.\n• Validar orden de ventana (inicio ≤ fin).",
            ],
        ],
        "C0392B",
    )

    add_h(doc, "5.5 Hoja Historias · HU-014 Actualizar una elección", 2)
    add_table(
        doc,
        ["Cuadro", "Quitar", "Dejar pegado esto"],
        [
            [
                "Historia",
                "corregir nombre, jornada o ventana",
                "Como funcionario, quiero corregir nombre o ventana de una elección de mi centro, para ajustar la convocatoria sin moverla de sede y sin pedir jornada en la elección.",
            ],
            [
                "Sí entra",
                "Editar nombre, jornada, fecha/hora…",
                "• Editar nombre, fecha y hora de una elección del centro de sesión. SIN jornada en la elección.\n• Validaciones idénticas a HU-013.\n• No cambiar el centro.",
            ],
        ],
        "C0392B",
    )

    add_h(doc, "5.6 Hoja Historias · HU-012 y HU-024 Import Excel", 2)
    add_table(
        doc,
        ["Cuadro", "Historia", "Quitar", "Dejar pegado / agregar"],
        [
            [
                "Criterios / Sí entra / campos",
                "HU-SIG-012-FU  (funcionario, SU centro)",
                "Cualquier frase de «el código pide jornada» o combo de jornada en la carga. El CA-P19 de jornada en el body ya no aplica: jornada NO va en el import.",
                "• Plantilla Reporte de Aprendices Sofia Plus: C2 = ficha - programa, filas desde 5.\n• Password inicial = número de documento (bcrypt).\n• NO se elige jornada en la carga. El aprendiz la elige al entrar.\n• Informe: insertados / actualizados / omitidos.\n• Centro = sesión (el funcionario no elige otra sede).",
            ],
            [
                "Criterios / Sí entra / campos",
                "HU-SIG-024-AD  (administrador elige centro)",
                "Igual: quitar jornada del import.",
                "• Misma plantilla Sofia Plus (C2, filas desde 5).\n• Password inicial = documento.\n• NO se elige jornada en la carga.\n• centroFormacionId obligatorio. El funcionario no usa esta vía.",
            ],
        ],
        "C0392B",
    )

    add_h(doc, "5.7 Hoja Historias · HU-016 Inscribir candidato", 2)
    add_table(
        doc,
        ["Cuadro", "Agregar (no borrar lo demás)"],
        [
            [
                "Sí entra",
                "• Select obligatorio de jornada del candidato: Mañana | Tarde | Noche (con ñ).\n• Unique de tarjetón + jornada en esa elección.\n• La urna lista candidatos con GET ?jornada= de la sesión del aprendiz.",
            ],
            [
                "Criterios de aceptación  (pegar al final, no borrar los CA-01 a CA-05 que ya están)",
                "CA-016-06\nDado el formulario de inscribir candidato\nCuando falta la jornada o no es Mañana, Tarde o Noche\nEntonces no se crea.\n\nCA-016-07\nDado un número de tarjetón que ya existe en ESA elección para la MISMA jornada\nCuando inscribe\nEntonces se rechaza. El mismo número en otra jornada sí se permite.",
            ],
        ],
        GREEN_HEX,
    )

    add_h(doc, "5.8 Lucero — lista de lo que NO hace", 2)
    add_p(
        doc,
        "No crear HU-026 de producto (026 ya es landing del Sprint 2). No hacer una HU de aprendiz y otra de funcionario para recuperar clave. "
        "No documentar PUT /api/aprendiz/actualizar/contrasena como flujo vigente. "
        "No usar HU-S2-032 como ID de producto. Landing, /equipo y el ojo del login NO son prioridad: primero 008 y 019, luego los parches de jornada. "
        "Si sobra tiempo el miércoles, se puede anotar HU-009 (ojo de clave + error de credenciales) — opcional, no bloquea el review.",
        size=10,
    )

    # ---------- ADRII ----------
    add_h(doc, "6. ADRII — Qué pegar (sin inventar criterios)", 1)
    callout(
        doc,
        "Tu trabajo de producto ya está escrito. Solo pegas. No reescribes.",
        "La regla: si ya hay una elección del 27 de agosto en un centro, no se crea otra ese día en ese centro. "
        "Otro centro el 27 sí. Editar la misma sí. Mover otra al 27 = 409. No se pisa el solape de ventanas. "
        "Mensaje exacto del 409 (cópialo tal cual, con tildes y el punto):\n\n"
        "Ya existe una elección para este centro el 27 de agosto. No se puede crear otra el mismo día.",
        SOFT_RED,
        RGBColor(0xC0, 0x39, 0x2B),
    )

    add_h(doc, "6.1 En la fila HU-013 (Crear una elección) — agregar, no borrar", 2)
    add_p(doc, "Abren la hoja Historias, buscan ID HU-SIG-013-FU. Van al cuadro que dice la izquierda y PEGAN al final (abajo de lo que ya está).", size=10)
    pegar_tabla(
        doc,
        [
            ("Sí entra  (agregar esta viñeta al final)", ADRII_VIÑETA_SI),
            ("No entra  (agregar esta viñeta al final)", ADRII_VIÑETA_NO),
            (
                "Criterios de aceptación  (pegar ESTO al final, debajo de los CA que ya tiene HU-013)",
                next(t for k, t in ADRII_HU if k.startswith("Criterios")),
            ),
        ],
        "C0392B",
    )

    add_h(doc, "6.2 En la fila HU-014 (Actualizar una elección) — agregar", 2)
    pegar_tabla(
        doc,
        [
            (
                "Sí entra  (agregar)",
                "• Si se cambia fecha_inicio a un día que ya tiene otra elección del mismo centro: 409. Editar nombre u horas de la misma, sin cambiar el día: 200.",
            ),
            (
                "Criterios de aceptación  (pegar al final)",
                "CA-014-S2-01\n"
                "Dado la elección del 27 (id E1)\n"
                "Cuando PUT /api/eleccionActualizar/E1 cambiando nombre u horas, sin cambiar el día\n"
                "Entonces 200. Editar la misma no viola la regla.\n\n"
                "CA-014-S2-02\n"
                "Dado E1 el 27 y E2 el 28, mismo centro\n"
                "Cuando PUT de E2 con fecha_inicio 2026-08-27\n"
                "Entonces 409. No se «mueve» al día ocupado. Mensaje: «Ya existe una elección para este centro el 27 de agosto. No se puede crear otra el mismo día.»",
            ),
        ],
        "C0392B",
    )

    add_h(doc, "6.3 Si el instructor pide una historia APARTE (fila nueva)", 2)
    add_p(
        doc,
        "Solo si les dicen “meté una HU nueva, no la mezclés con crear elección”. Entonces insertan UNA fila y pegan el bloque de abajo. "
        "El ID es HU-S2-029. No usen 008, 009 ni 019 (esos son de Lucero / huecos del Sprint 1).",
        size=10,
    )
    pegar_tabla(doc, ADRII_HU, "C0392B")

    add_h(doc, "6.4 Adrii — lista de lo que NO pega / NO cambia", 2)
    add_table(
        doc,
        ["Prohibido", "Por qué"],
        [
            ["Inventar CA-029-09 o cambiar el texto del 409", "El contrato del Sprint 2 son exactamente CA-029-01 a 08."],
            ["Rechazar dos elecciones que se solapan en días distintos", "CA-029-08 dice que NO se implementa. Queda nota, no código y no criterio nuevo."],
            ["Unicidad por created_at (el día del clic Guardar)", "La regla es fecha_inicio de la elección, en America/Bogota."],
            ["Tocar OTP, voto, acta, candidatos, jornada, landing", "Eso es de otras personas. Adrii solo crear/actualizar elección."],
            ["Usar alert() nativo para el 409", "Mebel pinta SweetAlert. El back solo devuelve 409 + el mensaje en español."],
        ],
        "C0392B",
    )

    add_h(doc, "7. Cómo se dan cuenta de que quedó bien (review viernes)", 1)
    add_table(
        doc,
        ["Quién", "Se ve en el Excel", "Se dice en el daily"],
        [
            [
                "Lucero",
                "Existe HU-SIG-008 con Como/quiero/para, Sí entra, No entra y CA-008-01 a 06.\nExiste HU-SIG-019-FU justo después de HU-018, con Mañana/Tarde/Noche.\nEP-SIG-001 ya no lista recuperar en Fuera.\nHU-013 ya no pide jornada en la convocatoria.",
                "“Dejé 008 y 019. Quitar jornada de 012/013/016/024.”",
            ],
            [
                "Adrii",
                "En HU-013 el cuadro Criterios termina con CA-029-01 a 08, textos idénticos a este Word.\nSi pidieron HU aparte: se ve la fila HU-S2-029.",
                "“Pegué CA-029 en HU-013. El 409 dice el mensaje del 27 de agosto. No inventé otra regla.”",
            ],
        ],
        GREEN_HEX,
    )

    add_h(doc, "8. Mapa rápido de IDs (para no chocar)", 1)
    add_table(
        doc,
        ["ID", "Quién lo pega", "Qué es", "Prohibido"],
        [
            ["HU-SIG-008 / RF-NU-008 / CU-08", "Lucero", "Recuperar contraseña, 4 roles", "No es de Adrii. No es landing."],
            ["HU-SIG-019-FU / RF-NU-019 / CU-19", "Lucero", "Informe por jornada", "No fusionar con HU-018. No usar HU-S2-032."],
            ["HU-S2-029 / RF-NU-029 / CU-29", "Adrii", "Una elección por centro el mismo día", "No usar 008, 009, 019."],
            ["HU-S2-032", "Nadie lo pega en producto", "Tarea de prototipo de Mebel esta semana", "No es ID de historia permanente."],
            ["HU-009", "Nadie este documento", "Hueco opcional (ojo de login de Maicol)", "No lo usen para recuperar ni para el 409."],
        ],
        NAVY_HEX,
    )

    add_p(
        doc,
        "Pregunta de último minuto: escríbanle a Alex. No inventen una regla “por si acaso”. Si un cuadro del Excel no existe en su plantilla (por ejemplo no tienen Puntos), dejen ese cuadro vacío y pegan el resto.",
        size=10,
        italic=True,
        color=MUTED,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))
    print(OUT)


if __name__ == "__main__":
    build()
