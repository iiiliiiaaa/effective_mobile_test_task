# Library Management System

## Описание

Консольное приложение для управления библиотекой книг пользователя


```
---------------------------------------
[Главная страница]
---------------------------------------
Добро пожаловать в библиотеку!

Выберите slug страницы:
c - Каталог
s - Поиск книг
n - Добавить книгу
q - Выход

-Ваш ввод: n

---------------------------------------
[Добавить книгу]
---------------------------------------
Введите название: Война и мир
Введите автора: Лев Толстой
Введите год издания: 1867

Книга успешно добавлена!

```

## Функциональные возможности

### 1. Навигация по приложению через ввод команд в консоли

На каждом экране приложение предлагает возможные пункты меню, на которые можно перейти. Пункты меню имеют вид slug - title, например:
```
------
Выберите slug страницы, на которую хотите перейти:
 с - Каталог
 s - Поиск
 h - Главная
 q - Выход
```

Навигация осуществляется путём отправки в консоль slug нужной страницы. На некоторых страницах может быть несколько меню или вложенные формы, например:
```
Введите id книги, к которой хотите перейти:
1. Война и мир, Лев Николаевич Толстой, 1867, В наличии
2. Ненасильственное общение, Маршалл Розенберг, 2018, Выдана

------
Выберите slug страницы, на которую хотите перейти:
 с - Каталог
 s - Поиск
```
При вводе команды система сначала будет искать совпадения из пунктов верхнего (внутреннего) меню страницы, а потом из нижнего. При отсутствии совпадений будет выдана ошибка, страница будет перезагружена.

### 2. Управление библиотекой книг
- Просмотр списка книг в библиотеке
- Просмотр страницы отдельной книги
- Создание книг, у каждой книги есть:
  - id
  - Название
  - Автор
  - Год
  - Статус (по-умолчанию: В наличии)
- Смена статуса книги
- Удаление книги
- Поиск книг строгий / по вхождению
  - по полю Название
  - по полю Автор
  - по полю Год

## Структура проекта
```
blocknote
├── tests/test_add_book.py        - Тесты на добавление книги
├── tests/test_remove_book.p      - Тесты на удаление книги
├── tests/test_start_app.py       - Тесты на запуск приложения 
├── tests/test_update_book.py     - Тесты на обновление книги
├── book_helpers.py               - Сериализатор, Инструменты для управления каталогом и книгами
├── data.json                     - Файл для хранения списка книг в формате json (создаётся автоматически при запуске проекта)
├── main.py                       - Точка входа
├── screen_renders.py             - Классы с экранами приложения
└── validators.py                 - Валидаторы данных
```

## Установка и запуск
- Склонировать репозиторий
- Запустить:
```
python main.py
```
- При первом запуске приложения, система создаст файл data.json для хранения данных
- Сохранение данных в файл происходит при создании книги, обновлении статуса и при выходе из приложения

## Требования
Разработано и протестировано на: Python 3.12.6
Зависимости - отсутствуют, система реализована без применения сторонних библиотек

## Тестирование
Для тестов использована библиотека unittest
Запуск тестов:
```
python -m unittest discover -s tests -p "test_*.py"
```

### Тестовое задание на позицию python-разработчик. Автор - Илья Бердышев. [t.me/berdyshev_ilia](https://t.me/berdyshev_ilia)