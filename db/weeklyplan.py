import sqlite3
import logging
import os
import sys 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("weekly_db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
weekly_db = os.path.join(BASE_DIR, 'weeklyplan.db')

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
        
    db_path = os.path.join(db_dir, "weeklyplan.db")
    return sqlite3.connect(db_path)

def init_weekly_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weekly_plan (
        id INTEGER PRIMARY KEY,
        day TEXT,
        meal_name TEXT,
        calories INTEGER,
        cost REAL
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Weekly Plan DB initialisiert.")

# ADD A MEAL TO THE WEEKLY PLAN
def add_to_plan(day, meal_name, calories, cost):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO weekly_plan (day, meal_name, calories, cost)
        VALUES (?, ?, ?, ?)
    ''', (day, meal_name, calories, cost))

    conn.commit()
    conn.close()

# GET ALL DATA OF A SINGLE ENTRY
def get_plan_by_day(day):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, meal_name, calories, cost FROM weekly_plan WHERE day=?", (day,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# GET THE WHOLE WEEKLY PLAN DATA
def get_full_weekly_plan():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weekly_plan")
    rows = cursor.fetchall()
    conn.close()
    return rows

# DELETE SINGLE MEAL FROM WEEKLY PLAN (NEEDED FOR WHEN A MEAL GETS REMOVED FROM SAVED MEAL LIST)
def remove_from_plan(entry_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weekly_plan WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()

# REMOVE SINGLE MEAL FROM WEEKLY PLAN
def remove_from_plan_by_name(meal_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weekly_plan WHERE meal_name=?", (meal_name,))
    conn.commit()
    conn.close()

# DELETE WHOLE WEEKLY PLAN DATA
def clear_entire_week():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weekly_plan")
    conn.commit()
    conn.close()

# UPDATE WEEKLY PLAN DATA ENTRY
def update_weekly_entries_by_name(old_name, new_name, calories, cost):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE weekly_plan 
        SET meal_name = ?, calories = ?, cost = ?
        WHERE meal_name = ?
    ''', (new_name, calories, cost, old_name))
    conn.commit()
    conn.close()