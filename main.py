import os
import requests
from dotenv import load_dotenv
from telebot import TeleBot, types
from telebot.apihelper import get_file
from title import processing_image

load_dotenv()
print('Start telegram bot...')

token_bot = os.getenv('TOKEN')
bot = TeleBot(token_bot)
user_data = {}


class SEND_TO:
    CHANNEL_YES = "send_to_channel_yes"
    CHANNEL_NO = "send_to_channel_no"


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне картинку, и я добавлю на нее случайный заголовок.")


@bot.message_handler(func=lambda message: True, content_types=['photo'])
def message_reply(message):
    file_id = message.photo[-1].file_id
    file_info = get_file(token_bot, file_id)
    file_path = file_info.get('file_path')
    url = f"https://api.telegram.org/file/bot{token_bot}/{file_path}"
    response = requests.get(url)
    image = response.content
    new_image = processing_image(image, message.chat.id)

    user_data[message.chat.id] = {
        'processed_image': new_image,
        'original_message': message
    }

    # Создаем клавиатуру с вопросом о пересылке
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да, отправить в канал', callback_data=SEND_TO.CHANNEL_YES)
    btn_no = types.InlineKeyboardButton('Нет, только для себя', callback_data=SEND_TO.CHANNEL_NO)
    keyboard.add(btn_yes, btn_no)

    # Отправляем обработанное фото и вопрос
    bot.send_photo(
        message.chat.id,
        photo=new_image,
        caption="Картинка обработана! Хочешь отправить ее в наш канал?",
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('send_to_channel'))
def handle_channel_decision(call):
    chat_id = call.message.chat.id
    bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    if chat_id not in user_data:
        bot.answer_callback_query(call.id, "Данные устарели. Отправь картинку заново.")
        return

    if call.data == SEND_TO.CHANNEL_YES:
        channel_id = os.getenv('CHANNEL_ID')
        # Получаем обработанное изображение
        processed_image = user_data[chat_id]['processed_image']

        # Отправляем в канал
        caption = f"Фото от пользователя @{call.from_user.username}" if call.from_user.username else "Фото от пользователя"
        bot.send_photo(
            chat_id=channel_id,
            photo=processed_image,
            caption=caption
        )

        bot.send_message(
            chat_id,
            f"✅ Фото успешно опубликовано в канале!",
            disable_web_page_preview=True
            )

    elif call.data == SEND_TO.CHANNEL_NO:
        bot.send_message(chat_id, "✅ Хорошо, фото осталось только у тебя!")
    else:
        bot.send_message(chat_id, "Неизвестная команда")

    # Очищаем временные данные
    if chat_id in user_data:
        del user_data[chat_id]

    bot.answer_callback_query(call.id)


if __name__ == '__main__':
    user_data.clear()
    bot.infinity_polling(skip_pending=True)
