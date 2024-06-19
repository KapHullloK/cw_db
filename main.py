from api.hh_api import HHAPI
from worker_db.fill_db import insert_employer, insert_vacancy
from worker_db.connect_db import connect_db
from worker_db.manager_db import DBManager


def worker_employers():
    do = input("Если вы хотите заполнить базу новой информацией введите 1 иначе 0 - ")
    print()
    if do == "1":
        print("Количество работодательей должно быть строго в этих пределах | 0 < x < 100 |")
        cnt_employers = int(input("Введите желаемое количество работодателей - "))
        search_text = input("Введите желаемый спектр работодателей - ")
        api = HHAPI(cnt_employers, search_text)

        for employer in api.id_employers:
            emp = api.get_employer_info(employer)

            serialized_emp = [emp['id'], emp["area"]["name"], emp["name"],
                              emp['accredited_it_employer'], emp['description']]

            insert_employer(*serialized_emp)

            vacancy_emp = api.get_employer_vacancy(emp["vacancies_url"])['items']

            for vacancy in vacancy_emp:
                if vacancy['salary'] is None or vacancy['salary']['from'] is None:
                    continue

                serialized_vacancy_emp = [vacancy['employer']['id'],
                                          vacancy['address']['raw'] if vacancy['address'] is not None else "None",
                                          vacancy['employment']['name'], vacancy['experience']['name'],
                                          vacancy['name'], vacancy['salary']['currency'],
                                          vacancy['salary']['from'],
                                          vacancy['salary']['to'] if vacancy['salary']['to'] is not None else
                                          vacancy['salary']['from']]
                if serialized_vacancy_emp:
                    insert_vacancy(*serialized_vacancy_emp)

    print("Панел упарвления бд\n"
          "0. Выход\n"
          "1. Получает список всех компаний и количество вакансий в каждой из них.\n"
          "2. Получает список всех вакансий с указанием названия компании, должности и зарплаты.\n"
          "3. Получает среднюю зарплату для всех вакансий.\n"
          "4. Получает список всех вакансий с зарплатой выше средней по всем вакансиям.\n"
          "5. Получает список всех вакансий, названия которых содержат слова\n")

    do2 = 1
    manage = DBManager(connect_db())

    while do2:
        do2 = int(input("Ввыедите номер команды - "))
        if do2 == 1:
            for res in manage.get_companies_and_vacancies_count():
                print(f"{res[0]}: {res[-1]}")

        elif do2 == 2:
            for res in manage.get_all_vacancies():
                print(f"{res[0]}: {res[1]} {res[2]}-{res[3]} {res[4]}")

        elif do2 == 3:
            print(f"{manage.get_avg_salary():.2f}")

        elif do2 == 4:
            for res in manage.get_vacancies_with_higher_salary():
                print(f"{res[0]}: {res[1]} {res[2]}-{res[3]} {res[4]}")

        elif do2 == 5:
            word = input("Введите название вакансии - ")
            for res in manage.get_vacancies_with_keyword(word):
                print(f"{res[0]}: {res[1]} {res[2]}-{res[3]} {res[4]}")


if __name__ == "__main__":
    worker_employers()
