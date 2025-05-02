import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
from database.modify_tables import create_insert_trigger, create_delete_trigger

class Database:
    def __init__(self, connection):
        self.connection = connection

    def get_animals(self, animal_id=None, name=None, species=None, shelter_id=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Animals"
        params = []
        where_clauses = []

        if animal_id is not None:
            where_clauses.append("animal_id = %s")
            params.append(animal_id)
        if name is not None:
            where_clauses.append("name = %s")
            params.append(name)
        if species is not None:
            where_clauses.append("species = %s")
            params.append(species)
        if shelter_id is not None:
            where_clauses.append("shelter_id = %s")
            params.append(shelter_id)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        animals = cursor.fetchall()
        cursor.close()
        return animals
    
    def post_animal(self, name, species, shelter_id):
        cursor = self.connection.cursor()
        query = "INSERT INTO Animals (name, species, shelter_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, species, shelter_id))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"animal_id": new_id, "name": name, "species": species, "shelter_id": shelter_id}
    
    def update_animal(self, animal_id, name=None, species=None, shelter_id=None):
        cursor = self.connection.cursor()
        query = "UPDATE Animals SET "
        params = []
        update_fields = []

        if name is not None:
            update_fields.append("name = %s")
            params.append(name)
        if species is not None:
            update_fields.append("species = %s")
            params.append(species)
        if shelter_id is not None:
            update_fields.append("shelter_id = %s")
            params.append(shelter_id)
        
        if not update_fields:
            cursor.close()
            return None
        
        query += ', '.join(update_fields) + " WHERE animal_id = %s"
        params.append(animal_id)
        cursor.execute(query, params)
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        
        if rows_affected > 0:
            return self.get_animals(animal_id=animal_id)[0]
        return None
    
    def delete_animal(self, animal_id, animal_name):
        cursor = self.connection.cursor()
        if animal_id is not None:
            query = "DELETE FROM Animals WHERE animal_id = %s"
            cursor.execute(query, (animal_id,))
        elif animal_name is not None:
            query = "DELETE FROM Animals WHERE name = %s"
            cursor.execute(query, (animal_name,))
        else:
            cursor.close()
            return False
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0
    

    def get_staff(self, staff_id=None, name=None, email=None, shelter_id=None, role=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Staff"
        params = []
        where_clauses = []

        if staff_id is not None:
            where_clauses.append("staff_id = %s")
            params.append(staff_id)
        if name is not None:
            where_clauses.append("name = %s")
            params.append(name)
        if email is not None:
            where_clauses.append("email = %s")
            params.append(email)
        if shelter_id is not None:
            where_clauses.append("shelter_id = %s")
            params.append(shelter_id)
        if role is not None:
            where_clauses.append("role = %s")
            params.append(role)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        staff_members = cursor.fetchall()
        cursor.close()
        return staff_members
    
    def post_staff(self, name, email, role, shelter_id):
        cursor = self.connection.cursor()
        query = "INSERT INTO Staff (name, email, role, shelter_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (name, email, role, shelter_id))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"staff_id": new_id, "name": name, "email": email, "role": role, "shelter_id": shelter_id}
    
    def update_staff(self, staff_id, name=None, email=None, role=None, shelter_id=None):
        cursor = self.connection.cursor()
        query = "UPDATE Staff SET "
        params = []
        update_fields = []

        if name is not None:
            update_fields.appends("name = %s")
            params.append(name)
        if email is not None:
            update_fields.append("email = %s")
            params.append(email)
        if role is not None:
            update_fields.append("role = %s")
            params.append(role)
        if shelter_id is not None:
            update_fields.append("shelter_id = %s")
            params.append(shelter_id)
        if not update_fields:
            cursor.close()
            return None
        
        query += ', '.join(update_fields) + " WHERE staff_id = %s"
        params.append(staff_id)

        cursor.execute(query, params)
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_staff(staff_id=staff_id)[0]
        return None
    
    def delete_staff(self, staff_id, staff_name):
        cursor = self.connection.cursor()
        if staff_id is not None:
            query = "DELETE FROM Staff WHERE staff_id = %s"
            cursor.execute(query, (staff_id,))
        elif staff_name is not None:
            query = "DELETE FROM Staff WHERE name = %s"
            cursor.execute(query, (staff_name,))
        else:
            cursor.close()
            return False
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def get_shelters(self, shelter_id=None, name=None, capacity=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM Shelters"
        params = []
        where_clauses = []

        if shelter_id is not None:
            where_clauses.append("shelter_id = %s")
            params.append(shelter_id)
        if name is not None:
            where_clauses.append("name = %s")
            params.append(name)
        if capacity is not None:
            where_clauses.append("capacity = %s")
            params.append(capacity)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        shelters = cursor.fetchall()
        cursor.close()
        return shelters
    
    def post_shelters(self, name, capacity, address, phone_number, email):
        cursor = self.connection.cursor()
        query = "INSERT INTO Shelters (name, capacity, address, phone_number, email) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (name, capacity, address, phone_number, email))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"shelter_id": new_id, "name": name, "capacity": capacity, "address": address, "phone_number": phone_number, "email": email}
    
    def update_shelter(self, shelter_id, name=None, capacity=None, address=None, phone_number=None, email=None):
        cursor = self.connection.cursor()
        query = "UPDATE Shelters SET "
        params = []
        update_fields = []

        if name is not None:
            update_fields.append("name = %s")
            params.append(name)
        if capacity is not None:
            update_fields.append("capacity = %s")
            params.append(capacity)
        if address is not None:
            update_fields.append("address = %s")
            params.append(address)
        if phone_number is not None:
            update_fields.append("phone_number = %s")
            params.append(phone_number)
        if email is not None:
            update_fields.append("email = %s")
            params.append(email)
        if not update_fields:
            cursor.close()
            return None

        query += ', '.join(update_fields) + " WHERE shelter_id = %s"
        params.append(shelter_id)

        cursor.execute(query, params)
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_shelters(shelter_id=shelter_id)[0]
        return None
    
    def delete_shelter(self, shelter_id, shelter_name):
        cursor = self.connection.cursor()
        if shelter_id is not None:
            query = "DELETE FROM Shelters WHERE shelter_id = %s"
            cursor.execute(query, (shelter_id,))
        elif shelter_name is not None:
            query = "DELETE FROM Shelters WHERE name = %s"
            cursor.execute(query, (shelter_name,))
        else:
            cursor.close()
            return False
        
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def get_care_records(self, animal_id=None, staff_id=None, date=None, notes=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM CareRecords"
        params = []
        where_clauses = []

        if animal_id is not None:
            where_clauses.append("animal_id = %s")
            params.append(animal_id)
        if staff_id is not None:
            where_clauses.append("staff_id = %s")
            params.append(staff_id)
        if date is not None:
            where_clauses.append("date = %s")
            params.append(date)
        if notes is not None:
            where_clauses.append("notes LIKE %s")
            params.append(f"%{notes}%")

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        care_records = cursor.fetchall()
        cursor.close()
        return care_records
    
    def post_care_record(self, animal_id, staff_id, date, notes):
        cursor = self.connection.cursor()
        query = "INSERT INTO CareRecords (animal_id, staff_id, date, notes) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (animal_id, staff_id, date, notes))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"record_id": new_id, "animal_id": animal_id, "staff_id": staff_id, "date": date, "notes": notes}
    
    def update_care_record(self, record_id, animal_id=None, staff_id=None, date=None, notes=None):
        cursor = self.connection.cursor()
        query = "UPDATE CareRecords SET "
        params = []
        update_fields = []
        
        if animal_id is not None:
            update_fields.append("animal_id = %s")
            params.append(animal_id)
        if staff_id is not None:
            update_fields.append("staff_id = %s")
            params.append(staff_id)
        if date is not None:
            update_fields.append("date = %s")
            params.append(date)
        if notes is not None:
            update_fields.append("notes = %s")
            params.append(notes)
        
        if not update_fields:
            cursor.close()
            return None
        
        query += ", ".join(update_fields)
        query += " WHERE record_id = %s"
        params.append(record_id)
        
        cursor.execute(query, params)
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        
        if rows_affected > 0:
            return self.get_care_records(record_id=record_id)[0]
        return None
    
    def delete_care_record(self, record_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM CareRecords WHERE record_id = %s"
        cursor.execute(query, (record_id,))
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def get_care_record_info(self, animal_id=None, supply_id=None, staff_id=None, staff_name=None, date=None, record_id=None):
        cursor = self.connection.cursor()
        query = """ 
        SELECT cr.record_id, a.name, s.name, cr.date, cr.notes, cs.name, su.quantity_used
        FROM CareRecords cr
        JOIN Animals a ON cr.animal_id = a.animal_id
        JOIN Staff s ON cr.staff_id = s.staff_id
        LEFT JOIN SupplyUsage su ON cr.record_id = su.record_id
        LEFT JOIN CareSupplies cs ON su.supply_id = cs.supply_id
        """

        params = []
        where_clauses = []
        if animal_id is not None:
            where_clauses.append("cr.animal_id = %s")
            params.append(animal_id)
        if supply_id is not None:
            where_clauses.append("su.supply_id = %s")
            params.append(supply_id)
        if staff_id is not None:
            where_clauses.append("cr.staff_id = %s")
            params.append(staff_id)
        if staff_name is not None:
            where_clauses.append("s.name = %s")
            params.append(staff_name)
        if date is not None:
            where_clauses.append("cr.date = %s")
            params.append(date)
        if record_id is not None:
            where_clauses.append("cr.record_id = %s")
            params.append(record_id)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        query += " ORDER BY cr.record_id"
        
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        return records
    
    def get_supply_inventory(self, supply_id=None, shelter_id=None, quantity=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM SupplyInventory"
        params = []
        where_clauses = []

        if supply_id is not None:
            where_clauses.append("supply_id = %s")
            params.append(supply_id)
        if shelter_id is not None:
            where_clauses.append("shelter_id = %s")
            params.append(shelter_id)
        if quantity is not None:
            where_clauses.append("quantity = %s")
            params.append(quantity)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        inventory = cursor.fetchall()
        cursor.close()
        return inventory

    def post_supply_inventory(self, supply_id, quantity, shelter_id):
        cursor = self.connection.cursor()
        query = "INSERT INTO SupplyInventory (supply_id, quantity, shelter_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (supply_id, quantity, shelter_id))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"supply_id": supply_id, "quantity": quantity, "shelter_id": shelter_id}

    def update_supply_inventory(self, supply_id, quantity, shelter_id):
        cursor = self.connection.cursor()
        query = "UPDATE SupplyInventory SET quantity = %s WHERE supply_id = %s AND shelter_id = %s"
        cursor.execute(query, (quantity, supply_id, shelter_id))
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_supply_inventory(supply_id=supply_id, shelter_id=shelter_id)[0]
        return None
    
    def delete_supply_inventory(self, supply_id, shelter_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM SupplyInventory WHERE supply_id = %s AND shelter_id = %s"
        cursor.execute(query, (supply_id, shelter_id))
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def get_care_supplies(self, supply_id=None, name=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM CareSupplies"
        params = []
        where_clauses = []

        if supply_id is not None:
            where_clauses.append("supply_id = %s")
            params.append(supply_id)
        if name is not None:
            where_clauses.append("name = %s")
            params.append(name)
        
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        cursor.execute(query)
        care_supplies = cursor.fetchall()
        cursor.close()
        return care_supplies
    def post_care_supplies(self, name):
        cursor = self.connection.cursor()
        query = "INSERT INTO CareSupplies (name) VALUES (%s)"
        cursor.execute(query, (name,))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"supply_id": new_id, "name": name}
    
    def update_care_supply(self, supply_id, name):
        cursor = self.connection.cursor()
        query = "UPDATE CareSupplies SET name = %s WHERE supply_id = %s"
        cursor.execute(query, (name, supply_id))
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_care_supplies(supply_id=supply_id)[0]
        return None
    
    def delete_care_supply(self, supply_id, supply_name):
        cursor = self.connection.cursor()
        if supply_id is not None:
            query = "DELETE FROM CareSupplies WHERE supply_id = %s"
            cursor.execute(query, (supply_id,))
        elif supply_name is not None:
            query = "DELETE FROM CareSupplies WHERE name = %s"
            cursor.execute(query, (supply_name,))
        else:
            cursor.close()
            return False
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0
    
        
    
    def get_supply_usage(self, record_id, supply_id, quantity_used):
        cursor = self.connection.cursor()
        query = "SELECT * FROM SupplyUsage"
        params = []
        where_clauses = []

        if record_id is not None:
            where_clauses.append("record_id = %s")
            params.append(record_id)
        if supply_id is not None:
            where_clauses.append("supply_id = %s")
            params.append(supply_id)
        if quantity_used is not None:
            where_clauses.append("quantity_used = %s")
            params.append(quantity_used)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)

        cursor.execute(query, params)
        supply_usage = cursor.fetchall()
        cursor.close()
        return supply_usage
    
    def post_supply_usage(self, record_id, supply_id, quantity_used):
        cursor = self.connection.cursor()
        query = "INSERT INTO SupplyUsage (record_id, supply_id, quantity_used) VALUES (%s, %s, %s)"
        cursor.execute(query, (record_id, supply_id, quantity_used))
        self.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        return {"record_id": record_id, "supply_id": supply_id, "quantity_used": quantity_used}  

    def update_supply_usage(self, record_id, supply_id, quantity_used):
        cursor = self.connection.cursor()
        query = "UPDATE SupplyUsage SET quantity_used = %s WHERE record_id = %s AND supply_id = %s"
        cursor.execute(query, (quantity_used, record_id, supply_id))
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_supply_usage(record_id=record_id, supply_id=supply_id)[0]
        return None
    
    def delete_supply_usage(self, record_id, supply_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM SupplyUsage WHERE record_id = %s AND supply_id = %s"
        cursor.execute(query, (record_id, supply_id))
        self.connection.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

if __name__ == "__main__":
    print("Getting db connection")
    db = mysql.connector.connect(
        host = os.getenv("DB_HOST"),
        user = os.getenv("DB_USER"),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_NAME')
    )
 

    


    
    


