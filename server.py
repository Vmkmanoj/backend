from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Allows all origins (for development)

# PostgreSQL connection string (update with your credentials)
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
    try:
        # Get data from the request
        data = request.json
        print("Received data:", data)

        name = data.get("name")
        roll_no = data.get("rollNo")
        email = data.get("email")
        gender = data.get("gender")
        department = data.get("department")

        # Validate required fields
        if not all([name, roll_no, email, gender, department]):
            return jsonify({"error": "All fields are required!"}), 400

        # Database interaction
        connection = get_db_connection()
        cursor = connection.cursor()

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
    



@app.route("/getUser", methods=["GET"])
def get_user():
    try:
        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Optional: Get specific user by ID (if `id` parameter is provided)
        user_id = request.args.get("id")
        if user_id:
            cursor.execute("SELECT * FROM students WHERE id = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM students")

        users = cursor.fetchall()

        # Prepare response
        user_list = []
        for user in users:
            user_list.append({
                "id": user[0],
                "name": user[1],
                "roll_no": user[2],
                "email": user[3],
                "gender": user[4],
                "department": user[5]
            })

        cursor.close()
        connection.close()

        return jsonify(user_list), 200

    except Exception as e:
        print(f"Error fetching user data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    try:
        # Get user ID from request
        user_id = request.args.get('id')
        if not user_id:
            return jsonify({"error": "User ID is required!"}), 400

        # Connect to the database
        connection = get_db_connection()
        cursor = connection.cursor()

        # Execute delete statement
        cursor.execute("DELETE FROM students WHERE id = %s", (user_id,))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found!"}), 404

        cursor.close()
        connection.close()

        return jsonify({"message": "User deleted successfully!"}), 200

    except Exception as e:
        print(f"Error while deleting user: {e}")
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(debug=True)
