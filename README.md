# Телеграм бот с картинками
По условиям задачи мы должны сделать бота, который принимает картинку и возвращает её же, но уже с текстом.

## Этап 1. Создание бота
Для начала создадим бота, который будем с нами здороваться на команду `/start`

![image_telebot – README md](https://github.com/eshmargunov/image_telebot/assets/12861849/21106bb0-d294-4d30-8e22-90b1d4579565)

```python

import os
from telebot import TeleBot

print('Start telegram bot...')

token_bot = os.getenv('TOKEN')
bot = TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
```
![image_telebot – main py](https://github.com/eshmargunov/image_telebot/assets/12861849/0a882456-f4b5-4c8b-bfeb-14be1aee3bd3)

Бот работает. Теперь можно приступать к работе с изображениями.

## Этап 2. Получение изображения и сохранение его на компьютер
1. Сделаем обработчик, который будет реагировать только на сообщения содержащие изображения
```python
@bot.message_handler(func=lambda message: True, content_types=['photo'])
def message_reply(message):
    pass
```
2. Получаем изображение c помощью API телеграма.
```python
import requests
from telebot.apihelper import get_file

@bot.message_handler(func=lambda message: True, content_types=['photo'])
def message_reply(message):
    file_id = message.photo[-1].file_id
    file_info = get_file(token_bot, file_id)
    file_path = file_info.get('file_path')
    url = f"https://api.telegram.org/file/bot{token_bot}/{file_path}"
    response = requests.get(url)
    image = response.content
```
## Этап 3. Сохранение картинки, добавление к ней надписи и отправка пользователю

3.1 Сохраняем картинку с правильным именем на компьютер в заранее настроенную папку.  
_Замечание_  
В требованиях указано имя файла в формате `«YYYY-MM-DD_HH:mm_<user id>.jpg».` с двоеточием. 
Операционная система не позволяет использовать данный символ поэтому заменим на подчеркивание.
```python
import datetime
import os


def save_file(folder, chat_id, image):
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M')
    file_name = f"{now}_{chat_id}.jpg"
    path = os.path.join(folder, file_name)
    with open(path, 'wb') as f:
        f.write(image)
    return path
```

3.2 Выбираем фразу из файла-сборника
Сделаем функцию для чтения файла-сборника фраз, которая будет нам возвращать одну случайную фразу
```python
import os
import random

def get_title() -> str:
    path = os.getenv("PATH_FILE_STORAGE")
    with open(path, "r", encoding="utf-8") as f:
        titles = f.readlines()
    title = random.choice(titles)
    return title
```

3.3. Добавим эту фразу к изображению с нужным шрифтом
```python
from PIL import Image, ImageFont, ImageDraw


def get_font(font_name):
    try:
        font = ImageFont.truetype(font_name, 40)
    except IOError:
        print("Font file not found. Please provide a valid path to a .ttf or .otf file.")
        font = ImageFont.load_default()
    return font


def add_title(path_file):
    img = Image.open(path_file)
    image = ImageDraw.Draw(img)
    font = get_font("Lobster-Regular.ttf")
    title = get_title()
    image.text((int(img.width/2), int(img.height/1.5)), title, align="center", fill='black', font=font)
    img.show()
    return img
```


## Этап 4. Научим бота отвечать нам картинкой с текстом
```python
import requests
from telebot.apihelper import get_file
from title import processing_image

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
```
## Этап 5. Проверяем результат

   ![image](https://github.com/eshmargunov/image_telebot/assets/12861849/9ed2a410-4929-47ec-8e9d-f32c64e41a2f)

Картинка добавилась. Всё работает!
