import time
from typing import TYPE_CHECKING, Union, Optional, Dict

from validators import validate_form_fields

if TYPE_CHECKING:
    # Импорт для проверки типов
    from main import Router
    from book_helpers import Book


class BasePage:
    """ Базовый класс для наследуемых страниц.

        Чтобы создать новую страницу нужно:
        - Создать новый класс страницы, наследовать его от этого класса
        - Определить в нем необходимые атрибуты (`title`, `page_links`).
        - Зарегистрировать страницу в роутере (Router) в main.py

        Атрибуты:
            router: экземпляр роутера
            title: заголовок страницы, выводится в меню
            page_links: список slug страниц, зарегистрированных в роутере
    """
    def __init__(self, router: 'Router') -> None:
        self.router = router
        self.title = "Page title"
        self.page_links = []

    def render(self, **kwargs) -> None:
        """ Рендерит контент страницы, обрабатываетввод и направляет пользователя на другие страницы. Порядок работы:
            - Выводит контент страницы
            - Выводит меню страницы
            - Запрашивает ввод пользователя
            - Обрабатывает ввод пользователя

            Аргументы:
                **kwargs: доп. параметры  для дочерней страницы
        """
        self.get_page_content(**kwargs)
        self.print_menu()
        input_string = input("\n-Ваш ввод: ")
        self.process_user_input(input_string, **kwargs)

    def get_page_content(self, **kwargs) -> None:
        """ Выводит контент и список действий на странице. """
        print(self.title)

    def process_user_input(self, input_string: str, **kwargs) -> None:
        """  Обрабатывает ввод пользователя. Вызывается в дочерних классах, чтобы перемещаться по меню. Т.е.:
            - Если в дочерней странице при обработке ввода не нашлось совпадений по действиям, можно вызвать этот метод для
            перебора по self.page_links.
            - Если в self.page_links таких ссылок нет, остаёмся на текущей странице.
        """
        if input_string in self.router.screens:
            self.router.redirect_to(input_string)
        else:
            print("\n--- Некорректный ввод ---")
            time.sleep(1)
            self.render(**kwargs)

    def print_menu(self) -> None:
        """ Печатает меню страницы в формате: slug - page title. Если у страницы есть НЕпустой self.page_links, то
        вконце каждой страницы печатает его."""
        if self.page_links:
            print("\n------")
            print("Выберите slug страницы, на которую хотите перейти:")
            for slug in self.page_links:
                print(f"{slug} - {self.router.screens[slug].title}")

    @staticmethod
    def print_header(text: str) -> None:
        """ Печатает красивую шапку страницы. """
        print("\n---------------------------------------")
        print(text)
        print("---------------------------------------\n")


class HomePage(BasePage):
    """ Главная (первая) страница библиотеки. """

    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Главная"
        self.page_links = [
            "c",  # slug for CatalogPage
            "s",  # slug for SearchPage
            "n",  # slug for AddBookPage
            "q",  # slug for Exit
        ]

    def get_page_content(self) -> None:
        self.print_header("Добро пожаловать в библиотеку!")
        print("Для навигации используйте краткие названия страниц(slug) на английской раскладке клавиатуры.")


class CatalogPage(BasePage):
    """  Страница каталога книг. Выводит список книг со ссылками, если они есть в библиотеке.
    Если нет - предложение создать. """

    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Каталог"
        self.page_links = [
            "s",  # slug for SearchPage
            "n",  # slug for AddBookPage
            "h",  # slug for HomePage
        ]

    def get_page_content(self) -> None:
        self.print_header(f"[{self.title}]")

        book_list = self.router.book_tools.get_book_list()
        if not book_list:
            print("В вашей библиотеке нет книг. Добавьте книги на странице создания книги")
        else:
            print("Введите id книги, к которой хотите перейти:")
            for item in self.router.book_tools.get_book_list():
                print(item)

    def process_user_input(self, input_string: str, **kwargs) -> None:
        """ Если пользователь ввёл id книги, то перебирает список книг и проверяет есть ли книга с таким id.
            Если есть - переводит пользователя на страницу книги.
            Если ввод пользователя - не id или такой книги нет, то передаём ввод в обработку родительскому классу.
        """
        result_search = self.router.book_tools.search_books(input_string, ['id'], strong=True)

        if result_search:
            self.router.redirect_to('b', book_object=result_search[0])
        else:
            super().process_user_input(input_string, **kwargs)


class SearchPage(BasePage):
    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Поиск книг"
        self.page_links = [
            "s",  # slug for Search item
            "c",  # slug for CatalogPage
        ]

    def get_page_content(self, **kwargs) -> None:
        self.print_header(f"[{self.title}]")
        print("Введите текст для поиска книг по полям: title | author | year: ")

    def process_user_input(self, input_string: str, **kwargs) -> None:
        """ Если есть результаты поиска - показывает ссылки на них.
            Если нет - предложение повторить поиск.
        """
        self.print_header(f"Результаты поиска: [{input_string}]")

        # Поиск книг
        result_search = self.router.book_tools.search_books(input_string, ['title', 'author', 'year'])
        if result_search:
            print("Введите номер книги, к которой хотите перейти:")
            for item in result_search:
                print(item)
        else:
            print("Пусто! Таких книг не найдено, попробуйте другой поиск.")

        # Показываем меню, чтобы можно было искать заново
        self.print_menu()
        input_string = input("\n-Ваш ввод: ")

        # Если переход по существующему id - редирект на книгу, если нет - передаём в родительский обработчик
        result_search = self.router.book_tools.search_books(input_string, ['id'], strong=True)
        if result_search:
            self.router.redirect_to('b', book_object=result_search[0])
        else:
            super().process_user_input(input_string, **kwargs)


