import json
import os
import unittest

from main import Router


class TestStartApplication(unittest.TestCase):
    def setUp(self):
        # Переименовываем файл, если он существует
        if os.path.exists("./data.json"):
            os.rename("./data.json", "./data_test.json")

    def tearDown(self):
        # Возвращаем файл обратно
        if os.path.exists("./data_test.json"):
            os.rename("./data_test.json", "./data.json")

    def test_start_app(self):
        # Запускаем приложение
        try:
            Router(test_mode=True)
        except Exception as e:
            self.fail(f"Приложение не может быть запущено: {e}")

    def test_file_creation(self):

        # Запускаем приложение
        Router(test_mode=True)

        # Проверяем, что файл был создан
        self.assertTrue(os.path.exists("data.json"), "Файл data.json не был создан.")

        # Проверяем что содержимое файла - пустой список
        with open("data.json", "r") as json_file:
            json_content = json.load(json_file)
            self.assertEqual(json_content, [], "Файл data.json содержит некорректные данные.")
