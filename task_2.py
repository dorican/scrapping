import requests
from constants import ACCESS_TOKEN

USER = 'dorican'
URL = f'https://api.vk.com/method/users.get?user_ids={USER}&fields=bdate&access_token={ACCESS_TOKEN}&v=5.130'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'}

response = requests.get(URL, headers=HEADERS).json()

with open("response_vk.txt", 'w', encoding="utf-8") as file:
    for item in response['response']:
        file.write(f'Данные пользователя {USER}:\n1. ID: {item["id"]}\n'
                   f'2. Имя: {item["first_name"]}\n3. Фамилия: {item["last_name"]}\n'
                   f'4. Дата рождения: {item["bdate"]}\n')

