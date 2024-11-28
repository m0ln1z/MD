import argparse
from msg_split import split_message

def main():
    """
    Основная функция для обработки командной строки и выполнения разделения HTML.

    - Принимает путь к HTML-файлу и максимальную длину фрагмента как аргументы.
    - Читает содержимое HTML-файла.
    - Разделяет содержимое на фрагменты заданной длины с помощью функции `split_message`.
    - Выводит каждый фрагмент на экран вместе с его длиной.

    Аргументы командной строки:
        file: Путь к HTML-файлу для обработки.
        --max-len: Максимальная длина фрагмента (по умолчанию 4096).
    """
    parser = argparse.ArgumentParser(description="Split HTML content into fragments of specified max length.")
    parser.add_argument("file", type=str, help="Path to the HTML file to process.")
    parser.add_argument("--max-len", type=int, default=4096, help="Maximum fragment length (default: 4096).")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as file:
            html_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
        return

    try:
        fragments = list(split_message(html_content, max_len=args.max_len))
    except Exception as e:
        print(f"Error during splitting: {e}")
        return

    for i, fragment in enumerate(fragments, start=1):
        print(f"--- Fragment #{i}: {len(fragment)} characters ---")
        print(fragment)
        print("")

if __name__ == "__main__":
    """
    Точка входа в скрипт.

    Запускает функцию `main` для выполнения обработки командной строки и разделения HTML.
    """
    main()
