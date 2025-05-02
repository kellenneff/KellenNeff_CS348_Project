import mysql.connector
from dotenv import load_dotenv
import os

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Animals (
            animal_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            species VARCHAR(50) NOT NULL,
            shelter_id INT REFERENCES Shelters(shelter_id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Shelters (
            shelter_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            capacity INT CHECK (capacity > 0),
            address TEXT,
            phone_number VARCHAR(20),
            email VARCHAR(100)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staff (
            staff_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(100),
            role VARCHAR(50),
            shelter_id INT REFERENCES Shelters(shelter_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CareSupplies (
            supply_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS SupplyInventory (
            supply_id INT REFERENCES CareSupplies(supply_id) ON DELETE CASCADE,
            quantity INT CHECK (quantity >= 0),
            shelter_id INT REFERENCES Shelters(shelter_id) ON DELETE CASCADE,
            PRIMARY KEY (supply_id, shelter_id)
        )               
    """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS SupplyUsage (
            record_id INT REFERENCES CareRecords(record_id),
            supply_id INT REFERENCES CareSupplies(supply_id),
            quantity_used INT CHECK (quantity_used > 0),
            PRIMARY KEY (record_id, supply_id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CareRecords (
            record_id SERIAL PRIMARY KEY,
            animal_id INT REFERENCES Animals(animal_id) ON DELETE CASCADE,
            staff_id INT REFERENCES Staff(staff_id),
            date DATE,
            notes TEXT
        )
    """)
    connection.commit()
    cursor.close()

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS SupplyUsage")
    cursor.execute("DROP TABLE IF EXISTS CareRecords")
    cursor.execute("DROP TABLE IF EXISTS CareSupplies")
    cursor.execute("DROP TABLE IF EXISTS Staff")
    cursor.execute("DROP TABLE IF EXISTS Shelters")
    cursor.execute("DROP TABLE IF EXISTS Animals")
    connection.commit()
    cursor.close()

def create_insert_trigger(connection):
    cursor = connection.cursor()
    cursor.execute("DELIMETER //")

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_inventory_after_insert
        AFTER INSERT ON SupplyUsage
        FOR EACH ROW
        BEGIN
            SET @shelter_id = (
                SELECT shelter_id
                FROM CareRecords cr
                JOIN Animals a ON cr.animal_id = a.animal_id
                WHERE cr.record_id = NEW.record_id       
            );
                   
            UPDATE SupplyInventory
            SET quantity = quantity - NEW.quantity_used
            WHERE supply_id = NEW.supply_id AND shelter_id = @shelter_id;
                   
        END //       
    """)
    cursor.execute("DELIMETER ;")
    connection.commit()
    cursor.close()

def create_delete_trigger(connection):
    cursor = connection.cursor()
    cursor.execute("DELIMETER //")

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_inventory_after_delete
        AFTER DELETE ON SupplyUsage
        FOR EACH ROW
        BEGIN
            SET @shelter_id = (
                SELECT shelter_id
                FROM CareRecords cr
                JOIN Animals a ON cr.animal_id = a.animal_id
                WHERE cr.record_id = OLD.record_id
            );
            
            UPDATE SupplyInventory
            SET quantity = quantity + OLD.quantity_used
            WHERE supply_id = OLD.supply_id AND shelter_id = @shelter_id;
    END//
    """)

    cursor.execute("DELIMETER ;")
    connection.commit()
    cursor.close()
