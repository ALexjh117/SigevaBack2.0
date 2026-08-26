# -*- coding: utf-8 -*-
"""Capturas tipo editor para las guías SIGEVA."""
from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SHOTS = HERE / "_shots_eleccion"
SHOTS.mkdir(exist_ok=True)

BG = (30, 30, 30)
GUTTER = (37, 37, 38)
TAB = (45, 45, 45)
BAR = (51, 51, 51)
FG = (212, 212, 212)
NUM = (133, 133, 133)
KW = (86, 156, 214)
STR = (206, 145, 120)
CMT = (106, 153, 85)
FN = (220, 220, 170)
TYPE = (78, 201, 176)
NUMLIT = (181, 206, 168)
PUNCT = (200, 200, 200)
ADD_BG = (22, 50, 39)
DEL_BG = (58, 29, 29)
ADD_FG = (87, 171, 90)
DEL_FG = (244, 135, 113)
WHITE = (255, 255, 255)
BADGE_RED = (139, 30, 63)
BADGE_GREEN = (31, 122, 77)
BADGE_NAVY = (27, 58, 75)

KEYWORDS = {
    "async",
    "await",
    "if",
    "else",
    "return",
    "const",
    "let",
    "export",
    "default",
    "class",
    "try",
    "catch",
    "new",
    "from",
    "import",
    "type",
    "interface",
    "true",
    "false",
    "null",
    "undefined",
    "void",
    "number",
    "string",
    "public",
    "static",
    "declare",
    "extends",
    "function",
    "andWhere",
    "where",
    "first",
    "query",
    "create",
    "preload",
    "alter",
    "table",
    "add",
    "column",
    "drop",
    "not",
    "sql",
}

