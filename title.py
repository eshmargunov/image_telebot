import datetime
import os
import random
from PIL import Image, ImageFont, ImageDraw


def get_title() -> str:
    path = os.getenv("PATH_FILE_STORAGE")
    with open(path, "r", encoding="utf-8") as f:
        titles = f.readlines()
    title = random.choice(titles)
    print('TITLE ', title)
    return title

def get_font(font_name):
    try:
        font = ImageFont.truetype(font_name, 40)
    except IOError:
        print("Font file not found. Please provide a valid path to a .ttf or .otf file.")
        font = ImageFont.load_default()
    return font


def add_title(path_file):
    title = get_title()
    img = Image.open(path_file)
    image = ImageDraw.Draw(img)
    font = get_font("Lobster-Regular.ttf")
    image.text((int(img.width/2), int(img.height/1.5)), title, align="center", fill='black', font=font)
    img.show()
    return img


def processing_image(image, chat_id):
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M')
    folder = os.getenv('PATH_FOLDER')
    if not os.path.exists(folder):
        os.mkdir(folder)
    file_name = f"{now}_{chat_id}.jpg"
    path = os.path.join(folder, file_name)
    with open(path, 'wb') as f:
        f.write(image)
    image_with_title = add_title(path)
    return image_with_title