import psycopg2 as psy
import random

# Подключение к локальной базе данных
hostname = "localhost"
database = "dictionary"
username = "postgres"
pwd = "admin"
port_id = 5432


# Добавление данных в БД
def db_insert(base_f, base_s, n_word) -> None:
    connection = None
    cursor = None
    try:
        connection = psy.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)

        cursor = connection.cursor()
        # Создание БД, если она отсутствует
        create_scr = ''' CREATE TABLE IF NOT EXISTS dictionary (
                                    phrase_id   int PRIMARY KEY,
                                    base_first  varchar(40),
                                    base_second varchar(40),
                                    next_word   varchar(40))'''
        cursor.execute(create_scr)
        read_scr = """  SELECT "phrase_id"
                        FROM "dictionary"
                        ORDER BY "phrase_id" DESC
                        LIMIT 1;    """
        cursor.execute(read_scr)
        id_data = cursor.fetchall()
        id_end = 0
        for id_cursor in id_data:
            id_end = id_cursor[0] + 1

        # Вставка
        insert_scr = 'INSERT INTO dictionary (phrase_id, base_first, base_second, next_word) VALUES (%s, %s, %s, %s)'
        insert_value = (id_end, base_f, base_s, n_word)
        data = (base_f, base_s, n_word)
        read_scr = """SELECT count(*) FROM dictionary
                                where base_first = %s and base_second = %s and next_word = %s"""
        cursor.execute(read_scr, data)
        t_find = cursor.fetchall()
        if (t_find[0][0] == 0):
            cursor.execute(insert_scr, insert_value)

        connection.commit()
    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


# Удаление БД
async def db_remove():
    connection = None
    cursor = None
    try:
        connection = psy.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)

        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS dictionary")
        connection.commit()
    except Exception as error:
        print(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


# Создание сообщения из БД
async def messageGen(message_len=10):
    connection = None
    cursor = None
    message = []
    try:
        connection = psy.connect(
            host=hostname,
            dbname=database,
            user=username,
            password=pwd,
            port=port_id)
        # Размер БД
        cursor = connection.cursor()
        size_scr = "SELECT count(*) FROM dictionary;"
        cursor.execute(size_scr)
        size = cursor.fetchall()[0]
        # Случайное первое слово
        base_len = size[0] - 1
        key_num = random.randint(0, base_len)
        read_scr = """SELECT * FROM dictionary
                           where phrase_id = %s"""
        cursor.execute(read_scr, (key_num,))
        bd_tuple = cursor.fetchall()[0]
        message.extend((bd_tuple[1], bd_tuple[2], bd_tuple[3]))
        value = (bd_tuple[2], bd_tuple[3])

        read_scr = """SELECT * FROM dictionary
                        where base_first = %s and base_second = %s"""
        i = 0
        while bd_tuple[3] != '' and i < message_len:
            cursor.execute(read_scr, value)
            tuples = cursor.fetchall()
            search = next((i for i, v in enumerate(tuples) if v[0] == ''), None)
            if i - 2 == message_len and search is not None:
                bd_tuple[3] = ''
            else:
                bd_tuple = tuples[random.randint(0, len(tuples) - 1)]
            if random.random() * 100 > 20:
                message.append(bd_tuple[3])
            value = (bd_tuple[2], bd_tuple[3])
            i += 1
        message_text = " ".join(message)
    except Exception as error:
        print(error)
        return
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
        return message_text