import sqlite3
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

# Returning all objects & history from comparison
def show_comparison():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Comparisons")
    comparisons = cursor.fetchall()
    connection.close()
    return json.dump(comparisons)

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
    connection.commit()
    connection.close()

# Comparing two objects together (Using Elo rating system)
def compare(object1_id, object2_id, did_object1_win):
    connection = get_connection()
    cursor = connection.cursor()
    
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

