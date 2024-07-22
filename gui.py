import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from TeamDominationClasses import Vehicle, Maintenance, CallSchedule, FleetManagementSystem

class FleetManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fleet Management System")
        self.root.configure(bg='grey')  # Change the background color to grey
        self.root.geometry("600x600")  # Set a fixed size for the window

        self.fms = FleetManagementSystem()

        self.create_widgets()
    
    def create_widgets(self):
        self.title_label = tk.Label(self.root, text=" F l e e t  M a n a g e m e n t S y s t e m ", font=("Helvetica", 40), bg='grey', pady=20)
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Configure grid columns to expand
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            #indentation? This seems to be part of the Configure grid columns to expand
        self.root.grid_rowconfigure(1, weight=1)

        # Arrange buttons in a 3x3 grid
        self.add_vehicle_button = tk.Button(self.root, text="Add Vehicle", command=self.add_vehicle, bg='lightgrey')
        self.add_vehicle_button.grid(row=1, column=0, padx=10, pady=10)

        self.remove_vehicle_button = tk.Button(self.root, text="Remove Vehicle", command=self.remove_vehicle, bg='lightgrey')
        self.remove_vehicle_button.grid(row=1, column=1, padx=10, pady=10)

        self.add_maintenance_button = tk.Button(self.root, text="Add Maintenance", command=self.add_maintenance, bg='lightgrey')
        self.add_maintenance_button.grid(row=1, column=2, padx=10, pady=10)

        self.remove_maintenance_button = tk.Button(self.root, text="Remove Maintenance", command=self.remove_maintenance, bg='lightgrey')
        self.remove_maintenance_button.grid(row=2, column=0, padx=10, pady=300) # Might want to reduce this, a little too much for my taste 

        self.add_call_schedule_button = tk.Button(self.root, text="Add Call Schedule", command=self.add_call_schedule, bg='lightgrey')
        self.add_call_schedule_button.grid(row=2, column=1, padx=10, pady=10)

        self.remove_call_schedule_button = tk.Button(self.root, text="Remove Call Schedule", command=self.remove_call_schedule, bg='lightgrey')
        self.remove_call_schedule_button.grid(row=2, column=2, padx=10, pady=10)

        self.view_vehicle_button = tk.Button(self.root, text="View Vehicle Details", command=self.view_vehicle, bg='lightgrey')
        self.view_vehicle_button.grid(row=3, column=0, padx=10, pady=10)

        self.view_call_schedule_button = tk.Button(self.root, text="View Call Schedule Details", command=self.view_call_schedule, bg='lightgrey')
        self.view_call_schedule_button.grid(row=3, column=1, padx=10, pady=10)

        self.view_maintenance_button = tk.Button(self.root, text="View Maintenance Records", command=self.view_maintenance, bg='lightgrey')
        self.view_maintenance_button.grid(row=3, column=2, padx=10, pady=10)

    def add_vehicle(self):
        self.add_vehicle_window = tk.Toplevel(self.root)
        self.add_vehicle_window.title("Add Vehicle")
        self.add_vehicle_window.configure(bg='grey')  # Change the background color for the new window

        tk.Label(self.add_vehicle_window, text="Vehicle ID", bg='grey').grid(row=0, column=0)
        tk.Label(self.add_vehicle_window, text="Make", bg='grey').grid(row=1, column=0)
        tk.Label(self.add_vehicle_window, text="Model", bg='grey').grid(row=2, column=0)
        tk.Label(self.add_vehicle_window, text="Year", bg='grey').grid(row=3, column=0)

        self.vehicle_id_entry = tk.Entry(self.add_vehicle_window)
        self.vehicle_id_entry.grid(row=0, column=1)
        self.make_entry = tk.Entry(self.add_vehicle_window)
        self.make_entry.grid(row=1, column=1)
        self.model_entry = tk.Entry(self.add_vehicle_window)
        self.model_entry.grid(row=2, column=1)
        self.year_entry = tk.Entry(self.add_vehicle_window)
        self.year_entry.grid(row=3, column=1)

        tk.Button(self.add_vehicle_window, text="Add", command=self.save_vehicle, bg='lightgrey').grid(row=4, column=0, columnspan=2)

    def save_vehicle(self):
        vehicle_id = self.vehicle_id_entry.get()
        make = self.make_entry.get()
        model = self.model_entry.get()
        year = self.year_entry.get()

        if vehicle_id and make and model and year:
            try:
                year = int(year)
                vehicle = Vehicle(vehicle_id, make, model, year)
                self.fms.add_vehicle(vehicle)
                messagebox.showinfo("Success", "Vehicle added successfully.")
                self.add_vehicle_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Year must be an integer.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def remove_vehicle(self):
        self.remove_vehicle_window = tk.Toplevel(self.root)
        self.remove_vehicle_window.title("Remove Vehicle")
        self.remove_vehicle_window.configure(bg='grey')  # Change the background color for the new window

        tk.Label(self.remove_vehicle_window, text="Vehicle ID", bg='grey').grid(row=0, column=0)

        self.remove_vehicle_id_entry = tk.Entry(self.remove_vehicle_window)
        self.remove_vehicle_id_entry.grid(row=0, column=1)

        tk.Button(self.remove_vehicle_window, text="Remove", command=self.delete_vehicle, bg='lightgrey').grid(row=1, column=0, columnspan=2)

    def delete_vehicle(self):
        vehicle_id = self.remove_vehicle_id_entry.get()

        if vehicle_id:
            if self.fms.remove_vehicle(vehicle_id):
                messagebox.showinfo("Success", "Vehicle removed successfully.")
                self.remove_vehicle_window.destroy()
            else:
                messagebox.showerror("Error", "Vehicle ID not found.")
        else:
            messagebox.showerror("Error", "Vehicle ID is required.")

    def add_maintenance(self):
        self.add_maintenance_window = tk.Toplevel(self.root)
        self.add_maintenance_window.title("Add Maintenance")
        self.add_maintenance_window.configure(bg='grey')  # Change the background color for the new window

        tk.Label(self.add_maintenance_window, text="Vehicle ID", bg='grey').grid(row=0, column=0)
        tk.Label(self.add_maintenance_window, text="Date (YYYY-MM-DD)", bg='grey').grid(row=1, column=0)
        tk.Label(self.add_maintenance_window, text="Description", bg='grey').grid(row=2, column=0)

        self.maintenance_vehicle_id_entry = tk.Entry(self.add_maintenance_window)
        self.maintenance_vehicle_id_entry.grid(row=0, column=1)
        self.maintenance_date_entry = tk.Entry(self.add_maintenance_window)
        self.maintenance_date_entry.grid(row=1, column=1)
        self.maintenance_description_entry = tk.Entry(self.add_maintenance_window)
        self.maintenance_description_entry.grid(row=2, column=1)

        tk.Button(self.add_maintenance_window, text="Add", command=self.save_maintenance, bg='lightgrey').grid(row=3, column=0, columnspan=2)

    def save_maintenance(self):
        vehicle_id = self.maintenance_vehicle_id_entry.get()
        date = self.maintenance_date_entry.get()
        description = self.maintenance_description_entry.get()

        if vehicle_id and date and description:
            maintenance = Maintenance(date, description)
            if self.fms.add_maintenance_record(vehicle_id, maintenance):
                messagebox.showinfo("Success", "Maintenance record added successfully.")
                self.add_maintenance_window.destroy()
            else:
                messagebox.showerror("Error", "Vehicle ID not found.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def remove_maintenance(self):
        # Implement remove maintenance functionality
        pass

    def add_call_schedule(self):
        # Implement add call schedule functionality
        pass

    def remove_call_schedule(self):
        # Implement remove call schedule functionality
        pass

    def view_vehicle(self):
        # Implement view vehicle functionality
        pass

    def view_call_schedule(self):
        # Implement view call schedule functionality
        pass

    def view_maintenance(self):
        # Implement view maintenance functionality
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = FleetManagementApp(root)
    root.mainloop()
