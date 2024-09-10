import requests


def get_company():
    """Функция для получения работодателей с HH.ru"""

    url_hh = 'https://api.hh.ru/vacancies'
    vacancies_hh = requests.get(url_hh, params={"currency": "RUR", "host": "hh.ru"}).json()
    company_list = []
    for i in range(0, 15):
        if {"id": vacancies_hh["items"][i]["employer"]["id"], "name": vacancies_hh["items"][i]["employer"]["name"], "url": vacancies_hh["items"][i]["employer"]["url"]} in company_list:
            continue
        else:
            company_list.append({"id": vacancies_hh["items"][i]["employer"]["id"], "name": vacancies_hh["items"][i]["employer"]["name"], "url": vacancies_hh["items"][i]["employer"]["url"]})
    return company_list


def get_vacancies(companies):
    """Функция для получения вакансий работодателей"""

    vacancies_list = []
    for company in companies:
        company_id = company["id"]
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancies = response.json()["items"]
            vacancies_list.extend(vacancies)

        else:
            print(f"Ошибка при запросе к API для компании {company["company_name"]}: {response.status_code}")
    return vacancies_list


def get_vacancies_transform(vacancies):
    """Функция для преобразования данных о вакансиях"""

    vacancies_transform_list = []
    for item in vacancies:
        company_id = item['employer']['id']
        company = item["employer"]["name"]
        job_title = item["name"]
        link_to_vacancy = item["employer"]["alternate_url"]

        try:
            salary_from = item["salary"]["from"]
        except:
            salary_from = 0

        try:
            salary_to = item["salary"]["to"]
        except:
            salary_to = 0

        try:
            currency = item["salary"]["currency"]
        except:
            currency = 0

        description = item["snippet"]["responsibility"]
        requirement = item["snippet"]["requirement"]
        vacancies_transform_list.append({
                    "company_id": company_id,
                    "company_name": company,
                    "job_title": job_title,
                    "link_to_vacancy": link_to_vacancy,
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "currency": currency,
                    "description": description,
                    "requirement": requirement
                })
    return vacancies_transform_list


if __name__ == "__main__":
    print(get_vacancies_transform(get_vacancies(get_company())))