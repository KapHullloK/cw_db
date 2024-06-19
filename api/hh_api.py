import requests
from pprint import pprint


class HHAPI:
    URL = f"https://api.hh.ru/employers"
    id_employers = []

    def __init__(self, cnt_employers: int, search_text: str):
        response = requests.get(self.URL, params={'per_page': cnt_employers, "text": search_text})
        for employer in response.json()['items']:
            self.id_employers.append(employer['id'])

    def get_employer_info(self, employer_id: int):
        local_url = f"{self.URL}/{employer_id}"
        response = requests.get(local_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_employer_vacancy(self, vacancy_url: str):
        response = requests.get(vacancy_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
