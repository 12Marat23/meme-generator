import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from PIL import ImageTk
from image_processor import ImageProcessor


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.left_icon = PhotoImage(file='image/стрелка_L.png')
        self.pack()
        self.image_processor = ImageProcessor()
        self.create_widgets()
        self.create_menu()

        self.master.bind("<Configure>", self.on_window_resize)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        #  меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Загрузить", command=self.on_load_image)
        file_menu.add_command(label="Сохранить", command=self.on_save_image)
        file_menu.add_command(label="Сохранить как", command=self.on_save_image)
        menubar.add_cascade(label="Файл", menu=file_menu)
        # Меню "Редактировать"
        file_edit_menu = tk.Menu(menubar, tearoff=0)
        file_edit_menu.add_command(label='Поворот по часовой стрелке', command=self.on_rotate_image_positive)
        file_edit_menu.add_command(label='Поворот против часовой стрелке', command=self.on_rotate_image_negative)
        menubar.add_cascade(label="Редактировать", menu=file_edit_menu)

        # Меню "О программе"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.about)

        self.master.config(menu=menubar)

    def create_widgets(self):
        frame = tk.Frame(self.master, bg="lightblue", padx=10, pady=10)
        frame.pack(fill=tk.BOTH)

        # Верхний текст, устанавливаем поля для ввода текста
        self.top_text_label = tk.Label(frame, text="Верхний текст", font=("Arial", 10), bg="lightblue")
        self.top_text_label.grid(row=0, column=0, sticky="ew")

        self.top_text_entry = tk.Entry(frame)
        self.top_text_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

        # Нижний текст, устанавливаем поля для ввода текста
        self.bottom_text_label = tk.Label(frame, text="Нижний текст", font=("Arial", 10), bg="lightblue")
        self.bottom_text_label.grid(row=0, column=1, sticky="ew")

        self.bottom_text_entry = tk.Entry(frame)
        self.bottom_text_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        # Выбор размера шрифта
        self.font_size_label = tk.Label(frame, text="Размер шрифта", font=("Arial", 10), bg="lightblue")
        self.font_size_label.grid(row=0, column=3)

        self.font_size_entry = tk.Entry(frame, width=3)
        self.font_size_entry.grid(row=1, column=3, padx=5, pady=5)

        self.left_arrow_button = tk.Button(frame, image=self.left_icon)
        self.left_arrow_button.grid(row=3, column=0, padx=5, pady=5)
        self.left_arrow_button.config(width=50, height=50, padx=5, pady=5)

        # Создаем кнопку "Создать мем"
        self.create_meme_button = tk.Button(frame, text='Создать мем', command=self.on_create_meme)
        self.create_meme_button.grid(row=0, column=4, rowspan=2, sticky='NSEW')

        # Область для отображения изображения
        frame_image = tk.Frame(self.master, padx=5, pady=5)
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
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if file_path:
                self.image_processor.save_image(file_path)

    def on_create_meme(self):
        """Обрабатывает создание мема."""
        if self.image_processor.get_image():
            top_text = self.top_text_entry.get()
            bottom_text = self.bottom_text_entry.get()
            font_size = int(self.font_size_entry.get() or 30)
            self.image_processor.add_text(top_text, bottom_text, font_size)
            self.update_image_display()

    def update_image_display(self):
        """Обновляет изображение в интерфейсе."""
        if self.image_processor.get_image():
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()
            resized_image = self.image_processor.resize_image(label_width, label_height)
            if resized_image:
                self.tk_image = ImageTk.PhotoImage(resized_image)
                self.image_label.config(image=self.tk_image)

    def on_window_resize(self, event):
        """Обрабатывает изменение размеров окна."""
        if self.image_processor.get_image():
            self.update_image_display()

    def on_rotate_image_positive(self):
        if self.image_processor.get_image():
            self.image_processor.rotate_image(-90)
            self.update_image_display()

    def on_rotate_image_negative(self):
        if self.image_processor.get_image():
            self.image_processor.rotate_image(90)
            self.update_image_display()

    def about(self):
        messagebox.showinfo("О программе", "Простая программа для создания мемов")
