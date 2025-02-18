from gui import Application
import tkinter as tk

"""
Главный файл приложения, запускает цикл приложения
"""
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Мемасы")
    root.geometry("700x600")
    app = Application(master=root)
    app.mainloop()
