def validate_form_fields(field: str, value: str) -> tuple[bool, str]:
    """  Валидация полей формы.

        :param field: поле формы
        :param value: проверяемое значение
        """
    error = ""

    if field == "id":
        if not value.isdigit() or int(value) <= 0:
            error = "\n--- Некорректный ввод: ID должен быть числом > 0 ---\n"
            return False, error

    if field == "title" or field == "author":
        if len(value) < 3:
            error = "\n--- Некорректный ввод: строка должна быть больше 2-х символов ---\n"
            return False, error

    if field == "year":
        if not value.isdigit() or int(value) < 0 or int(value) > 2024:
            error = "\n--- Некорректный ввод: год должен быть числом больше нуля, меньше 2025 ---\n"
            return False, error

    return True, error
