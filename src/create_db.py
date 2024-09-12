import psycopg2


def create_db_tb(database_name, params):
    """Создание базы данных и таблиц в ней для хранения данных о работодателях и вакансиях"""

    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                link_to_company TEXT
            )
        """
        )

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                company_id INTEGER REFERENCES companies(company_id),
                company_name VARCHAR(255) NOT NULL,
                job_title VARCHAR(255) NOT NULL,
                link_to_vacancy TEXT,
                salary_from INTEGER DEFAULT NULL,
                salary_to INTEGER DEFAULT NULL,
                salary_currency VARCHAR(255) DEFAULT NULL,
                description TEXT NULL,
                requirement TEXT NULL
            )
        """
        )

    conn.commit()
    conn.close()
