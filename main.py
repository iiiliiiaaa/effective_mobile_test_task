from book_helpers import BookTools, Book
from screen_renders import HomePage, CatalogPage, ExitPage, SearchPage, AddBookPage, BookPage, UpdateBookPage, RemoveBookPage


class Router:
    """ Класс маршрутизатора.

        Атрибуты:
        - self.book_tools: экземпляр BookTools
        - self.screens: словарь зарегистрированных экземпляров страниц
        - self.redirect_to(): метод перенаправления пользователя на другую страницу

    """

    def __init__(self, test_mode: bool = False) -> None:
        self.test_mode = test_mode
        self.book_tools = BookTools()
        self.screens = {
            "h": HomePage(self),
            "c": CatalogPage(self),
            "s": SearchPage(self),
            "n": AddBookPage(self),
            "b": BookPage(self),
            "r": RemoveBookPage(self),
            "u": UpdateBookPage(self),
            "q": ExitPage(self)
        }
        self.redirect_to("h")  # slug for HomePage

    def redirect_to(self, screen_slug: str, **kwargs: dict[str, 'Book']) -> None:
        """  Метод перенаправления пользователя на другую страницу.

            :param screen_slug: slug страницы
            :param kwargs: полезные данные
        """
        if not self.test_mode:
            self.screens[screen_slug].render(**kwargs)


if __name__ == "__main__":
    Router()
