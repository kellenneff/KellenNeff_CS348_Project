import mysql.connector

class StaffDB:
    def __init__(self, connection):
        self.connection = connection

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
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0
