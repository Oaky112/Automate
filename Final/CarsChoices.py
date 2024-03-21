import tkinter as tk
from tkinter import ttk, messagebox
import csv

from Final.RefineChoices import RefineChoicesPage

class CarsChoicesPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.car_data = self.read_car_data()
        self.selected_makes = []
        self.selected_models = set()

        make_label = ttk.Label(self, text="Select Make(s):")
        make_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.make_var = tk.StringVar()
        self.make_dropdown = ttk.Combobox(self, textvariable=self.make_var, width=20)
        self.make_dropdown['values'] = self.get_unique_values('make')
        self.make_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.make_dropdown.bind("<<ComboboxSelected>>", self.on_make_select)

        self.selected_makes_label = ttk.Label(self, text="")
        self.selected_makes_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        self.model_checkbuttons = []
        self.create_model_checkboxes()

        # Add a submit button
        submit_button = ttk.Button(self, text="Submit", command=self.submit_selection)
        submit_button.grid(row=2, column=0, padx=5, pady=10, sticky="w")

    def create_model_checkboxes(self):
        models = self.get_unique_values('model')
        num_columns = 10  # Adjust the number of columns as per your preference
        for index, model in enumerate(models):
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(self, text=model, variable=var)
            row_index = index // num_columns
            column_index = index % num_columns
            checkbox.grid(row=row_index + 10, column=column_index, padx=5, pady=5, sticky="w")
            self.model_checkbuttons.append((model, var))

    def on_make_select(self, event):
        selected_make = self.make_var.get()
        if selected_make not in self.selected_makes:
            self.selected_makes.append(selected_make)
            self.update_selected_makes_label()

    def update_selected_makes_label(self):
        if self.selected_makes:
            self.selected_makes_label.config(text=f"Selected Makes: {' - '.join(self.selected_makes)}")
        else:
            self.selected_makes_label.config(text="")

    def submit_selection(self):
        selected_models = [model for model, var in self.model_checkbuttons if var.get() == 1]
        print("Selected Makes:")
        print(self.selected_makes)
        
        print("\nSelected Models:")
        print(selected_models)
        
        # Destroy the current page
        self.destroy()

        # Show the CarsChoicesPage in the same window
        self.master.show_page(RefineChoicesPage)

    def read_car_data(self):
        car_data = []
        # Assuming car_data.csv has 'make' and 'model' columns
        with open('car_data.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                car_data.append(row)
        return car_data

    def get_unique_values(self, column_name):
        return list(set(row[column_name] for row in self.car_data))

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Car Choices")
    CarsChoicesPage(app).pack(expand=True, fill="both")
    app.mainloop()
