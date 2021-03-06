import requests

USER = 'dorican'
URL = f'https://api.github.com/users/{USER}/repos'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

response = requests.get(URL, headers=HEADERS).json()

with open("user_repositories.txt", 'w', encoding="utf-8") as file:
    numb = 1
    file.write(f'Репозитории пользователя {USER}:\n')
    for item in response:
        file.write(f'{numb}.{item["name"]};\n')
        numb += 1
