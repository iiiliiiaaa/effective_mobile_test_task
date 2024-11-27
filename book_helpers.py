import json
import os
import time

from validators import validate_form_fields


class Book:
    """  Класс для репрезентации объекта книги. """
    def __init__(self, id: int, title: str, author: str, year: str, status: str = "В наличии") -> None:
        """ Инициализация объекта книги.

            :param id: идентификатор книги
            :param title: название книги
            :param author: автор книги
            :param year: год издания книги
            :param status: статус книги, по умолчанию 'В наличии'
        """
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self) -> str:
        return f"{self.id}. {self.title}, {self.author}, {self.year}, {self.status}"

    def full_repr(self) -> str:
        return f" id: {self.id}\n Название: {self.title}\n Автор: {self.author}\n Год издания: {self.year}\n Статус: {self.status}"


class BookTools:
    """  Класс с методами для работы с книгами.

        Методы:
        - :get_book_list(): возвращает книги из data.json
        - :search_books(): поиск книг по названию, автору, году
        - :add_book(): добавление новой книги
        - :remove_book(): удаление книги
        - :update_book(): обновление книги
        - :save_book_list(): сохранение изменений в data.json
        - :validate_form_fields(): валидация полей формы
    """
    def __init__(self) -> None:
        self.check_data_file()
        self.book_list = self.get_book_list()

    @staticmethod
    def get_book_list() -> list[Book]:
        """  Получение списка книг из data.json. """
        with open("data.json", "r") as json_file:
            json_content = json.load(json_file)
            return [Book(**item) for item in json_content]

    @staticmethod
    def check_data_file(file_path: str = "data.json") -> None:
        """  Проверка наличия файла. Если нет - создаем его с пустым списком.

            :param file_path: путь к файлу
         """
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                json.dump([], file)
            # print(f"Создан файл данных: {file_path}")  # debug

    def search_books(self, query: str, search_fields: list[str], strong: bool = False) -> list[Book] | None:
        """  Поиск книг по номеру, названию, автору, году.

            :param query: строка поиска
            :param search_fields: список полей поиска
            :param strong: если True - то ищем точное совпадение, если False - то вхождение
        """
        if search_fields == ['id']:
            success, error = validate_form_fields('id', query)
            if not success:
                return None

        result = []
        for item in self.book_list:
            if strong:
                if all(query in str(getattr(item, field)) for field in search_fields):
                    result.append(item)
            else:
                if any(query.lower() in str(getattr(item, field)).lower() for field in search_fields):
                    result.append(item)
        return result

    def add_book(self, title: str, author: str, year: str) -> None:
        """  Добавление новой книги.

            :param title: название книги
            :param author: автор книги
            :param year: год издания книги
        """
        last_id = self.book_list[-1].id if self.book_list else 0
        self.book_list.append(Book(last_id + 1, title, author, year))
        self.save_book_list()
        print("Книга успешно добавлена!")
        time.sleep(1)  # Чтобы пользователь успел увидеть сообщение

    def remove_book(self, book_id: int) -> None:
        """  Удаление книги.

            :param book_id: идентификатор книги
        """
        self.book_list = [item for item in self.book_list if item.id != book_id]
        print("Книга успешно удалена!")
        self.save_book_list()
        time.sleep(1)  # Чтобы пользователь успел увидеть сообщение

    def update_book(self, book_object: Book, field: str, value: str) -> None:
        """  Обновление книги.

            :param book_object: объект книги
            :param field: атрибут для обновления
            :param value: новое значение
        """
        setattr(book_object, field, value)
        # self.save_book_list()  # Отключено для скорости, сохранение происходит при выходе из приложения
        print("Книга успешно обновлена!")
        time.sleep(1)  # Чтобы пользователь успел увидеть сообщение

    def save_book_list(self) -> None:
        """  Сохранение списка книг в JSON-файл. Полная перезапись. """
        with open("data.json", "w", encoding="utf-8") as json_file:
            json.dump([item.__dict__ for item in self.book_list], json_file, indent=4, ensure_ascii=False)