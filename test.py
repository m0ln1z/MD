import unittest
from msg_split import split_message

class TestHTMLSplitter(unittest.TestCase):
    """
    Тестовый набор для функции разделения HTML.

    Этот тестовый набор содержит несколько методов для проверки поведения функции split_message
    при разделении HTML-сообщений на фрагменты.

    Каждый метод представляет собой конкретный сценарий и проверяет ожидаемые результаты.
    """

    def test_basic_split(self):
        """
        Тест базовой функциональности разделения функции split_message.
        """
        html = "<p>Hello, <b>world</b>! <i>Nice to meet you!</i></p>"
        fragments = list(split_message(html, max_len=30))
        self.assertEqual(len(fragments), 2)  
        self.assertTrue(fragments[0].endswith("</b></p>") or fragments[0].endswith("</p>"))  
        self.assertTrue(fragments[1].startswith("<p>"))  

    def test_nested_tags(self):
        """
        Тест разделения функции split_message с вложенными HTML-тегами.
        """
        html = "<div><p>" + "A" * 4000 + "</p><p>" + "B" * 100 + "</p></div>"
        fragments = list(split_message(html, max_len=4096))
        self.assertEqual(len(fragments), 2)  
        self.assertTrue(fragments[0].endswith("</p></div>") or fragments[0].endswith("</p>"))  
        self.assertTrue(fragments[1].startswith("<div><p>") or fragments[1].startswith("<p>")) 

    def test_long_text(self):
        """
        Тест поведения функции split_message, когда входной HTML слишком длинный.
        """
        html = "<p>" + "A" * 5000 + "</p>"
        with self.assertRaises(ValueError):
            list(split_message(html, max_len=4096))  

    def test_fragment_lengths(self):
        """
        Тест длины каждого фрагмента, созданного функцией split_message.
        """
        html = "<p>" + "A" * 100 + "</p>" * 50
        fragments = list(split_message(html, max_len=500))
        for fragment in fragments:
            self.assertLessEqual(len(fragment), 500) 

if __name__ == "__main__":
    unittest.main()
