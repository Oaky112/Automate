import tkinter as tk
from tkinter import ttk


class FilteredDataPage(ttk.Frame):
    def __init__(self, master, **kwargs):  # Accept additional keyword arguments
        super().__init__(master, **kwargs)

        # Create a label widget to display "hello world"
        hello_label = ttk.Label(self, text="Hello World!")
        hello_label.pack(padx=20, pady=20)  # Adjust padx and pady as needed


if __name__ == "__main__":
    app = FilteredDataPage()
    app.mainloop()
