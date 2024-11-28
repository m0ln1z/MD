import unittest
from msg_split import split_message  # Импорт функции

class TestSplitMessage(unittest.TestCase):
    def test_large_element(self):
        source = "<p>" + "A" * 5000 + "</p>" 
        with self.assertRaises(ValueError):
            list(split_message(source, max_len=4096))
    
    def test_split_basic(self):
        source = "<p>Hello, world!</p>" * 10
        fragments = list(split_message(source, max_len=50))
        self.assertGreater(len(fragments), 1)  

if __name__ == "__main__":
    unittest.main()