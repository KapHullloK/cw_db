from worker_db.connect_db import connect_db
from psycopg2 import errors


def insert_employer(id_employer, location, name, accredited, description):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO employers (id_employer, location, name, accredited, description)
            VALUES (%s, %s, %s, %s, %s) RETURNING id_employer;
        """, (id_employer, location, name, accredited, description))
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def insert_vacancy(id_employer, address, employment, experience, name, currency, salary_from, salary_to):
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO vacancies (id_employer, address, employment, experience, name, currency, salary_from, salary_to)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """, (id_employer, address, employment, experience, name, currency, salary_from, salary_to))
        conn.commit()
    except errors.UniqueViolation:
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
