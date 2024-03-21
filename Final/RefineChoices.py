import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import date
from geopy.geocoders import Nominatim
import geopy.distance
from tkinter import *


import csv


class RefineChoicesPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.car_data = self.read_car_data()
        self.selected_makes = []

        self.selected_models = set()
        self.available_models = set()
        self.model_var = []  # List to store model variables for checkboxes
        self.model_checkbuttons = []  # List to store model checkboxes
        self.colour_checkboxes = []  # List to store colour checkboxes
        self.selected_colours = []  # List to store selected colours
        self.selected_engine_range = [1.0, 3.0]  # Default engine size range

        # Create Age of car
        year_label = ttk.Label(self, text="Select Age of Car:")
        year_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Create a list of values for the year dropdowns in descending order
        years_list = [str(year) for year in range(2007, 2025)]

        # Create dropdown for minimum year
        year_min_var = tk.StringVar()
        self.year_min_dropdown = ttk.Combobox(
            self, textvariable=year_min_var, values=years_list, state="readonly"
        )
        self.year_min_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Create dropdown for maximum year
        year_max_var = tk.StringVar()
        self.year_max_dropdown = ttk.Combobox(
            self, textvariable=year_max_var, values=years_list, state="readonly"
        )
        self.year_max_dropdown.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Set default values for dropdowns
        self.year_min_dropdown.set(years_list[0])
        self.year_max_dropdown.set(years_list[-1])

        # Set event bindings to update the max dropdown based on the min dropdown
        self.year_min_dropdown.bind("<<ComboboxSelected>>", self.update_max_dropdown)

        # Create dropdowns for price range
        price_label = ttk.Label(self, text="Select Price Range (£):")
        price_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Create a list of values for the price dropdowns
        price_values = [str(i) for i in range(0, 100001, 500)]

        # Create dropdown for minimum price
        price_min_var = tk.StringVar()
        self.price_min_dropdown = ttk.Combobox(
            self,
            textvariable=price_min_var,
            values=price_values,
            state="readonly",
        )
        self.price_min_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="e")

        # Create dropdown for maximum price
        price_max_var = tk.StringVar()
        self.price_max_dropdown = ttk.Combobox(
            self,
            textvariable=price_max_var,
            values=price_values,
            state="readonly",
        )
        self.price_max_dropdown.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # Set default values for price dropdowns
        self.price_min_dropdown.set(price_values[0])
        self.price_max_dropdown.set(price_values[-1])

        # Bind event to update max price dropdown based on min price dropdown
        self.price_min_dropdown.bind(
            "<<ComboboxSelected>>", self.update_max_price_dropdown
        )

        # Create dropdowns for mileage range
        mileage_label = ttk.Label(self, text="Select Mileage Range (km):")
        mileage_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        # Create a list of values for the mileage dropdowns
        mileage_values = [str(i) for i in range(0, 50501, 500)]

        # Create dropdown for minimum mileage
        mileage_min_var = tk.StringVar()
        self.mileage_min_dropdown = ttk.Combobox(
            self,
            textvariable=mileage_min_var,
            values=mileage_values,
            state="readonly",
        )
        self.mileage_min_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="e")

        # Create dropdown for maximum mileage
        mileage_max_var = tk.StringVar()
        self.mileage_max_dropdown = ttk.Combobox(
            self,
            textvariable=mileage_max_var,
            values=mileage_values,
            state="readonly",
        )
        self.mileage_max_dropdown.grid(row=3, column=2, padx=5, pady=5, sticky="w")

        # Set default values for mileage dropdowns
        self.mileage_min_dropdown.set(mileage_values[0])
        self.mileage_max_dropdown.set(mileage_values[-1])

        # Bind event to update max mileage dropdown based on min mileage dropdown
        self.mileage_min_dropdown.bind(
            "<<ComboboxSelected>>", self.update_max_mileage_dropdown
        )

        # Create other dropdowns and checkboxes as before

        # Create dropdown for transmission
        transmission_label = ttk.Label(self, text="Select Transmission Type:")
        transmission_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        transmission_var = tk.StringVar()
        self.transmission_dropdown = ttk.Combobox(
            self,
            textvariable=transmission_var,
            values=self.get_unique_values("transmission"),
            state="readonly",
        )
        self.transmission_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="e")

        # Create dropdown for fuel type
        fuel_label = ttk.Label(self, text="Select Fuel Type:")
        fuel_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        fuel_var = tk.StringVar()
        self.fuel_dropdown = ttk.Combobox(
            self,
            textvariable=fuel_var,
            values=self.get_unique_values("fuelType"),
            state="readonly",
        )
        self.fuel_dropdown.grid(row=5, column=1, padx=5, pady=5, sticky="e")

        # Create dropdowns for engine size range
        engine_label = ttk.Label(self, text="Select Engine Size Range (Litres):")
        engine_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")

        engine_values = [
            "{:.1f}".format(val) for val in list((0.1 * i) + 1.0 for i in range(21))
        ]
        engine_min_var = tk.StringVar()
        self.engine_min_dropdown = ttk.Combobox(
            self,
            textvariable=engine_min_var,
            values=engine_values,
            state="readonly",
        )
        self.engine_min_dropdown.grid(row=6, column=1, padx=5, pady=5, sticky="e")

        engine_max_var = tk.StringVar()
        self.engine_max_dropdown = ttk.Combobox(
            self,
            textvariable=engine_max_var,
            values=engine_values,
            state="readonly",
        )
        self.engine_max_dropdown.grid(row=6, column=2, padx=5, pady=5, sticky="w")

        self.engine_min_dropdown.set(engine_values[0])
        self.engine_max_dropdown.set(engine_values[-1])

        self.engine_min_dropdown.bind(
            "<<ComboboxSelected>>", self.update_max_engine_dropdown
        )

        # Create dropdown for road tax
        road_tax_label = ttk.Label(self, text="Select Road Tax (£):")
        road_tax_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        road_tax_values = [str(i) for i in range(0, 501, 20)]

        road_tax_var = tk.StringVar()
        self.road_tax_dropdown = ttk.Combobox(
            self,
            textvariable=road_tax_var,
            values=road_tax_values,
            state="readonly",
        )
        self.road_tax_dropdown.grid(row=7, column=1, padx=5, pady=5, sticky="e")

        # Create dropdowns for yearly maintenance cost range
        maintenance_label = ttk.Label(
            self, text="Estimated Yearly Maintenance Cost (£):"
        )
        maintenance_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")

        # Create a list of values for the maintenance cost dropdowns
        maintenance_min_values = [str(i) for i in range(0, 5001, 100)]
        maintenance_max_values = [str(i) for i in range(100, 5101, 100)]

        # Create dropdown for maintenance cost
        maintenance_min_var = tk.StringVar()
        self.maintenance_min_dropdown = ttk.Combobox(
            self,
            textvariable=maintenance_min_var,
            values=maintenance_min_values,
            state="readonly",
        )
        self.maintenance_min_dropdown.grid(row=8, column=1, padx=5, pady=5, sticky="e")

        # Create checkboxes for selecting colors
        colour_label = ttk.Label(self, text="Select Colour:")
        colour_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")

        colours = self.get_unique_values("colour")
        self.colour_checkbuttons = []
        for index, colour in enumerate(colours):
            var = tk.IntVar()
            checkbox = ttk.Checkbutton(
                self,
                text=colour,
                variable=var,
                onvalue=1,
                offvalue=0,
                command=lambda v=var, c=colour: self.toggle_colour_selection(v, c),
            )
            checkbox.grid(
                row=10 + index // 3, column=index % 3 + 1, padx=5, pady=5, sticky="w"
            )
            self.colour_checkbuttons.append((checkbox, var))

        # Create dropdown for stars rating
        self.stars_mapping = {
            "5": "5",
            "4 +": "4, 5",
            "3 +": "3, 5",
            "2 +": "2, 5",
            "1 +": "1, 5",
        }

        stars_label = ttk.Label(self, text="Select Stars Rating:")
        stars_label.grid(
            row=11 + len(self.get_unique_values("colour")) // 3 + 1,
            column=0,
            padx=5,
            pady=5,
            sticky="w",
        )
        stars_var = tk.StringVar()
        self.stars_dropdown = ttk.Combobox(
            self,
            textvariable=stars_var,
            values=list(self.stars_mapping.keys()),
            state="readonly",
        )
        self.stars_dropdown.grid(
            row=11 + len(self.get_unique_values("colour")) // 3 + 1,
            column=1,
            padx=5,
            pady=5,
            sticky="e",
        )

        # Function to get the selected stars rating in the desired format
        def get_selected_stars(self):
            selected_value = self.stars_dropdown.get()
            return stars_mapping.get(
                selected_value, ""
            )  # Return mapped value or empty string if not found

        # Create LEZ Checkbox
        self.lez_var = tk.IntVar()  # Store the variable as an instance attribute
        self.lez_checkbox = ttk.Checkbutton(
            self, text="ULEZ Car (Ultra Low-Emission Zone)", variable=self.lez_var
        )
        self.lez_checkbox.grid(row=18, column=0, columnspan=2, padx=10, pady=5)

        # Create a label and entry box for car ownership duration
        duration_label = ttk.Label(
            self, text="How Long Do You Intend to Keep the Car (in years):"
        )
        duration_label.grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.duration_entry = ttk.Entry(self)
        self.duration_entry.grid(row=12, column=1, padx=5, pady=5, sticky="w")

        # Submit button
        submit_btn = ttk.Button(self, text="Submit", command=self.filter_cars)
        submit_btn.grid(
            row=20 + len(self.get_unique_values("colour")) // 3 + 2,
            column=1,
            columnspan=3,
            pady=20,
        )

    def read_car_data(self):
        car_data = []
        with open("car_data.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                car_data.append(row)
        return car_data

    def get_unique_values(self, column_name):
        unique_values = set()
        for car in self.car_data:
            unique_values.add(car[column_name])
        return list(unique_values)

    def toggle_colour_selection(self, var, colour):
        if var.get() == 1:
            self.selected_colours.append(colour)
        else:
            self.selected_colours.remove(colour)

    def filter_cars(self):
        # Get the selected values from the dropdowns and checkboxes
        year_min = self.year_min_dropdown.get()
        year_max = self.year_max_dropdown.get()
        price_min = self.price_min_dropdown.get()
        price_max = self.price_max_dropdown.get()
        mileage_min = self.mileage_min_dropdown.get()
        mileage_max = self.mileage_max_dropdown.get()
        transmission = self.transmission_dropdown.get()
        fuel_type = self.fuel_dropdown.get()
        engine_size_min = self.engine_min_dropdown.get()
        engine_size_max = self.engine_max_dropdown.get()
        road_tax = self.road_tax_dropdown.get()
        maintenance_min = self.maintenance_min_dropdown.get()
        stars_rating = self.get_selected_stars()
        car_duration = self.duration_entry.get()

        # Convert empty values to appropriate defaults or handle them as needed
        year_min = int(year_min) if year_min else 2008
        year_max = int(year_max) if year_max else 2024
        price_min = int(price_min) if price_min else 0
        price_max = int(price_max) if price_max else 100000
        mileage_min = int(mileage_min) if mileage_min else 0
        mileage_max = int(mileage_max) if mileage_max else 50500
        road_tax = (
            int(self.road_tax_dropdown.get()) if self.road_tax_dropdown.get() else ""
        )
        maintenance_min = int(maintenance_min) if maintenance_min else ""
        car_duration = int(car_duration) if car_duration else None
        lez_value = "Yes" if self.lez_var.get() == 1 else "No"

        # Get user's entries as a 2D array
        user_entries = [
            [year_min, year_max],
            [price_min, price_max],
            [mileage_min, mileage_max],
            [transmission],
            [fuel_type],
            [engine_size_min, engine_size_max],
            [0, road_tax],
            [0, maintenance_min],
            self.selected_colours,  # Include selected colours
            [car_duration],  # Include car ownership duration
            [stars_rating],
            [lez_value],  # Include LEZ value
        ]

        # Print the arrays to the terminal
        for i, arr in enumerate(user_entries):
            var_name = f"array_{i}"
            globals()[var_name] = arr
            print(f"{var_name}: {arr}")

        # Perform filtering based on the selected criteria
        filtered_results = []  # Placeholder, replace with actual filtering logic

        # Create a new window for displaying the 2D array
        result_window = tk.Toplevel(self.master)
        result_window.title("Filtered Data")

        # Create a label to display the 2D array
        result_label = tk.Label(result_window, text="User Entries:")
        result_label.pack(padx=20, pady=10)

        # Display the 2D array in the label
        for i, arr in enumerate(user_entries):
            label_text = f"array_{i}: {arr}"
            entry_label = tk.Label(result_window, text=label_text)
            entry_label.pack()

        # Optionally, you can add a button to close the result window
        close_button = ttk.Button(
            result_window, text="Close", command=result_window.destroy
        )
        close_button.pack(pady=10)

        # Placeholder for actual filtering logic and displaying results in FilteredDataPage
        # Replace this with your actual logic
        filtered_results = []  # Placeholder, replace with actual filtering logic

    def get_selected_stars(self):
        selected_value = self.stars_dropdown.get()
        return self.stars_mapping.get(
            selected_value, ""
        )  # Return mapped value or empty string if not found

    def update_max_price_dropdown(self, event):
        # Get the selected minimum price
        min_price = int(self.price_min_dropdown.get())

        # Filter the price range values to include only those greater than or equal to the selected minimum price
        filtered_prices = [str(i) for i in range(min_price, 100001, 500)]

        # Update the values in the max price dropdown
        self.price_max_dropdown["values"] = filtered_prices

    def update_max_mileage_dropdown(self, event):
        # Get the selected minimum mileage
        min_mileage = int(self.mileage_min_dropdown.get())

        # Filter the mileage range values to include only those greater than or equal to the selected minimum mileage
        filtered_mileages = [str(i) for i in range(min_mileage, 50501, 500)]

        # Update the values in the max mileage dropdown
        self.mileage_max_dropdown["values"] = filtered_mileages

    def update_max_dropdown(self, event):
        # Get the selected minimum year
        min_year = int(self.year_min_dropdown.get())

        # Filter the years list to include only those less than or equal to the selected minimum year
        filtered_years = [
            year for year in range(min_year, 2025)
        ]  # Assuming max year is 2024

        # Update the values in the max dropdown
        self.year_max_dropdown["values"] = filtered_years[
            ::-1
        ]  # Reverse the list for descending order

    def update_max_engine_dropdown(self, event):
        min_engine = float(self.engine_min_dropdown.get())
        max_engine_values = [
            "{:.1f}".format(val)
            for val in list(
                (0.1 * i) + min_engine for i in range(int((3.0 - min_engine) * 10) + 1)
            )
        ]
        self.engine_max_dropdown["values"] = max_engine_values
        self.engine_max_dropdown.set(max_engine_values[-1])

    def get_selected_road_tax(self):
        road_tax_str = self.road_tax_dropdown.get()
        road_tax = (
            int(road_tax_str) if road_tax_str else 0
        )  # Convert to int if not empty, otherwise default to 0
        return [0, road_tax]


if __name__ == "__main__":
    app = RefineChoicesPage()
    app.mainloop()

# Created methods to filter by range or selection


# Filters options where you select multiple
def filterBySelection(df, column_name, values_to_keep):
    # Check if the array of values to keep is empty and if so return all
    if len(values_to_keep) == 0:
        return df
    # Filter the DataFrame based on whether values in the specified column are present in the array
    filtered_df = df[df[column_name].isin(values_to_keep)]
    # Reset the index after filtering
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df


# Filters options in a range
def filterByRange(df, column_name, range):
    # Check if the array of values to keep is empty and if so return all
    if len(range) == 0:
        return df
    lower, higher = range
    # Filter the DataFrame based on the range of values in the specified column
    filtered_df = df[(df[column_name] >= lower) & (df[column_name] <= higher)]
    # Reset the index after filtering
    filtered_df.reset_index(drop=True, inplace=True)
    return filtered_df
