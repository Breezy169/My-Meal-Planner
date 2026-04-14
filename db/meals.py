import sqlite3
import logging
import os
import sys 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("meals_db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
meals_db = os.path.join(BASE_DIR, 'meals.db')

def get_connection():
    # Get the directory where .exe lies
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create path to the db folder
    db_dir = os.path.join(base_path, "db")
    
    # Ensuring that the folder exists
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    db_path = os.path.join(db_dir, "meals.db") 
    return sqlite3.connect(db_path)

def init_meals_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS meals (
        id INTEGER PRIMARY KEY,
        name TEXT,
        calories INTEGER,
        proteins INTEGER,
        carbs INTEGER,
        fats INTEGER,
        cost INTEGER
    )
    ''')
    
    # Safely try to add the new recipe column if it doesn't exist yet
    try:
        cursor.execute("ALTER TABLE meals ADD COLUMN recipe TEXT")
    except sqlite3.OperationalError:
        pass # Column already exists, safe to ignore

    conn.commit()
    conn.close()

# ADD A MEAL
def add_meal(name, calories, proteins, carbs, fats, cost, recipe):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO meals (name, calories, proteins, carbs, fats, cost, recipe)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, calories, proteins, carbs, fats, cost, recipe))

    conn.commit()
    conn.close()

# GET ALL MEALS
def get_all_meals():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, calories, proteins, carbs, fats, cost, recipe FROM meals")
    rows = cursor.fetchall()
    conn.close()
    return rows

# UPDATE A MEAL
def update_meal(meal_id, name, calories, proteins, carbs, fats, cost, recipe):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE meals 
        SET name=?, calories=?, proteins=?, carbs=?, fats=?, cost=?, recipe=?
        WHERE id=?
    ''', (name, calories, proteins, carbs, fats, cost, recipe, meal_id))
    conn.commit()
    conn.close()

# DELETE A MEAL
def delete_meal(meal_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM meals WHERE id=?", (meal_id,))
    conn.commit()
    conn.close()