class BookPage(BasePage):
    """ Страница книги. Выводит полную информацию о книге и ссылки на:
        - смену статуса
        - удаление книги.
      """
    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Книга"
        self.page_links = [
            "c",  # slug for CatalogPage
        ]

    def get_page_content(self, **kwargs) -> None:
        self.print_header(f"[{self.title}]: {kwargs['book_object'].title}")

        # Вывод полной информации о книге с заголовками полей
        print(kwargs['book_object'].full_repr())

        print("\n---")
        print("Выберите действие: ")
        print("u - Поменять статус")  # slug for UpdateBookPage
        print("r - Удалить книгу")  # slug for RemoveBookPage

    def process_user_input(self, input_string: str, **kwargs) -> None:
        match input_string:
            case "u":
                self.router.redirect_to('u', book_object=kwargs['book_object'])
            case "r":
                self.router.redirect_to('r', book_object=kwargs['book_object'])
            case _:
                super().process_user_input(input_string, **kwargs)


class AddBookPage(BasePage):
    """ Страница ç формой добавления новой книги в каталог.
        После успешного добавления происходит редирект на Каталог.

        Временные переменные для хранения данных ввода:
        - self.temp_title
        - self.temp_author
        - self.temp_year
    """
    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Добавить книгу в каталог"
        self.temp_title = ""
        self.temp_author = ""
        self.temp_year = ""

    def get_page_content(self) -> None:
        """ Пользователь находится в цикле до тех пор, пока все данные не будут заполнены и не пройдут валидацию. """
        self.print_header(f"[{self.title}]")

        form_fields = {
            "title": "Введите название:",
            "author": "Введите автора:",
            "year": "Введите год издания:",
        }

        # Цикл формы
        for field, value in form_fields.items():
            while not getattr(self, f"temp_{field}", None):
                print(value)
                input_string = input("\n-Ваш ввод: ")
                self.process_user_input(input_string, field=field)

    def process_user_input(self, input_string: str, **kwargs) -> None:
        field = kwargs['field']

        # Валидация ввода
        success, error = validate_form_fields(field, input_string)
        if success:
            setattr(self, f"temp_{field}", input_string)
            print()
        else:
            print(error)

        # Если все данные введены - выходим из цикла
        if self.temp_title and self.temp_author and self.temp_year:

            # Добавляем книгу
            self.router.book_tools.add_book(self.temp_title, self.temp_author, self.temp_year)

            # Очищаем временные переменные
            if not self.router.test_mode:
                self.temp_title, self.temp_author, self.temp_year = "", "", ""

            # Редирект на каталог
            self.router.redirect_to('c')


class UpdateBookPage(BasePage):
    """  Смена статуса книги, варианты:
        - В наличии
        - Выдана
        После смены статуса происходит редирект на страницу книги.
    """
    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Обновить статус книги"

    def get_page_content(self, **kwargs) -> None:
        self.print_header(f"[{self.title}]: {kwargs['book_object'].title}")
        print(f"Текущий статус: {kwargs['book_object'].status}\n")
        print("Выберите новый статус: ")
        print("1. В наличии")
        print("2. Выдана")

    def process_user_input(self, input_string: str, **kwargs) -> None:
        match input_string:
            case "1":
                self.router.book_tools.update_book(kwargs['book_object'], "status", "В наличии")
                self.router.redirect_to('b', book_object=kwargs['book_object'])
            case "2":
                self.router.book_tools.update_book(kwargs['book_object'], "status", "Выдана")
                self.router.redirect_to('b', book_object=kwargs['book_object'])
            # case _:
            #     super().process_user_input(input_string, **kwargs)


class RemoveBookPage(BasePage):
    """  Удаление книги из каталога. После удаления происходит редирект на каталог. """
    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Удалить книгу"

    def get_page_content(self, **kwargs) -> None:
        self.print_header(f"[{self.title}]: {kwargs['book_object'].title}")
        print("Вы уверены, что хотите удалить эту книгу?")
        print("1. Да")
        print("2. Нет")

    def process_user_input(self, input_string: str, **kwargs) -> None:
        match input_string:
            case "1":
                self.router.book_tools.remove_book(kwargs['book_object'].id)
                self.router.redirect_to('c')
            case _:
                self.router.redirect_to('c')


class ExitPage(BasePage):
    """  Выход из приложения. Перед выходом сохраняет актуальный список книг. """
    def __init__(self, router: 'Router') -> None:
        super().__init__(router)
        self.title = "Выход"

    def render(self) -> None:
        self.router.book_tools.save_book_list()
        self.print_header("Всего доброго! Приходите ещё!")
        exit()
