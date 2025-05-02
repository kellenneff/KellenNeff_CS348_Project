import mysql.connector
class AnimalDB:
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
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected > 0