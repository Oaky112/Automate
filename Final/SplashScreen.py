import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class SplashScreen(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        splash_label = ttk.Label(self)
        splash_label.pack(pady=50)

        logo_image = Image.open("automate2.png")
        logo_image = logo_image.resize((400, 300), Image.ANTIALIAS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_photo = logo_photo
        logo_label = ttk.Label(self, image=logo_photo)
        logo_label.pack(pady=20)

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Orange.Horizontal.TProgressbar",
            troughcolor="white",
            background="#ff5019",
            bordercolor="orange",
            lightcolor="orange",
            darkcolor="orange",
        )
        self.loading_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            length=200,
            mode="determinate",
            style="Orange.Horizontal.TProgressbar",
        )
        self.loading_bar.pack(pady=10)

        self.loading_animation(0)
        self.after(3000, self.close_splash_screen)

    def loading_animation(self, value):
        self.loading_bar["value"] = value
        if value < 100:
            self.after(10, lambda: self.loading_animation(value + 1))

    def close_splash_screen(self):
        self.destroy()
        self.master.show_main_window()  # Change this line to call the appropriate method