from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# PostgreSQL connection string
DATABASE_URL = "postgres://neondb_owner:npg_E1WdY0SHGliu@ep-old-smoke-a1mlqqco-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    connection = psycopg2.connect(DATABASE_URL, sslmode="require")
    return connection

@app.route('/add-student', methods=['POST'])
def add_student():
    data = request.json
    name = data.get("name")
    roll_no = data.get("rollNo")
    email = data.get("email")
    gender = data.get("gender")
    department = data.get("department")
    
    if not all([name, roll_no, email, gender, department]):
        return jsonify({"error": "All fields are required!"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO students (name, roll_no, email, gender, department) VALUES (%s, %s, %s, %s, %s)",
        (name, roll_no, email, gender, department)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Student added successfully!"}), 201

@app.route("/getUser", methods=["GET"])
def get_user():
    connection = get_db_connection()
    cursor = connection.cursor()
    user_id = request.args.get("id")
    if user_id:
        cursor.execute("SELECT * FROM students WHERE id = %s", (user_id,))
    else:
        cursor.execute("SELECT * FROM students")

    users = cursor.fetchall()
    user_list = [{"id": user[0], "name": user[1], "roll_no": user[2], "email": user[3], "gender": user[4], "department": user[5]} for user in users]
    cursor.close()
    connection.close()

    return jsonify(user_list), 200

@app.route('/delete-user', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "User ID is required!"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (user_id,))
    connection.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "User not found!"}), 404

    cursor.close()
    connection.close()

    return jsonify({"message": "User deleted successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
