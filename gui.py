import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import ImageTk
from image_processor import ImageProcessor

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.image_processor = ImageProcessor()
        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Загрузить", command=self.on_load_image)
        file_menu.add_command(label="Сохранить", command=self.on_save_image)
        file_menu.add_command(label="Сохранить как", command=self.on_save_image)

        menubar.add_cascade(label="Файл", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.about)

        self.master.config(menu=menubar)

    def create_widgets(self):
        frame = tk.Frame(self.master, bg="lightblue", padx=10, pady=10)
        frame.pack(fill=tk.BOTH)

        # Верхний текст
        self.top_text_label = tk.Label(frame, text="Верхний текст", font=("Arial", 20))
        self.top_text_label.grid(row=0, column=0, sticky="ew")

        self.top_text_entry = tk.Entry(frame)
        self.top_text_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # Нижний текст
        self.bottom_text_label = tk.Label(frame, text="Нижний текст", font=("Arial", 20))
        self.bottom_text_label.grid(row=0, column=1, sticky="ew")

        self.bottom_text_entry = tk.Entry(frame)
        self.bottom_text_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Кнопка "Создать мем"
        self.create_meme_button = tk.Button(frame, text='Создать мем', command=self.on_create_meme)
        self.create_meme_button.grid(row=0, column=3, rowspan=2, sticky='NSEW')

        # Область для отображения изображения
        frame_image = tk.Frame(self.master, padx=10, pady=10)
        frame_image.pack(fill=tk.BOTH, expand=True)
        self.image_label = tk.Label(frame_image)
        self.image_label.pack()

    def on_load_image(self):
        """Обрабатывает загрузку изображения."""
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Изображения", "*.jpg *.png *.jpeg")])
        try:
            if file_path:
                self.image_processor.load_image(file_path)
                self.update_image_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def on_save_image(self):
        """Обрабатывает сохранение изображения."""
        if self.image_processor.get_image():
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if file_path:
                self.image_processor.save_image(file_path)

    def on_create_meme(self):
        """Обрабатывает создание мема."""
        if self.image_processor.get_image():
            top_text = self.top_text_entry.get()
            bottom_text = self.bottom_text_entry.get()
            self.image_processor.add_text(top_text, bottom_text)
            self.update_image_display()

    def update_image_display(self):
        """Обновляет изображение в интерфейсе."""
        self.tk_image = ImageTk.PhotoImage(self.image_processor.get_image())
        self.image_label.config(image=self.tk_image)

    def about(self):
        messagebox.showinfo("О программе", "Простая программа для создания мемов")


