import telebot
import config
from telebot import types
from scraper import start


bot = telebot.TeleBot(config.configure['TOKEN'])


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет! Этот бот поможет тебе скачать фото и видео из Instagram!\n'
                                      'Если готов, то напиши "Поехали"', disable_web_page_preview=True)


@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.text.lower() == "поехали":
        replay_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        replay_keyboard.add(types.KeyboardButton("Фото"), types.KeyboardButton("Видео"))
        msg = bot.send_message(message.chat.id, "Что хочешь скачать: фото или видео?", reply_markup=replay_keyboard)
        bot.register_next_step_handler(msg, user_answer)
    else:
        bot.send_message(message.chat.id, "Извини, мой функционал пока ограничени и я не до конца тебя понимаю ;(\n"
                                          "Если тебе нужна помощь введи команду /help")


def user_answer(message):
    content_type = None
    ext = None
    replay_keyboard = types.ReplyKeyboardRemove(selective=False)
    if message.text.lower() == "видео":
        content_type = "video"
        ext = "mp4"
    elif message.text.lower() == "фото":
        content_type = "image"
        ext = "jpg"
    msg = bot.send_message(message.chat.id, f"Отправь ссылку на {message.text.lower()}",
                           reply_markup=replay_keyboard)
    bot.register_next_step_handler(msg, download, content_type, ext)


def download(message, content_type, ext):
    error_message = "Упс! Что-то пошло не так, перепроверь ссылку.\n" \
                    "Обрати внимание, что бот пока не может обрабатывать Reels'ы, " \
                    "но мы это скоро исправим :)"
    url = message.text
    if "http://" in url or "https://" in url:
        bot.send_message(message.chat.id, "Подожди пару секунд")
        try:
            content = start(content_type, ext, url)
            print(content)
            data = open(content, 'rb')
            if content_type == "video":
                bot.send_video(message.chat.id, data)
            elif content_type == "image":
                bot.send_photo(message.chat.id, data)

        except (TypeError, AttributeError):
            bot.send_message(message.chat.id, error_message)
    else:
        bot.send_message(message.chat.id, error_message)


bot.polling(none_stop=True, interval=0)