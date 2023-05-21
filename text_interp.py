import re
from data_base import db_insert


# Разделение текста на слова
def textSlicer(text):
    text = textNormalize(text)
    return text.split()


def textNormalize(text):
    text = text.lower()                     # Удаление регистра
    text = re.sub(' +', ' ', text)          # Удаление повторных пробелов
    text = re.sub(r'[^\w\s"!"]', '', text)  # Удаление всех символов, кроме букв и пробелов
    text = re.sub('_', '', text)
    return text


# Добавление фраз в базу данных
async def tupleCreator(text):
    if text[0] == '/':
        return
    text = textSlicer(text)
    tuples = {}
    text_len = len(text)
    if text_len > 0:
        for i in range(text_len):
            value = []
            key = ()
            n_word = '' if (i == text_len - 1) else text[i+1]
            key = (text[i], n_word)
            if i + 2 < text_len:
                value.append(text[i+2])
            if tuples.get(key) is None:
                tuples[key] = value
            else:
                ex_value = tuples.get(key) + value
                tuples.update({key: ex_value})
    print(tuples)
    for key in tuples:
        db_insert(key[0], key[1], ''.join(tuples.get(key)))