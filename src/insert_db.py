import psycopg2


def save_data_to_database(companies_data, vacancies_data, database_name, params):
    """Функция для сохранения данных о компаниях и вакансиях в таблицах базы данных"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for company in companies_data:
            cur.execute(
                """INSERT INTO companies (company_id, company_name, link_to_company)
                                VALUES (%s, %s, %s)""",
                (company["id"], company["name"], company["url"]),
            )

        for vacancy in vacancies_data:
            cur.execute(
                """INSERT INTO vacancies (company_id, company_name, job_title, link_to_vacancy, salary_from, salary_to, salary_currency, description, requirement)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    vacancy["company_id"],
                    vacancy["company_name"],
                    vacancy["job_title"],
                    vacancy["link_to_vacancy"],
                    vacancy["salary_from"],
                    vacancy["salary_to"],
                    vacancy["currency"],
                    vacancy["description"],
                    vacancy["requirement"],
                ),
            )

    conn.commit()
    conn.close()
