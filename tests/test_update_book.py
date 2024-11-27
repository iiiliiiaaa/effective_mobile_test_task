import os
import unittest

from book_helpers import BookTools
from main import Router
from screen_renders import AddBookPage, UpdateBookPage


class TestUpdateBook(unittest.TestCase):
    def setUp(self):
        # Переименовываем файл, если он существует
        if os.path.exists("./data.json"):
            os.rename("./data.json", "./data_test.json")

        self.mock_router = Router(test_mode=True)
        self.page = UpdateBookPage(self.mock_router)

        # Для начала создадим нову книгу
        self.add_page = AddBookPage(self.mock_router)
        self.add_page.process_user_input("Valid Title", field="title")
        self.add_page.process_user_input("Valid Author", field="author")
        self.add_page.process_user_input("2023", field="year")
        self.new_book = self.add_page.router.book_tools.get_book_list()[-1]

    def tearDown(self):
        # Возвращаем файл обратно
        if os.path.exists("./data_test.json"):
            os.rename("./data_test.json", "./data.json")

    def test_update_book_status(self):
        # Проверяем что у новой книги статус "В наличии"
        self.assertEqual(self.new_book.status, "В наличии")

        # Обновляем статус книги
        self.page.process_user_input("2", book_object=self.new_book)

        # Проверяем что статус книги изменился
        self.assertEqual(self.new_book.status, "Выдана")

        # Обновляем статус книги
        self.page.process_user_input("1", book_object=self.new_book)

        # Проверяем что статус книги изменился
        self.assertEqual(self.new_book.status, "В наличии")

        # Проверяем что статус книги не изменился, при ошибке ввода
        invalid_inputs = ["", "0", "test", "30"]
        for value in invalid_inputs:
            self.page.process_user_input(value, book_object=self.new_book)
            self.assertEqual(self.new_book.status, "В наличии")







