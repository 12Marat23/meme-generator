import logging

import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter import ttk
from PIL import ImageTk, Image
from image_processor import ImageProcessor
import tkinter.font as tkFont

logging.basicConfig(level=logging.INFO)


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
        # Иконки для кнопок поворота картинки
        self.left_icon = PhotoImage(file='image/стрелка_L.png')
        self.right_icon = PhotoImage(file='image/стрелка_R.png')

        # Иконки для кнопок выравнивания
        self.align_left_icon = PhotoImage(file='image/align_left_icon.png')
        self.align_centre_icon = PhotoImage(file='image/align_centre_icon.png')
        self.align_right_icon = PhotoImage(file='image/align_right_icon.png')

        # Переменные для выравнивания
        self.is_fixed = [False, False, False]
        self.buttons = []
        self.current_alignment = "left"

        # Начальные значения шрифта
        self.selected_size = 12
        self.selected_font = 'arial'

        # переменная для хранения пути к изображенью
        self.current_image_path = None

        # Вызов функции
        self.pack()
        self.image_processor = ImageProcessor()
        self.create_widgets()
        self.create_buttons()
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
        file_menu.add_command(label="Сохранить как", command=self.on_save_as_image)
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

    def create_widgets(self):
        """
        Создание виджетов
        """
        #  Создаем первый frame
        self.frame = tk.Frame(self.master, bg="lightblue", padx=5, pady=5)
        self.frame.pack(side=tk.TOP, fill=tk.X)

        # Выбор шрифта и размера
        self.font_choice()
        self.size_choice()

        # Создаем второй frame
        self.frame2 = tk.Frame(self.master, bg="lightgreen", padx=5, pady=5)
        self.frame2.pack(side=tk.TOP, fill=tk.X)

        # Кнопка применения изменений шрифта и размера
        apply_button = tk.Button(self.frame, text="Применить", command=self.update_font)
        apply_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.meme_text_input()
        self.rotate_image()

        # Кнопка создания мема
        self.create_meme_button = tk.Button(self.frame2, text='Создать мем', command=self.on_create_meme)
        self.create_meme_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка очистки изображения
        self.clear_button = tk.Button(self.frame2, text='Очистить', command=lambda: self.clear_or_delete_meme("clear"))
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка удаления мема
        self.delete_button = tk.Button(self.frame2, text="Удалить", command=lambda: self.clear_or_delete_meme("delete"))
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Запуск области для отображения изображения
        self.frame_images()

    def frame_images(self):
        """
        Создание области для отображения изображения
        """
        frame_image = tk.Frame(self.master, padx=5, pady=5)
        frame_image.pack(fill=tk.BOTH, expand=True)
        self.image_processor.clear_text_on_image()
        self.image_label = tk.Label(frame_image)
        self.image_label.pack()

    def create_buttons(self):
        """
        Кнопки для выбора выравнивания текста

        """
        align_list = (self.align_left_icon, self.align_centre_icon, self.align_right_icon)
        for button in range(3):
            btn = tk.Button(self.frame, image=align_list[button], borderwidth=0,
                            command=lambda index=button: self.align_button_state(index),
                            bg='lightblue')

            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.buttons.append(btn)

    def align_button_state(self, btn_index):
        """
        Выбор выравнивания текста
        """
        for i in range(len(self.buttons)):
            self.is_fixed[i] = False
            self.buttons[i].config(bg='lightblue')

        # Устанавливаем состояние нажатой кнопки
        self.is_fixed[btn_index] = True
        self.buttons[btn_index].config(bg='grey')
        self.current_alignment = ["left", "center", "right"][btn_index]

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

    def update_font(self):
        """
        Обновление выбранного шрифта и размера
        """
        try:
            self.selected_font = self.font_combobox.get()
            self.selected_size = int(self.size_combobox.get())

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить шрифт: {e}")

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

    def on_load_image(self):
        """
        Обрабатывает загрузку изображения.
        """
        file_path = filedialog.askopenfilename(title="Выберите файл", filetypes=[("Изображения", "*.jpg *.png *.jpeg")])
        try:
            if file_path:
                self.current_image_path = file_path
                self.image_processor.load_image(file_path)
                self.update_image_display()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

    def on_save_image(self):
        """
        Обрабатывает сохранение изображения. Перезаписывает старый файл
        """
        if self.image_processor.get_image() and self.current_image_path:
            try:
                self.image_processor.save_image(self.current_image_path)
                messagebox.showinfo("Сохранение", "Изображение успешно сохранено.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Нет загруженного изображения для сохранения.")

    def on_save_as_image(self):
        """
        Обрабатывает сохранение изображения.
        Сохраняет в новый файл.
        """
        if self.image_processor.get_image():
            try:
                file_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                         filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
                if file_path:
                    self.image_processor.save_image(file_path)
                messagebox.showinfo("Сохранение", "Изображение успешно сохранено.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
        else:
            messagebox.showwarning("Предупреждение", "Нет загруженного изображения для сохранения.")

    def on_create_meme(self):
        """
        Обрабатывает создание мема.
        """
        if self.image_processor.get_image():
            top_text = self.top_text_entry.get()
            bottom_text = self.bottom_text_entry.get()
            font_tk_font = tkFont.Font(family=self.selected_font, size=self.selected_size)
            logging.info(f'{font_tk_font.actual()["family"]}, {font_tk_font.actual()["size"]}')
            self.image_processor.add_text(top_text, bottom_text, font_tk_font, self.current_alignment)
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

    def rotate_image(self):
        """
        Поворот изображения вокруг оси
        """
        self.rotate_image_label = tk.Label(self.frame, text="Угол поворота", font=("Arial", 10), bg="lightblue")
        self.rotate_image_label.pack(side=tk.LEFT, padx=5, pady=5)
        self.rotate_image_entry = tk.Entry(self.frame, width=5)
        self.rotate_image_entry.pack(side=tk.LEFT, padx=5, pady=5)
        self.rotate_image_entry.insert(0, "90")  # Значение по умолчанию
        self.button_rotate = tk.Button(self.frame, image=self.right_icon,
                                       command=self.on_rotate_image_clockwise)
        self.button_rotate.pack(side=tk.LEFT, padx=5, pady=5)

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

    def clear_or_delete_meme(self, event):
        """
        Очищает поля ввода.
        """
        self.top_text_entry.delete(0, tk.END)
        self.bottom_text_entry.delete(0, tk.END)
        if event == 'clear':
            self.image_processor.clear_text_on_image()
        elif event == 'delete':
            self.image_processor.delete_image()
        self.update_image_display()

    def about(self):
        """
        Отображает информацию о программе.
        """
        messagebox.showinfo("О программе", "Простая программа для создания мемов")
