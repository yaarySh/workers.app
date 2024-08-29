# app.py
from flask import Flask, jsonify, request
from db_connection import get_db_connection

app = Flask(__name__)


@app.route("/workers", methods=["GET"])
def get_workers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, job, phone, picture FROM workers;")
    workers = cur.fetchall()
    cur.close()
    conn.close()

    # No need to manually convert to dictionaries
    return jsonify(workers)


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

    # Check if worker exists
    cur.execute("SELECT id FROM workers WHERE id = %s;", (id,))
    worker = cur.fetchone()

    if worker:
        cur.execute("DELETE FROM workers WHERE id = %s;", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"result": "Worker deleted successfully"}), 200
    else:
        cur.close()
        conn.close()
        return jsonify({"result": "Worker not found"}), 404


@app.route("/workers/<int:id>", methods=["GET"])
def get_worker_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, job, phone, picture FROM workers WHERE id = %s;", (id,)
    )
    worker = cur.fetchone()
    cur.close()
    conn.close()

    if worker:
        return jsonify(worker)  # worker is already a dictionary
    else:
        return jsonify({"result": "Worker not found"}), 404


@app.route("/workers/<int:id>", methods=["PUT"])
def update_worker(id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Get the data from the request
    updated_data = request.get_json()

    # Check if worker exists
    cur.execute("SELECT id FROM workers WHERE id = %s;", (id,))
    worker = cur.fetchone()

    if worker:
        # Update the worker details
        cur.execute(
            """
            UPDATE workers 
            SET name = %s, job = %s, phone = %s, picture = %s
            WHERE id = %s;
            """,
            (
                updated_data.get("name"),
                updated_data.get("job"),
                updated_data.get("phone"),
                updated_data.get("picture"),
                id,
            ),
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"result": "Worker updated successfully"}), 200
    else:
        cur.close()
        conn.close()
        return jsonify({"result": "Worker not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
