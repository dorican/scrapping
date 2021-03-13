import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

CLIENT = MongoClient('localhost', 27017)
DB = CLIENT['db_hh']
users = DB.users

MAIN_LINK = 'https://hh.ru/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}


class Parser():
    def __init__(self, db_cursor):
        self.main_link = MAIN_LINK
        self.headers = HEADERS
        self.db_cursor = db_cursor

    def get_vacancies_by_salary(self, value):
        result = self.db_cursor.find({'min_salary': {'$gte': value}})
        for item in result:
            print(f'{item}\n')

    def parse_data(self, position):
        page = 0
        vacancies = []
        params = {
            'area': '1624',
            'st': 'searchVacancy',
            'fromSearchLine': 'true',
            'text': position,
            'page': page
        }
        while True:
            params['page'] = page
            response = requests.get(f'{MAIN_LINK}/search/vacancy', params=params, headers=HEADERS)
            if response.ok:
                soup = bs(response.content, 'html.parser')
                vacancies_soup = soup.findAll('div', attrs={'class': 'vacancy-serp-item'})
                for item in vacancies_soup:
                    vacancy_dict = {}
                    vacancy_a = item.find('a', attrs={'class': 'bloko-link'})
                    link = vacancy_a['href']
                    name = vacancy_a.getText()
                    salary_obj = item.find('div', attrs={
                        'class': 'vacancy-serp-item__sidebar'}).find('span')
                    if salary_obj:
                        salary = salary_obj.getText()
                        currency = salary[-4:]
                        if 'от' in salary:
                            min_salary = salary[3:-4].strip().replace('\xa0', '')
                            max_salary = 0
                        elif 'до' in salary:
                            min_salary = 0
                            max_salary = salary[3:-4].strip().replace('\xa0', '')
                        else:
                            min_salary, max_salary = [s.replace('\xa0', '') for s in salary[:-4].strip().split('-')]
                    else:
                        min_salary = 0
                        max_salary = 0
                        currency = 'Не указано'
                    vacancy_dict['vacancy_name'] = name
                    vacancy_dict['vacancy_link'] = link
                    vacancy_dict['min_salary'] = int(min_salary)
                    vacancy_dict['max_salary'] = int(max_salary)
                    vacancy_dict['currency'] = currency
                    vacancy_dict['site_link'] = MAIN_LINK
                    vacancies.append(vacancy_dict)
                if soup.find('a', attrs={'class': 'HH-Pager-Controls-Next'}):
                    page += 1
                else:
                    for item in vacancies:
                        if not self.data_exists(item):
                            self.db_cursor.insert_one(item)
                    break

    def data_exists(self, item):
        if self.db_cursor.find_one(item):
            return True
        return False


parser = Parser(users)

while True:
    reaction = input('Хотите парсить? Нажмите: 1\n'
                     'Хотите посмотреть вакансии? Нажмите: 2\n'
                     '(для выхода нажмите "q"): ')
    if reaction == '1':
        position = input('Введите поисковую фразу (для выхода нажмите "q"): ')
        if position == 'q':
            break
        else:
            print('Собираю данные...')
            parser.parse_data(position)
    if reaction == '2':
        salary = int(input('Введите зп для поиска (для выхода нажмите "q"): '))
        if salary == 'q':
            break
        else:
            parser.get_vacancies_by_salary(salary)
    if reaction == 'q':
        break
