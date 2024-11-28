from html.parser import HTMLParser
from typing import Generator

MAX_LEN = 4096

def split_message(source: str, max_len: int = MAX_LEN) -> Generator[str, None, None]:
    """
    Разделяет исходное HTML-сообщение на фрагменты указанной длины.

    Аргументы:
        source (str): HTML-контент для разделения.
        max_len (int): Максимальная длина каждого фрагмента.

    Возвращает:
        str: Допустимые фрагменты HTML.
    """
    class HTMLSplitter(HTMLParser):
        """
        Класс для разделения HTML-сообщения на фрагменты указанной длины.

        Атрибуты:
            max_len (int): Максимальная длина каждого фрагмента.
            fragments (list): Список фрагментов HTML.
            current_fragment (str): Текущий фрагмент HTML.
            current_length (int): Текущая длина фрагмента HTML.
            open_tags (list): Список открытых тегов HTML.
            current_element_length (int): Текущая длина элемента HTML.
        """
        def __init__(self, max_len: int):
            super().__init__()
            self.max_len = max_len
            self.fragments = []
            self.current_fragment = ""
            self.current_length = 0
            self.open_tags = []
            self.current_element_length = 0

        def handle_starttag(self, tag, attrs):
            """
            Обработчик начального тега HTML.

            Аргументы:
                tag (str): Имя начального тега.
                attrs (list): Список атрибутов начального тега.
            """
            attrs_str = "".join(f' {k}="{v}"' for k, v in attrs)
            tag_str = f"<{tag}{attrs_str}>"
            if len(tag_str) > self.max_len:
                raise ValueError(f"Одиночный элемент <{tag}> превышает максимальную длину {self.max_len} символов.")
            self._append(tag_str)
            self.open_tags.append(tag)
            self.current_element_length += len(tag_str)

        def handle_endtag(self, tag):
            """
            Обработчик закрывающего тега HTML.

            Аргументы:
            tag (str): Имя закрывающего тега.
            """
            if tag in self.open_tags:
            tag_str = f"</{tag}>"
            self._append(tag_str)
            self.open_tags.remove(tag)
            self.current_element_length += len(tag_str)
            if self.current_element_length > self.max_len:
                raise ValueError(f"Элемент <{tag}>... превышает максимальную длину {self.max_len} символов.")
            self.current_element_length = 0  # Сбросить для следующего элемента

        def handle_data(self, data):
            """
            Обработчик данных HTML.

            Аргументы:
            data (str): Данные HTML.
            """
            while data:
            remaining_space = self.max_len - self.current_length
            if remaining_space <= 0:
                self._finalize_fragment()
                continue

            chunk = data[:remaining_space]
            self.current_fragment += chunk
            self.current_length += len(chunk)
            self.current_element_length += len(chunk)
            data = data[remaining_space:]

        def _append(self, content):
            """
            Добавляет контент к текущему фрагменту.

            Аргументы:
            content (str): Контент для добавления.
            """
            if self.current_length + len(content) > self.max_len:
            self._finalize_fragment()
            self.current_fragment += content
            self.current_length += len(content)

        def _finalize_fragment(self):
            """
            Завершает текущий фрагмент и добавляет его в список фрагментов.
            """
            if self.current_fragment:
            for tag in reversed(self.open_tags):
                self.current_fragment += f"</{tag}>"
            self.fragments.append(self.current_fragment)
            self.current_fragment = ""
            self.current_length = 0
            for tag in self.open_tags:
                self.current_fragment += f"<{tag}>"
                self.current_length += len(f"<{tag}>")

        def get_fragments(self):
            """
            Возвращает список фрагментов HTML.
            """
            if self.current_fragment:
            self._finalize_fragment()
            return self.fragments
