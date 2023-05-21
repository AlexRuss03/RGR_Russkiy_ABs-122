import requests
from bs4 import BeautifulSoup as bs
import random


# Парсер сайта
def parser():
    URL = "https://www.anekdot.ru/last/good"  # Сайт с анекдотами
    req = requests.get(URL)
    soup = bs(req.text, "html.parser")
    rough_jokes = soup.find_all('div', class_='text')
    jokes = [c.text for c in rough_jokes]
    return jokes


# Поиск анекдота по последнему сообщению
async def jokeGen(list, last_message="Я"):
    last_message = last_message.split()
    random.shuffle(last_message)
    for word in last_message:
        for joke in list:
            if word.lower() in joke.lower():
                output_joke = joke
                joke = ''
                return output_joke
    output_joke = random.choice(list)
    while output_joke == '':
        output_joke = random.choice(list)
    return random.choice(list)
