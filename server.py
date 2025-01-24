from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# PostgreSQL connection string
DATABASE_URL = "postgres://neondb_owner:npg_E1WdY0SHGliu@ep-old-smoke-a1mlqqco-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Connect to PostgreSQL
def get_db_connection():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode="require")
        print("Database connection successful!")
        return connection
    except Exception as e:
        print(f"Database connection failed: {e}")
        raise

@app.route('/add-student', methods=['POST'])
def add_student():
    data = request.json  # Get data from the request body
    # Sample data for testing
    name = "ArunKumar"
    roll_no = "1234"
    email = "234355@gmail.com"
    gender = "male"
    department = "MCA"

    # Validate required fields
    if not all([name, roll_no, email, gender, department]):
        return jsonify({"error": "All fields are required!"}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert data into the database
        cursor.execute(
            "INSERT INTO students (name, roll_no, email, gender, department) VALUES (%s, %s, %s, %s, %s)",
            (name, roll_no, email, gender, department),
        )

        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"message": "Student added successfully!"}), 201

    except Exception as e:
        print(f"Error while inserting data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
