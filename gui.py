import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
from tkinter import font, scrolledtext
from tkinter import ttk
from PIL import ImageTk
from image_processor import ImageProcessor
import tkinter.font as tkFont


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.left_icon = PhotoImage(file='image/стрелка_L.png')
        self.right_icon = PhotoImage(file='image/стрелка_R.png')
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
        file_edit_menu.add_command(image=self.right_icon, command=self.on_rotate_image_positive)
        file_edit_menu.add_command(image=self.left_icon, command=self.on_rotate_image_negative)
        menubar.add_cascade(label="Редактировать", menu=file_edit_menu)

        # Меню "О программе"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.about)

        self.master.config(menu=menubar)

    def update_font(self):
        # Получаем выбранный шрифт и размер
        self.selected_font = self.font_family.get()
        self.selected_size = self.size_menu.get()
        print(self.selected_font, self.selected_size)

    def create_widgets(self):
        self.frame = tk.Frame(self.master, bg="lightblue", padx=10, pady=10)
        self.frame.pack(side=tk.TOP, fill=tk.X)
        self.fount_choice()


        # Область для отображения изображения
        frame_image = tk.Frame(self.master, padx=5, pady=5)
        frame_image.pack(fill=tk.BOTH, expand=True)
        self.image_label = tk.Label(frame_image)
        self.image_label.pack()
    def fount_choice(self):
        fonts = tkFont.families()
        font_combobox = ttk.Combobox(self.frame, values=fonts)
        font_combobox.pack(side=tk.LEFT, padx=5, pady=5)
        font_combobox.set("Arial")

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
            angle_size = int(self.rotate_image_entry.get() or 90)
            self.image_processor.rotate_image(-angle_size)
            self.update_image_display()

    def on_rotate_image_negative(self):
        if self.image_processor.get_image():
            angle_size = int(self.rotate_image_entry.get() or 90)
            self.image_processor.rotate_image(angle_size)
            self.update_image_display()

    def about(self):
        messagebox.showinfo("О программе", "Простая программа для создания мемов")
