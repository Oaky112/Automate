import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Final.SplashScreen import SplashScreen
from Final.HomePage import HomePage
from Final.CarsChoices import CarsChoicesPage
from Final.MainWindow import MainWindow
from Final.RefineChoices import RefineChoicesPage  # Import RefineChoicesPage


class AutomateGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Insurance Calculator")
        self.geometry("800x600")

        self.show_splash_screen_page()

    def show_splash_screen_page(self):
        splash_screen_page = SplashScreen(self)
        splash_screen_page.pack(fill="both", expand=True)

        # After a delay, switch to the main window
        self.after(2000, self.show_main_window)

    def show_main_window(self):
        main_window = MainWindow(self)  # Create an instance of MainWindow
        main_window.pack(fill="both", expand=True)  # Pack the main window

        # Inside MainWindow, create and pack the HomePage
        home_page = HomePage(main_window)
        home_page.pack(fill="both", expand=True)

        # Call a method in MainWindow to set the logo
        main_window.set_logo("automate2.png")  # Provide the correct image path

        # You can add more content or functionality to MainWindow as needed

    def show_page(self, page_class):
        # Destroy the current page widget
        for widget in self.winfo_children():
            widget.destroy()

        # Create and pack the new page widget
        new_page = page_class(self)
        new_page.pack(fill="both", expand=True)

    def navigate_to_car_choices(self, master):
        cars_choices_page = CarsChoicesPage(master)  # Use master instead of main_window
        cars_choices_page.pack(fill="both", expand=True)
        
    def navigate_to_refine_choices(self, master, selected_models_dict):  # Pass selected_models_dict
        refine_choices_page = RefineChoicesPage(master, selected_models_dict)  # Use master and selected_models_dict
        refine_choices_page.pack(fill="both", expand=True)
        

if __name__ == "__main__":
    app = AutomateGUI()
    app.mainloop()
