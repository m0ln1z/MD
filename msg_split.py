from html.parser import HTMLParser
from typing import Generator

MAX_LEN = 4096

def split_message(source: str, max_len: int = MAX_LEN) -> Generator[str, None, None]:
    """
    Splits the original HTML message into fragments of the specified length.

    Args:
        source (str): The HTML content to split.
        max_len (int): Maximum length of each fragment.

    Yields:
        str: Valid HTML fragments.
    """
    class HTMLSplitter(HTMLParser):
        def __init__(self, max_len: int):
            super().__init__()
            self.max_len = max_len
            self.fragments = []
            self.current_fragment = ""
            self.current_length = 0
            self.open_tags = []
            self.current_element_length = 0  

        def handle_starttag(self, tag, attrs):
            attrs_str = "".join(f' {k}="{v}"' for k, v in attrs)
            tag_str = f"<{tag}{attrs_str}>"
            if len(tag_str) > self.max_len:
                raise ValueError(f"Single element <{tag}> exceeds max length of {self.max_len} characters.")
            self._append(tag_str)
            self.open_tags.append(tag)
            self.current_element_length += len(tag_str)

        def handle_endtag(self, tag):
            if tag in self.open_tags:
                tag_str = f"</{tag}>"
                self._append(tag_str)
                self.open_tags.remove(tag)
                self.current_element_length += len(tag_str)
                if self.current_element_length > self.max_len:
                    raise ValueError(f"Element <{tag}>... exceeds max length of {self.max_len} characters.")
                self.current_element_length = 0  # Reset for the next element

        def handle_data(self, data):
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
            if self.current_length + len(content) > self.max_len:
                self._finalize_fragment()
            self.current_fragment += content
            self.current_length += len(content)

        def _finalize_fragment(self):
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
            if self.current_fragment:
                self._finalize_fragment()
            return self.fragments

    splitter = HTMLSplitter(max_len)
    splitter.feed(source)
    yield from splitter.get_fragments()
