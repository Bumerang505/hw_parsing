import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

vacancies_json = []


def get_headers():
    return Headers(browser="chrome", os="win").generate()


search_response = requests.get('https://spb.hh.ru/search/vacancy?L_save_area=true&text=python%2C++Flask%2C+Django'
                               '&excluded_text=&area=1&area=2&salary=&currency_code=RUR&experience=doesNotMatter'
                               '&order_by=relevance&search_period=0&items_on_page=50&hhtmFrom=vacancy_search_filter',
                               headers=get_headers())
response_html = search_response.text
main_soup = BeautifulSoup(response_html, 'lxml')
vacancy_list = main_soup.find('main', class_='vacancy-serp-content')

vacancies = vacancy_list.find_all('div', class_='vacancy-card--z_UXteNo7bRGzxWVcL7y font-inter')

for vacancy in vacancies:
    a_tag = vacancy.find('a')
    reference = a_tag['href']

    vacancy_name = vacancy.find('span', class_='vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link').text
    salary_raw = vacancy.find('span', class_='fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni '
                                             'compensation-text--kTJ0_rp54B2vNeZ3CTt2 '
                                             'separate-line-on-xs--mtby5gO4J0ixtqzW38wh')
    city = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-address_narrow'}).text

    if salary_raw is None:
        salary = 'Зарплата не указана'
    else:
        salary_n = salary_raw.text
        salary = salary_n.replace(" ", " ").replace(" ", " ")

    vacancy_dict = {'Название': vacancy_name, 'Зарплата': salary, 'Город': city, 'Ссылка': reference}
    vacancies_json.append(vacancy_dict)


with open('hh_ru_vacancies.json', 'w', encoding='UTF-8') as file:
    json.dump(vacancies_json, file, ensure_ascii=False, indent=4)

