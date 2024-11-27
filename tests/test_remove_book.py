import os
import random
import unittest

from book_helpers import BookTools
from main import Router
from screen_renders import AddBookPage, UpdateBookPage, RemoveBookPage


class TestUpdateBook(unittest.TestCase):
    def setUp(self):
        # Переименовываем файл, если он существует
        if os.path.exists("./data.json"):
            os.rename("./data.json", "./data_test.json")

        self.mock_router = Router(test_mode=True)
        self.page = RemoveBookPage(self.mock_router)

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

    def test_remove_book_function(self):

        # Проверяем что новая книга существует и data-файл не пустой
        self.assertTrue(self.new_book)
        self.assertEqual(len(self.mock_router.book_tools.get_book_list()), 1)

        # Проверяем что книга не удалена при ошибке ввода или отказе
        invalid_inputs = ["2", "", "0", "test", "30"]
        for value in invalid_inputs:
            self.page.process_user_input(value, book_object=self.new_book)
            self.assertEqual(len(self.mock_router.book_tools.get_book_list()), 1)

        # Проверяем что нельзя удалить книгу по id которого нет
        exist_id = []
        for book in self.mock_router.book_tools.get_book_list():
            exist_id.append(book.id)

        while True:
            random_number = random.randrange(100)
            if random_number not in exist_id:
                break

        self.mock_router.book_tools.remove_book(random_number)
        self.assertEqual(len(self.mock_router.book_tools.get_book_list()), 1)

    def test_remove_book_form(self):
        # Удаляем книгу
        self.page.process_user_input("1", book_object=self.new_book)

        # Проверяем что книга удалена из каталога
        self.assertEqual(self.mock_router.book_tools.book_list, [])

        # Проверяем что книга удалена из data-файла
        self.assertEqual(self.mock_router.book_tools.get_book_list(), [])








