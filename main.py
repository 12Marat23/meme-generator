from gui import Application
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Мемасы")
    root.geometry("500x500")
    app = Application(master=root)
    app.mainloop()
