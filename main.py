import argparse

from src.utils.b2b_parser import main


if __name__ == "__main__":
    # Запуск парсера производится с помощью команды python main.py --max 10 --output tenders.csv

    parser = argparse.ArgumentParser(
        description="Парсер тендеров b2b-center.ru"
    )
    parser.add_argument(
        "--max", type=int, help="Максимальное количество тендеров для парсинга"
    )
    parser.add_argument(
        "--output", type=str, help="Имя выходного CSV файла"
    )

    args = parser.parse_args()

    if not args.max and not args.output:
        print("Ошибка! При запуске укажите данные о количестве запрашиваемых "
              "тендеров и название файла для сохранения данных, например: "
              "python main.py --max 10 --output tenders.csv")
    elif not args.max:
        print("Ошибка! При запуске укажите данные о количестве запрашиваемых, "
              "например: python main.py --max 10 --output tenders.csv")
    elif not args.output:
        print("Ошибка! При запуске укажите название файла для сохранения данных, "
              "например: python main.py --max 10 --output tenders.csv")
    else:
        main(count_tenders=args.max, output_filename=args.output)
