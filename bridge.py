import sqlite3
import random
import json

# Pathways to files.
schema_file_path = "data/schema.sql"
sample_file_path = "data/sample.csv"
database_file_path = "data/database.db"

# Default variables
default_score = 1500

# Connect to the database
def get_connection():
    connection = sqlite3.connect(database_file_path)
    return connection

# Creating the database
def create_db():
    # Creating sqlite database. (database.db)
    connection = sqlite3.connect(database_file_path)
    with open(schema_file_path) as schema_file:
        connection.executescript(schema_file.read())
    
    # Closing connections.
    connection.commit()
    connection.close()

# Returning all objects & history from comparison
def show_comparison():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Comparisons")
    comparisons = cursor.fetchall()
    connection.close()
    return json.dumps(comparisons)

# Returning all objects from comparison
def show_objects():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Objects")
    objects = cursor.fetchall()
    connection.close()
    return json.dumps(objects)

# Returning all history from comparison
def show_history():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM History")
    history = cursor.fetchall()
    connection.close()
    return json.dumps(history)

# Creating new comparison
def new_comparison(title):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Comparisons (title) VALUES (?)", (title,))
    comparison_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return comparison_id

# Adding new object to comparison
def add_object_to_comparison(title, comparison_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Objects (title, score, comparison_id) VALUES (?, ?, ?)", (title, default_score, comparison_id))
    object_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return object_id

# Comparing two objects together (Using Elo rating system)
def compare(object1_id, object2_id, did_object1_win):
    connection = get_connection()
    cursor = connection.cursor()

    # Getting current scores of players
    cursor.execute("SELECT score FROM Objects WHERE id = ?", (object1_id,))
    score1 = cursor.fetchone()[0]

    cursor.execute("SELECT score FROM Objects WHERE id = ?", (object2_id,))
    score2 = cursor.fetchone()[0]

    # Calculate expected scores
    expected_score1 = 1 / (1 + 10 ** ((score2 - score1) / 400))
    expected_score2 = 1 / (1 + 10 ** ((score1 - score2) / 400))

    # Update scores based on game result
    k = 32
    if did_object1_win:
        score1 = score1 + k * (1 - expected_score1)
        score2 = score2 + k * (0 - expected_score2)
    else:
        score1 = score1 + k * (0 - expected_score1)
        score2 = score2 + k * (1 - expected_score2)
    
    # Update scores in database
    cursor.execute("UPDATE Objects SET score = ? WHERE id = ?", (round(score1), object1_id))
    cursor.execute("UPDATE Objects SET score = ? WHERE id = ?", (round(score2), object2_id))

    # Record game result in history
    cursor.execute("INSERT INTO History (object1_id, object2_id, did_object1_win) VALUES (?, ?, ?)", (object1_id, object2_id, did_object1_win))

    # Comming & close connections
    connection.commit()
    connection.close()

# Gets two random objects 
def get_random_objects(comparison_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Objects WHERE comparison_id = ?", (comparison_id,))
    objects = cursor.fetchall()
    connection.close()

    if len(objects) < 2:
        return None, None

    object1, object2 = random.sample(objects, 2)
    return object1, object2

# Returns a title of an object
def get_object_title(object_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM Objects WHERE id = ?", (object_id,))
    result = cursor.fetchall()
    connection.close()

    if result is None:
        return None
    
    return result[0]

# Just testing if everything works.
def test():
    create_db()
    key = new_comparison("Test_Compare")
    print("Comparisons:")
    print(show_comparison())
    object1_id = add_object_to_comparison("Apple", key)
    object2_id = add_object_to_comparison("Banana", key)
    object3_id = add_object_to_comparison("Baby", key)
    object4_id = add_object_to_comparison("Adult", key)
    print("Objects:")
    print(show_objects())
    compare(object1_id, object2_id, True)
    print("Objects: (after 1 game)")
    print(show_objects())
    compare(object1_id, object2_id, True)
    print("Objects: (after 2 game)")
    print(show_objects())
    print("History:")
    print(show_history())
    get_random_objects(key)
