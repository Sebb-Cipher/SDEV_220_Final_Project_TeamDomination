# activate virtual environment
# python /Users/<user-name>/Desktop/FleetManagementApp2.1_Updates.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import sqlite3
from datetime import datetime

# Vehicle Class
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

# Maintenance Class
class Maintenance:
    def __init__(self, date, description):
        self.date = date
        self.description = description
        self.completed = False
    
    def complete_maintenance(self):
        self.completed = True

# Schedule Call Class
class CallSchedule:
    def __init__(self, call_id, customer_name, date, time, job_type, vehicle_id=None):
        self.call_id = call_id
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.job_type = job_type
        self.vehicle_id = vehicle_id

    def assign_vehicle(self, vehicle_id):
        self.vehicle_id = vehicle_id

# Inventory Class
class Inventory:
    def __init__(self):
        self.items = {
            "Heating Service Kit": 5,
            "AC Service Kit": 5,
            "Plumbing Service Kit": 5,
            "Drain/Sewer Service Kit": 5,
            "Electrical Service Kit": 5
        }

    def use_item(self, item):
        if self.items[item] > 0:
            self.items[item] -= 1
            return True
        return False

    def restock_item(self, item, quantity):
        self.items[item] += quantity

# Database
class FleetManagementSystem:
    def __init__(self, db_name="fleet_management.db"):
        # Initialize the fleet management system, connecting to the database
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.inventory = Inventory()

    def create_tables(self):
        # Create necessary tables if they don't exist
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
                job_type TEXT,
                vehicle_id TEXT,
                FOREIGN KEY(vehicle_id) REFERENCES vehicles(vehicle_id)
            )
        ''')
        self.conn.commit()

    def add_vehicle(self, vehicle):
        # Add a new vehicle to the vehicles table
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO vehicles (vehicle_id, make, model, year, status) VALUES (?, ?, ?, ?, ?)
        ''', (vehicle.vehicle_id, vehicle.make, vehicle.model, vehicle.year, vehicle.status))
        self.conn.commit()

    def remove_vehicle(self, vehicle_id):
        # Remove a vehicle from the vehicles table
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM vehicles WHERE vehicle_id = ?', (vehicle_id,))
        self.conn.commit()

    def add_call_schedule(self, call_schedule):
        # Add call schedule to the call_schedule table
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO call_schedules (call_id, customer_name, date, time, job_type, vehicle_id) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (call_schedule.call_id, call_schedule.customer_name, call_schedule.date, 
            call_schedule.time, call_schedule.job_type, call_schedule.vehicle_id))
        self.conn.commit()

    def remove_call_schedule(self, call_id):
        # Remove a call schedule from the call_schedules table
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM call_schedules WHERE call_id = ?', (call_id,))
        self.conn.commit()

    def assign_vehicle_to_call(self, call_id, vehicle_id):
        # Assign a vehicle to a call and update vehicle status
        cursor = self.conn.cursor()
        cursor.execute('UPDATE call_schedules SET vehicle_id = ? WHERE call_id = ?', (vehicle_id, call_id))
        cursor.execute('UPDATE vehicles SET status = "Assigned to Call" WHERE vehicle_id = ?', (vehicle_id,))
        self.conn.commit()

    def add_maintenance_record(self, vehicle_id, maintenance):
        # Add a maintenance record to the maintenance table
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO maintenance (vehicle_id, date, description, completed) VALUES (?, ?, ?, ?)
        ''', (vehicle_id, maintenance.date, maintenance.description, int(maintenance.completed)))
        self.conn.commit()

    def remove_maintenance_record(self, maintenance_id):
        # Remove a maintenance record from the maintenance table
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM maintenance WHERE id = ?', (maintenance_id,))
        self.conn.commit()

    def complete_maintenance_record(self, maintenance_id):
        # Mark a maintenance record as completed
        cursor = self.conn.cursor()
        cursor.execute('UPDATE maintenance SET completed = 1 WHERE id = ?', (maintenance_id,))
        self.conn.commit()

    def get_vehicle(self, vehicle_id):
        # Retrieve a vehicle's details from the vehicles table
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM vehicles WHERE vehicle_id = ?', (vehicle_id,))
        return cursor.fetchone()

    def get_call_schedule(self, call_id):
        # Retrieve a call schedule's details from the call_schedules table
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM call_schedules WHERE call_id = ?', (call_id,))
        return cursor.fetchone()

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        # Initialize the login window
        super().__init__(parent)
        self.parent = parent
        self.title("Login")
        self.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        # Create widgets for the login window
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=10, pady=10)

        self.username_entry = ttk.Entry(self)
        self.password_entry = ttk.Entry(self, show="*")

        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button for the login
        ttk.Button(self, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # just using a simple login for now. This checks for the correct login, then closes that window and
        # opens the main window.
        if username == "admin" and password == "password":
            self.parent.current_user = username
            self.destroy()
            self.parent.deiconify()
            self.parent.create_main_interface()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")


# GUI Application
class FleetManagementApp(tk.Tk):
    def __init__(self, root):
        super().__init__()
        self.title("Fleet Management System")
        self.geometry("1600x1200")
        self.current_user = None
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize the FleetManagementSystem
        self.fleet_system = FleetManagementSystem()

        self.withdraw()  # Hide the main window
        self.login_window = LoginWindow(self)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def create_main_interface(self):
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

        # Vehicles List Snapshot
        vehicles_frame = ttk.Frame(dashboard_frame)
        vehicles_frame.pack(pady=10, fill="x")
        ttk.Label(vehicles_frame, text="Vehicles List").pack(pady=5)
        self.vehicle_tree_dashboard = ttk.Treeview(vehicles_frame, columns=("ID", "Make", "Model", "Year", "Status"), show="headings")
        self.vehicle_tree_dashboard.heading("ID", text="ID")
        self.vehicle_tree_dashboard.heading("Make", text="Make")
        self.vehicle_tree_dashboard.heading("Model", text="Model")
        self.vehicle_tree_dashboard.heading("Year", text="Year")
        self.vehicle_tree_dashboard.heading("Status", text="Status")
        self.vehicle_tree_dashboard.pack(pady=10, padx=10, expand=True, fill="both")

        # Maintenance Schedule Snapshot
        maintenance_frame = ttk.Frame(dashboard_frame)
        maintenance_frame.pack(pady=10, fill="x")
        ttk.Label(maintenance_frame, text="Maintenance Schedule").pack(pady=5)
        self.maintenance_tree_dashboard = ttk.Treeview(maintenance_frame, columns=("ID", "Vehicle ID", "Date", "Description", "Completed"), show="headings")
        self.maintenance_tree_dashboard.heading("ID", text="ID")
        self.maintenance_tree_dashboard.heading("Vehicle ID", text="Vehicle ID")
        self.maintenance_tree_dashboard.heading("Date", text="Date")
        self.maintenance_tree_dashboard.heading("Description", text="Description")
        self.maintenance_tree_dashboard.heading("Completed", text="Completed")
        self.maintenance_tree_dashboard.pack(pady=10, padx=10, expand=True, fill="both")

        # Call Schedule Snapshot
        schedule_frame = ttk.Frame(dashboard_frame)
        schedule_frame.pack(pady=10, fill="x")
        ttk.Label(schedule_frame, text="Call Schedule").pack(pady=5)
        self.schedule_tree_dashboard = ttk.Treeview(schedule_frame, columns=("ID", "Customer Name", "Date", "Time", "Job Type", "Vehicle ID"), show="headings")
        self.schedule_tree_dashboard.heading("ID", text="ID")
        self.schedule_tree_dashboard.heading("Customer Name", text="Customer Name")
        self.schedule_tree_dashboard.heading("Date", text="Date")
        self.schedule_tree_dashboard.heading("Time", text="Time")
        self.schedule_tree_dashboard.heading("Job Type", text="Job Type")
        self.schedule_tree_dashboard.heading("Vehicle ID", text="Vehicle ID")
        self.schedule_tree_dashboard.pack(pady=10, padx=10, expand=True, fill="both")

        # Populate the dashboard with data
        self.refresh_dashboard()

        ttk.Button(schedule_frame, text="Logout", command=self.logout).pack(side="bottom", padx=5)

    def refresh_dashboard(self):
        self.refresh_vehicle_dashboard()
        self.refresh_maintenance_dashboard()
        self.refresh_schedule_dashboard()

    def refresh_vehicle_dashboard(self):
        for row in self.vehicle_tree_dashboard.get_children():
            self.vehicle_tree_dashboard.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM vehicles')
        for row in cursor.fetchall():
            self.vehicle_tree_dashboard.insert('', 'end', values=row)

    def refresh_maintenance_dashboard(self):
        for row in self.maintenance_tree_dashboard.get_children():
            self.maintenance_tree_dashboard.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM maintenance')
        for row in cursor.fetchall():
            self.maintenance_tree_dashboard.insert('', 'end', values=row)

    def refresh_schedule_dashboard(self):
        for row in self.schedule_tree_dashboard.get_children():
            self.schedule_tree_dashboard.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM call_schedules')
        for row in cursor.fetchall():
            self.schedule_tree_dashboard.insert('', 'end', values=row)

    def create_vehicles_tab(self):
        vehicles_frame = ttk.Frame(self.notebook)
        self.notebook.add(vehicles_frame, text="Vehicles")

        ttk.Label(vehicles_frame, text="Vehicles").pack(pady=10)
        ttk.Button(vehicles_frame, text="Logout", command=self.logout).pack(side="bottom", padx=5)

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
        ttk.Button(maintenance_frame, text="Logout", command=self.logout).pack(side="bottom", padx=5)

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
        ttk.Button(schedule_frame, text="Logout", command=self.logout).pack(side="bottom", padx=5)

        # Create a treeview to display call schedules
        self.schedule_tree = ttk.Treeview(schedule_frame, columns=("ID", "Customer Name", "Date", "Time", "Job Type", "Vehicle ID"), show="headings")
        self.schedule_tree.heading("ID", text="ID")
        self.schedule_tree.heading("Customer Name", text="Customer Name")
        self.schedule_tree.heading("Date", text="Date")
        self.schedule_tree.heading("Time", text="Time")
        self.schedule_tree.heading("Job Type", text="Job Type")
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

    def add_call_schedule_popup(self):
        popup = tk.Toplevel()
        popup.title("Add Call Schedule")

        tk.Label(popup, text="Call ID").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(popup, text="Customer Name").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(popup, text="Date").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(popup, text="Job Type").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(popup, text="Time").grid(row=4, column=0, padx=10, pady=10)

        call_id_entry = tk.Entry(popup)
        customer_name_entry = tk.Entry(popup)
        date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        time_entry = tk.Entry(popup)
        job_type_var = tk.StringVar()
        job_types = ["Heating", "AC", "Plumbing", "Drain/Sewer", "Electrical"]
        job_type_dropdown = ttk.Combobox(popup, textvariable=job_type_var, values=job_types)

        call_id_entry.grid(row=0, column=1, padx=10, pady=10)
        customer_name_entry.grid(row=1, column=1, padx=10, pady=10)
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        time_entry.grid(row=3, column=1, padx=10, pady=10)
        job_type_dropdown.grid(row=4, column=1, padx=10, pady=10)

        def add_call_schedule():
            if not job_type_var.get():
                messagebox.showwarning("Missing Information", "Please select a job type.")
                return
    
            selected_date = date_entry.get_date()
            formatted_date = selected_date.strftime("%Y-%m-%d")
    
            call_schedule = CallSchedule(
                call_id_entry.get(),
                customer_name_entry.get(),
                formatted_date,
                time_entry.get(),
                job_type_var.get()
            )
            self.fleet_system.add_call_schedule(call_schedule)
            self.refresh_schedule_list()
            popup.destroy()

        tk.Button(popup, text="Add", command=add_call_schedule).grid(row=5, column=0, columnspan=2, pady=10)

    def assign_vehicle_popup(self):
        selected_item = self.schedule_tree.selection()
        if selected_item:
            call_id = self.schedule_tree.item(selected_item)['values'][0]
            popup = tk.Toplevel()
            popup.title("Assign Vehicle")

            tk.Label(popup, text="Select Vehicle").grid(row=0, column=0, padx=10, pady=10)
    
            # Fetch available vehicles from the database with all details
            cursor = self.fleet_system.conn.cursor()
            cursor.execute('SELECT vehicle_id, make, model, year FROM vehicles WHERE status = "Available"')
            available_vehicles = cursor.fetchall()

            # Create a dictionary to store vehicle information
            vehicle_dict = {}
            vehicle_list = []
            for vehicle in available_vehicles:
                vehicle_id, make, model, year = vehicle
                display_text = f"{vehicle_id} - {make} {model} ({year})"
                vehicle_dict[display_text] = vehicle_id
                vehicle_list.append(display_text)

            vehicle_var = tk.StringVar()
            vehicle_dropdown = ttk.Combobox(popup, textvariable=vehicle_var, values=vehicle_list, width=50)
            vehicle_dropdown.grid(row=0, column=1, padx=10, pady=10)

            def assign_vehicle():
                selected_vehicle_display = vehicle_var.get()
                if selected_vehicle_display:
                    selected_vehicle_id = vehicle_dict[selected_vehicle_display]
                    selected_item = self.inventory_checklist()
                    if selected_item:
                        self.fleet_system.inventory.use_item(selected_item)
                        self.fleet_system.assign_vehicle_to_call(call_id, selected_vehicle_id)
                        self.refresh_schedule_list()
                        self.refresh_vehicle_list()
                        self.refresh_inventory_list()
                        popup.destroy()
                    else:
                        messagebox.showwarning("Inventory Check Failed", "Please select an inventory item before assigning a vehicle.")
                else:
                    messagebox.showwarning("No Vehicle Selected", "Please select a vehicle before assigning.")

            tk.Button(popup, text="Assign", command=assign_vehicle).grid(row=1, column=0, columnspan=2, pady=10)

    def inventory_checklist(self):
        checklist_popup = tk.Toplevel()
        checklist_popup.title("Inventory Checklist")

        items = self.fleet_system.inventory.items.keys()
        selected_item = tk.StringVar()

        for i, item in enumerate(items):
            ttk.Radiobutton(checklist_popup, text=f"{item} (Qty: {self.fleet_system.inventory.items[item]})", 
                            variable=selected_item, value=item).grid(row=i, column=0, sticky="w", padx=10, pady=5)

        result = {'selected': None}

        def confirm_checklist():
            selected = selected_item.get()
            if selected:
                if self.fleet_system.inventory.items[selected] > 0:
                    result['selected'] = selected
                    checklist_popup.destroy()
                else:
                    messagebox.showwarning("Out of Stock", f"There are no {selected} items available in the inventory.")
            else:
                messagebox.showwarning("No Selection", "Please select an inventory item before confirming.")

        ttk.Button(checklist_popup, text="Confirm", command=confirm_checklist).grid(row=len(items), column=0, pady=10)

        checklist_popup.wait_window()
        return result['selected']

    def logout(self):
        self.current_user = None
        self.withdraw()
        self.login_window = LoginWindow(self)

    def create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")

        ttk.Label(inventory_frame, text="Inventory").pack(pady=10)

        self.inventory_tree = ttk.Treeview(inventory_frame, columns=("Item", "Quantity"), show="headings")
        self.inventory_tree.heading("Item", text="Item")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.pack(pady=10, padx=10, expand=True, fill="both")

        button_frame = ttk.Frame(inventory_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Restock Item", command=self.restock_item_popup).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh Inventory", command=self.refresh_inventory_list).pack(side="left", padx=5)

        # Refresh the inventory list after creating the tree
        self.refresh_inventory_list()

    def refresh_inventory_list(self):
        if hasattr(self, 'inventory_tree'):
            for row in self.inventory_tree.get_children():
                self.inventory_tree.delete(row)
            for item, quantity in self.fleet_system.inventory.items.items():
                self.inventory_tree.insert('', 'end', values=(item, quantity))

    def restock_item_popup(self):
        popup = tk.Toplevel()
        popup.title("Restock Item")

        tk.Label(popup, text="Item").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(popup, text="Quantity").grid(row=1, column=0, padx=10, pady=10)

        item_var = tk.StringVar()
        item_combobox = ttk.Combobox(popup, textvariable=item_var, values=list(self.fleet_system.inventory.items.keys()))
        quantity_entry = tk.Entry(popup)

        item_combobox.grid(row=0, column=1, padx=10, pady=10)
        quantity_entry.grid(row=1, column=1, padx=10, pady=10)

        def restock_item():
            item = item_var.get()
            quantity = int(quantity_entry.get())
            self.fleet_system.inventory.restock_item(item, quantity)
            self.refresh_inventory_list()
            popup.destroy()

        tk.Button(popup, text="Restock", command=restock_item).grid(row=2, column=0, columnspan=2, pady=10)

    # Clears and reloads vehicle list from database
    def refresh_vehicle_list(self):
        for row in self.vehicle_tree.get_children():
            self.vehicle_tree.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM vehicles')
        for row in cursor.fetchall():
            self.vehicle_tree.insert('', 'end', values=row)

    # Clears and reloads maintenance record list from database
    def refresh_maintenance_list(self):
        for row in self.maintenance_tree.get_children():
            self.maintenance_tree.delete(row)
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT * FROM maintenance')
        for row in cursor.fetchall():
            self.maintenance_tree.insert('', 'end', values=row)
    
    # Clears and reloads call schedule list from database
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
        
            # Create a list of status options
            status_options = ["Available", "In for maintenance", "Assigned to Call"]
        
            # Create a StringVar to hold the selected status
            status_var = tk.StringVar(popup)
            status_var.set(status_options[0])  # Set the default value
        
            # Create the dropdown menu
            status_dropdown = ttk.Combobox(popup, textvariable=status_var, values=status_options, state="readonly")
            status_dropdown.grid(row=0, column=1, padx=10, pady=10)

            def update_status():
                new_status = status_var.get()
                self.fleet_system.conn.cursor().execute('UPDATE vehicles SET status = ? WHERE vehicle_id = ?', (new_status, vehicle_id))
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

        # Fetch available vehicles from the database
        cursor = self.fleet_system.conn.cursor()
        cursor.execute('SELECT vehicle_id FROM vehicles')
        available_vehicles = [row[0] for row in cursor.fetchall()]

        vehicle_var = tk.StringVar()
        vehicle_dropdown = ttk.Combobox(popup, textvariable=vehicle_var, values=available_vehicles)
        vehicle_dropdown.grid(row=0, column=1, padx=10, pady=10)

        date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        date_entry.grid(row=1, column=1, padx=10, pady=10)

        description_entry = tk.Entry(popup)
        description_entry.grid(row=2, column=1, padx=10, pady=10)

        def add_maintenance():
            selected_vehicle = vehicle_var.get()
            if not selected_vehicle:
                messagebox.showwarning("Missing Information", "Please select a vehicle.")
                return
        
            selected_date = date_entry.get_date()
            formatted_date = selected_date.strftime("%Y-%m-%d")
        
            maintenance = Maintenance(formatted_date, description_entry.get())
            self.fleet_system.add_maintenance_record(selected_vehicle, maintenance)
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
        tk.Label(popup, text="Date").grid(row=2, column=0, padx=10, pady=10)
        tk.Label(popup, text="Time").grid(row=3, column=0, padx=10, pady=10)
        tk.Label(popup, text="Job Type").grid(row=4, column=0, padx=10, pady=10)

        call_id_entry = tk.Entry(popup)
        customer_name_entry = tk.Entry(popup)
        date_entry = DateEntry(popup, width=12, background='darkblue', foreground='white', borderwidth=2)
        time_entry = tk.Entry(popup)
        job_type_var = tk.StringVar()
        job_types = ["Heating", "AC", "Plumbing", "Drain/Sewer", "Electrical"]
        job_type_dropdown = ttk.Combobox(popup, textvariable=job_type_var, values=job_types)

        call_id_entry.grid(row=0, column=1, padx=10, pady=10)
        customer_name_entry.grid(row=1, column=1, padx=10, pady=10)
        date_entry.grid(row=2, column=1, padx=10, pady=10)
        time_entry.grid(row=3, column=1, padx=10, pady=10)
        job_type_dropdown.grid(row=4, column=1, padx=10, pady=10)

        def add_call_schedule():
            if not job_type_var.get():
                messagebox.showwarning("Missing Information", "Please select a job type.")
                return
            call_schedule = CallSchedule(
                call_id_entry.get(),
                customer_name_entry.get(),
                date_entry.get_date().strftime("%Y-%m-%d"),
                time_entry.get(),
                job_type_var.get()
            )
            self.fleet_system.add_call_schedule(call_schedule)
            self.refresh_schedule_list()
            popup.destroy()

        tk.Button(popup, text="Add", command=add_call_schedule).grid(row=5, column=0, columnspan=2, pady=10)

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

            tk.Label(popup, text="Select Vehicle").grid(row=0, column=0, padx=10, pady=10)
    
            # Fetch available vehicles from the database with all details
            cursor = self.fleet_system.conn.cursor()
            cursor.execute('SELECT vehicle_id, make, model, year FROM vehicles WHERE status = "Available"')
            available_vehicles = cursor.fetchall()

            # Create a dictionary to store vehicle information
            vehicle_dict = {}
            vehicle_list = []
            for vehicle in available_vehicles:
                vehicle_id, make, model, year = vehicle
                display_text = f"{vehicle_id} - {make} {model} ({year})"
                vehicle_dict[display_text] = vehicle_id
                vehicle_list.append(display_text)

            # Use a Listbox instead of Combobox
            listbox = tk.Listbox(popup, width=50, height=10)
            listbox.grid(row=0, column=1, padx=10, pady=10)
            for item in vehicle_list:
                listbox.insert(tk.END, item)

            def assign_vehicle():
                selection = listbox.curselection()
                if selection:
                    selected_vehicle_display = listbox.get(selection[0])
                    selected_vehicle_id = vehicle_dict[selected_vehicle_display]
                    selected_item = self.inventory_checklist()
                    if selected_item:
                        self.fleet_system.inventory.use_item(selected_item)
                        self.fleet_system.assign_vehicle_to_call(call_id, selected_vehicle_id)
                        self.refresh_schedule_list()
                        self.refresh_vehicle_list()
                        self.refresh_inventory_list()
                        popup.destroy()
                    else:
                        messagebox.showwarning("Inventory Check Failed", "Please select an inventory item before assigning a vehicle.")
                else:
                    messagebox.showwarning("No Vehicle Selected", "Please select a vehicle before assigning.")

            tk.Button(popup, text="Assign", command=assign_vehicle).grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = FleetManagementApp(root)
    root.mainloop()