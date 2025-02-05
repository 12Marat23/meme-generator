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

    def add_text(self, top_text, bottom_text,  font_size):
        """Добавляет текст на изображение."""
        if self.image:
            try:
                draw = ImageDraw.Draw(self.image)
                font = ImageFont.truetype('arial.ttf', font_size)

                # Добавление верхнего текста
                draw.text((10, 10), top_text, fill="white", font=font)

                # Добавление нижнего текста
                draw.text((10, self.image.height - 50-font_size), bottom_text, fill="white", font=font)
            except Exception as e:
                print(f"Ошибка при добавлении текста: {e}")

    def get_image(self):
        """Возвращает текущее изображение."""
        return self.image

    def resize_image(self, max_width, max_height):
        """Масштабирует изображение с сохранением пропорций."""
        if self.image:
            width, height = self.image.size
            ratio = min(max_width / width, max_height / height)
            new_size = (int(width * ratio), int(height * ratio))
            return self.image.resize(new_size, Image.Resampling.LANCZOS)
        return None

    def rotate_image(self, angle):
        if self.image:
            # self.image = self.image.rotate(angle, Image.Resampling.LANCZOS)
            self.image = self.image.rotate(angle, Image.Resampling.NEAREST)
        return None
    