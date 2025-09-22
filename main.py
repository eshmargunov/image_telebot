import os
import requests
from telebot import TeleBot
from telebot.apihelper import get_file
from title import processing_image

print('Start telegram bot...')

token_bot = os.getenv('TOKEN')
bot = TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def message_reply(message):
    file_id = message.photo[-1].file_id
    file_info = get_file(token_bot, file_id)
    file_path = file_info.get('file_path')
    url = f"https://api.telegram.org/file/bot{token_bot}/{file_path}"
    response = requests.get(url)
    image = response.content
    new_image = processing_image(image, message.chat.id)
    bot.send_photo(message.chat.id, photo=new_image)


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
