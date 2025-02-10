from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import matplotlib.font_manager as fm


class ImageProcessor:
    """
    Класс для обработки изображений.
    """
    def __init__(self):
        """
          Конструктор класса обработки изображений.
          """
        self.image = None

    def load_image(self, file_path):
        """
        Загружает изображение.
        """
        self.image = Image.open(file_path)

    def save_image(self, output_path):
        """
        Сохраняет изображение.
        """
        if self.image:
            self.image.save(output_path)

    def get_font_path(self, font_name):
        """
        Возвращает путь к шрифту по его имени.
        """
        for font in fm.fontManager.ttflist:
            if font.name == font_name:
                print(f'get_font_path: {font.name}')
                return font.fname
        return None

    def add_text(self, top_text, bottom_text, font_is_font, is_bold=False, is_italic=False, is_underline=False, font_size=30, font_path=None):
        """
        Добавляет текст на изображение.
        """
        if self.image:
            try:
                draw = ImageDraw.Draw(self.image)
                font_path = self.get_font_path(font_is_font.actual()["family"])
                print(font_path)
                if font_path:
                    if is_bold:
                        font = ImageFont.truetype(font_path, font_size)  # Жирный шрифт
                    if is_italic:
                        font = ImageFont.truetype(font_path, font_size)  # Курсивный шрифт
                    if is_underline:
                        # Подчеркивание текста (не поддерживается напрямую в Pillow)
                        pass
                    print(f"Найден шрифт:font {font_path}")
                else:
                    font = ImageFont.load_default(font_size)
                    print(f"Не найден шрифт: {font_path}, используется шрифт по умолчанию{font}")
                # Перенос текста
                max_width = self.image.width - 20
                top_text_lines = wrap(top_text, width=max_width // font_size)
                bottom_text_lines = wrap(bottom_text, width=max_width // font_size)

                # Добавление верхнего текста
                y = 10
                for line in top_text_lines:
                    draw.text((10, y), line, fill="white", font=font)
                    print(font)
                    y += font_size + 5

                # Добавление нижнего текста
                y = self.image.height - 50
                for line in bottom_text_lines:
                    draw.text((10, y), line, fill="white", font=font)
                    y += font_size + 5
            except Exception as e:
                print(f"Ошибка при добавлении текста: {e}")

    def get_image(self):
        """
        Возвращает текущее изображение.
        """
        return self.image

    def resize_image(self, max_width, max_height):
        """
        Масштабирует изображение с сохранением пропорций.
        """
        if self.image:
            width, height = self.image.size
            ratio = min(max_width / width, max_height / height)
            new_size = (int(width * ratio), int(height * ratio))
            return self.image.resize(new_size, Image.Resampling.LANCZOS)
        return None

    def rotate_image(self, angle):
        """
        Поворачивает изображение на заданный угол.
        """
        if self.image:
            self.image = self.image.rotate(angle, Image.Resampling.NEAREST)
        return None
