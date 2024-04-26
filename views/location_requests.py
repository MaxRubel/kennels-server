import sqlite3
import json
from models import Location, Employee, Animal
LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()


        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.address
        FROM location a
        """)

        locations = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row['id'], row['name'], row['address'])
            locations.append(location.__dict__) 
            
        for location in locations:
            location_id = location['id']
            
            #get employees of location:
            db_cursor.execute("""
            SELECT
                e.id,
                e.name,
                e.location_id
            FROM employee e
            WHERE e.location_id = ?
            """,(location_id,))
            dataset = db_cursor.fetchall()
            
            employess = []
            
            for row in dataset:
                employee = Employee(row['id'], row['name'], row['location_id'])
                employess.append(employee.__dict__)
                
            location["employees"] = employess
            
            #get animals of location:
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.customer_id,
                a.location_id,
                a.status
            FROM animal a
            WHERE a.location_id = ?
            """,(location_id,))
            
            dataset = db_cursor.fetchall()
            animals = []
            
            for row in dataset:
                animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['customer_id'], row['location_id'])
                animals.append(animal.__dict__)
                
            location['animals'] = animals
      
        return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            a.id,
            a.address
        FROM location a
        WHERE a.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        location = Location(data['id'], data['address'])

        return location.__dict__

def create_location(location):
    max_id = LOCATIONS[-1]["id"]
    location["id"] = max_id + 1
    LOCATIONS.append(location)
    return location

def update_location(id, new_location):
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break
            
def delete_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM location
        WHERE id = ?
        """, (id, ))