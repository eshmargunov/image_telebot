import unittest
from unittest.mock import patch
import os
import tempfile
import shutil
from PIL import Image

from title import get_title, get_font, add_title, save_file


class TestTitleFunctions(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.test_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.test_dir, "test.jpg")

        # Создаем тестовое изображение
        img = Image.new('RGB', (100, 100), color='red')
        img.save(self.test_image_path)

        # Устанавливаем переменные окружения для тестов
        os.environ['PATH_FILE_STORAGE'] = os.path.join(self.test_dir, 'titles.txt')
        os.environ['PATH_FOLDER'] = self.test_dir

        # Создаем тестовый файл с заголовками
        with open(os.environ['PATH_FILE_STORAGE'], 'w', encoding='utf-8') as f:
            f.write("Заголовок 1\nЗаголовок 2\nЗаголовок 3\n")

    def tearDown(self):
        """Очистка после каждого теста"""
        shutil.rmtree(self.test_dir)

    def test_get_title(self):
        """Тест функции get_title"""
        title = get_title()
        self.assertIn(title, ["Заголовок 1\n", "Заголовок 2\n", "Заголовок 3\n"])


    def test_get_font(self):
        """Тест функции get_font"""
        # всегда должен вернуться шрифт
        font = get_font("test_font.ttf")
        # Проверяем, что возвращается объект шрифта
        self.assertIsNotNone(font)


    def test_add_title(self):
        """Тест функции add_title"""
        # Мокаем random.choice чтобы возвращать предсказуемый результат
        with patch('random.choice') as mock_choice:
            mock_choice.return_value = "Тестовый заголовок"
            result_image = add_title(self.test_image_path)
            self.assertIsInstance(result_image, Image.Image)

    def test_save_file(self):
        """Тест функции save_file"""
        test_data = b"test image data"
        chat_id = 12345

        # Вызываем функцию
        result_path = save_file(self.test_dir, test_data, chat_id)

        # Проверяем, что файл был создан
        self.assertTrue(os.path.exists(result_path))

        # Проверяем содержимое файла
        with open(result_path, 'rb') as f:
            content = f.read()
        self.assertEqual(content, test_data)

        # Проверяем формат имени файла
        filename = os.path.basename(result_path)
        self.assertIn(str(chat_id), filename)
        self.assertTrue(filename.endswith('.jpg'))


if __name__ == '__main__':
    unittest.main()