from flask import Flask, jsonify, g, request
import mysql.connector
from dotenv import load_dotenv
import os
import sys
import traceback
from db import Database
from database.animals import AnimalDB
from database.staff import StaffDB
from database.care_records import CareRecordDB
from database.care_supplies import CareSuppliesDB
from database.shelters import ShelterDB
from database.supply_inventory import SupplyInventoryDB
from database.supply_usage import SupplyUsageDB
from datetime import datetime

app = Flask(__name__)
load_dotenv()

def get_db_connection():
    print("Getting db connection", file=sys.stderr)
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host = os.getenv("DB_HOST"),
            user = os.getenv("DB_USER"),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME')
        )
    return g.db

@app.teardown_appcontext
def close_db_conenction(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/api/animals", methods=["GET", "POST"])
@app.route("/api/animals/<int:animal_id>", methods=["PUT", "DELETE"])
def animals(animal_id=None):
    db = get_db_connection()
    d = AnimalDB(db)

    try:
        if request.method == "GET":
            animal_id_param = request.args.get('animal_id')
            name = request.args.get('name')
            species = request.args.get('species')
            shelter_id = request.args.get('shelter_id')

            animals = d.get_animals(animal_id=animal_id_param, name=name, species=species, shelter_id=shelter_id)
            return jsonify(animals)
        
        elif request.method == "POST":
            data = request.get_json()
            if not data or 'name' not in data or 'species' not in data:
                return jsonify({"error": "Invalid input"}), 400
            
            name = data['name']
            species = data['species']
            shelter_id = None
            if 'shelter_id' in data:
                shelter_id = data['shelter_id']
            new_animal = d.post_animal(name, species, shelter_id)
            db.commit()
            return jsonify(new_animal), 201
        
        elif request.method == "PUT":
            if animal_id is None:
                return jsonify({"error": "No animal_id provided"}), 400

            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            name = data.get('name')
            species = data.get('species')
            shelter_id = data.get('shelter_id')
            new_animal = d.update_animal(animal_id, name, species, shelter_id)
            db.commit()
            return jsonify(new_animal), 201
        
        elif request.method == "DELETE":
            if animal_id is None:
                return jsonify({"error": "No animal_id provided"}), 400
            deleted_animal = d.delete_animal(animal_id)
            db.commit()
            if deleted_animal:
                return jsonify({"message": "Animal deleted"}), 200
            else:
                return jsonify({"error": "Animal not found"}), 404
          
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/staff", methods=["GET", "POST"])
@app.route("/api/staff/<int:staff_id>", methods=["PUT", "DELETE"])
def staff(staff_id=None):
    db = get_db_connection()
    d = StaffDB(db)

    try:
        if request.method == "GET":
            staff_id = request.args.get('staff_id')
            name = request.args.get('name')
            email = request.args.get('email')
            role = request.args.get('role')
            shelter_id = request.args.get('shelter_id')

            staff = d.get_staff(staff_id=staff_id, name=name, email=email, role=role, shelter_id=shelter_id)
            return jsonify(staff)
        
        elif request.method == "POST":
            data = request.get_json()
            if not data or 'name' not in data or 'email' not in data or 'role' not in data or 'shelter_id' not in data:
                return jsonify({"error": "Invalid input"}), 400
            
            name = data['name']
            email = data['email']
            role = data['role']
            shelter_id = data['shelter_id']
            new_staff = d.post_staff(name, email, role, shelter_id)
            db.commit()
            return jsonify(new_staff), 201
        
        elif request.method == "PUT":
            if staff_id is None:
                return jsonify({"error": "No staff_id provided"}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            name = data.get('name')
            email = data.get('email')
            role = data.get('role')
            shelter_id = data.get('shelter_id')

            new_staff = d.update_staff(staff_id, name, email, role, shelter_id)
            db.commit()
            return jsonify(new_staff), 201
        elif request.method == "DELETE":
            if staff_id is None:
                return jsonify({"error": "No staff_id provided"}), 400
            deleted_staff = d.delete_staff(staff_id)
            db.commit()
            if deleted_staff:
                return jsonify({"message": "Staff deleted"}), 200
            else:
                return jsonify({"error": "Staff not found"}), 404

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
    
@app.route("/api/shelters", methods=["GET", "POST"])
@app.route("/api/shelters/<int:shelter_id>", methods=["PUT", "DELETE"])
def shelters(shelter_id=None):
    db = get_db_connection()
    d = ShelterDB(db)

    try:
        if request.method == "GET":
            shelter_id = request.args.get('shelter_id')
            name = request.args.get('name')
            capacity = request.args.get('capacity')

            shelters = d.get_shelters(shelter_id=shelter_id, name=name, capacity=capacity)
            return jsonify(shelters)
        
        elif request.method == "POST":
            data = request.get_json()
            if not data or 'name' not in data or 'capacity' not in data:
                return jsonify({"error": "Invalid input"}), 400
            
            name = data['name']
            capacity = data['capacity']
            address = None
            phone_number = None,
            email = None
            if 'address' in data:
                address = data['address']
            if 'phone_number' in data:
                phone_number = data['phone_number']
            if 'email' in data:
                email = data['email']
            
            new_shelter = d.post_shelters(name, capacity, address, phone_number, email)
            db.commit()
            return jsonify(new_shelter), 201
        
        elif request.method == "PUT":
            if shelter_id is None:
                return jsonify({"error": "No shelter_id provided"}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            name = data.get('name')
            capacity = data.get('capacity')
            address = data.get('address')
            phone_number = data.get('phone_number')
            email = data.get('email')
            new_shelter = d.update_shelter(shelter_id, name, capacity, address, phone_number, email)
            db.commit()
            return jsonify(new_shelter), 201
        
        elif request.method == "DELETE":
            if shelter_id is None:
                return jsonify({"error": "No shelter_id provided"}), 400
            deleted_shelter = d.delete_shelter(shelter_id)
            db.commit()
            if deleted_shelter:
                return jsonify({"message": "Shelter deleted"}), 200
            else:
                return jsonify({"error": "Shelter not found"}), 404

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
    
@app.route("/api/care_records", methods=["GET", "POST"])
@app.route("/api/care_records/<int:record_id>", methods=["PUT", "DELETE"])
def care_record(record_id=None):
    db = get_db_connection()
    d = CareRecordDB(db)

    try:
        if request.method == "GET":
            animal_id = request.args.get('animal_id')
            staff_id = request.args.get('staff_id')
            date = request.args.get('date')
            notes = request.args.get('notes')

            care_records = d.get_care_records(animal_id=animal_id, staff_id=staff_id, date=date, notes=notes)
            return jsonify(care_records)
        
        elif request.method == "POST":
            data = request.get_json()
            if not data or 'animal_id' not in data or 'staff_id' not in data or 'date' not in data:
                return jsonify({"error": "Invalid input"}), 400

            animal_id = data['animal_id']
            staff_id = data['staff_id']
            date = data['date']
            notes = None
            if 'notes' in data:
                notes = data['notes']
            new_care_record = d.post_care_record(animal_id, staff_id, date, notes)
            db.commit()
            return jsonify(new_care_record), 201
        elif request.method == "PUT":
            if record_id is None:
                return jsonify({"error": "No record_id provided"}), 400
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            animal_id = data.get('animal_id')
            staff_id = data.get('staff_id')
            date = data.get('date')
            notes = data.get('notes')
            new_care_record = d.update_care_record(record_id, animal_id, staff_id, date, notes)
            db.commit()
            return jsonify(new_care_record), 201
        
        elif request.method == "DELETE":
            if record_id is None:
                return jsonify({"error": "No record_id provided"}), 400
            deleted_care_record = d.delete_care_record(record_id)
            db.commit()
            if deleted_care_record:
                return jsonify({"message": "Care record deleted"}), 200
            else:
                return jsonify({"error": "Care record not found"}), 404
            
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
    
@app.route('/api/supplies_with_inventory', methods=["GET"])
def supplies_with_inventory():
    db = get_db_connection()
    d = CareSuppliesDB(db)

    try:
        supply_id = request.args.get('supply_id')
        name = request.args.get('name')
        quantity = request.args.get('quantity')
        shelter_id = request.args.get('shelter_id')

        supplies = d.get_care_supplies_with_inventory(supply_id=supply_id, supply_name=name, quantity=quantity, shelter_id=shelter_id)
        return jsonify(supplies)
    
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
    
    

@app.route("/api/supplies", methods=["GET", "POST"])
@app.route("/api/supplies/<int:supply_id>", methods=["PUT", "DELETE"])
def supplies(supply_id=None):
    db = get_db_connection()
    d = CareSuppliesDB(db)

    try: 
        if request.method == "GET":
            supply_id = request.args.get('supply_id')
            name = request.args.get('name')

            supplies = d.get_care_supplies(supply_id=supply_id, name=name)
            return jsonify(supplies)
        
        elif request.method == "POST": 
            data = request.get_json()
            if not data or 'name' not in data:
                return jsonify({"error": "Invalid input"}), 400

            name = data['name']
            new_supply = d.post_care_supplies(name)
            db.commit()
            return jsonify(new_supply), 201
        elif request.method == "PUT":
            if supply_id is None:
                return jsonify({"error": "No supply_id provided"}), 400
            
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            name = data.get('name')
            new_supply = d.update_care_supplies(supply_id, name)
            db.commit()
            return jsonify(new_supply), 201
        elif request.method == "DELETE":
            if supply_id is None:
                return jsonify({"error": "No supply_id provided"}), 400
            deleted_supply = d.delete_care_supplies(supply_id)
            db.commit()
            if deleted_supply:
                return jsonify({"message": "Supply deleted"}), 200
            else:
                return jsonify({"error": "Supply not found"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
    
@app.route("/api/supply_inventory", methods=["GET", "POST"])
@app.route("/api/supply_inventory/<int:supply_id>/<int:shelter_id>", methods=["PUT", "DELETE"])
def supply_inventory(supply_id=None, shelter_id=None):
    db = get_db_connection()
    d = SupplyInventoryDB(db)

    try:
        if request.method == "GET":
            supply_id = request.args.get('supply_id')
            quantity = request.args.get('quantity')
            shelter_id = request.args.get('shelter_id')

            supply_inventory = d.get_supply_inventory(supply_id=supply_id, quantity=quantity, shelter_id=shelter_id)
            return jsonify(supply_inventory)
        
        elif request.method == "POST":
            data = request.get_json()
            if not data or 'supply_id' not in data or 'quantity' not in data or 'shelter_id' not in data:
                return jsonify({"error": "Invalid input"}), 400

            supply_id = data['supply_id']
            quantity = data['quantity']
            shelter_id = data['shelter_id']
            new_supply_inventory = d.post_supply_inventory(supply_id, quantity, shelter_id)
            db.commit()
            return jsonify(new_supply_inventory), 201
        
        elif request.method == "PUT":
            if supply_id is None or shelter_id is None:
                return jsonify({"error": "No supply_id or shelter_id provided"}), 400
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            quantity = data.get('quantity')
            new_supply_inventory = d.update_supply_inventory(supply_id, shelter_id, quantity)
            db.commit()
            return jsonify(new_supply_inventory), 201
        
        elif request.method == "DELETE":
            if supply_id is None or shelter_id is None:
                return jsonify({"error": "No supply_id or shelter id provided"}), 400
            deleted_supply_inventory = d.delete_supply_inventory(supply_id, shelter_id)
            db.commit()
            if deleted_supply_inventory:
                return jsonify({"message": "Supply inventory deleted"}), 200
            else:
                return jsonify({"error": "Supply inventory not found"}), 404
            
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/supply_usage", methods=["GET", "POST"])
@app.route("/api/supply_usage/<int:care_record_id>", methods=["PUT", "DELETE"])
def supply_usage(supply_id = None, care_record_id = None):
    db = get_db_connection()
    d = SupplyUsageDB(db)

    try:
        if request.method == "GET":
            supply_id = request.args.get('supply_id')
            quantity = request.args.get('quantity')
            care_record_id = request.args.get('care_record_id')

            supply_usage = d.get_supply_usage(supply_id=supply_id, quantity_used=quantity, record_id=care_record_id)
            return jsonify(supply_usage)
        elif request.method == "POST":
            data = request.get_json()
        
            print("Received supply usage data:", data)
        
            if not isinstance(data, list):
                return jsonify({"error": "Input must be a list of supply usages"}), 400

            for item in data:
                if not all(key in item for key in ['supply_id', 'quantity', 'care_record_id']):
                    return jsonify({
                        "error": "Invalid input. Each item must contain supply_id, quantity, and care_record_id",
                        "problematic_item": item
                    }), 400

            supplies_data = [
                (item['care_record_id'], item['supply_id'], item['quantity']) 
                for item in data
            ]
            
            new_supply_usage = d.bulk_post_supply_usage(supplies_data)
            db.commit()
            return jsonify(new_supply_usage), 201
            
        elif request.method == "PUT":
            if supply_id is None or care_record_id is None:
                return jsonify({"error": "No supply_id or care_record_id provided"}), 400
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            quantity = data.get('quantity')
            new_supply_usage = d.update_supply_usage(supply_id, care_record_id, quantity)
            db.commit()
            return jsonify(new_supply_usage), 201
        
        elif request.method == "DELETE":
            if care_record_id is None:
                return jsonify({"error": "No supply_id or care_record_id provided"}), 400

            deleted_supply_usage = d.delete_supply_usage(care_record_id)
            db.commit()
            if deleted_supply_usage:
                return jsonify({"message": "Supply usage deleted"}), 200
            else:
                return jsonify({"error": "Supply usage not found"}), 404
            
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@app.route("/api/care_records_info",methods=["GET"])
def care_record_info():
    db = get_db_connection()
    d = CareRecordDB(db)

    try:
        if request.method == "GET":
            animal_id = request.args.get('animal_id')
            supply_id = request.args.get('supply_id')
            staff_id = request.args.get('staff_id')
            staff_name = request.args.get('staff_name')
            date = request.args.get('date')
            record_id = request.args.get('record_id')

            records = d.get_care_record_info(animal_id=animal_id, supply_id=supply_id, staff_id=staff_id, staff_name=staff_name, date=date, record_id=record_id)
            care_records = {}
            for row in records:
                record_id = row[0]
                if record_id not in care_records:
                    care_records[record_id] = {
                        "record_id": record_id,
                        "animal_id": row[1],
                        "animal_name": row[2],
                        "shelter_id": row[3],
                        "shelter_name": row[4],
                        "staff_id": row[5],
                        "staff_name": row[6],
                        "date": row[7].strftime("%Y-%m-%d"),
                        "notes": row[8],
                        "supplies": []
                    }
                if row[8]:
                    care_records[record_id]["supplies"].append({
                        "supply_id": row[9],
                        "supply_name": row[10],
                        "supply_quantity": row[11]
                    })
            return jsonify(list(care_records.values()))
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@app.route("/api/report", methods=['POST'])
def generate_report():
    try:
        data = request.json

        start_date = data.get('startDate')
        end_date = data.get('endDate')
        shelter_ids = data.get('shelterIds', [])
        animal_ids = data.get('animalIds', [])
        supply_ids = data.get('supplyIds', [])
        staff_ids = data.get('staffIds', [])

        shelter_string = ','.join(map(str, shelter_ids)) if shelter_ids else None
        animal_string = ','.join(map(str, animal_ids)) if animal_ids else None
        supply_string = ','.join(map(str, supply_ids)) if supply_ids else None
        staff_string = ','.join(map(str, staff_ids)) if staff_ids else None

        parsed_start_date =  start_date if start_date else None
        parsed_end_date = end_date if end_date else None
        
        db = get_db_connection()
        
        try:
            cursor = db.cursor(dictionary=True)
            cursor.callproc('GenerateReport', [
                parsed_start_date,
                parsed_end_date,
                shelter_string,
                animal_string,
                supply_string,
                staff_string
            ])

            results = list(cursor.stored_results())
            if len(results) >= 2:
                stats_data = results[0].fetchall()
                
                records = results[1].fetchall()
            else:
                stats_data = []
                records = results[0].fetchall() if results else []

            care_records = {}
            for row in records:
                record_id = row['record_id']
                if record_id not in care_records:
                    care_records[record_id] = {
                        "record_id": record_id,
                        "animal_id": row['animal_id'],
                        "animal_name": row['animal_name'],
                        "shelter_id": row['shelter_id'],
                        "shelter_name": row['shelter_name'],
                        "staff_id": row['staff_id'],
                        "staff_name": row['staff_name'],
                        "date": row['record_date'].strftime("%Y-%m-%d"),
                        "notes": row['notes'],
                        "supplies": []
                    }
                
                if row['supply_id'] is not None:
                    care_records[record_id]["supplies"].append({
                        "supply_id": row['supply_id'],
                        "supply_name": row['supply_name'],
                        "supply_quantity": row['quantity_used']
                    })

            statistics = {}
            for stat in stats_data:
                statistics[stat['stat_name']] = {
                    'value': stat['stat_value'],
                    'count': stat['stat_count']
                }

            response = {
                'statistics': statistics,
                'care_records': list(care_records.values())
            }

            return jsonify(response)
        
        except mysql.connector.Error as err:
            return jsonify({'error': f'Database error: {err}'}), 500
        
        finally:
            if cursor:
                cursor.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
    

                
            
    
    

    

if __name__ == "__main__":
    app.run(debug=True)