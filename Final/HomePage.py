import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import date
from geopy.geocoders import Nominatim
import geopy.distance
from Final.CarsChoices import CarsChoicesPage

class HomePage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Gender selection
        gender_frame = ttk.Frame(self)
        gender_frame.pack(pady=10, fill="x")
        gender_label = ttk.Label(gender_frame, text="Select your gender:")
        gender_label.grid(row=0, column=0, sticky="w")
        gender_var = tk.StringVar()
        gender_dropdown = ttk.Combobox(
            gender_frame, textvariable=gender_var, values=["male", "female", "other"], state="readonly"
        )
        gender_dropdown.grid(row=0, column=1, padx=10, sticky="w")

        # Date of Birth input
        dob_frame = ttk.Frame(self)
        dob_frame.pack(pady=10, fill="x")
        dob_label = ttk.Label(dob_frame, text="Enter your date of birth:")
        dob_label.grid(row=0, column=0, sticky="w")

        # Day dropdown
        day_var = tk.StringVar()
        day_dropdown = ttk.Combobox(dob_frame, textvariable=day_var, values=[str(i).zfill(2) for i in range(1, 32)])
        day_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Month dropdown
        month_var = tk.StringVar()
        month_dropdown = ttk.Combobox(
            dob_frame, textvariable=month_var,
            values=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                    'October', 'November', 'December']
        )
        month_dropdown.grid(row=0, column=2, padx=5, pady=5)

        # Year dropdown
        year_var = tk.StringVar()
        year_dropdown = ttk.Combobox(dob_frame, textvariable=year_var, values=[str(i) for i in range(2024, 1900, -1)])
        year_dropdown.grid(row=0, column=3, padx=5, pady=5)

        # Employment status selection
        employment_frame = ttk.Frame(self)
        employment_frame.pack(pady=10, fill="x")
        employment_label = ttk.Label(employment_frame, text="Select your employment status:")
        employment_label.grid(row=0, column=0, sticky="w")
        employment_var = tk.StringVar()
        employment_dropdown = ttk.Combobox(
            employment_frame,
            textvariable=employment_var,
            values=["Full-time", "Part-time", "Unemployed"],
            state="readonly",
        )
        employment_dropdown.grid(row=0, column=1, padx=10, sticky="w")

        # Postcodes input
        postcodes_frame = ttk.Frame(self)
        postcodes_frame.pack(pady=10, fill="x")
        self.home_postcode_label = ttk.Label(postcodes_frame, text="Enter your home postcode:")
        self.home_postcode_label.grid(row=0, column=0, sticky="w")
        self.home_postcode_var = tk.StringVar()
        self.home_postcode_entry = ttk.Entry(postcodes_frame, textvariable=self.home_postcode_var)
        self.home_postcode_entry.grid(row=0, column=1, padx=10, sticky="w")

        self.work_postcode_label = ttk.Label(postcodes_frame, text="Enter your work postcode:")
        self.work_postcode_label.grid(row=0, column=2, sticky="w")
        self.work_postcode_var = tk.StringVar()
        self.work_postcode_entry = ttk.Entry(postcodes_frame, textvariable=self.work_postcode_var)
        self.work_postcode_entry.grid(row=0, column=3, padx=10, sticky="w")

        # Holiday weeks input
        holiday_weeks_frame = ttk.Frame(self)
        holiday_weeks_frame.pack(pady=10, fill="x")
        holiday_weeks_label = ttk.Label(holiday_weeks_frame, text="Enter the number of holiday weeks:")
        holiday_weeks_label.grid(row=0, column=0, sticky="w")
        holiday_weeks_var = tk.StringVar()
        holiday_weeks_entry = ttk.Entry(holiday_weeks_frame, textvariable=holiday_weeks_var)
        holiday_weeks_entry.grid(row=0, column=1, padx=10, sticky="w")

        # Submit button
        submit_btn = ttk.Button(
            self, text="Calculate", command=lambda: self.validate_input(master, gender_var.get(), day_var.get(),
                                                                         month_var.get(), year_var.get(),
                                                                         employment_var.get(), holiday_weeks_var.get())
        )
        submit_btn.pack(pady=10)

    def validate_input(self, master, gender, day, month, year, employment_status, holiday_weeks):
        if not all([gender, day, month, year, employment_status, holiday_weeks]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            if employment_status != "Unemployed":
                home_postcode = self.home_postcode_var.get()
                work_postcode = self.work_postcode_var.get()
                # Use Geopy to calculate distance between postcodes
                distance = self.calculate_distance(home_postcode, work_postcode)
            else:
                # If unemployed, set distance to 0
                distance = 0.0
                # Hide the home postcode and work postcode fields
                self.hide_postcode_fields(employment_status)

            dob = date(int(year), self.get_month_number(month), int(day))
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 17:
                messagebox.showerror("Error", "You must be older than 17 to continue.")
                return
            else:
                insurance_per_annum = self.calculate_insurance(age, gender, employment_status)
                mileage_per_annum = self.calculate_mileage(distance, employment_status, int(holiday_weeks))
                insurance_per_annum = round(insurance_per_annum, 3)
                mileage_per_annum = round(mileage_per_annum, 3)

                # Print the calculated values in the terminal
                print(f"Distance between postcodes: {distance} miles")
                print(f"Holiday Weeks: {holiday_weeks}")
                print(f"Estimated Insurance per year: £{insurance_per_annum}")
                print(f"Estimated Mileage per year: {mileage_per_annum}")

                confirmation_message = f"Age: {age}\nGender: {gender}\nEmployment Status: {employment_status}"

                # Employment Status: {employment_status}"
                # Disable sounds on message boxes
                messagebox.no_sound = True

                confirmation = messagebox.askquestion("Confirmation", f"Is this information correct?\n\n{confirmation_message}")
            if confirmation == 'yes':
                # Destroy the current HomePage
                self.destroy()
                # Show the CarsChoicesPage in the same window
                master.show_page(CarsChoicesPage)
        except ValueError:
            messagebox.showerror("Error", "Invalid date.")
            
    def navigate_to_car_choices(self, master):
        # Create an instance of CarsChoicesPage and navigate to it
        car_choices_page = CarsChoicesPage(master)
        car_choices_page.pack(fill="both", expand=True)
        
    def replace_with_car_choices(self):
        self.pack_forget()  # Remove the HomePage from the window
        self.master.show_page(CarsChoicesPage)  # Show the CarsChoicesPage

    def hide_postcode_fields(self, employment_status):
        if employment_status == "Unemployed":
            # Hide the home postcode and work postcode fields
            self.home_postcode_label.grid_remove()
            self.home_postcode_entry.grid_remove()
            self.work_postcode_label.grid_remove()
            self.work_postcode_entry.grid_remove()
        else:
            # Show the home postcode and work postcode fields if not unemployed
            self.home_postcode_label.grid()
            self.home_postcode_entry.grid()
            self.work_postcode_label.grid()
            self.work_postcode_entry.grid()

    def calculate_distance(self, home_postcode, work_postcode):
        try:
            # Initialize a geopy Nominatim geocoder
            geolocator = Nominatim(user_agent="Automate")

            # Get the location coordinates for home and work postcodes
            home_location = geolocator.geocode(home_postcode)
            work_location = geolocator.geocode(work_postcode)

            if home_location is None or work_location is None:
                raise ValueError("Invalid postcodes or unable to calculate distance.")

            # Calculate the distance between the two locations using geopy
            distance = geopy.distance.geodesic(
                (home_location.latitude, home_location.longitude),
                (work_location.latitude, work_location.longitude),
            ).miles

            return round(distance, 2)
        except geopy.exc.GeocoderInsufficientPrivileges as e:
            messagebox.showerror("Error", f"Geocoding error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
    def calculate_insurance(self, age, gender, employment_status):
        if age < 30:
            metric = 30 - age
            age_metric = metric * 0.2
        else:
            age_metric = 1

        gender_metric = 1 if gender.lower() == 'male' else 1.2  # Assuming genders list isn't defined here

        if employment_status == 'Full-time':  # Assuming employment_statuses list isn't defined here
            employment_metric = 1
        elif employment_status == 'Part-time':
            employment_metric = 1.5
        else:
            employment_metric = 2

        insurance_per_annum = 450 * age_metric * gender_metric * employment_metric
        return insurance_per_annum


    def calculate_mileage(self, work_miles, employment_status, holiday_weeks):
        emp_metric = 5 if employment_status == 'Full-time' else (3 if employment_status == 'Part-time' else 1)
        work_mile_cost = emp_metric * (52 - holiday_weeks) * work_miles * 2
        mileage_per_annum = work_mile_cost * 1.6
        return mileage_per_annum

    @staticmethod
    def get_month_number(month_name):
        months_dict = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
            'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        return months_dict.get(month_name, 1)

    def on_submit(self):
        # Call the navigate_to_car_choices method of the AutomateGUI instance
        self.app.navigate_to_car_choices(self.master)


if __name__ == "__main__":
    app = tk.Tk()  # Initialize Tkinter root window
    app.title("Insurance Calculator")  # Set the window title
    main_frame = HomePage(app)  # Create an instance of HomePage
    main_frame.pack(fill="both", expand=True)  # Pack the main frame to fill the window
    app.mainloop()
