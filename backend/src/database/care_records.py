import mysql.connector

class CareRecordDB:
    def __init__(self, connection):
        self.connection = connection
    
    def get_care_records(self, record_id=None, animal_id=None, staff_id=None, date=None, notes=None):
        cursor = self.connection.cursor()
        query = "SELECT * FROM CareRecords"
        params = []
        where_clauses = []

        if record_id is not None:
            where_clauses.append("record_id = %s")
            params.append(record_id)
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

        print(query)
        
        cursor.execute(query, params)
        rows_affected = cursor.rowcount
        cursor.close()
        if rows_affected > 0:
            return self.get_care_records(record_id=record_id)[0]
        return None
    
    def delete_care_record(self, record_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM CareRecords WHERE record_id = %s"
        cursor.execute(query, (record_id,))
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0

    def get_care_record_info(self, animal_id=None, supply_id=None, staff_id=None, staff_name=None, date=None, record_id=None):
        cursor = self.connection.cursor()
        query = """ 
        SELECT cr.record_id, a.animal_id, a.name, a.shelter_id, sh.name, s.staff_id, s.name, cr.date, cr.notes, cs.supply_id, cs.name, su.quantity_used
        FROM CareRecords cr
        JOIN Animals a ON cr.animal_id = a.animal_id
        JOIN Staff s ON cr.staff_id = s.staff_id
        JOIN Shelters sh ON a.shelter_id = sh.shelter_id
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