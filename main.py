from src.api_company_vacancies_hh import get_company, get_vacancies, get_vacancies_transform
from src.class_manager import DBManager
from src.config import config
from src.create_db import create_db_tb
from src.insert_db import save_data_to_database


def main():
    """Главная функция для взаимодействия с пользователем"""

    params = config()

    db_user_input = int(
        input(
            """Вы воспользовались приложением для просмотра вакансий.
                    Выберите необходимый параметр (укажите число от 1 до 5):
                    1) Показать компании с количеством вакансий от каждой;
                    2) Показать вакансии с указанием ссылки на неё на hh.ru, компаний, зарплаты;
                    3) Показать среднюю зарплату;
                    4) Показать вакансии с зарплатой выше средней;
                    5) Показать вакансии по ключевому слову.\n"""
        )
    )

    if db_user_input == 1:
        manager = DBManager("companies_and_vacancies")
        manager.get_companies_and_vacancies_count("companies_and_vacancies", params)
    elif db_user_input == 2:
        manager = DBManager("companies_and_vacancies")
        manager.get_all_vacancies("companies_and_vacancies", params)
    elif db_user_input == 3:
        manager = DBManager("companies_and_vacancies")
        manager.get_avg_salary("companies_and_vacancies", params)
    elif db_user_input == 4:
        manager = DBManager("companies_and_vacancies")
        manager.get_vacancies_with_higher_salary("companies_and_vacancies", params)
    elif db_user_input == 5:
        keyword_input = input("Введите ключевое слово для поиска вакансий\n")
        manager = DBManager("companies_and_vacancies")
        manager.get_vacancies_with_keyword("companies_and_vacancies", params, keyword_input)


if __name__ == "__main__":
    params = config()
    create_db_tb("companies_and_vacancies", params)
    save_data_to_database(
        get_company(), get_vacancies_transform(get_vacancies(get_company())), "companies_and_vacancies", params
    )
    main()
