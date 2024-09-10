import psycopg2


class DBManager:
    """Класс для работы с данными из таблиц"""
    def __init__(self, database_name):
        self.database_name = database_name

    def get_companies_and_vacancies_count(self, database_name, params):
        """Метод для получения списка компаний с количеством вакансий"""

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT companies.company_name, COUNT(vacancies.company_name) AS quantity_vac
                    FROM companies
                    INNER JOIN vacancies USING(company_id)
                    GROUP BY companies.company_name;
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)

    def get_all_vacancies(self, database_name, params):
        """Метод для получения вакансий с указанием компании, зарплаты, ссылки"""

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT job_title, salary_from, salary_to, link_to_vacancy, companies.company_name
                    FROM vacancies
                    INNER JOIN companies USING(company_id);
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)


    def get_avg_salary(self, database_name, params):
        """Метод для получения средней зарплаты по вакансиям"""

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT AVG((salary_from+salary_to)/2) AS average_salary
                    FROM vacancies;
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)


    def get_vacancies_with_higher_salary(self, database_name, params):
        """Метод для получения вакансий с зарплатой выше средней"""

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT *
                    FROM vacancies
                    WHERE (salary_from+salary_to)/2 > (SELECT AVG((salary_from+salary_to)/2) FROM vacancies);
                """)
                rows = cur.fetchall()
                for row in rows:
                    print(row)


    def get_vacancies_with_keyword(self, database_name, params, keyword):
        """Метод для получения вакансий по заданному слову"""

        with psycopg2.connect(dbname=database_name, **params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT * FROM vacancies
                    WHERE LOWER(job_title) LIKE %s
                """, ('%' + keyword.lower() + '%',))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
