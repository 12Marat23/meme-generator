from PIL import Image, ImageDraw, ImageFont

class ImageProcessor:
    def __init__(self):
        self.image = None

    def load_image(self, file_path):
        """Загружает изображение."""
        self.image = Image.open(file_path)

    def save_image(self, output_path):
        """Сохраняет изображение."""
        if self.image:
            self.image.save(output_path)

    def add_text(self, top_text, bottom_text,  font_size=30):
        """Добавляет текст на изображение."""
        if self.image:
            draw = ImageDraw.Draw(self.image)
            font = ImageFont.truetype('arial.ttf', font_size)

            # Добавление верхнего текста
            draw.text((10, 10), top_text, fill="white", font=font)

            # Добавление нижнего текста
            draw.text((10, self.image.height - 50), bottom_text, fill="white", font=font)

    def get_image(self):
        """Возвращает текущее изображение."""
        return self.image