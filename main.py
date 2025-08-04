import csv
import re
from typing import Optional

import argparse
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = "https://www.b2b-center.ru"
BASE_MARKET_URL = "https://www.b2b-center.ru/market/"
COUNTER = 0


def fetch_page_html(current_url: str) -> Optional[str]:
    """Выполнение запроса"""

    try:
        response = requests.get(url=current_url)
    except Exception as exc:
        print(f"Ошибка при запросе {current_url}: {exc}")
        return None

    return response.text


def parse_tenders(html_data: str) -> list[Tag]:
    """Извлечение основного блока html со всеми тендерами на странице"""

    soup = BeautifulSoup(html_data, "lxml")
    common_class = soup.find(
        "table", class_=["table table-hover table-filled search-results"]
    )
    rows = common_class.find("tbody").find_all("tr")

    return rows


def extract_tenders_data(
        tenders_data: list[Tag], count_tenders: int
) -> list[dict]:
    """Извлечение данных тендера из html и добавление во временное хранилище"""

    global COUNTER
    tenders_list = []

    for tender in tenders_data:
        COUNTER += 1
        tender_td_blocks = tender.select("td")

        tender_organizer = tender_td_blocks[1].text
        tender_url = tender_td_blocks[0].find("a").get("href")
        tender_full_url = BASE_URL + tender_url
        tender_id = re.search(r"/tender[s]?-(\d+)/", tender_url).group(1)
        tender_description = tender.find(
            "div", class_=["search-results-title-desc"]
        ).text
        tender_date_of_end = tender_td_blocks[3].text

        tenders_list.append({
            "№": tender_id,
            "Организатор": tender_organizer,
            "Ссылка": tender_full_url,
            "Описание": tender_description,
            "Дата окончания": tender_date_of_end
        })

        if COUNTER == count_tenders:
            break

    return tenders_list


def save_to_csv(tenders: list[dict], filename: str) -> None:
    """Запись данных о тендерах в .csv формат"""

    if not tenders:
        print("Нет данных для сохранения.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=tenders[0].keys())
        writer.writeheader()
        writer.writerows(tenders)

    print(f"CSV сохранён: {filename}")


def main(count_tenders: int, output_filename: str) -> None:
    html: Optional[str] = fetch_page_html(BASE_MARKET_URL)
    if not html:
        print("Не удалось получить html!")
        return

    html_tenders: list[Tag] = parse_tenders(html)
    if not html_tenders:
        print("Нет данных о тендерах!")

    tenders_data: list[dict] = extract_tenders_data(
        html_tenders, count_tenders
    )
    save_to_csv(tenders_data, output_filename)


if __name__ == "__main__":
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
