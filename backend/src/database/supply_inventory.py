class SupplyInventoryDB:
    def __init__(self, connection):
        self.connection = connection
    
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
        new_id = cursor.lastrowid
        cursor.close()
        return {"supply_id": supply_id, "quantity": quantity, "shelter_id": shelter_id}

    def update_supply_inventory(self, supply_id, quantity, shelter_id):
        cursor = self.connection.cursor()
        query = "UPDATE SupplyInventory SET quantity = %s WHERE supply_id = %s AND shelter_id = %s"
        cursor.execute(query, (quantity, supply_id, shelter_id))
        rows_affected = cursor.rowcount
        cursor.close()

        if rows_affected > 0:
            return self.get_supply_inventory(supply_id=supply_id, shelter_id=shelter_id)[0]
        return None
    
    def delete_supply_inventory(self, supply_id, shelter_id):
        cursor = self.connection.cursor()
        query = "DELETE FROM SupplyInventory WHERE supply_id = %s AND shelter_id = %s"
        cursor.execute(query, (supply_id, shelter_id))
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0