"""
Рендер сертификата о прохождении курса - накладывает имя студента,
название курса и дату на шаблон (assets/certificates/template_default.jpg).

Координаты и размеры подобраны конкретно под этот шаблон (1280x906,
текстовая зона x=75..740). Если дизайн шаблона сменится - подбирать
координаты заново (проще всего - наложить сетку, см. историю разработки).
"""
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')
TEMPLATE_PATH = os.path.join(ASSETS_DIR, 'certificates', 'template_default.jpg')
FONT_REGULAR = os.path.join(ASSETS_DIR, 'fonts', 'DejaVuSerif.ttf')
FONT_BOLD = os.path.join(ASSETS_DIR, 'fonts', 'DejaVuSerif-Bold.ttf')

TEXT_CENTER_X = 407
TEXT_MAX_WIDTH = 640
NAME_Y = 383
COURSE_Y = 508
DATE_CENTER_X = 176
DATE_MAX_WIDTH = 190
DATE_Y = 728
TEXT_COLOR = (20, 20, 20)
DATE_COLOR = (60, 60, 60)

MONTHS_ES = [
    'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',
]


def _fit_font(draw, text, font_path, max_width, start_size, min_size=14):
    """ Подбирает наибольший размер шрифта, при котором текст влезает в max_width. """
    size = start_size
    while size > min_size:
        font = ImageFont.truetype(font_path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 1
    return ImageFont.truetype(font_path, min_size)


def _draw_centered(draw, text, center_x, y, font_path, max_width, start_size, fill):
    font = _fit_font(draw, text, font_path, max_width, start_size)
    width = draw.textlength(text, font=font)
    draw.text((center_x - width / 2, y), text, font=font, fill=fill)


def format_date_es(dt):
    return f"{dt.day:02d} de {MONTHS_ES[dt.month - 1]} de {dt.year}"


def render_certificate(student_name, course_title, issued_at):
    """ Возвращает PNG-байты сертификата (BytesIO). """
    image = Image.open(TEMPLATE_PATH).convert('RGB')
    draw = ImageDraw.Draw(image)

    _draw_centered(draw, student_name, TEXT_CENTER_X, NAME_Y, FONT_BOLD, TEXT_MAX_WIDTH, 44, TEXT_COLOR)
    _draw_centered(draw, course_title, TEXT_CENTER_X, COURSE_Y, FONT_REGULAR, TEXT_MAX_WIDTH, 32, TEXT_COLOR)
    _draw_centered(draw, format_date_es(issued_at), DATE_CENTER_X, DATE_Y, FONT_REGULAR, DATE_MAX_WIDTH, 20, DATE_COLOR)

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
