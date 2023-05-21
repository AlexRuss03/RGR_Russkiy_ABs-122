from vkbottle import PhotoMessageUploader
from vkbottle import VKAPIError
from vkbottle.dispatch.rules.base import ChatActionRule, FromUserRule
from vkbottle_types.objects import MessagesMessageActionStatus
from vkbottle.bot import Bot, Message
import asyncio
import random

from config import BotToken
import meme_gen
import data_base as db
from text_interp import tupleCreator
import jokes_gen as jokes

# Библиотека для корректной работы бота
import sys
from loguru import logger
logger.remove()
logger.add(sys.stderr, level="INFO")

# Считываем учетные данные
vk_bot = Bot(token=BotToken)
uploader = PhotoMessageUploader(vk_bot.api)
last_message = ""

#Список анекдотов
anecdots_list = jokes.parser()


@vk_bot.on.chat_message(ChatActionRule(MessagesMessageActionStatus.CHAT_INVITE_USER.value))
async def invited(message: Message) -> None:
    #Приветствие при приглашении бота в беседу
    if (
            message.action is not None
            and message.group_id is not None
            and message.action.member_id == -message.group_id
    ):
        await message.answer("""Я родился!
Предоставьте мне доступ к переписке и права администратора.
Для сброса базы данных используйте команду /reset.\n
Для просмотра команд используйте /commands или /help""")


# Описание команд
@vk_bot.on.chat_message(text=["/commands", "/help"])
async def reset(message: Message) -> None:
    inf =""" \n/reset - очистка базы данных\n
            /meme, /mem - создание мема\n
            /joke - поиск анекдота\n
            /commands, /help - список команд"""
    await message.answer(inf)

# Сброс базы данных
@vk_bot.on.chat_message(text=["/reset"])
async def reset(message: Message) -> None:
    try:
        members = await message.ctx_api.messages.get_conversation_members(
            peer_id=message.peer_id
        )
    except VKAPIError[917]:
        await message.reply(
            "Не удалось проверить, являетесь ли вы администратором,"
            " потому что я не администратор."
        )
        return
    admins = {member.member_id for member in members.items if member.is_admin}
    if message.from_id in admins:
        await db.db_remove()
        reply = f"@id{message.from_id}, база данных успешно сброшена."
    else:
        reply = "Сбрасывать базу данных могут только администраторы."
    await message.reply(reply)


# Создание мема
@vk_bot.on.chat_message(text=["/meme", "/mem"])
async def reset(message: Message) -> None:
    src = await meme_gen.new_meme()
    attachment = await uploader.upload(src)
    await message.answer("Смотри мем!", attachment=attachment)

# Поиск анекдота
@vk_bot.on.chat_message(text=["/joke"])
async def reset(message: Message) -> None:
    joke = await jokes.jokeGen(anecdots_list, last_message)
    await message.answer(joke)


# Генерация сообщения
@vk_bot.on.chat_message()
async def talk(message: Message) -> None:
    if message.text:
        last_message = message.text
        await tupleCreator(last_message)
    if random.random() * 100 > 40:
        return
    if random.random() * 100 > 30:
        src = await meme_gen.new_meme()
        attachment = await uploader.upload(src)
        await message.answer("Смотри мем!", attachment=attachment)
        return
    response = await db.messageGen()
    await message.answer(response)

vk_bot.run_forever()