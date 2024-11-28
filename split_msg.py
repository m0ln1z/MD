import argparse
from msg_split import split_message

def main():
    parser = argparse.ArgumentParser(description="Разделение HTML-сообщения на фрагменты.")
    parser.add_argument("file", type=str, help="Путь к HTML-файлу.")
    parser.add_argument("--max-len", type=int, default=4096, help="Максимальная длина фрагмента.")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            source = f.read()
        for i, fragment in enumerate(split_message(source, max_len=args.max_len), start=1):
            print(f"fragment #{i}: {len(fragment)} chars")
            print(fragment)
            print("-" * 80)
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
