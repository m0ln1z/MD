from html.parser import HTMLParser
from typing import Generator

MAX_LEN = 4096


class TagHandler(HTMLParser):
    """
    Класс для обработки и хранения текущей структуры открытых тегов.
    """

    def __init__(self):
        super().__init__()
        self.stack = []  # Стек открытых тегов
        self.result = []  # Хранилище собранного текста

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        self.result.append(f"<{tag}{self._format_attrs(attrs)}>")

    def handle_endtag(self, tag):
        while self.stack and self.stack[-1] != tag:
            self.result.append(f"</{self.stack.pop()}>")
        if self.stack:
            self.stack.pop()
            self.result.append(f"</{tag}>")

    def handle_data(self, data):
        self.result.append(data)

    def _format_attrs(self, attrs):
        return "".join(f' {name}="{value}"' for name, value in attrs)

    def get_current_structure(self):
        """Возвращает текущую структуру открытых тегов."""
        return "".join(f"<{tag}>" for tag in self.stack)

    def close_tags(self):
        """Закрывает все открытые теги."""
        return "".join(f"</{tag}>" for tag in reversed(self.stack))


def split_message(source: str, max_len: int = MAX_LEN) -> Generator[str, None, None]:
    """
    Разделяет HTML-сообщение на фрагменты заданной длины, сохраняя структуру тегов.
    """
    parser = TagHandler()
    current_fragment = []
    current_length = 0

    parser.feed(source)

    for piece in parser.result:
        piece_length = len(piece)
        if piece_length > max_len:
            # Если элемент слишком велик для одного фрагмента, выбрасываем исключение
            raise ValueError(f"Элемент длиной {piece_length} превышает максимальный размер {max_len}.")

        if current_length + piece_length > max_len:
            if current_length == 0:
                raise ValueError("Невозможно разделить текст: один элемент превышает max_len.")
            # Закрываем текущий фрагмент
            yield "".join(current_fragment) + parser.close_tags()
            # Открываем новый фрагмент
            current_fragment = [parser.get_current_structure()]
            current_length = 0

        current_fragment.append(piece)
        current_length += piece_length

    # Последний фрагмент
    if current_fragment:
        yield "".join(current_fragment) + parser.close_tags()