TOKEN = re.compile(
    r"(//.*?$)|('(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`)"
    r"|(\b\d+\b)|(\b[A-Za-z_][A-Za-z0-9_]*\b)|(\s+)|(.)",
    re.M,
)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = []
    if bold:
        names += [
            r"C:\Windows\Fonts\consolab.ttf",
            r"C:\Windows\Fonts\CascadiaCode.ttf",
        ]
    names += [
        r"C:\Windows\Fonts\consola.ttf",
        r"C:\Windows\Fonts\CascadiaMono.ttf",
        r"C:\Windows\Fonts\cour.ttf",
    ]
    for path in names:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _ui(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return _font(size, bold)


def _w(font, text: str) -> int:
    box = font.getbbox(text or " ")
    return box[2] - box[0]


def _h(font, text: str = "Ag") -> int:
    box = font.getbbox(text)
    return box[3] - box[1]


def _color(kind: str, token: str, nxt: str) -> tuple[int, int, int]:
    if kind == "cmt":
        return CMT
    if kind == "str":
        return STR
    if kind == "num":
        return NUMLIT
    if kind == "id":
        if token in KEYWORDS:
            return KW
        if nxt.startswith("("):
            return FN
        if token[:1].isupper():
            return TYPE
        return FG
    return PUNCT if kind == "other" else FG


def _tokens(line: str):
    for m in TOKEN.finditer(line):
        cmt, str_, num, ident, space, other = m.groups()
        if cmt:
            yield "cmt", cmt
        elif str_:
            yield "str", str_
        elif num:
            yield "num", num
        elif ident:
            yield "id", ident
        elif space:
            yield "sp", space
        else:
            yield "other", other or ""


def shot(
    name: str,
    filename: str,
    code: str,
    *,
    badge: str,
    badge_color: tuple[int, int, int] = BADGE_NAVY,
    start_line: int = 1,
    marks: dict[int, str] | None = None,
) -> Path:
    """marks: line number (1-based in the snippet) -> 'add' | 'del'"""
    marks = marks or {}
    lines = code.replace("\t", "  ").splitlines() or [""]
    code_font = _font(15)
    ui = _ui(13)
    ui_b = _ui(13, bold=True)
    num_font = _font(13)

    line_h = 22
    pad_x = 14
    gutter_w = 52
    tab_h = 36
    badge_h = 28
    max_code = max((_w(code_font, ln) for ln in lines), default=200)
    width = min(1100, max(720, gutter_w + pad_x * 2 + max_code + 24))
    height = badge_h + tab_h + 12 + line_h * len(lines) + 16

    img = Image.new("RGB", (width, height), BG)
    dr = ImageDraw.Draw(img)

    dr.rectangle([0, 0, width, badge_h], fill=badge_color)
    dr.text((12, 6), badge, font=ui_b, fill=WHITE)

    dr.rectangle([0, badge_h, width, badge_h + tab_h], fill=TAB)
    dr.ellipse([14, badge_h + 13, 24, badge_h + 23], fill=(255, 95, 86))
    dr.ellipse([30, badge_h + 13, 40, badge_h + 23], fill=(255, 189, 46))
    dr.ellipse([46, badge_h + 13, 56, badge_h + 23], fill=(39, 201, 63))
    dr.text((72, badge_h + 9), filename, font=ui, fill=(220, 220, 220))

    y0 = badge_h + tab_h
    dr.rectangle([0, y0, gutter_w, height], fill=GUTTER)

    y = y0 + 8
    for i, ln in enumerate(lines):
        n = start_line + i
        mark = marks.get(i + 1)
        if mark == "add":
            dr.rectangle([gutter_w, y - 2, width, y + line_h - 2], fill=ADD_BG)
            dr.rectangle([gutter_w, y - 2, gutter_w + 4, y + line_h - 2], fill=ADD_FG)
        elif mark == "del":
            dr.rectangle([gutter_w, y - 2, width, y + line_h - 2], fill=DEL_BG)
            dr.rectangle([gutter_w, y - 2, gutter_w + 4, y + line_h - 2], fill=DEL_FG)
        dr.text((gutter_w - 8 - _w(num_font, str(n)), y), str(n), font=num_font, fill=NUM)
        x = gutter_w + pad_x
        rest = ln
        toks = list(_tokens(ln))
        for ti, (kind, tok) in enumerate(toks):
            nxt = ""
            for kind2, tok2 in toks[ti + 1 :]:
                if kind2 != "sp":
                    nxt = tok2
                    break
            col = _color(kind, tok, nxt)
            if mark == "del" and kind != "cmt":
                col = DEL_FG
            if mark == "add" and kind != "cmt":
                col = tuple(min(255, c + 20) for c in col)
            dr.text((x, y), tok, font=code_font, fill=col)
            x += _w(code_font, tok)
        y += line_h

    path = SHOTS / f"{name}.png"
    img.save(path, "PNG")
    return path


def _wrap_lines(text: str, width: int = 68) -> list[str]:
    out: list[str] = []
    for raw in text.splitlines() or [""]:
        line = raw.replace("\t", "  ")
        if len(line) <= width:
            out.append(line)
            continue
        while len(line) > width:
            out.append(line[:width])
            line = "  " + line[width:]
        if line.strip():
            out.append(line)
    return out


def http_shot(
    name: str,
    *,
    title: str,
    method: str,
    url: str,
    body: str | None,
    status: str,
    response: str,
    ok_when: str,
    body_label: str = "Body que mandas (copia esto):",
    warn: str | None = None,
    listo: bool = True,
) -> Path:
    """Foto tipo Thunder/Postman: método, URL, JSON y respuesta esperada."""
    code_font = _font(13)
    ui = _ui(13)
    ui_b = _ui(14, bold=True)
    small = _ui(12)
    method_c = {
        "POST": (31, 122, 77),
        "PUT": (154, 107, 47),
        "GET": (27, 58, 75),
        "DELETE": (139, 30, 63),
    }.get(method, BADGE_NAVY)

    left = [body_label] + _wrap_lines(body if body is not None else "(sin body — solo URL)")
    right = [f"Si te dio bien  →  HTTP {status}"] + _wrap_lines(response)
    line_h = 19
    pad = 16
    col_w = 530
    header_h = 88
    warn_h = 32 if warn else 0
    n = max(len(left), len(right), 7)
    width = pad + col_w + 16 + col_w + pad
    height = header_h + warn_h + 8 + n * line_h + 22 + 52

    img = Image.new("RGB", (width, height), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    white = (255, 255, 255)
    card = (30, 30, 30)

    dr.rectangle((0, 0, width, 36), fill=method_c)
    dr.text((14, 8), title, font=ui_b, fill=white)

    dr.rounded_rectangle((pad, 48, pad + 72, 78), 4, fill=method_c)
    dr.text((pad + 12, 54), method, font=ui_b, fill=white)
    dr.text((pad + 86, 54), url, font=ui, fill=navy)

    y0 = header_h
    if warn:
        dr.rounded_rectangle((pad, y0, width - pad, y0 + 26), 5, fill=(254, 243, 199), outline=(146, 64, 14))
        dr.text((pad + 10, y0 + 5), warn, font=small, fill=(146, 64, 14))
        y0 += warn_h

    def panel(x, y, w, h, lines):
        dr.rounded_rectangle((x, y, x + w, y + h), 8, fill=card)
        yy = y + 10
        for i, ln in enumerate(lines):
            col = (180, 220, 190) if i == 0 else (212, 212, 212)
            font = ui_b if i == 0 else code_font
            dr.text((x + 12, yy), ln, font=font, fill=col)
            yy += line_h

    panel_h = 18 + n * line_h
    panel(pad, y0, col_w, panel_h, left)
    panel(pad + col_w + 16, y0, col_w, panel_h, right)

    fy = y0 + panel_h + 10
    if listo:
        dr.rounded_rectangle((pad, fy, width - pad, fy + 36), 6, fill=(232, 245, 238), outline=(31, 122, 77))
        dr.text((pad + 12, fy + 9), "Marca LISTO si Thunder/Postman te dio exactamente esto:  " + ok_when, font=small, fill=(31, 122, 77))
    else:
        dr.rounded_rectangle((pad, fy, width - pad, fy + 36), 6, fill=(253, 236, 236), outline=(139, 30, 63))
        dr.text((pad + 12, fy + 9), "NO marques LISTO si te dio esto:  " + ok_when, font=small, fill=(139, 30, 63))

    path = SHOTS / f"{name}.png"
    img.save(path, "PNG")
    return path


def diagram_flujo() -> Path:
    """Hoy: 3 elecciones. To-be: 1 elección, jornada en el candidato."""
    w, h = 1100, 420
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    title = _ui(18, True)
    body = _ui(14)
    small = _ui(13)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    muted = (74, 85, 99)
    white = (255, 255, 255)
    card = (255, 255, 255)
    line = (208, 213, 221)

    def round_rect(xy, fill, outline=None, r=10):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((28, 18), "Por qué se mueve la jornada (foto del flujo)", font=title, fill=navy)

    round_rect((24, 56, 530, 392), (232, 238, 242), line)
    dr.text((44, 72), "HOY  —  tres elecciones", font=_ui(15, True), fill=navy)
    dr.text((44, 98), "El funcionario crea una urna por jornada.", font=small, fill=muted)
    for i, label in enumerate(["Elección Mañana", "Elección Tarde", "Elección Noche"]):
        y = 140 + i * 72
        round_rect((48, y, 506, y + 58), card, line)
        dr.rectangle((48, y, 56, y + 58), fill=(139, 30, 63))
        dr.text((72, y + 10), label, font=_ui(14, True), fill=navy)
        dr.text((72, y + 32), "misma fecha · mismos candidatos “tipo” · urna aparte", font=small, fill=muted)

    round_rect((570, 56, 1076, 392), (232, 245, 238), line)
    dr.text((590, 72), "TO-BE  —  una elección del centro", font=_ui(15, True), fill=green)
    dr.text((590, 98), "Una ventana. Tres bloques de candidatos.", font=small, fill=muted)
    round_rect((594, 140, 1052, 368), card, line)
    dr.rectangle((594, 140, 602, 368), fill=green)
    dr.text((618, 156), "Elección Representante 2026", font=_ui(14, True), fill=navy)
    dr.text((618, 182), "Centro + fechas + horas. Sin jornada.", font=small, fill=muted)
    for i, label in enumerate(["Candidatos Mañana", "Candidatos Tarde", "Candidatos Noche"]):
        y = 218 + i * 44
        round_rect((618, y, 1028, y + 36), (232, 245, 238), (31, 122, 77))
        dr.text((634, y + 8), label, font=small, fill=green)

    path = SHOTS / "flujo-hoy-tobe.png"
    img.save(path, "PNG")
    return path


def diagram_carriles() -> Path:
    """Cinco carriles en paralelo: nadie amarra al otro."""
    w, h = 1100, 430
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    muted = (74, 85, 99)
    line = (208, 213, 221)
    white = (255, 255, 255)

    def rr(xy, fill, outline=line, r=8):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((24, 16), "Como se trabaja: cinco carriles a la vez", font=_ui(18, True), fill=navy)
    dr.text(
        (24, 44),
        "Nadie espera un merge. El SQL ya lo corrio cada uno. El flujo de exito se prueba al final, juntos.",
        font=_ui(13),
        fill=muted,
    )

    lanes = [
        ("Alex", "Back · crear", "eleccion_controller\n(arriba)", (232, 238, 242)),
        ("Mebel", "Back · listar", "FiltroJorElCen\n+ GET abajo", (232, 245, 238)),
        ("Maicol", "Back · candidato", "candidatos.ts\nservice + GET", (232, 238, 242)),
        ("Paula", "Front · form", "Crear eleccion\nsin jornada", (232, 245, 238)),
        ("Sofia", "Front · tarjeton", "Select jornada\n+ filtro urna", (232, 238, 242)),
    ]
    gap = 12
    x0 = 24
    lane_w = (w - 48 - gap * 4) / 5
    top = 86
    for i, (name, rol, files, bg) in enumerate(lanes):
        x = x0 + i * (lane_w + gap)
        rr((x, top, x + lane_w, 390), bg, (27, 58, 75) if i in (0, 1) else line)
        rr((x + 8, top + 10, x + lane_w - 8, top + 52), (27, 58, 75), (27, 58, 75))
        dr.text((x + 18, top + 22), name, font=_ui(16, True), fill=white)
        dr.text((x + 14, top + 68), rol, font=_ui(12, True), fill=navy)
        for li, line_t in enumerate(files.split("\n")):
            dr.text((x + 14, top + 98 + li * 20), line_t, font=_ui(12), fill=muted)
        rr((x + 8, 330, x + lane_w - 8, 372), (31, 122, 77), (31, 122, 77))
        dr.text((x + 18, 342), "Tu LISTO", font=_ui(13, True), fill=white)

    path = SHOTS / "carriles-paralelo.png"
    img.save(path, "PNG")
    return path


def diagram_archivo_split() -> Path:
    """Alex arriba, Mebel abajo: mismo archivo, no se amarran."""
    w, h = 1100, 420
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    muted = (74, 85, 99)
    line = (208, 213, 221)
    white = (255, 255, 255)
    card = (255, 255, 255)

    def rr(xy, fill, outline=line, r=8):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((24, 16), "Mismo archivo, dos mitades  ·  eleccion_controller.ts", font=_ui(18, True), fill=navy)
    dr.text(
        (24, 44),
        "No es “espera a Alex”. Es: tu mitad no se cruza con la de el. Los dos avanzan el mismo dia.",
        font=_ui(13),
        fill=muted,
    )

    rr((40, 80, 620, 392), card, navy)
    dr.rectangle((40, 80, 52, 392), fill=navy)
    dr.text((68, 96), "app/controllers/eleccion_controller.ts", font=_ui(14, True), fill=navy)

    rr((64, 130, 596, 236), (232, 238, 242), navy)
    dr.rectangle((64, 130, 76, 236), fill=(27, 58, 75))
    dr.text((92, 144), "ARRIBA  —  Alex", font=_ui(15, True), fill=navy)
    dr.text((92, 172), "crearEleccion", font=_ui(13), fill=muted)
    dr.text((92, 194), "actualizarEleccion", font=_ui(13), fill=muted)
    dr.text((92, 216), "Quita jornada del POST y del PUT", font=_ui(12), fill=muted)

    rr((64, 252, 596, 372), (232, 245, 238), green)
    dr.rectangle((64, 252, 76, 372), fill=green)
    dr.text((92, 266), "ABAJO  —  Mebel", font=_ui(15, True), fill=green)
    dr.text((92, 294), "traerPorCentroFormacion  /  Todas", font=_ui(13), fill=muted)
    dr.text((92, 316), "traerPorJornada  /  traerFiltrado", font=_ui(13), fill=muted)
    dr.text((92, 338), "FiltroJorElCen.ts es SOLO de Mebel (otro archivo)", font=_ui(12), fill=muted)

    rr((652, 80, 1060, 220), (232, 238, 242), navy)
    dr.text((672, 100), "Alex termina cuando", font=_ui(14, True), fill=navy)
    dr.text((672, 132), "El crear ya no pide jornada.", font=_ui(13), fill=muted)
    dr.text((672, 156), "No necesita el GET de Mebel", font=_ui(13), fill=muted)
    dr.text((672, 180), "para marcar su LISTO.", font=_ui(13), fill=muted)

    rr((652, 244, 1060, 392), (232, 245, 238), green)
    dr.text((672, 264), "Mebel termina cuando", font=_ui(14, True), fill=green)
    dr.text((672, 296), "El listado no manda jornada", font=_ui(13), fill=muted)
    dr.text((672, 320), "y el filtro recorta candidatos.", font=_ui(13), fill=muted)
    dr.text((672, 344), "No necesita el POST de Alex", font=_ui(13), fill=muted)
    dr.text((672, 368), "para marcar su LISTO.", font=_ui(13), fill=muted)

    path = SHOTS / "archivo-alex-mebel.png"
    img.save(path, "PNG")
    return path


def diagram_exito() -> Path:
    """Flujo de exito: una eleccion del centro, de punta a punta."""
    w, h = 1100, 520
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    muted = (74, 85, 99)
    line = (208, 213, 221)
    white = (255, 255, 255)

    def rr(xy, fill, outline=line, r=8):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((24, 14), "Flujo de exito (cuando los cinco marcaron LISTO)", font=_ui(18, True), fill=navy)
    dr.text(
        (24, 42),
        "No es un voto. Es: entrar a Elecciones, crear UNA para todo el centro, ver el tarjeton recortado.",
        font=_ui(13),
        fill=muted,
    )

    steps = [
        ("1", "Gestion", "Funcionario entra\na Elecciones"),
        ("2", "Crear", "Una eleccion del\ncentro. Sin jornada."),
        ("3", "Listado", "Una sola card.\nNo tres urnas."),
        ("4", "Candidatos", "Tres personas:\nManana, Tarde, Noche"),
        ("5", "Urna", "Aprendiz Tarde ve\nESA eleccion"),
        ("6", "Exito", "Solo candidatos\nde Tarde"),
    ]
    y = 86
    box_w = 160
    gap = 18
    x0 = 24
    for i, (num, title, body) in enumerate(steps):
        x = x0 + i * (box_w + gap)
        fill = (31, 122, 77) if i == 5 else (255, 255, 255)
        ol = green if i == 5 else navy
        rr((x, y, x + box_w, y + 168), fill, ol)
        badge = (31, 122, 77) if i != 5 else (27, 58, 75)
        dr.ellipse((x + 12, y + 12, x + 42, y + 42), fill=badge)
        dr.text((x + 22, y + 16), num, font=_ui(14, True), fill=white)
        tc = white if i == 5 else navy
        dr.text((x + 12, y + 56), title, font=_ui(15, True), fill=tc)
        for li, lt in enumerate(body.split("\n")):
            dr.text((x + 12, y + 86 + li * 20), lt, font=_ui(12), fill=white if i == 5 else muted)
        if i < 5:
            ax = x + box_w + 2
            dr.polygon([(ax, y + 80), (ax + 12, y + 88), (ax, y + 96)], fill=green)

    rr((24, 278, 1076, 496), (255, 255, 255), navy)
    dr.text((44, 296), "Que tienen que ver en pantalla (exito de verdad)", font=_ui(15, True), fill=navy)
    lines = [
        "En Gestion: menu Elecciones → Nueva → nombre, fechas y horas. NO aparece jornada. Guardar.",
        "El listado del centro muestra ESA convocatoria una sola vez (no Manana / Tarde / Noche aparte).",
        "En esa eleccion: inscribir tres aprendices, tarjeton 01, uno por jornada. Los tres quedan.",
        "En la Urna, un aprendiz cuya jornada de login es Tarde: ve esa eleccion y solo el bloque Tarde.",
        "Si eso pasa, el paquete sirvio. No hace falta votar ni generar acta para declararlo.",
    ]
    for i, t in enumerate(lines):
        dr.text((44, 332 + i * 28), str(i + 1) + ".  " + t, font=_ui(13), fill=muted)

    path = SHOTS / "flujo-exito.png"
    img.save(path, "PNG")
    return path


def network_shot(
    name: str,
    *,
    title: str,
    method: str,
    url: str,
    status: str,
    kind: str,
    payload: str,
    ok_when: str,
    warn: str | None = None,
    listo: bool = True,
) -> Path:
    """Foto tipo F12 → Network: URL, payload y cuándo marcar LISTO."""
    code_font = _font(13)
    ui = _ui(13)
    ui_b = _ui(14, bold=True)
    small = _ui(12)
    method_c = {
        "POST": (31, 122, 77),
        "PUT": (154, 107, 47),
        "GET": (27, 58, 75),
    }.get(method, BADGE_NAVY)

    lines = _wrap_lines(payload, 88)
    line_h = 20
    pad = 16
    header_h = 96
    warn_h = 34 if warn else 0
    n = max(len(lines), 6)
    width = 1100
    panel_h = 28 + n * line_h
    height = header_h + warn_h + panel_h + 70

    img = Image.new("RGB", (width, height), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    white = (255, 255, 255)
    card = (30, 30, 30)

    dr.rectangle((0, 0, width, 38), fill=(55, 55, 55))
    dr.text((14, 10), "Chrome DevTools  ·  Network  ·  " + title, font=ui_b, fill=white)

    dr.rounded_rectangle((pad, 50, pad + 72, 80), 4, fill=method_c)
    dr.text((pad + 12, 56), method, font=ui_b, fill=white)
    dr.text((pad + 86, 56), url, font=ui, fill=navy)

    st_fill = (31, 122, 77) if listo else (139, 30, 63)
    st_w = 8 + _w(ui_b, status)
    dr.rounded_rectangle((width - pad - st_w - 16, 50, width - pad, 80), 4, fill=st_fill)
    dr.text((width - pad - st_w - 6, 56), status, font=ui_b, fill=white)

    y0 = header_h
    if warn:
        dr.rounded_rectangle((pad, y0, width - pad, y0 + 28), 5, fill=(254, 243, 199), outline=(146, 64, 14))
        dr.text((pad + 10, y0 + 6), warn, font=small, fill=(146, 64, 14))
        y0 += warn_h

    dr.rounded_rectangle((pad, y0, width - pad, y0 + panel_h), 8, fill=card)
    dr.text((pad + 14, y0 + 8), kind + "  (F12 → la petición → Payload)", font=ui_b, fill=(180, 220, 190))
    yy = y0 + 32
    for ln in lines:
        col = (158, 206, 146) if "jornada" in ln.lower() else (212, 212, 212)
        dr.text((pad + 14, yy), ln, font=code_font, fill=col)
        yy += line_h

    fy = y0 + panel_h + 12
    if listo:
        dr.rounded_rectangle((pad, fy, width - pad, fy + 40), 6, fill=(232, 245, 238), outline=(31, 122, 77))
        dr.text((pad + 12, fy + 11), "Marca LISTO si Network te dio exactamente esto:  " + ok_when, font=small, fill=(31, 122, 77))
    else:
        dr.rounded_rectangle((pad, fy, width - pad, fy + 40), 6, fill=(253, 236, 236), outline=(139, 30, 63))
        dr.text((pad + 12, fy + 11), "NO marques LISTO si ves esto:  " + ok_when, font=small, fill=(139, 30, 63))

    path = SHOTS / f"{name}.png"
    img.save(path, "PNG")
    return path


def diagram_paula_listo() -> Path:
    """Pantalla LISTO de Paula: form sin jornada, listado una fila."""
    w, h = 1100, 540
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    red = (139, 30, 63)
    muted = (74, 85, 99)
    line = (208, 213, 221)
    white = (255, 255, 255)
    card = (255, 255, 255)

    def rr(xy, fill, outline=line, r=8):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((24, 14), "Paula LISTO — asi se ve Gestion (no es un mock: es tu pantalla)", font=_ui(18, True), fill=navy)
    dr.text((24, 42), "Izquierda = hoy (tres urnas). Derecha = cuando tu parte cerro.", font=_ui(13), fill=muted)

    rr((24, 72, 538, 518), (253, 236, 236), red)
    dr.text((44, 86), "HOY  —  no esta LISTO", font=_ui(15, True), fill=red)
    rr((44, 118, 518, 268), card, red)
    dr.text((56, 128), "Crear nueva eleccion", font=_ui(13, True), fill=navy)
    dr.text((56, 152), "Nombre  [ Representante 2026          ]", font=_ui(12), fill=muted)
    dr.text((56, 176), "Jornada [ Mañana ▼ ]   ← este combo se QUITA", font=_ui(12), fill=red)
    dr.text((56, 200), "Fechas y horas...", font=_ui(12), fill=muted)
    dr.text((56, 232), "Network: el JSON lleva  jornada: \"Mañana\"", font=_ui(12), fill=red)

    rr((44, 284, 518, 498), card, red)
    dr.text((56, 296), "Listado /elecciones", font=_ui(13, True), fill=navy)
    headers = ["Titulo", "Inicio", "Fin", "Jornada"]
    for i, hd in enumerate(headers):
        dr.text((56 + i * 110, 324), hd, font=_ui(12, True), fill=muted)
    rows = [
        ("Repr. 2026", "01/09", "05/09", "Mañana"),
        ("Repr. 2026", "01/09", "05/09", "Tarde"),
        ("Repr. 2026", "01/09", "05/09", "Noche"),
    ]
    for ri, row in enumerate(rows):
        y = 350 + ri * 42
        rr((52, y, 510, y + 36), (254, 243, 199), red)
        for ci, cell in enumerate(row):
            dr.text((56 + ci * 110, y + 8), cell, font=_ui(12), fill=navy)

    rr((562, 72, 1076, 518), (232, 245, 238), green)
    dr.text((582, 86), "LISTO  —  una convocatoria del centro", font=_ui(15, True), fill=green)
    rr((582, 118, 1056, 268), card, green)
    dr.text((594, 128), "Crear nueva eleccion", font=_ui(13, True), fill=navy)
    dr.text((594, 152), "Nombre  [ Representante 2026          ]", font=_ui(12), fill=muted)
    dr.text((594, 176), "(no hay combo de jornada)", font=_ui(12), fill=green)
    dr.text((594, 200), "Fechas y horas...  Centro = sesion", font=_ui(12), fill=muted)
    dr.text((594, 232), "Network: 201 y el JSON NO tiene jornada", font=_ui(12), fill=green)

    rr((582, 284, 1056, 498), card, green)
    dr.text((594, 296), "Listado /elecciones", font=_ui(13, True), fill=navy)
    for i, hd in enumerate(["Titulo", "Inicio", "Fin", "Estado"]):
        dr.text((594 + i * 110, 324), hd, font=_ui(12, True), fill=muted)
    rr((590, 350, 1048, 430), (232, 245, 238), green)
    dr.text((598, 362), "Representante de centro 2026", font=_ui(13, True), fill=navy)
    dr.text((598, 386), "01/09/2026  -  05/09/2026     Activa", font=_ui(12), fill=muted)
    dr.text((598, 410), "Una sola fila. No hay columna Jornada.", font=_ui(12), fill=green)

    path = SHOTS / "paula-pantalla-listo.png"
    img.save(path, "PNG")
    return path


def diagram_sofia_listo() -> Path:
    """Pantalla LISTO de Sofia: select, 3 bloques, urna recortada."""
    w, h = 1100, 560
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    muted = (74, 85, 99)
    line = (208, 213, 221)
    white = (255, 255, 255)
    card = (255, 255, 255)

    def rr(xy, fill, outline=line, r=8):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((24, 14), "Sofia LISTO — tres fotos en una: form, gestion, urna", font=_ui(18, True), fill=navy)
    dr.text((24, 42), "El recorte es de CANDIDATOS, no de crear tres elecciones.", font=_ui(13), fill=muted)

    rr((24, 76, 360, 536), card, navy)
    dr.rectangle((24, 76, 36, 536), fill=navy)
    dr.text((48, 90), "1. Form candidato", font=_ui(14, True), fill=navy)
    dr.text((48, 118), "/gestion-candidatos/:id", font=_ui(12), fill=muted)
    rr((48, 148, 336, 188), (232, 245, 238), green)
    dr.text((60, 158), "Jornada del tarjeton *", font=_ui(12, True), fill=green)
    rr((48, 200, 336, 248), (248, 250, 252), navy)
    dr.text((60, 214), "Tarde                    ▼", font=_ui(13), fill=navy)
    for i, t in enumerate(["Mañana", "Tarde  ← elegida", "Noche"]):
        dr.text((60, 264 + i * 24), t, font=_ui(12), fill=green if i == 1 else muted)
    dr.text((48, 348), "Network Form Data:", font=_ui(12, True), fill=navy)
    dr.text((48, 372), "numero_tarjeton = 01", font=_ui(12), fill=muted)
    dr.text((48, 396), "jornada = Tarde", font=_ui(13, True), fill=green)
    dr.text((48, 428), "POST 201 las TRES veces", font=_ui(12), fill=green)
    dr.text((48, 452), "(mismo 01, una jornada cada una)", font=_ui(12), fill=muted)
    dr.text((48, 488), "Si el 2o 01 falla = unique de Maicol", font=_ui(11), fill=muted)

    rr((380, 76, 720, 536), card, navy)
    dr.rectangle((380, 76, 392, 536), fill=green)
    dr.text((404, 90), "2. Gestion — 3 bloques", font=_ui(14, True), fill=navy)
    dr.text((404, 118), "GET /api/candidatos/listar/12", font=_ui(12), fill=muted)
    dr.text((404, 138), "(SIN ?jornada=)", font=_ui(12), fill=muted)
    for i, (title, who) in enumerate(
        [("Mañana", "01  Ana"), ("Tarde", "01  Luis"), ("Noche", "01  Maria")]
    ):
        y = 172 + i * 108
        rr((404, y, 696, y + 96), (232, 245, 238), green)
        dr.text((416, y + 10), title, font=_ui(14, True), fill=green)
        dr.text((416, y + 38), who + "  ·  tarjeton 01", font=_ui(12), fill=navy)
        dr.text((416, y + 62), "Misma eleccion, otra franja", font=_ui(11), fill=muted)

    rr((740, 76, 1076, 536), card, navy)
    dr.rectangle((740, 76, 752, 536), fill=(27, 58, 75))
    dr.text((764, 90), "3. Urna aprendiz Tarde", font=_ui(14, True), fill=navy)
    dr.text((764, 118), "/votaciones  →  /seleccion/12", font=_ui(12), fill=muted)
    rr((764, 152, 1052, 220), (232, 245, 238), green)
    dr.text((776, 162), "Una eleccion del centro", font=_ui(13, True), fill=navy)
    dr.text((776, 186), "NO tres menus Mañana/Tarde/Noche", font=_ui(12), fill=green)
    dr.text((764, 236), "GET listar/12?jornada=Tarde", font=_ui(12, True), fill=navy)
    rr((764, 268, 1052, 360), (232, 245, 238), green)
    dr.text((776, 280), "Tarjeton 01  ·  Luis", font=_ui(13, True), fill=navy)
    dr.text((776, 306), "jornada: Tarde", font=_ui(12), fill=green)
    dr.text((776, 330), "Solo esta franja", font=_ui(12), fill=muted)
    rr((764, 380, 1052, 456), (253, 236, 236), (139, 30, 63))
    dr.text((776, 392), "NO sale Ana (Mañana)", font=_ui(12), fill=(139, 30, 63))
    dr.text((776, 416), "NO sale Maria (Noche)", font=_ui(12), fill=(139, 30, 63))
    dr.text((764, 476), "jornada sale del LOGIN.", font=_ui(12, True), fill=navy)
    dr.text((764, 500), "Si viene null: no armes modal.", font=_ui(12), fill=muted)

    path = SHOTS / "sofia-pantalla-listo.png"
    img.save(path, "PNG")
    return path


def diagram_urna_bug() -> Path:
    """El filtro viejo de elecciones rompe el modelo nuevo."""
    w, h = 1100, 420
    img = Image.new("RGB", (w, h), (248, 250, 252))
    dr = ImageDraw.Draw(img)
    navy = (27, 58, 75)
    green = (31, 122, 77)
    red = (139, 30, 63)
    muted = (74, 85, 99)
    line = (208, 213, 221)
    white = (255, 255, 255)
    card = (255, 255, 255)

    def rr(xy, fill, outline=line, r=8):
        dr.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=1)

    dr.text((24, 14), "Sofia — el bug que deja la urna vacia (VotacionesActivasPage)", font=_ui(18, True), fill=navy)
    dr.text(
        (24, 42),
        "Si filtras ELECCIONES por jornada, la convocatoria nueva (jornada null) desaparece. El recorte va en candidatos.",
        font=_ui(13),
        fill=muted,
    )

    rr((24, 80, 538, 392), (253, 236, 236), red)
    dr.text((44, 96), "HOY — esto rompe el flujo del back", font=_ui(14, True), fill=red)
    dr.text((44, 128), "votaciones.filter(val => val.jornada == user.jornada)", font=_ui(12), fill=navy)
    rr((44, 164, 518, 248), card, red)
    dr.text((56, 176), "Eleccion  jornada: null", font=_ui(13, True), fill=navy)
    dr.text((56, 204), "Aprendiz  jornada: Tarde", font=_ui(13), fill=muted)
    dr.text((56, 228), "null == Tarde  →  se tira la card", font=_ui(12), fill=red)
    dr.text((44, 272), "El aprendiz entra a /votaciones y no ve NADA.", font=_ui(13), fill=red)
    dr.text((44, 300), "Alex/Paula ya crearon la eleccion bien.", font=_ui(12), fill=muted)
    dr.text((44, 324), "El back ya no etiqueta la convocatoria.", font=_ui(12), fill=muted)
    dr.text((44, 348), "Este filter es el que hay que QUITAR.", font=_ui(12, True), fill=red)

    rr((562, 80, 1076, 392), (232, 245, 238), green)
    dr.text((582, 96), "LISTO — una card, recorte en el tarjeton", font=_ui(14, True), fill=green)
    dr.text((582, 128), "Pinta votaciones (eleccionesActivas) SIN filtrar.", font=_ui(12), fill=navy)
    rr((582, 164, 1056, 248), card, green)
    dr.text((594, 176), "Eleccion  Representante 2026", font=_ui(13, True), fill=navy)
    dr.text((594, 204), "Una card. Sin texto Jornada.", font=_ui(13), fill=muted)
    dr.text((594, 228), "Participar → /seleccion/12", font=_ui(12), fill=green)
    dr.text((582, 272), "Ahi si: GET listar/12?jornada=Tarde", font=_ui(13, True), fill=green)
    dr.text((582, 300), "user.jornada del login (ya viene del grupo).", font=_ui(12), fill=muted)
    dr.text((582, 324), "Solo candidatos de Tarde.", font=_ui(12), fill=muted)
    dr.text((582, 348), "Si user.jornada es null: no armes modal.", font=_ui(12), fill=muted)

    path = SHOTS / "sofia-urna-bug.png"
    img.save(path, "PNG")
    return path


