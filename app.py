from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(
    app, origins=["https://workers-front.onrender.com"]
)  # Allow specific frontend origin


def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return conn


@app.route("/workers", methods=["GET"])
def get_workers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM workers;")
    workers = cur.fetchall()
    cur.close()
    conn.close()

    workers_list = [
        {
            "id": worker[0],
            "name": worker[1],
            "job": worker[2],
            "phone": worker[3],
            "picture": worker[4],
        }
        for worker in workers
    ]
    return jsonify(workers_list)


@app.route("/workers/<int:id>", methods=["GET"])
def get_worker(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM workers WHERE id = %s;", (id,))
    worker = cur.fetchone()
    cur.close()
    conn.close()

    if worker:
        return jsonify(
            {
                "id": worker[0],
                "name": worker[1],
                "job": worker[2],
                "phone": worker[3],
                "picture": worker[4],
            }
        )
    else:
        return jsonify({"result": "Worker not found"}), 404


@app.route("/workers", methods=["POST"])
def add_worker():
    new_worker = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO workers (name, job, phone, picture) VALUES (%s, %s, %s, %s) RETURNING id;",
        (
            new_worker["name"],
            new_worker["job"],
            new_worker["phone"],
            new_worker["picture"],
        ),
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"result": "Worker added successfully", "id": new_id})


@app.route("/workers/<int:id>", methods=["DELETE"])
def delete_worker(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM workers WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"result": "Worker deleted successfully"})


@app.route("/workers/<int:id>", methods=["PUT"])
def update_worker(id):
    updated_worker = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE workers SET name = %s, job = %s, phone = %s, picture = %s WHERE id = %s;",
        (
            updated_worker["name"],
            updated_worker["job"],
            updated_worker["phone"],
            updated_worker["picture"],
            id,
        ),
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"result": "Worker updated successfully"})


if __name__ == "__main__":
    app.run(debug=True)
