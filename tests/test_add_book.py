import os
import unittest

from book_helpers import BookTools
from main import Router
from screen_renders import AddBookPage


class TestAddBook(unittest.TestCase):
    def setUp(self):
        # Переименовываем файл, если он существует
        if os.path.exists("./data.json"):
            os.rename("./data.json", "./data_test.json")

        self.mock_router = Router(test_mode=True)
        self.page = AddBookPage(self.mock_router)

    def tearDown(self):
        # Возвращаем файл обратно
        if os.path.exists("./data_test.json"):
            os.rename("./data_test.json", "./data.json")

    def test_process_field_title(self):
        # Тестируем некорректные данные в поле title
        test_invalid_title_values = ["", "Va", "123"]
        for value in test_invalid_title_values:
            self.page.process_user_input(value, field="title")
            self.assertNotEqual(self, self.page.temp_title, value)

        # Тестируем корректные данные в поле title
        self.page.process_user_input("Valid Title", field="title")
        self.assertEqual(self.page.temp_title, "Valid Title")

    def test_process_field_author(self):
        # Для начала отправим корректные данные в поле title
        self.page.process_user_input("Valid Title", field="title")

        # Тестируем некорректные данные в поле author
        test_invalid_author_values = ["", "Va", "123"]
        for value in test_invalid_author_values:
            self.page.process_user_input(value, field="author")
            self.assertNotEqual(self, self.page.temp_author, value)

        # Тестируем корректные данные в поле author
        self.page.process_user_input("Valid Author", field="author")
        self.assertEqual(self.page.temp_author, "Valid Author")

    def test_process_field_year(self):
        # Для начала отправим корректные данные в поле title, author
        self.page.process_user_input("Valid Title", field="title")
        self.page.process_user_input("Valid Author", field="author")

        # Тестируем некорректные данные в поле year
        test_invalid_year_values = ["", "Va", "test", "0", "2030"]
        for value in test_invalid_year_values:
            self.page.process_user_input(value, field="year")
            self.assertNotEqual(self, self.page.temp_year, value)

        # Тестируем корректные данные в поле year
        self.page.process_user_input("2023", field="year")
        self.assertEqual(self.page.temp_year, "2023")

    def test_book_added_to_data_file(self):
        test_title = "Valid Title test"

        # Для начала проверим что книги с таким названием нет в файле
        for book in self.mock_router.book_tools.get_book_list():
            self.assertNotEqual(book.title, test_title)

        # Отправим корректные данные в поле title, author, year
        self.page.process_user_input(test_title, field="title")
        self.page.process_user_input("Valid Author", field="author")
        self.page.process_user_input("2023", field="year")

        # Проверим что книга есть в списке каталога
        self.assertEqual(self.mock_router.book_tools.book_list[-1].title, test_title)

        # Проверим что книга с таким названием есть в файле
        self.assertEqual(self.mock_router.book_tools.get_book_list()[-1].title, test_title)






