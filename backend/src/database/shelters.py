import mysql.connector

class ShelterDB:
    def __init__(self, connection):
        self.connection = connection

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
        
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0