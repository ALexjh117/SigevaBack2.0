# -*- coding: utf-8 -*-
"""Guía SIGEVA: por qué se cambia, para qué sirve, código en capturas."""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _code_shots import (  # noqa: E402
    BADGE_GREEN,
    BADGE_NAVY,
    BADGE_RED,
    diagram_archivo_split,
    diagram_carriles,
    diagram_exito,
    diagram_flujo,
    diagram_paula_listo,
    diagram_sofia_listo,
    diagram_urna_bug,
    http_shot,
    network_shot,
    shot,
)
from _guia_pasos import escribir_pasos  # noqa: E402

OUT = HERE / "SIGEVA-Guia-Codigo-Eleccion-Global.docx"

NAVY = RGBColor(0x1B, 0x3A, 0x4B)
GREEN = RGBColor(0x1F, 0x7A, 0x4D)
SENA = RGBColor(0x00, 0x73, 0x32)
MUTED = RGBColor(0x4A, 0x55, 0x63)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AMBER = RGBColor(0x92, 0x40, 0x0E)
NAVY_HEX = "1B3A4B"
ROW_HEX = "F2F4F7"
SOFT_GREEN = "E8F5EE"
SOFT_AMBER = "FEF3C7"
SOFT_RED = "FDECEC"
SOFT_NAVY = "E8EEF2"


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


def no_borders(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tbl_pr.append(borders)


def cell_text(cell, text, *, bold=False, color=BLACK, size=10, fill=None):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
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
    for run in p.runs:
        set_run(run, size=size, bold=True, color=NAVY)
    p.paragraph_format.space_before = Pt(12 if level == 1 else 8)
    p.paragraph_format.space_after = Pt(6)
    return p


def add_table(doc, headers, rows, col_cm=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, header in enumerate(headers):
        cell_text(table.rows[0].cells[i], header, bold=True, color=WHITE, fill=NAVY_HEX)
    for r_i, row in enumerate(rows):
        bg = ROW_HEX if r_i % 2 == 0 else "FFFFFF"
        for c_i, val in enumerate(row):
            cell_text(table.rows[r_i + 1].cells[c_i], val, fill=bg)
    if col_cm:
        for row in table.rows:
            for i, width in enumerate(col_cm):
                row.cells[i].width = Cm(width)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table


def callout(doc, title, body, fill=SOFT_AMBER, title_color=AMBER):
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    shade(cell, fill)
    set_cell_margins(cell, top=0.16, bottom=0.16, left=0.25, right=0.25)
    cell.text = ""
    p1 = cell.paragraphs[0]
    r1 = p1.add_run(title)
    set_run(r1, size=11, bold=True, color=title_color)
    p2 = cell.add_paragraph()
    r2 = p2.add_run(body)
    set_run(r2, size=11, color=BLACK)
    no_borders(table)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def banner(doc, title, subtitle):
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    shade(cell, NAVY_HEX)
    set_cell_margins(cell, top=0.22, bottom=0.22, left=0.3, right=0.3)
    cell.text = ""
    p1 = cell.paragraphs[0]
    r1 = p1.add_run(title)
    set_run(r1, size=14, bold=True, color=WHITE)
    p2 = cell.add_paragraph()
    r2 = p2.add_run(subtitle)
    set_run(r2, size=10, color=WHITE)
    no_borders(table)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)


def dicc(doc, rows):
    add_p(doc, "Qué dice ese código, en cristiano:", size=11, bold=True, color=NAVY, space_after=4)
    add_table(
        doc,
        ["Pedazo", "Qué hace", "Para qué se pone", "Si no va"],
        rows,
        col_cm=[3.4, 4.4, 4.6, 4.4],
    )


def cambio(doc, kind: str, archivo: str, detalle: str):
    """kind = NUEVO | SE MODIFICA"""
    fill = SOFT_GREEN if kind == "NUEVO" else SOFT_AMBER
    title_color = GREEN if kind == "NUEVO" else AMBER
    titulo = (
        "CÓDIGO NUEVO — se agrega lo que no existía"
        if kind == "NUEVO"
        else "CÓDIGO EXISTENTE — se modifica lo que ya está"
    )
    callout(doc, f"{titulo}  ·  {archivo}", detalle, fill=fill, title_color=title_color)


def sql_block(doc, text: str):
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    shade(cell, "1E1E1E")
    set_cell_margins(cell, top=0.2, bottom=0.2, left=0.25, right=0.25)
    cell.text = ""
    first = True
    for line in text.split("\n"):
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(0xD4, 0xD4, 0xD4)
        r_pr = run._element.get_or_add_rPr()
        r_fonts = r_pr.find(qn("w:rFonts"))
        if r_fonts is None:
            r_fonts = OxmlElement("w:rFonts")
            r_pr.append(r_fonts)
        for key in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            r_fonts.set(qn(key), "Consolas")
    no_borders(table)
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(10)
    r = cap.add_run("Copia este bloque entero, pégalo en pgAdmin o DBeaver, F5. Cada uno en SU base local.")
    set_run(r, size=9, italic=True, color=MUTED)


def paso(doc, n, titulo, quien, mientras):
    banner(doc, f"PASO {n} DE 9  —  {titulo}", f"Lo hace: {quien}")
    callout(doc, "Mientras tú haces esto", mientras, fill=SOFT_NAVY, title_color=NAVY)


def photo(doc, path: Path, caption: str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(path), width=Cm(16.2))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(12)
    r = cap.add_run(caption)
    set_run(r, size=9, italic=True, color=MUTED)


def add_page_number(paragraph):
    run = paragraph.add_run()
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)


