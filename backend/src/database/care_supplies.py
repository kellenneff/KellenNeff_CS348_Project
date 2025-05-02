import mysql.connector
class CareSuppliesDB:
    def __init__(self, connection):
        self.connection = connection

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
    
    def get_care_supplies_with_inventory(self, shelter_id=None, supply_id=None, supply_name=None, quantity=None):
        cursor = self.connection.cursor()
        query = """
            SELECT cs.supply_id, cs.name, si.quantity, si.shelter_id FROM CareSupplies cs
            JOIN SupplyInventory si ON cs.supply_id = si.supply_id
        """
        params = []
        where_clauses = []

        if shelter_id is not None:
            where_clauses.append("si.shelter_id = %s")
            params.append(shelter_id)
        if supply_id is not None:
            where_clauses.append('cs.supply_id = %s')
            params.append(supply_id)
        if supply_name is not None:
            where_clauses.append('cs.name = %s')
            params.append(supply_name)
        if quantity is not None:
            where_clauses.append('si.quantity >= %s')
            params.append(quantity)

        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        cursor.execute(query, params)
        care_supplies = cursor.fetchall()
        cursor.close()
        return care_supplies      

    def post_care_supplies(self, name):
        cursor = self.connection.cursor()
        query = "INSERT INTO CareSupplies (name) VALUES (%s)"
        cursor.execute(query, (name,))
        new_id = cursor.lastrowid
        cursor.close()
        return {"supply_id": new_id, "name": name}
        
    def update_care_supply(self, supply_id, name):
        cursor = self.connection.cursor()
        query = "UPDATE CareSupplies SET name = %s WHERE supply_id = %s"
        cursor.execute(query, (name, supply_id))
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
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0