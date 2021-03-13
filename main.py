import requests
from bs4 import BeautifulSoup as bs
import json



MAIN_LINK = 'https://hh.ru/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

# POSITION = input('Введите поисковую фразу: ')
POSITION = 'python'


def main():
    page = 0
    vacancies = []
    params = {
        'area': '1624',
        'st': 'searchVacancy',
        'fromSearchLine': 'true',
        'text': POSITION,
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
                        max_salary = 'Не указано'
                    elif 'до' in salary:
                        min_salary = 'Не указано'
                        max_salary = salary[3:-4].strip().replace('\xa0', '')
                    else:
                        min_salary, max_salary = [s.replace('\xa0', ' ') for s
                                                  in salary[:-4].strip().split(
                                '-')]
                else:
                    min_salary = 'Не указано'
                    max_salary = 'Не указано'
                    currency = 'Не указано'
                vacancy_dict['vacancy_name'] = name
                vacancy_dict['vacancy_link'] = link
                vacancy_dict['min_salary'] = min_salary
                vacancy_dict['max_salary'] = max_salary
                vacancy_dict['currency'] = currency
                vacancy_dict['site_link'] = MAIN_LINK
                vacancies.append(vacancy_dict)
            if soup.find('a', attrs={'class': 'HH-Pager-Controls-Next'}):
                page += 1
            else:
                # for item in vacancies:
                #     users.insert_one(item)
                with open('homework_2.json', 'w', encoding='utf-8') as file:
                    json.dump(vacancies, file, indent=2, ensure_ascii=False)
                break

if __name__ == '__main__':
    main()

