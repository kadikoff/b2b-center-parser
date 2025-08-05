import asyncio

import argparse

from src.utils.b2b_parser import main


if __name__ == "__main__":
    # Запуск парсера производится с помощью команды python main.py --max 10

    parser = argparse.ArgumentParser(
        description="Парсер тендеров b2b-center.ru"
    )
    parser.add_argument(
        "--max", type=int, help="Максимальное количество тендеров для парсинга"
    )

    args = parser.parse_args()
    if not args.max:
        print("Ошибка! При запуске укажите данные о количестве запрашиваемых тендеров, "
              "например: python main.py --max 10")
    else:
        asyncio.run(main(count_tenders=args.max))
