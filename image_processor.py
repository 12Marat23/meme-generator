from tkinter import messagebox
import logging
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
import matplotlib.font_manager as fm

logging.basicConfig(level=logging.INFO)


class ImageProcessor:
    """
    Класс для обработки изображений.
    """

    def __init__(self):
        """
          Конструктор класса обработки изображений.
          """
        self.image = None
        self.original_image = None

    def load_image(self, file_path):
        """
        Загружает изображение.
        """
        self.image = Image.open(file_path)
        self.original_image = self.image.copy()

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
                return font.fname
        logging.error(f"Шрифт не найден: {font_name}")
        return None

    def add_text(self, top_text, bottom_text, font_tk, alignment):
        """
        Добавляет текст на изображение.
        """
        if self.image:
            font = font_tk.actual()["family"]
            font_size = font_tk.actual()["size"]
            logging.info(f'font = {font}, font_size = {font_size}')
            try:
                draw = ImageDraw.Draw(self.image)
                font_path = self.get_font_path(font)
                logging.info(font_path)
                if font_path:
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
                    logging.error(f"Не найден шрифт: {font_path}, используется шрифт по умолчанию{font}")

                # Перенос текста
                max_width = self.image.width - 20
                top_text_lines = wrap(top_text, width=max_width // font_size)
                bottom_text_lines = wrap(bottom_text, width=max_width // font_size)

                y_top = 10
                y_bottom = self.image.height - (font_size + 50)

                for line in top_text_lines:
                    # Используем textbbox для получения размеров текста
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    if alignment == "left":
                        x = 10
                    elif alignment == "center":
                        x = (self.image.width - text_width) // 2
                    elif alignment == "right":
                        x = self.image.width - text_width - 10

                    draw.text((x, y_top), line, fill="white", font=font)
                    y_top += text_height + 5

                    # Добавление нижнего текста с учетом выравнивания
                for line in bottom_text_lines:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]

                    if alignment == "left":
                        x = 10
                    elif alignment == "center":
                        x = (self.image.width - text_width) // 2
                    elif alignment == "right":
                        x = self.image.width - text_width - 10

                    draw.text((x, y_bottom), line, fill="white", font=font)
                    y_bottom += text_height + 5
            except Exception as e:
                logging.error(f"Ошибка при добавлении текста: {e}")
                messagebox.showerror("Ошибка", f"Не удалось добавить текст: {e}")

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

    def delete_image(self):
        """
        Очищает текст на изображении, перерисовывая его без текста.
        """
        if self.image:
            blank_image = Image.new("RGB", self.image.size, (240, 240, 240))
            self.image = blank_image

    def clear_text_on_image(self):
        """
        Очищает текст на изображении, перерисовывая его без текста.
        """
        if self.image:
            self.image = self.original_image.copy()
