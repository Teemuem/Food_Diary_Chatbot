# db_utils.py
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Function to establish a connection to the MySQL database
def connect_to_mysql():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),  # Docker service name for MySQL
        user=os.getenv("MYSQL_USER"),  # MySQL username
        password=os.getenv("MYSQL_PASSWORD"),  # MySQL password
        database=os.getenv("MYSQL_DATABASE")  # MySQL database name
    )
    create_table(connection)  # Ensure table is created on startup
    return connection

# Function to create necessary tables if they do not exist
def create_table(connection):
    cursor = connection.cursor()
    
    # Create food_logs table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS food_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            food_name VARCHAR(255),
            quantity VARCHAR(255),
            meal_time VARCHAR(255),
            category VARCHAR(100),
            calories FLOAT,
            protein FLOAT,
            carbohydrates FLOAT,
            fats FLOAT,
            fiber FLOAT,
            sugars FLOAT,
            `log_date` DATE,
            image_path VARCHAR(255)
        )
    """)
    
    # Create daily_notes table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            log_date DATE UNIQUE,  -- Ensure only one note per day
            notes TEXT
        )
    """)
    
    connection.commit() # Save changes to the database

# Function to insert food log data into the database
def insert_food_data(connection, food_items, meal_time, log_date):
    cursor = connection.cursor()
    for item in food_items:
        # Convert possible numpy.int64 to Python int
        calories = int(item["calories"]) if isinstance(item["calories"], (int, float)) else 0
        protein = float(item["protein"]) if isinstance(item["protein"], (int, float)) else 0.0
        carbohydrates = float(item["carbohydrates"]) if isinstance(item["carbohydrates"], (int, float)) else 0.0
        fats = float(item["fats"]) if isinstance(item["fats"], (int, float)) else 0.0
        fiber = float(item["fiber"]) if isinstance(item["fiber"], (int, float)) else 0.0
        sugars = float(item["sugars"]) if isinstance(item["sugars"], (int, float)) else 0.0

        cursor.execute("""
            INSERT INTO food_logs (food_name, quantity, meal_time, category, calories, protein, carbohydrates, fats, fiber, sugars, `log_date`, image_path)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item["food_name"], item["quantity"], meal_time, item["category"],
            calories, protein, carbohydrates, fats, fiber, sugars, log_date, item.get("image_path")
        ))
    connection.commit()

# Function to edit an existing food log entry
def edit_log(connection, log_id, updated_data):
    cursor = connection.cursor()
    
    cursor.execute("""
        UPDATE food_logs 
        SET food_name = %s, quantity = %s, meal_time = %s, category = %s, 
            calories = %s, protein = %s, carbohydrates = %s, fats = %s, 
            fiber = %s, sugars = %s 
        WHERE id = %s
    """, (
        updated_data["food_name"], updated_data["quantity"], updated_data["meal_time"],
        updated_data["category"], 
        float(updated_data["calories"]), 
        float(updated_data["protein"]), 
        float(updated_data["carbohydrates"]), 
        float(updated_data["fats"]), 
        float(updated_data["fiber"]), 
        float(updated_data["sugars"]), 
        int(log_id)  # Ensure log_id is an int
    ))
    connection.commit()

# Function to delete a food log entry
def delete_log(connection, log_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM food_logs WHERE id = %s", (log_id,))
    connection.commit()

# Function to save or update daily notes
def save_daily_notes(connection, log_date, notes):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO daily_notes (log_date, notes)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE notes = %s
    """, (log_date, notes, notes))
    connection.commit()

# Function to retrieve daily notes for a specific date
def get_daily_notes(connection, log_date):
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM daily_notes WHERE log_date = %s", (log_date,))
    result = cursor.fetchone()
    return result[0] if result else ""