def header_footer(doc):
    for section in doc.sections:
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(1.7)
        section.right_margin = Cm(1.7)
        hp = section.header.paragraphs[0]
        r = hp.add_run("SIGEVA")
        set_run(r, size=9, bold=True, color=SENA)
        r2 = hp.add_run("   ·   Guía de código   ·   Elección global")
        set_run(r2, size=9, color=MUTED)
        fp = section.footer.paragraphs[0]
        r = fp.add_run("Rojo = quitar    Verde = pegar    ·    Alex · Maicol · Mebel · Paula · Sofia     Pág. ")
        set_run(r, size=8, color=MUTED)
        add_page_number(fp)


def make_shots() -> dict[str, Path]:
    s: dict[str, Path] = {}
    s["flujo"] = diagram_flujo()
    s["carriles"] = diagram_carriles()
    s["archivo_split"] = diagram_archivo_split()
    s["exito"] = diagram_exito()
    s["paula_pantalla"] = diagram_paula_listo()
    s["sofia_pantalla"] = diagram_sofia_listo()
    s["urna_bug"] = diagram_urna_bug()

    s["sql_todos"] = shot(
        "sql-todos",
        "PostgreSQL  ·  lo corre CADA uno en su PC  ·  no esperen al otro",
        """-- No recrea la base. Solo agrega / suelta un NOT NULL.
-- Si dice already exists, ignora esa línea y sigue.

ALTER TABLE elecciones
  ALTER COLUMN jornada DROP NOT NULL;

ALTER TABLE candidatos
  ADD COLUMN IF NOT EXISTS jornada VARCHAR(20);

CREATE UNIQUE INDEX IF NOT EXISTS uq_candidatos_tarjeton_jornada
  ON candidatos (ideleccion, jornada, numero_tarjeton)
  WHERE jornada IS NOT NULL;""",
        badge="TODOS copian este SQL. Nadie sube la base por el otro.",
        badge_color=BADGE_NAVY,
        start_line=1,
        marks={4: "add", 5: "add", 7: "add", 8: "add", 10: "add", 11: "add", 12: "add"},
    )

    s["alex_antes"] = shot(
        "alex-antes",
        "app/controllers/eleccion_controller.ts  ·  crearEleccion",
        """const dataEleccion = request.only([
  'idcentro_formacion',
  'jornada',
  'fecha_inicio',
  'fecha_fin',
  'hora_inicio',
  'hora_fin',
  'nombre',
])

if (
  dataEleccion.jornada != 'Mañana' &&
  dataEleccion.jornada != 'Tarde' &&
  dataEleccion.jornada != 'Noche'
) {
  return response.status(400).json({ message: 'La jornada no es válida' })
}""",
        badge="ANTES — esto es lo que obliga a crear tres elecciones. QUÍTALO.",
        badge_color=BADGE_RED,
        start_line=37,
        marks={2: "del", 3: "del", 11: "del", 12: "del", 13: "del", 14: "del", 15: "del", 16: "del", 17: "del"},
    )

    s["alex_despues"] = shot(
        "alex-despues",
        "app/controllers/eleccion_controller.ts  ·  crearEleccion",
        """const dataEleccion = request.only([
  'idcentro_formacion',
  'fecha_inicio',
  'fecha_fin',
  'hora_inicio',
  'hora_fin',
  'nombre',
])

// Ya no se valida jornada. La elección es del centro, no de una jornada.
if (!dataEleccion.idcentro_formacion) {
  return response.status(400).json({
    message: 'El campo del centro de formacion es obligatorio',
  })
}""",
        badge="DESPUÉS — pega esto. Deja las validaciones de fechas y horas como están.",
        badge_color=BADGE_GREEN,
        start_line=37,
        marks={1: "add", 2: "add", 3: "add", 4: "add", 5: "add", 6: "add", 7: "add", 8: "add", 10: "add"},
    )

    s["alex_modelo"] = shot(
        "alex-modelo",
        "app/models/eleccione.ts",
        """@column({ columnName: 'jornada' })
declare jornada: string | null""",
        badge="PEGA — la columna puede nacer vacía. No la borres de la tabla.",
        badge_color=BADGE_GREEN,
        start_line=18,
        marks={1: "add", 2: "add"},
    )

    s["alex_sql"] = shot(
        "alex-sql",
        "PostgreSQL  ·  una sola vez",
        """ALTER TABLE elecciones
  ALTER COLUMN jornada DROP NOT NULL;""",
        badge="SQL de Alex — las elecciones nuevas nacen sin jornada.",
        badge_color=BADGE_NAVY,
        start_line=1,
        marks={1: "add", 2: "add"},
    )

    s["maicol_sql"] = shot(
        "maicol-sql",
        "PostgreSQL  ·  corre esto ANTES que el resto",
        """ALTER TABLE candidatos
  ADD COLUMN jornada VARCHAR(20);""",
        badge="SQL de Maicol — aquí vive ahora la jornada.",
        badge_color=BADGE_NAVY,
        start_line=1,
        marks={1: "add", 2: "add"},
    )

    s["maicol_modelo"] = shot(
        "maicol-modelo",
        "app/models/candidatos.ts",
        """@column()
declare numero_tarjeton: string

@column()
declare jornada: string""",
        badge="PEGA este campo. Es el dato nuevo del tarjetón.",
        badge_color=BADGE_GREEN,
        start_line=28,
        marks={4: "add", 5: "add"},
    )

    s["maicol_val"] = shot(
        "maicol-validator",
        "app/validators/store_candidato_validator.ts",
        """export const storeCandidatoValidator = vine.compile(
  vine.object({
    nombres: vine.string().trim().optional(),
    ideleccion: vine.number(),
    idaprendiz: vine.number(),
    propuesta: vine.string().trim(),
    numero_tarjeton: vine.string().trim(),
    jornada: vine.enum(['Mañana', 'Tarde', 'Noche']),
    foto_url: vine.string().url().optional(),
  })
)""",
        badge="PEGA la línea jornada. Las tres cadenas van CON eñe, igual que antes.",
        badge_color=BADGE_GREEN,
        start_line=3,
        marks={8: "add"},
    )

    s["maicol_unique_antes"] = shot(
        "maicol-unique-antes",
        "app/services/candidatos_service.ts  ·  checkDuplicateTarjeton",
        """static async checkDuplicateTarjeton(
  ideleccion: number,
  numero_tarjeton: string
) {
  const exists = await Candidatos.query()
    .where('ideleccion', ideleccion)
    .andWhere('numero_tarjeton', numero_tarjeton)
    .first()""",
        badge="ANTES — unique por elección sola. Impide un 01 en mañana Y un 01 en tarde.",
        badge_color=BADGE_RED,
        start_line=15,
        marks={6: "del", 7: "del"},
    )

    s["maicol_unique"] = shot(
        "maicol-unique",
        "app/services/candidatos_service.ts  ·  checkDuplicateTarjeton",
        """static async checkDuplicateTarjeton(
  ideleccion: number,
  numero_tarjeton: string,
  jornada: string
) {
  const exists = await Candidatos.query()
    .where('ideleccion', ideleccion)
    .andWhere('jornada', jornada)
    .andWhere('numero_tarjeton', numero_tarjeton)
    .first()

  if (exists) {
    throw new Error(
      'Ya existe ese número de tarjetón en esta jornada'
    )
  }
}""",
        badge="DESPUÉS — unique por elección + jornada. El 01 puede existir tres veces.",
        badge_color=BADGE_GREEN,
        start_line=15,
        marks={4: "add", 8: "add"},
    )

    s["maicol_create"] = shot(
        "maicol-create",
        "app/services/candidatos_service.ts  ·  Candidatos.create",
        """await this.checkDuplicateTarjeton(
  data.ideleccion,
  data.numero_tarjeton,
  data.jornada
)

const candidato = await Candidatos.create(
  {
    nombres: data.nombres,
    ideleccion: data.ideleccion,
    idaprendiz: data.idaprendiz,
    propuesta: data.propuesta,
    numero_tarjeton: data.numero_tarjeton,
    jornada: data.jornada,
    foto: fotoUrl ?? '',
  },
  { client: trx }
)""",
        badge="PEGA jornada en el unique y en el create. Si no, la columna nace vacía.",
        badge_color=BADGE_GREEN,
        start_line=26,
        marks={4: "add", 14: "add"},
    )

    s["maicol_get"] = shot(
        "maicol-get",
        "app/services/candidatos_service.ts  ·  getAllCandidatosByIdEleccion",
        """static async getAllCandidatosByIdEleccion(
  ideleccion: number,
  jornada?: string
) {
  const query = Candidatos.query().where('ideleccion', ideleccion)

  if (jornada) {
    query.andWhere('jornada', jornada)
  }

  return query
    .orderByRaw('RANDOM()')
    .preload('aprendiz', (aprendiz) => {
      aprendiz.preload('centro_formacion')
    })
}""",
        badge="PEGA — sin query lista los tres bloques (gestión). Con query, solo esa jornada (urna).",
        badge_color=BADGE_GREEN,
        start_line=58,
        marks={3: "add", 7: "add", 8: "add"},
    )

    s["maicol_ctrl"] = shot(
        "maicol-ctrl",
        "app/controllers/candidatos_controller.ts  ·  getByEleccion",
        """public async getByEleccion({ params, request, response }: HttpContext) {
  const ideleccion = Number(params.ideleccion)
  const { jornada } = request.qs()

  const candidatos = await CandidatosService.getAllCandidatosByIdEleccion(
    ideleccion,
    jornada
  )

  return response.ok({
    message: 'Candidatos obtenidos correctamente',
    data: candidatos,
  })
}""",
        badge="PEGA — misma ruta. Sofia manda ?jornada=Tarde. No crees otra URL.",
        badge_color=BADGE_GREEN,
        start_line=57,
        marks={3: "add", 7: "add"},
    )

    s["maicol_store"] = shot(
        "maicol-store",
        "app/controllers/candidatos_controller.ts  ·  store",
        """const candidato = await CandidatosService.createWithOptionalUpload(
  {
    nombres: payload.nombres ?? 'Candidato',
    ideleccion: payload.ideleccion,
    idaprendiz: payload.idaprendiz,
    propuesta: payload.propuesta,
    numero_tarjeton: payload.numero_tarjeton,
    jornada: payload.jornada,
    foto_url: payload.foto_url ?? null,
  },
  fotoFile?.tmpPath ?? null
)""",
        badge="PEGA jornada: payload.jornada — el validator ya la trae.",
        badge_color=BADGE_GREEN,
        start_line=17,
        marks={8: "add"},
    )

    s["mebel_antes"] = shot(
        "mebel-antes",
        "app/services/FiltroJorElCen.ts",
        """.preload('candidato', (consultarCandidatos) => {
  consultarCandidatos.preload('aprendiz', (consultarAprendiz) => {
    consultarAprendiz.preload('grupo', (consultarGrupo) => {
      if (jornada) consultarGrupo.where('jornada', jornada)
    })
  })
})""",
        badge="ANTES — filtra la FICHA del aprendiz. Eso ya no es la contienda.",
        badge_color=BADGE_RED,
        start_line=19,
        marks={2: "del", 3: "del", 4: "del", 5: "del"},
    )

    s["mebel_despues"] = shot(
        "mebel-despues",
        "app/services/FiltroJorElCen.ts",
        """.preload('candidato', (consultarCandidatos) => {
  if (jornada) {
    consultarCandidatos.where('jornada', jornada)
  }
  consultarCandidatos.preload('aprendiz')
})""",
        badge="DESPUÉS — filtra candidatos.jornada. Centro y fechas se quedan.",
        badge_color=BADGE_GREEN,
        start_line=19,
        marks={2: "add", 3: "add", 4: "add"},
    )

    s["mebel_json"] = shot(
        "mebel-json",
        "eleccion_controller.ts  ·  traerPorCentroFormacion",
        """eleccionesActivas.push({
  ideleccion: eleccion.ideleccion,
  titulo: eleccion.nombre,
  fechaInicio: eleccion.fecha_inicio,
  fechaFin: eleccion.fecha_fin,
  centro: eleccion.centro.centro_formacioncol,
  horaInicio: eleccion.hora_inicio,
  horaFin: eleccion.hora_fin,
})""",
        badge="QUITA jornada: eleccion.jornada del push. Igual en traerPorCentroFormacionTodas.",
        badge_color=BADGE_GREEN,
        start_line=201,
    )

    s["mebel_jornada"] = shot(
        "mebel-traer-jornada",
        "eleccion_controller.ts  ·  traerPorJornada",
        """const elecciones = await Eleccione.query().preload('candidato', (q) => {
  if (jornada) {
    q.where('jornada', jornada)
  }
  q.preload('aprendiz')
})""",
        badge="PEGA — misma URL /api/eleccionJornada/listar. Cambia el significado, no el path.",
        badge_color=BADGE_GREEN,
        start_line=269,
        marks={2: "add", 3: "add"},
    )

    s["paula_antes"] = shot(
        "paula-antes",
        "src/pages/funcionario/FormEleccion.tsx  ·  el archivo YA existe",
        """const [jornada, setJornada] = useState<string>("")

<FormLabel>Selecciona la jornada</FormLabel>
<Form.Select required onChange={(e) => setJornada(e.target.value)}>
  <option value="">Seleccione...</option>
  <option value="Mañana">Mañana</option>
  <option value="Tarde">Tarde</option>
  <option value="Noche">Noche</option>
</Form.Select>

await api.post(`/api/eleccion/crear`, {
  idcentro_formacion: user?.centroFormacion,
  nombre,
  jornada,
  fecha_inicio,
  fecha_fin,
  hora_inicio: `${fecha_inicio} ${hora_inicio}:00`,
  hora_fin: `${fecha_fin} ${hora_fin}:00`,
})""",
        badge="ANTES — este combo y la clave jornada del POST se BORRAN. El resto del form se queda.",
        badge_color=BADGE_RED,
        start_line=10,
        marks={1: "del", 3: "del", 4: "del", 5: "del", 6: "del", 7: "del", 8: "del", 9: "del", 15: "del"},
    )

    s["paula_despues"] = shot(
        "paula-despues",
        "src/pages/funcionario/FormEleccion.tsx  ·  crear",
        """// Sin useState de jornada. Sin <Form.Select> de jornada.
// El centro sale de la sesión. No armes combo de sedes.

if (!user?.centroFormacion) return
await api.post(`/api/eleccion/crear`, {
  idcentro_formacion: user.centroFormacion,
  nombre,
  fecha_inicio,
  fecha_fin,
  hora_inicio: `${fecha_inicio} ${hora_inicio}:00`,
  hora_fin: `${fecha_fin} ${hora_fin}:00`,
})""",
        badge="DESPUÉS — mismas fechas/horas de siempre. El JSON ya NO lleva jornada.",
        badge_color=BADGE_GREEN,
        start_line=10,
        marks={1: "add", 2: "add", 5: "add", 6: "add", 7: "add", 8: "add", 9: "add", 10: "add", 11: "add"},
    )

    s["paula_edit_antes"] = shot(
        "paula-edit-antes",
        "src/components/EleccionEditarModal.tsx",
        """const payload: any = {
  nombre: formData.nombre,
  jornada: formData.jornada,
}

<Form.Label>Jornada</Form.Label>
<Form.Select name="jornada" value={formData.jornada}>
  <option value="">Seleccionar</option>
  <option value="Mañana">Mañana</option>
  <option value="Tarde">Tarde</option>
  <option value="Noche">Noche</option>
</Form.Select>

await api.put(`/api/eleccionActualizar/${eleccion.ideleccion}`, payload)""",
        badge="ANTES — el PUT también manda jornada. Si solo arreglas el crear, el editar vuelve a forzar tres urnas.",
        badge_color=BADGE_RED,
        start_line=80,
        marks={3: "del", 6: "del", 7: "del", 8: "del", 9: "del", 10: "del", 11: "del", 12: "del"},
    )

    s["paula_edit_despues"] = shot(
        "paula-edit-despues",
        "src/components/EleccionEditarModal.tsx  ·  PUT",
        """const payload = {
  idcentro_formacion: user.centroFormacion, // el de la sesión
  nombre: formData.nombre,
  fecha_inicio: formData.fecha_inicio,
  fecha_fin: formData.fecha_fin,
  hora_inicio: `${formData.fecha_inicio}T${formData.hora_inicio}:00`,
  hora_fin: `${formData.fecha_fin}T${formData.hora_fin}:00`,
}
// Sin jornada. Sin combo. El PUT SÍ lleva JSON (no va vacío).
await api.put(`/api/eleccionActualizar/${eleccion.ideleccion}`, payload)""",
        badge="DESPUÉS — mismos campos que el POST. Cambia el 12 por eleccion.ideleccion. Status 200.",
        badge_color=BADGE_GREEN,
        start_line=76,
        marks={2: "add", 3: "add", 4: "add", 5: "add", 6: "add", 7: "add", 8: "add"},
    )

    s["paula_tabla_antes"] = shot(
        "paula-tabla-antes",
        "src/pages/funcionario/EleccionesActivasPage.tsx  ·  columns",
        """{
  name: <b>Jornada</b>,
  selector: (row) => row.jornada ?? "Sin jornada",
},""",
        badge="ANTES — esta columna pinta jornada aunque Mebel ya no la mande. QUÍTALA.",
        badge_color=BADGE_RED,
        start_line=125,
        marks={1: "del", 2: "del", 3: "del", 4: "del"},
    )

    s["paula_tabla_despues"] = shot(
        "paula-tabla-despues",
        "src/pages/funcionario/EleccionesActivasPage.tsx",
        """const res = await api.get(
  `/api/eleccion/traerTodas/${user.centroFormacion}`
)
setEleccionActiva(res.data.eleccionesActivas)
// Cada item usa titulo (no nombre). NO pintes jornada.
// Deja Título, fechas, estado, acciones. Una fila = una convocatoria.""",
        badge="DESPUÉS — el GET se queda. Lo que cambia es que no hay columna Jornada.",
        badge_color=BADGE_GREEN,
        start_line=51,
        marks={5: "add", 6: "add"},
    )

    s["paula_detalle"] = shot(
        "paula-detalle",
        "src/components/EleccionDetalleModal.tsx",
        """<h4>{eleccion.titulo}</h4>
<p>{eleccion.fechaInicio} - {eleccion.fechaFin}</p>
{/* BORRA esta línea: */}
<p><strong>Jornada:</strong> {eleccion.jornada}</p>""",
        badge="QUITA el <p> de Jornada. Si el JSON todavía la trae, tú igual no la muestres.",
        badge_color=BADGE_RED,
        start_line=137,
        marks={3: "del", 4: "del"},
    )

    s["sofia_form"] = shot(
        "sofia-form",
        "src/components/candidatos/AgregarCandidatoModal.tsx",
        """const [formData, setFormData] = useState({
  nombres: "",
  idaprendiz: null as number | null,
  ideleccion: idEleccion || null,
  propuesta: "",
  numero_tarjeton: "",
  jornada: "",
})

<Form.Group className="mb-3">
  <Form.Label>Jornada del tarjetón</Form.Label>
  <Form.Select name="jornada" value={formData.jornada} onChange={handleChange} required>
    <option value="">Seleccione...</option>
    <option value="Mañana">Mañana</option>
    <option value="Tarde">Tarde</option>
    <option value="Noche">Noche</option>
  </Form.Select>
</Form.Group>

data.append("ideleccion", String(formData.ideleccion))
data.append("idaprendiz", String(formData.idaprendiz))
data.append("numero_tarjeton", String(formData.numero_tarjeton))
data.append("jornada", formData.jornada)
await api.post(`/api/candidatos/crear`, data, {
  headers: { "Content-Type": "multipart/form-data" },
})""",
        badge="PEGA el select y el append. Grafía exacta con ñ. Igual en ModificarCandidatoModal (PUT).",
        badge_color=BADGE_GREEN,
        start_line=25,
        marks={7: "add", 10: "add", 11: "add", 12: "add", 13: "add", 14: "add", 15: "add", 16: "add", 17: "add", 18: "add", 23: "add"},
    )

    s["sofia_get_antes"] = shot(
        "sofia-get-antes",
        "src/pages/funcionario/GestionCandidatos.tsx  ·  fetchCandidatos",
        """const res = await api.get(
  `/api/candidatos/listar/cformacion/${user?.centroFormacion}`
)
const filtrados = res.data.data.filter(
  (c) => c.ideleccion === Number(idEleccion)
)
setCandidatos(filtrados || [])""",
        badge="ANTES — pides TODO el centro y filtras en el cliente. Cambia a listar/:ideleccion SIN query.",
        badge_color=BADGE_RED,
        start_line=58,
        marks={2: "del", 4: "del", 5: "del", 6: "del"},
    )

    s["sofia_get_despues"] = shot(
        "sofia-get-despues",
        "src/pages/funcionario/GestionCandidatos.tsx",
        """const res = await api.get(`/api/candidatos/listar/${idEleccion}`)
const lista = res.data.data || []
setCandidatos(lista)

const bloques = {
  Mañana: lista.filter((c) => c.jornada === "Mañana"),
  Tarde: lista.filter((c) => c.jornada === "Tarde"),
  Noche: lista.filter((c) => c.jornada === "Noche"),
}
// Pinta tres <h5> Mañana / Tarde / Noche y una tabla (o cards) por bloque.""",
        badge="DESPUÉS — SIN ?jornada=. data[] trae los tres. Tú agrupas. No inventes otra URL.",
        badge_color=BADGE_GREEN,
        start_line=53,
        marks={1: "add", 5: "add", 6: "add", 7: "add", 8: "add", 9: "add"},
    )

    s["sofia_votaciones_antes"] = shot(
        "sofia-votaciones-antes",
        "src/pages/aprendiz/VotacionesActivasPage.tsx",
        """const response = await api.get(
  `/api/eleccionPorCentro/${user?.CentroFormacion}`
)
setVotaciones(response.data.eleccionesActivas)

const filtraJornada = votaciones.filter(
  (val) => val.jornada == user?.jornada
)

{filtraJornada.map((vote) => (
  <VotacionCard {...vote} />
))}""",
        badge="ANTES — filtra ELECCIONES por jornada. Con jornada null la urna queda vacía. QUITA el filter.",
        badge_color=BADGE_RED,
        start_line=19,
        marks={6: "del", 7: "del", 8: "del", 10: "del"},
    )

    s["sofia_votaciones_despues"] = shot(
        "sofia-votaciones-despues",
        "src/pages/aprendiz/VotacionesActivasPage.tsx",
        """const response = await api.get(
  `/api/eleccionPorCentro/${user?.CentroFormacion}`
)
setVotaciones(response.data.eleccionesActivas)

// UNA card por convocatoria. No filtres por jornada aquí.
{votaciones.map((vote) => (
  <VotacionCard {...vote} />
))}""",
        badge="DESPUÉS — el menú de la urna lista UNA elección del centro, no tres urnas.",
        badge_color=BADGE_GREEN,
        start_line=19,
        marks={6: "add", 7: "add", 8: "add"},
    )

    s["sofia_card"] = shot(
        "sofia-card",
        "src/components/aprendiz/VotacionCard.tsx",
        """<Card.Title>{titulo}</Card.Title>
<Card.Text>{centro}</Card.Text>
{/* BORRA esto: no pintes jornada en la elección */}
<Card.Text>
  <span>Jornada:</span> {jornada === null ? "no disponible" : jornada}
</Card.Text>
<Button onClick={() => navigate(`/seleccion/${ideleccion}`)}>
  Participar
</Button>""",
        badge="QUITA el texto Jornada de la card. La franja se recorta en /seleccion, no aquí.",
        badge_color=BADGE_RED,
        start_line=17,
        marks={3: "del", 4: "del", 5: "del", 6: "del"},
    )

    s["sofia_urna"] = shot(
        "sofia-urna",
        "src/pages/aprendiz/SeleccionarCandidatoPage.tsx",
        """const { user } = useAuth()
const jornada = user?.jornada // 'Mañana' | 'Tarde' | 'Noche' | null

const response = await api.get(`/api/candidatos/listar/${id}`, {
  params: jornada ? { jornada } : {},
})
setCandidatos(response.data.data)

// Si jornada es null, NO armes modal “elige tu jornada”.
// Eso es otro paquete. Deja el GET sin query y listo.""",
        badge="PEGA — F12 debe mostrar ?jornada=Tarde. El login ya trajo data.jornada del grupo.",
        badge_color=BADGE_GREEN,
        start_line=10,
        marks={1: "add", 2: "add", 4: "add", 5: "add"},
    )

    s["http_alex_post"] = http_shot(
        "http-alex-post",
        title="ALEX  ·  crear  ·  esto pegas en Thunder. NO es el PUT.",
        method="POST",
        url="/api/eleccion/crear",
        warn="NO pongas jornada. Si la pones y te sale 400 “La jornada no es válida”, el if viejo sigue ahí.",
        body="""{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-05",
  "hora_inicio": "2026-09-01T08:00:00.000Z",
  "hora_fin": "2026-09-05T16:00:00.000Z"
}""",
        status="201",
        response="""{
  "message": "Eleccion creada con exito",
  "eleccion": {
    "ideleccion": 12,
    "idcentro_formacion": 1,
    "nombre": "Representante de centro 2026",
    "jornada": null,
    "fecha_inicio": "2026-09-01T00:00:00.000Z",
    "fecha_fin": "2026-09-05T00:00:00.000Z"
  }
}""",
        ok_when="201 + message “Eleccion creada con exito” + jornada null. No 400.",
    )

    s["http_alex_put"] = http_shot(
        "http-alex-put",
        title="ALEX  ·  actualizar  ·  cambia el :idEleccion por el que te devolvió el POST",
        method="PUT",
        url="/api/eleccionActualizar/12",
        warn="Mismos campos que el crear. NO mandes jornada. Status 200, no 201.",
        body="""{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026 (horario ampliado)",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-06",
  "hora_inicio": "2026-09-01T08:00:00.000Z",
  "hora_fin": "2026-09-06T18:00:00.000Z"
}""",
        status="200",
        response="""{
  "message": "Eleccion actualizada con exito",
  "eleccion": {
    "ideleccion": 12,
    "nombre": "Representante de centro 2026 (horario ampliado)",
    "jornada": null,
    "fecha_fin": "2026-09-06T00:00:00.000Z"
  }
}""",
        ok_when="200 + “Eleccion actualizada con exito”. El nombre/fecha que mandaste quedó guardado.",
    )

    s["http_alex_mal"] = http_shot(
        "http-alex-mal",
        title="ALEX  ·  si AÚN te sale esto, no está LISTO (el if de jornada sigue vivo)",
        method="POST",
        url="/api/eleccion/crear",
        warn="Esto es el FALLO. No marques LISTO. Vuelve a quitar jornada del only y borra el if.",
        body="""{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-05",
  "hora_inicio": "2026-09-01T08:00:00.000Z",
  "hora_fin": "2026-09-05T16:00:00.000Z"
}""",
        status="400",
        response="""{
  "message": "La jornada no es válida"
}""",
        ok_when="Si ves 400 con este texto, el crear AÚN exige jornada. No es LISTO.",
        listo=False,
    )

    s["http_maicol_post"] = http_shot(
        "http-maicol-post",
        title="MAICOL  ·  crear candidato  ·  hazlo TRES veces (Mañana, Tarde, Noche) mismo tarjetón 01",
        method="POST",
        url="/api/candidatos/crear",
        warn="Body = form-data (no JSON puro). jornada es NUEVO. Grafía: Mañana / Tarde / Noche (con ñ).",
        body_label="Campos del form-data (el POST, no el GET):",
        body="""ideleccion        = 12
idaprendiz        = 401
nombres           = Ana Pérez
propuesta         = Más bienestar en talleres
numero_tarjeton   = 01
jornada           = Tarde
foto              = (archivo jpg opcional)""",
        status="201",
        response="""{
  "message": "Candidato registrado exitosamente",
  "data": {
    "idcandidatos": 88,
    "ideleccion": 12,
    "numero_tarjeton": "01",
    "jornada": "Tarde"
  }
}""",
        ok_when="201 las TRES veces con tarjetón 01 (una por jornada). Si el 2º da “ya existe”, el unique viejo sigue.",
    )

    s["http_maicol_get_all"] = http_shot(
        "http-maicol-get-all",
        title="MAICOL  ·  listar SIN filtro  ·  gestión ve los tres bloques",
        method="GET",
        url="/api/candidatos/listar/12",
        body=None,
        status="200",
        response="""{
  "message": "Candidatos obtenidos correctamente",
  "data": [
    { "numero_tarjeton": "01", "jornada": "Mañana" },
    { "numero_tarjeton": "01", "jornada": "Tarde" },
    { "numero_tarjeton": "01", "jornada": "Noche" }
  ]
}""",
        ok_when="200 y data.length = 3. Sin ?jornada= salen las tres franjas.",
    )

    s["http_maicol_get_tarde"] = http_shot(
        "http-maicol-get-tarde",
        title="MAICOL  ·  listar CON filtro  ·  misma URL, query nueva. Esto usa la urna.",
        method="GET",
        url="/api/candidatos/listar/12?jornada=Tarde",
        warn="No crees otra ruta. Es el mismo GET + ?jornada=Tarde (ñ y mayúscula).",
        body=None,
        status="200",
        response="""{
  "message": "Candidatos obtenidos correctamente",
  "data": [
    { "numero_tarjeton": "01", "jornada": "Tarde" }
  ]
}""",
        ok_when="200 y data.length = 1 (solo Tarde). Mañana y Noche no salen.",
    )

    s["http_mebel_centro"] = http_shot(
        "http-mebel-centro",
        title="MEBEL  ·  GET por centro  ·  una card, SIN clave jornada",
        method="GET",
        url="/api/eleccionPorCentro/1",
        warn="Cambia el 1 por tu idcentro_formacion. En el JSON NO debe existir “jornada”.",
        body=None,
        status="200",
        response="""{
  "message": "Elecciones por centros de formacion traidos correctamente",
  "eleccionesActivas": [
    {
      "ideleccion": 12,
      "titulo": "Representante de centro 2026",
      "fechaInicio": "...",
      "fechaFin": "...",
      "centro": "Centro ejemplo",
      "horaInicio": "...",
      "horaFin": "..."
    }
  ]
}""",
        ok_when="200, UNA fila por convocatoria, y ninguna clave jornada en el objeto.",
    )

    s["http_mebel_jornada"] = http_shot(
        "http-mebel-jornada",
        title="MEBEL  ·  GET urna  ·  misma URL de siempre; ahora recorta CANDIDATOS",
        method="GET",
        url="/api/eleccionJornada/listar?jornada=Tarde",
        warn="No renombres la URL. La elección sale igual; dentro, solo candidatos de Tarde.",
        body=None,
        status="200",
        response="""{
  "message": "Elecciones filtradas por jornada",
  "elecciones": [
    {
      "ideleccion": 12,
      "nombre": "Representante de centro 2026",
      "candidato": [
        { "numero_tarjeton": "01", "jornada": "Tarde" }
      ]
    }
  ]
}""",
        ok_when="200, la elección aparece, y candidato[] no trae Mañana ni Noche.",
    )

    s["http_login_aprendiz"] = http_shot(
        "http-login-aprendiz",
        title="SOFIA  ·  el login YA trae jornada. No armes pantalla nueva.",
        method="POST",
        url="/api/aprendiz/login",
        warn="Esto ya existe. Solo LÉELO. data.jornada sale del grupo. Si viene null, no armes modal.",
        body="""{
  "email": "aprendiz.tarde@sena.edu.co",
  "password": "********"
}""",
        status="200",
        response="""{
  "success": true,
  "data": {
    "id": 401,
    "nombre": "Luis",
    "perfil": "Aprendiz",
    "jornada": "Tarde",
    "CentroFormacion": 1
  }
}""",
        ok_when="200 y data.jornada es Mañana, Tarde, Noche o null. Eso es lo que usa /seleccion.",
    )

    s["net_paula_post"] = network_shot(
        "net-paula-post",
        title="Paula  ·  crear elección  ·  F12 → Network",
        method="POST",
        url="/api/eleccion/crear",
        status="201",
        kind="Request payload  ·  JSON",
        payload="""{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-05",
  "hora_inicio": "2026-09-01 08:00:00",
  "hora_fin": "2026-09-05 16:00:00"
}""",
        warn="Cuenta las claves: NO puede aparecer jornada. El centro es el de user.centroFormacion.",
        ok_when="201 + el JSON de la izquierda SIN jornada + response.eleccion.jornada = null.",
    )

    s["net_paula_put"] = network_shot(
        "net-paula-put",
        title="Paula  ·  editar elección  ·  F12 → Network",
        method="PUT",
        url="/api/eleccionActualizar/12",
        status="200",
        kind="Request payload  ·  JSON  (sí hay body, no va vacío)",
        payload="""{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026 (horario ampliado)",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-06",
  "hora_inicio": "2026-09-01T08:00:00",
  "hora_fin": "2026-09-06T18:00:00"
}""",
        warn="El 12 es eleccion.ideleccion. Mismos campos que el POST. Sin jornada.",
        ok_when="200 + “Eleccion actualizada con exito” + el nombre/fecha que cambiaste quedó.",
    )

    s["net_paula_mal"] = network_shot(
        "net-paula-mal",
        title="Paula  ·  si AÚN ves jornada en el payload, no está LISTO",
        method="POST",
        url="/api/eleccion/crear",
        status="201 o 400",
        kind="Request payload  ·  esto está MAL",
        payload="""{
  "idcentro_formacion": 1,
  "nombre": "Representante de centro 2026",
  "jornada": "Mañana",
  "fecha_inicio": "2026-09-01",
  "fecha_fin": "2026-09-05",
  "hora_inicio": "2026-09-01 08:00:00",
  "hora_fin": "2026-09-05 16:00:00"
}""",
        warn="Si jornada sigue en el JSON, el select no se quitó o el state sigue en el post.",
        ok_when="El payload todavía tiene jornada. Vuelve a FormEleccion.tsx y borra esa clave.",
        listo=False,
    )

    s["net_sofia_post"] = network_shot(
        "net-sofia-post",
        title="Sofia  ·  crear candidato  ·  F12 → Payload → Form Data",
        method="POST",
        url="/api/candidatos/crear",
        status="201",
        kind="Form Data  (NO es JSON puro — Content-Type: multipart/form-data)",
        payload="""ideleccion: 12
idaprendiz: 401
nombres: Ana Pérez
propuesta: Más bienestar en talleres
numero_tarjeton: 01
jornada: Tarde
foto: (binary)""",
        warn="La línea jornada tiene que existir y decir Mañana, Tarde o Noche (con ñ). Repite tres veces, tarjetón 01.",
        ok_when="201 “Candidato registrado exitosamente” y Form Data muestra jornada. Las tres altas pasan.",
    )

    s["net_sofia_urna"] = network_shot(
        "net-sofia-urna",
        title="Sofia  ·  tarjetón  ·  F12 → la petición GET",
        method="GET",
        url="/api/candidatos/listar/12?jornada=Tarde",
        status="200",
        kind="Query string  (no hay body)",
        payload="""Request URL:
http://localhost:5173/api/candidatos/listar/12?jornada=Tarde

Query:
  jornada = Tarde

Response data[]: solo candidatos con jornada Tarde.""",
        warn="Si la URL NO trae ?jornada=, el aprendiz ve las tres franjas. Eso no es LISTO.",
        ok_when="La URL lleva ?jornada=Tarde (ñ) y en pantalla solo sale el bloque Tarde.",
    )

    s["net_sofia_mal"] = network_shot(
        "net-sofia-mal",
        title="Sofia  ·  urna MAL  ·  GET sin query = ve a todo el mundo",
        method="GET",
        url="/api/candidatos/listar/12",
        status="200",
        kind="Query string  ·  esto está MAL en la urna (en gestión SÍ va así)",
        payload="""Request URL:
/api/candidatos/listar/12

(sin ?jornada=)

Response data[]:
  01 Mañana, 01 Tarde, 01 Noche""",
        warn="En GESTIÓN este GET sin query está bien. En la URNA (/seleccion) tiene que ir ?jornada=.",
        ok_when="La urna llamó listar/:id SIN query y el aprendiz vio Mañana+Tarde+Noche.",
        listo=False,
    )

    return s


def build():
    shots = make_shots()
    doc = Document()
    doc.styles["Normal"].font.name = "Arial"
    doc.styles["Normal"].font.size = Pt(11)
    header_footer(doc)
    escribir_pasos(doc, shots, {
        "add_p": add_p,
        "add_h": add_h,
        "add_table": add_table,
        "callout": callout,
        "photo": photo,
        "dicc": dicc,
        "paso": paso,
        "cambio": cambio,
        "sql_block": sql_block,
        "banner": banner,
    })
    doc.save(OUT)
    print(f"OK {OUT}")


if __name__ == "__main__":
    build()
