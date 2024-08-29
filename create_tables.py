from db_connection import get_db_connection

# create_table.py
from db_connection import get_db_connection


def create_workers_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS workers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            job VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            picture TEXT
        );
    """
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Table 'workers' created successfully!")


if __name__ == "__main__":
    create_workers_table()
