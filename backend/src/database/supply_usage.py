import mysql.connector
class SupplyUsageDB:
    def __init__(self, connection):
        self.connection = connection

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
        new_id = cursor.lastrowid
        cursor.close()
        return {"record_id": record_id, "supply_id": supply_id, "quantity_used": quantity_used}  
    
    def bulk_post_supply_usage(self, supplies_data):
        cursor = self.connection.cursor()
        query = "INSERT INTO SupplyUsage (record_id, supply_id, quantity_used) VALUES (%s, %s, %s)"
        
        try:
            cursor.executemany(query, supplies_data)
            
            # Get the IDs of inserted records if needed
            inserted_ids = cursor.rowcount
            cursor.close()
            
            return {
                "message": "Bulk insert successful",
                "inserted_records": inserted_ids
            }
        except Exception as e:
            self.connection.rollback()
            raise

    def update_supply_usage(self, record_id, supply_id, quantity_used):
        cursor = self.connection.cursor()
        query = "UPDATE SupplyUsage SET quantity_used = %s WHERE record_id = %s AND supply_id = %s"
        cursor.execute(query, (quantity_used, record_id, supply_id))
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_supply_usage(record_id=record_id, supply_id=supply_id)[0]
        return None
    
    def delete_supply_usage(self, record_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM SupplyUsage WHERE record_id = %s"
        print(query)
        cursor.execute(query, (record_id,))
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0
    
    