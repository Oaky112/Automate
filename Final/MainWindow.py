import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainWindow(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title_label = ttk.Label(
            self.master,
            text="",
            font=("Arial", 16, "bold"),
            anchor="w",
            background="#FFFFFF",
        )
        self.logo_label = ttk.Label(self.master, background="#FFFFFF")
        self.title_label.pack(pady=10, fill="x")
        self.logo_label.pack(pady=10)

    def set_title(self, title):
        self.title_label.config(text=title)

    def set_logo(self, image_path):
        try:
            logo_image = Image.open(image_path)
            resized_image = logo_image.resize((300, 200))
            self.logo_photo = ImageTk.PhotoImage(resized_image)
            self.logo_label.config(image=self.logo_photo)
        except FileNotFoundError:
            print("Image file not found.")

    def show_page(self, page_class):
        # Destroy the current page widget
        for widget in self.master.winfo_children():
            widget.destroy()

        # Create and pack the new page widget
        new_page = page_class(self.master)
        new_page.pack(fill="both", expand=True)
