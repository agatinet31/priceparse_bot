DEFAULT_REQUEST_ERROR_MSG = "Ошибка получения данных!"


class PriceParseError(Exception):
    """Класс исключения парсинга."""

    pass


class PriceParseRequestError(PriceParseError):
    """Класс исключения при запросе информации."""

    def __init__(self, url, xpath, message=DEFAULT_REQUEST_ERROR_MSG):
        self.url = url
        self.xpath = xpath
        super().__init__(f"{message} URL: {url}. " f"XPath={xpath}.")


class PriceParseNotFoundError(PriceParseRequestError):
    """Класс исключения при отсутствии информации по товару."""

    pass


class PriceParseDBNotFoundError(PriceParseError):
    """Класс исключения при отсутствии информации в базе данных."""

    def __init__(self, product_link_id):
        self.product_link_id = product_link_id
        super().__init__(
            f"Информация для парсинга с идентификтором {product_link_id} "
            "не найдена в БД!"
        )


class ImportExcelFileError(Exception):
    """Класс исключения при импорте Excel файла."""

    pass
