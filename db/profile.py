import sqlite3
import logging
import os
from datetime import date
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("profile_db")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
profile_db = os.path.join(BASE_DIR, 'profile.db')

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
        
    db_path = os.path.join(db_dir, "profile.db") 
    return sqlite3.connect(db_path)

def init_profile_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS profile (
        id INTEGER PRIMARY KEY,
        username TEXT,
        start_date TEXT,
        plan_name TEXT,
        daily_calories INTEGER,
        starting_weight REAL,
        current_weight REAL,
        body_fat REAL,
        max_deadlift REAL,
        max_squat REAL,
        longest_run REAL
    )
    ''')
    
    # Check if profile exists, else take the standard values
    cursor.execute("SELECT COUNT(*) FROM profile")
    if cursor.fetchone()[0] == 0:
        today_str = date.today().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO profile (
                id, username, start_date, plan_name, daily_calories, 
                starting_weight, current_weight, body_fat, 
                max_deadlift, max_squat, longest_run
            )
            VALUES (1, 'User', ?, 'Cut', 2000, 80.0, 85.0, 15.0, 100.0, 80.0, 5.0)
        ''', (today_str,))
        logger.info("Standard Profile created.")

    conn.commit()
    conn.close()
    logger.info("Profile DB initialized.")

# GET PROFILE DATA
def get_profile():
    conn = get_connection()
    cursor = conn.cursor()
    # SINGLE PROFILE
    cursor.execute("SELECT * FROM profile WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return row

# UPDATE PROFILE
def update_profile(username, plan_name, daily_calories, starting_weight, current_weight, body_fat, max_deadlift, max_squat, longest_run):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE profile 
        SET username = ?, 
            plan_name = ?, 
            daily_calories = ?, 
            starting_weight = ?, 
            current_weight = ?, 
            body_fat = ?, 
            max_deadlift = ?, 
            max_squat = ?, 
            longest_run = ?
        WHERE id = 1
    ''', (username, plan_name, daily_calories, current_weight, starting_weight, body_fat, max_deadlift, max_squat, longest_run))
    
    conn.commit()
    conn.close()
    logger.info("Profil erfolgreich aktualisiert.")

# OPTIONAL: CHANGE START DATE IF YOU WANT TO START OVER
def update_start_date(new_date_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE profile SET start_date = ? WHERE id = 1", (new_date_str,))
    conn.commit()
    conn.close()
    logger.info(f"Startdatum auf {new_date_str} geändert.")