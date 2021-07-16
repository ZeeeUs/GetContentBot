import requests.exceptions
import telebot
import config
from telebot import types
import main

bot = telebot.TeleBot(config.configure['TOKEN'])


@bot.message_handler(commands=['/start', '/help'])
def welcome_message(message):
    bot.send_message(message.chat.id, "Привет! Этот бот поможет тебе скачать фото и видео из Instagram, "
                                      "просто отправь ссылку!")


@bot.message_handler(func=lambda message: True, content_types=['text'])
def accept_url(message):
    id_one = message.chat.id
    url = message.text
    try:
        all_url = main.start(url)
        select_item(id_one, all_url)
    except (AttributeError, requests.exceptions.MissingSchema):
        bot.send_message(message.chat.id, "Упс! Что-то пошло не так, проверь ссылку и попробуй снова")


def select_item(id_one, all_url):
    items_count = len(all_url.keys())
    if items_count > 1:
        replay_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(items_count):
            replay_keyboard.add(types.KeyboardButton(f"{i + 1}"))
        replay_keyboard.add(types.KeyboardButton("Все"))
        msg = bot.send_message(id_one, "Выбери что надо скачать", reply_markup=replay_keyboard)
        bot.register_next_step_handler(msg, get_content, all_url)
    else:
        one_item(id_one, all_url)


def one_item(id_one, all_url):
    bot.send_message(id_one, "Подожди пару секунд")
    content, ext = main.download(all_url)
    switch(content, ext, id_one)


def get_content(message, all_url):
    replay_keyboard = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Подожди пару секунд", reply_markup=replay_keyboard)
    if message.text.lower() != "все":
        content, ext = main.download(all_url[int(message.text) - 1])
        switch(content, ext, message.chat.id)


def switch(content, ext, id_one):
    data = open("./media/" + content, 'rb')
    if ext == "jpg":
        bot.send_photo(id_one, data)
    else:
        bot.send_video(id_one, data)


bot.polling(none_stop=True, interval=0)
