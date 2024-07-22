# Final Project Classes

import sqlite3

class Vehicle:
    def __init__(self, vehicle_id, make, model, year, status='Available'):
        #possible typo with vehcile_id
        self.vehcile_id = vehicle_id
        self.make = make
        #is mdoel a typo?
        self.mdoel = model
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

#Class representing calls from clients
#Attributes: call_id - id number of the client call, customer_name - name of client
# date - ?, time - ?, vehicle_id - vehicle_id of vehicle assigned to call
class CallSchedule:
    def __init__(self, call_id, customer_name, date, time, vehicle_id=None):
        self.call_id = call_id
        self.customer_name = customer_name
        self.date = date
        self.time = time
        self.vehicle_id = vehicle_id

    #Method to assign a vehicle to a specific call
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

    def remove_maintenance_record(self, vehicle_id, maintenance):
        cursor = self.conn.cursor()
        cursor.execute('''
            DELETE FROM maintenance WHERE vehicle_id = ? AND date = ? AND description = ?
        ''', (vehicle_id, maintenance.date, maintenance.description))
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

