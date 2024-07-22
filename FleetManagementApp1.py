import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3
from datetime import datetime

# Classes

class Vehicle:
    def __init__(self, vehicle_id, make, model, year, status='Available'):
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.status = status
        self.maintenance_schedule = []

    def update_status(self, status):
        self.status = status

    def add_maintenance(self, maintenance):
        self.maintenance_schedule.append(maintenance)
    
    def remove_maintenance(self, maintenance):
        if maintenance in self.maintenance_schedule:
            self.maintenance_schedule.remove(maintenance)

class Maintenance:
    def __init__(self, date, description):
        self.date = date
        self.description = description
        self.completed = False
    
    def complete_maintenance(self):
        self.completed = True

class CallSchedule:
    def __init__(self, call_id, customer_name, date, time, vehicle_id=None):
        self.call_id = call_id
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.vehicle_id = vehicle_id

    def assign_vehicle(self, vehicle_id):
        self.vehicle_id = vehicle_id

class FleetManagementSystem:
    def __init__(self, db_name="fleet_management.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicles (
                vehicle_id TEXT PRIMARY KEY,
                make TEXT,
                model TEXT,
                year INTEGER,
                status TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_id TEXT,
                date TEXT,
                description TEXT,
                completed INTEGER,
                FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS call_schedules (
                call_id TEXT PRIMARY KEY,
                customer_name TEXT,
                date TEXT,
                time TEXT,
                vehicle_id TEXT,
                FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
            )
        ''')
        self.conn.commit()

    def add_vehicle(self, vehicle):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vehicles (vehicle_id, make, model, year, status) VALUES (?, ?, ?, ?, ?)
        ''', (vehicle.vehicle_id, vehicle.make, vehicle.model, vehicle.year, vehicle.status))
        self.conn.commit()

    def remove_vehicle(self, vehicle_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM vehicles WHERE vehicle_id = ?', (vehicle_id,))
        self.conn.commit()

    def add_call_schedule(self, call_schedule):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO call_schedules (call_id, customer_name, date, time, vehicle_id) VALUES (?, ?, ?, ?, ?)
        ''', (call_schedule.call_id, call_schedule.customer_name, call_schedule.date, call_schedule.time, call_schedule.vehicle_id))
        self.conn.commit()

    def remove_call_schedule(self, call_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM call_schedules WHERE call_id = ?', (call_id,))
        self.conn.commit()

    def assign_vehicle_to_call(self, call_id, vehicle_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE call_schedules SET vehicle_id = ? WHERE call_id = ?', (vehicle_id, call_id))
        cursor.execute('UPDATE vehicles SET status = "Assigned to Call" WHERE vehicle_id = ?', (vehicle_id,))
        self.conn.commit()

    def add_maintenance_record(self, vehicle_id, maintenance):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO maintenance (vehicle_id, date, description, completed) VALUES (?, ?, ?, ?)
        ''', (vehicle_id, maintenance.date, maintenance.description, int(maintenance.completed)))
        self.conn.commit()

    def remove_maintenance_record(self, maintenance_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM maintenance WHERE id = ?', (maintenance_id,))
        self.conn.commit()

    def complete_maintenance_record(self, maintenance_id):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE maintenance SET completed = 1 WHERE id = ?', (maintenance_id,))
        self.conn.commit()

    def get_vehicle(self, vehicle_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vehicles WHERE vehicle_id = ?', (vehicle_id,))
        return cursor.fetchone()

    def get_call_schedule(self, call_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM call_schedules WHERE call_id = ?', (call_id,))
        return cursor.fetchone()

    def get_maintenance_records(self, vehicle_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM maintenance WHERE vehicle_id = ?', (vehicle_id,))
        return cursor.fetchall()

    def print_vehicle_details(self, vehicle_id):
        vehicle = self.get_vehicle(vehicle_id)
        if vehicle:
            print(f"Vehicle ID: {vehicle[0]}")
            print(f"Make: {vehicle[1]}")
            print(f"Model: {vehicle[2]}")
            print(f"Year: {vehicle[3]}")
            print(f"Status: {vehicle[4]}")
        else:
            print(f"No vehicle found with ID: {vehicle_id}")

    def print_call_schedule_details(self, call_id):
        call_schedule = self.get_call_schedule(call_id)
        if call_schedule:
            print(f"Call ID: {call_schedule[0]}")
            print(f"Customer Name: {call_schedule[1]}")
            print(f"Date: {call_schedule[2]}")
            print(f"Time: {call_schedule[3]}")
            print(f"Assigned Vehicle ID: {call_schedule[4]}")
        else:
            print(f"No call schedule found with ID: {call_id}")

    def print_maintenance_records(self, vehicle_id):
        maintenance_records = self.get_maintenance_records(vehicle_id)
        if maintenance_records:
            for record in maintenance_records:
                print(f"Record ID: {record[0]}")
                print(f"Vehicle ID: {record[1]}")
                print(f"Date: {record[2]}")
                print(f"Description: {record[3]}")
                print(f"Completed: {bool(record[4])}")
                print("-----")
        else:
            print(f"No maintenance records found for vehicle ID: {vehicle_id}")

# GUI Application

class FleetManagementApp(tk.Tk):
    def __init__(self, root):
        super().__init__()
        self.title("Fleet Management System")
        self.geometry("800x600")

        # Initialize the FleetManagementSystem
        self.fleet_system = FleetManagementSystem()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        self.create_dashboard_tab()
        self.create_vehicles_tab()
        self.create_maintenance_tab()
        self.create_schedule_tab()
        self.create_inventory_tab()

    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")

        ttk.Label(dashboard_frame, text="Dashboard").pack(pady=10)

    def create_vehicles_tab(self):
        vehicles_frame = ttk.Frame(self.notebook)
        self.notebook.add(vehicles_frame, text="Vehicles")

        ttk.Label(vehicles_frame, text="Vehicles").pack(pady=10)
        ttk.Button(vehicles_frame, text="Dashboard").pack(side="right", padx=5)
        ttk.Button(vehicles_frame, text="Logout").pack(side="right", padx=5)

        # Create a treeview to display vehicles
        self.vehicle_tree = ttk.Treeview(vehicles_frame, columns=("ID", "Make", "Model", "Year", "Status"), show="headings")
        self.vehicle_tree.heading("ID", text="ID")
        self.vehicle_tree.heading("Make", text="Make")
        self.vehicle_tree.heading("Model", text="Model")
        self.vehicle_tree.heading("Year", text="Year")
        self.vehicle_tree.heading("Status", text="Status")
        self.vehicle_tree.pack(pady=10, padx=10, expand=True, fill="both")

        # Buttons for vehicle operations
        button_frame = ttk.Frame(vehicles_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Vehicle", command=self.add_vehicle_popup).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Remove Vehicle", command=self.remove_vehicle).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Status", command=self.update_vehicle_status).pack(side="left", padx=5)

        # Populate the treeview with vehicles from the database
        self.refresh_vehicle_list()

    def create_maintenance_tab(self):
        maintenance_frame = ttk.Frame(self.notebook)
        self.notebook.add(maintenance_frame, text="Maintenance")

        ttk.Label(maintenance_frame, text="Maintenance").pack(pady=10)
        ttk.Button(maintenance_frame, text="Dashboard").pack(side="right", padx=5)
        ttk.Button(maintenance_frame, text="Logout").pack(side="right", padx=5)

        # Create a treeview to display maintenance records
        self.maintenance_tree = ttk.Treeview(maintenance_frame, columns=("ID", "Vehicle ID", "Date", "Description", "Completed"), show="headings")
        self.maintenance_tree.heading("ID", text="ID")
        self.maintenance_tree.heading("Vehicle ID", text="Vehicle ID")
        self.maintenance_tree.heading("Date", text="Date")
        self.maintenance_tree.heading("Description", text="Description")
        self.maintenance_tree.heading("Completed", text="Completed")
        self.maintenance_tree.pack(pady=10, padx=10, expand=True, fill="both")

        # Buttons for maintenance operations
        button_frame = ttk.Frame(maintenance_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Maintenance Record", command=self.add_maintenance_popup).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Remove Maintenance Record", command=self.remove_maintenance_record).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Complete Maintenance", command=self.complete_maintenance_record).pack(side="left", padx=5)

        # Populate the treeview with maintenance records from the database
        self.refresh_maintenance_list()

    def create_schedule_tab(self):
        schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(schedule_frame, text="Call Schedules")

        ttk.Label(schedule_frame, text="Call Schedules").pack(pady=10)
        ttk.Button(schedule_frame, text="Dashboard").pack(side="right", padx=5)
        ttk.Button(schedule_frame, text="Logout").pack(side="right", padx=5)

        # Create a treeview to display call schedules
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=("ID", "Customer Name", "Date", "Time", "Vehicle ID"), show="headings")
        self.schedule_tree.heading("ID", text="ID")
        self.schedule_tree.heading("Customer Name", text="Customer Name")
        self.schedule_tree.heading("Date", text="Date")
        self.schedule_tree.heading("Time", text="Time")
        self.schedule_tree.heading("Vehicle ID", text="Vehicle ID")
        self.schedule_tree.pack(pady=10, padx=10, expand=True, fill="both")

        # Buttons for schedule operations
        button_frame = ttk.Frame(schedule_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Call Schedule", command=self.add_call_schedule_popup).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Remove Call Schedule", command=self.remove_call_schedule).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Assign Vehicle", command=self.assign_vehicle_popup).pack(side="left", padx=5)

        # Populate the treeview with call schedules from the database
        self.refresh_schedule_list()

    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")

        ttk.Label(inventory_frame, text="Inventory").pack(pady=10)

        # Inventory related UI components will go here

    def refresh_vehicle_list(self):
        for row in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM vehicles')
        for row in cursor.fetchall():
            self.vehicle_tree.insert('', 'end', values=row)

    def refresh_maintenance_list(self):
        for row in self.maintenance_tree.get_children():
            self.maintenance_tree.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM maintenance')
        for row in cursor.fetchall():
            self.maintenance_tree.insert('', 'end', values=row)

    def refresh_schedule_list(self):
        for row in self.schedule_tree.get_children():
            self.schedule_tree.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM call_schedules')
        for row in cursor.fetchall():
            self.schedule_tree.insert('', 'end', values=row)

    def add_vehicle_popup(self):
        popup = tk.Toplevel()
        popup.title("Add Vehicle")

        tk.Label(popup, text="Vehicle ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(popup, text="Make").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(popup, text="Model").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(popup, text="Year").grid(row=3, column=0, padx=10, pady=10)

        vehicle_id_entry = tk.Entry(popup)
        make_entry = tk.Entry(popup)
        model_entry = tk.Entry(popup)
        year_entry = tk.Entry(popup)

        vehicle_id_entry.grid(row=0, column=1, padx=10, pady=10)
        make_entry.grid(row=1, column=1, padx=10, pady=10)
        model_entry.grid(row=2, column=1, padx=10, pady=10)
        year_entry.grid(row=3, column=1, padx=10, pady=10)

        def add_vehicle():
            vehicle = Vehicle(vehicle_id_entry.get(), make_entry.get(), model_entry.get(), int(year_entry.get()))
            self.fleet_system.add_vehicle(vehicle)
            self.refresh_vehicle_list()
            popup.destroy()

        tk.Button(popup, text="Add", command=add_vehicle).grid(row=4, column=0, columnspan=2, pady=10)

    def remove_vehicle(self):
        selected_item = self.vehicle_tree.selection()
        if selected_item:
            vehicle_id = self.vehicle_tree.item(selected_item)['values'][0]
            self.fleet_system.remove_vehicle(vehicle_id)
            self.refresh_vehicle_list()

    def update_vehicle_status(self):
        selected_item = self.vehicle_tree.selection()
        if selected_item:
            vehicle_id = self.vehicle_tree.item(selected_item)['values'][0]
            popup = tk.Toplevel()
            popup.title("Update Vehicle Status")

            tk.Label(popup, text="New Status").grid(row=0, column=0, padx=10, pady=10)
            status_entry = tk.Entry(popup)
            status_entry.grid(row=0, column=1, padx=10, pady=10)

            def update_status():
                self.fleet_system.conn.cursor().execute('UPDATE vehicles SET status = ? WHERE vehicle_id = ?', (status_entry.get(), vehicle_id))
                self.fleet_system.conn.commit()
                self.refresh_vehicle_list()
                popup.destroy()

            tk.Button(popup, text="Update", command=update_status).grid(row=1, column=0, columnspan=2, pady=10)

    def add_maintenance_popup(self):
        popup = tk.Toplevel()
        popup.title("Add Maintenance Record")

        tk.Label(popup, text="Vehicle ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(popup, text="Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(popup, text="Description").grid(row=2, column=0, padx=10, pady=10)

        vehicle_id_entry = tk.Entry(popup)
        date_entry = tk.Entry(popup)
        description_entry = tk.Entry(popup)

        vehicle_id_entry.grid(row=0, column=1, padx=10, pady=10)
        date_entry.grid(row=1, column=1, padx=10, pady=10)
        description_entry.grid(row=2, column=1, padx=10, pady=10)

        def add_maintenance():
            maintenance = Maintenance(date_entry.get(), description_entry.get())
            self.fleet_system.add_maintenance_record(vehicle_id_entry.get(), maintenance)
            self.refresh_maintenance_list()
            popup.destroy()

        tk.Button(popup, text="Add", command=add_maintenance).grid(row=3, column=0, columnspan=2, pady=10)

    def remove_maintenance_record(self):
        selected_item = self.maintenance_tree.selection()
        if selected_item:
            maintenance_id = self.maintenance_tree.item(selected_item)['values'][0]
            self.fleet_system.remove_maintenance_record(maintenance_id)
            self.refresh_maintenance_list()

    def complete_maintenance_record(self):
        selected_item = self.maintenance_tree.selection()
        if selected_item:
            maintenance_id = self.maintenance_tree.item(selected_item)['values'][0]
            self.fleet_system.complete_maintenance_record(maintenance_id)
            self.refresh_maintenance_list()

    def add_call_schedule_popup(self):
        popup = tk.Toplevel()
        popup.title("Add Call Schedule")

        tk.Label(popup, text="Call ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(popup, text="Customer Name").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(popup, text="Date (YYYY-MM-DD)").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(popup, text="Time").grid(row=3, column=0, padx=10, pady=10)

        call_id_entry = tk.Entry(popup)
        customer_name_entry = tk.Entry(popup)
        date_entry = tk.Entry(popup)
        time_entry = tk.Entry(popup)

        call_id_entry.grid(row=0, column=1, padx=10, pady=10)
        customer_name_entry.grid(row=1, column=1, padx=10, pady=10)
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        time_entry.grid(row=3, column=1, padx=10, pady=10)

        def add_call_schedule():
            call_schedule = CallSchedule(call_id_entry.get(), customer_name_entry.get(), date_entry.get(), time_entry.get())
            self.fleet_system.add_call_schedule(call_schedule)
            self.refresh_schedule_list()
            popup.destroy()

        tk.Button(popup, text="Add", command=add_call_schedule).grid(row=4, column=0, columnspan=2, pady=10)

    def remove_call_schedule(self):
        selected_item = self.schedule_tree.selection()
        if selected_item:
            call_id = self.schedule_tree.item(selected_item)['values'][0]
            self.fleet_system.remove_call_schedule(call_id)
            self.refresh_schedule_list()

    def assign_vehicle_popup(self):
        selected_item = self.schedule_tree.selection()
        if selected_item:
            call_id = self.schedule_tree.item(selected_item)['values'][0]
            popup = tk.Toplevel()
            popup.title("Assign Vehicle")

            tk.Label(popup, text="Vehicle ID").grid(row=0, column=0, padx=10, pady=10)
            vehicle_id_entry = tk.Entry(popup)
            vehicle_id_entry.grid(row=0, column=1, padx=10, pady=10)

            def assign_vehicle():
                self.fleet_system.assign_vehicle_to_call(call_id, vehicle_id_entry.get())
                self.refresh_schedule_list()
                self.refresh_vehicle_list()
                popup.destroy()

            tk.Button(popup, text="Assign", command=assign_vehicle).grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FleetManagementApp(root)
    root.mainloop()