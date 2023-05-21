from PIL import Image, ImageDraw, ImageFont
import random
from data_base import messageGen


# Создание мема
async def new_meme():
    src = ""
    text = await messageGen(4)
    mem_num = random.randint(0, 4)
    if mem_num == 0:
        src = "data/Fresco_mem.jpg"
        fresco(text)
        return src
    elif mem_num == 1:
        src = "data/Aladin_mem.jpg"
        aladin(text + "?")
        return src
    elif mem_num == 2:
        text = await messageGen(3)
        text_s = await messageGen(3)
        src = "data/Doge_mem.jpg"
        doge(text, text_s)
        return src
    elif mem_num == 3:
        src = "data/Genius_mem.jpg"
        genius(text)
        return src
    elif mem_num == 4:
        src = "data/Hey_you_mem.jpg"
        hey_you(text)
        return src
    else:
        return


# Отрисовка мемов
def fresco(text):
    img = Image.open("data/Fresco.jpg")
    font = ImageFont.truetype("impact.ttf", size=20)
    idraw = ImageDraw.Draw(img)
    idraw.text((20, 100), text, font=font, fill=(0, 0, 0, 0))
    img.save('data/Fresco_mem.jpg', 'JPEG')
    return "data/Fresco_mem.jpg"


def aladin(text):
    img = Image.open("data/Aladin.jpg")
    font = ImageFont.truetype("impact.ttf", size=35)
    idraw = ImageDraw.Draw(img)
    idraw.text((50, 570), text, font=font, fill=(0, 0, 0, 0))
    img.save('data/Aladin_mem.jpg', 'JPEG')
    return "data/Aladin_mem.jpg"


def doge(text_f, text_s):
    img = Image.open("data/Doge.jpg")
    font = ImageFont.truetype("impact.ttf", size=22)
    idraw = ImageDraw.Draw(img)
    idraw.text((10, 380), text_f, font=font, fill=(0, 0, 0, 0))
    idraw.text((360, 380), text_s, font=font, fill=(0, 0, 0, 0))
    img.save('data/Doge_mem.jpg', 'JPEG')
    return "data/Doge_mem.jpg"


def genius(text):
    img = Image.open("data/Genius.jpg")
    font = ImageFont.truetype("impact.ttf", size=20)
    idraw = ImageDraw.Draw(img)
    idraw.text((10, 5), text, font=font)
    img.save('data/Genius_mem.jpg', 'JPEG')
    return "data/Genius_mem.jpg"


def hey_you(text):
    img = Image.open("data/Hey_you.jpg")
    font = ImageFont.truetype("impact.ttf", size=50)
    idraw = ImageDraw.Draw(img)
    idraw.text((10, 900), text, font=font)
    img.save('data/Hey_you_mem.jpg', 'JPEG')
    img = Image.open('data/Hey_you_mem.jpg')
    return "data/Hey_you_mem.jpg"
