import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter import font, scrolledtext
from tkinter import ttk
from PIL import ImageTk
from image_processor import ImageProcessor
import tkinter.font as tkFont


class Application(tk.Frame):
    """
    Класс приложения
    """

    def __init__(self, master=None):
        """
        Конструктор класса приложения
        """
        super().__init__(master)
        self.master = master
        self.left_icon = PhotoImage(file='image/стрелка_L.png')
        self.right_icon = PhotoImage(file='image/стрелка_R.png')
        self.selected_size = 12
        self.selected_font = 'arial'
        self.pack()
        self.image_processor = ImageProcessor()
        self.create_widgets()
        self.create_menu()

        self.master.bind("<Configure>", self.on_window_resize)  # ширина окна

    def create_menu(self):
        """
        Создание меню
        """
        menubar = tk.Menu(self.master)
        #  меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Загрузить", command=self.on_load_image)
        file_menu.add_command(label="Сохранить", command=self.on_save_image)
        file_menu.add_command(label="Сохранить как", command=self.on_save_image)
        menubar.add_cascade(label="Файл", menu=file_menu)
        # Меню "Редактировать"
        file_edit_menu = tk.Menu(menubar, tearoff=0)
        file_edit_menu.add_command(label="Повернуть вправо", image=self.right_icon,
                                   command=self.on_rotate_image_clockwise)
        file_edit_menu.add_command(label="Повернуть влево", image=self.left_icon,
                                   command=self.on_rotate_image_counterclockwise)
        menubar.add_cascade(label="Редактировать", menu=file_edit_menu)

        # Меню "О программе"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.about)

        self.master.config(menu=menubar)

    def update_font(self):
        """
        Обновление выбранного шрифта и размера
        """
        try:
            self.selected_font = self.font_combobox.get()
            self.selected_size = int(self.size_combobox.get())
            print(self.selected_font)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить шрифт: {e}")

    def create_widgets(self):
        """
        Создание виджетов
        """
        self.frame = tk.Frame(self.master, bg="lightblue", padx=5, pady=5)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        self.font_choice()  # выбор шрифта
        self.size_choice()  # выбор размера

        self.frame2 = tk.Frame(self.master, bg="lightgreen", padx=5, pady=5)
        self.frame2.pack(side=tk.TOP, fill=tk.X)

        # Кнопка применения изменений шрифта и размера
        apply_button = tk.Button(self.frame, text="Применить", command=self.update_font)
        apply_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.meme_text_input()  # ввод текста
        self.rotate_image()  # Поворот изображения

        # Кнопка создания мема
        self.create_meme_button = tk.Button(self.frame2, text='Создать мем', command=self.on_create_meme)
        self.create_meme_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Область для отображения изображения
        frame_image = tk.Frame(self.master, padx=5, pady=5)
        frame_image.pack(fill=tk.BOTH, expand=True)
        self.image_label = tk.Label(frame_image)
        self.image_label.pack()

    def rotate_image(self):
        """
        Поворот изображения вокруг оси
        """
        self.rotate_image_label = tk.Label(self.frame, text="Угол поворота", font=("Arial", 10), bg="lightblue")
        self.rotate_image_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.rotate_image_entry = tk.Entry(self.frame, width=5)
        self.rotate_image_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.rotate_image_entry.insert(0, "90")  # Значение по умолчанию

    def font_choice(self):
        """
        Выбор шрифта
        """
        fonts = tkFont.families()  # возвращает список всех доступных шрифтов в системе
        self.font_combobox = ttk.Combobox(self.frame, values=fonts, width=10)
        self.font_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.font_combobox.set("Arial")  # Установка начального значения ttk.Combobox

    def size_choice(self):
        """
        Выбор размера шрифта
        """
        size = [i for i in range(8, 50)]
        self.size_combobox = ttk.Combobox(self.frame, values=size, width=3)
        self.size_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        self.size_combobox.set(12)

    def meme_text_input(self):
        """
        Ввод текста в поля ввода
        """
        # Верхний текст
        self.top_text_label = tk.Label(self.frame2, text="Верхний текст", font=("Arial", 10), bg="lightblue")
        self.top_text_label.pack(side=tk.LEFT, padx=5, pady=5)
        # Поле ввод для верхнего текста
        self.top_text_entry = tk.Entry(self.frame2, width=20)
        self.top_text_entry.pack(side=tk.LEFT, padx=5, pady=5)

        # Нижний текст
        self.bottom_text_label = tk.Label(self.frame2, text="Нижний текст", font=("Arial", 10), bg="lightblue")
        self.bottom_text_label.pack(side=tk.LEFT, padx=5, pady=5)
        #  Поля для ввода текста
        self.bottom_text_entry = tk.Entry(self.frame2, width=20)
        self.bottom_text_entry.pack(side=tk.LEFT, padx=5, pady=5)

    def on_load_image(self):
        """
        Обрабатывает загрузку изображения.
        """
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Изображения", "*.jpg *.png *.jpeg")])
        try:
            if file_path:
                self.image_processor.load_image(file_path)
                self.update_image_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def on_save_image(self):
        """
        Обрабатывает сохранение изображения.
        """
        if self.image_processor.get_image():
            file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
            if file_path:
                self.image_processor.save_image(file_path)

    def on_create_meme(self):
        """
        Обрабатывает создание мема.
        """
        if self.image_processor.get_image():
            top_text = self.top_text_entry.get()
            bottom_text = self.bottom_text_entry.get()
            font_size = int(self.selected_size)
            font_path = self.selected_font
            self.image_processor.add_text(top_text, bottom_text, font_size, font_path)
            self.update_image_display()

    def update_image_display(self):
        """
        Обновляет изображение в интерфейсе.
        """
        if self.image_processor.get_image():
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()
            resized_image = self.image_processor.resize_image(label_width, label_height)
            if resized_image:
                self.tk_image = ImageTk.PhotoImage(resized_image)
                self.image_label.config(image=self.tk_image)

    def on_window_resize(self, event):
        """
        Обрабатывает изменение размеров окна.
        """
        if self.image_processor.get_image():
            self.update_image_display()

    def on_rotate_image_clockwise(self):
        """
        Обрабатывает поворот изображения по часовой стрелке.
        """
        if self.image_processor.get_image():
            angle_size = int(self.rotate_image_entry.get() or 90)
            self.image_processor.rotate_image(-angle_size)
            self.update_image_display()

    def on_rotate_image_counterclockwise(self):
        """
        Обрабатывает поворот изображения против часовой стрелки.
        """
        if self.image_processor.get_image():
            angle_size = int(self.rotate_image_entry.get() or 90)
            self.image_processor.rotate_image(angle_size)
            self.update_image_display()

    def about(self):
        """
        Отображает информацию о программе.
        """
        messagebox.showinfo("О программе", "Простая программа для создания мемов")
