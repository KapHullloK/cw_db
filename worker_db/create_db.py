from worker_db import connect_db


def create_tables():
    conn = connect_db.connect_db()
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                id SERIAL PRIMARY KEY,
                id_employer INT UNIQUE NOT NULL,
                location VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                accredited BOOLEAN,
                description TEXT
            );
        """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                id_employer INT NOT NULL,
                address VARCHAR(255),
                employment VARCHAR(255) NOT NULL,
                experience VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                currency VARCHAR(255) NOT NULL,
                salary_from INT NOT NULL,
                salary_to INT NOT NULL,
                FOREIGN KEY (id_employer) REFERENCES employers(id_employer) ON DELETE CASCADE
            );
        """)

    conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
