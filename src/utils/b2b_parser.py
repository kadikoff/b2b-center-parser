import csv
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

BASE_URL = "https://www.b2b-center.ru"
BASE_MARKET_URL = "https://www.b2b-center.ru/market/"
TENDERS_LIST = []


def fetch_page_html(page_url: str) -> Optional[str]:
    """Выполнение запроса"""

    try:
        response = requests.get(url=page_url)
    except Exception as exc:
        print(f"Ошибка при запросе {page_url}: {exc}")
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
) -> None:
    """Извлечение данных тендера из html и добавление во временное хранилище"""

    for tender in tenders_data:
        tender_td_blocks = tender.select("td")

        tender_organizer = tender_td_blocks[1].text
        tender_url = tender_td_blocks[0].find("a").get("href")
        tender_full_url = BASE_URL + tender_url
        tender_id = re.search(r"/tender[s]?-(\d+)/", tender_url).group(1)
        tender_description = tender.find(
            "div", class_=["search-results-title-desc"]
        ).text
        tender_date_of_end = tender_td_blocks[3].text

        TENDERS_LIST.append({
            "№": tender_id,
            "Организатор": tender_organizer,
            "Ссылка": tender_full_url,
            "Описание": tender_description,
            "Дата окончания": tender_date_of_end
        })

        if len(TENDERS_LIST) == count_tenders:
            break


def save_to_csv(tenders: list[dict], filename: str) -> None:
    """Запись данных о тендерах в .csv формат"""

    if not tenders:
        print("Нет данных для сохранения.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=tenders[0].keys())
        writer.writeheader()
        writer.writerows(tenders)

    print(f"\nCSV сохранён: {filename}, количество тендеров: {len(TENDERS_LIST)}")


def main(count_tenders: int, output_filename: str) -> None:
    print(f"Запуск парсера, количество тендеров: {count_tenders}\n")

    offset = 0
    limit = 20

    while len(TENDERS_LIST) < count_tenders:
        current_page_url = f"{BASE_MARKET_URL}?from={offset}"
        print(f"Парсинг страницы: {current_page_url}")

        html: Optional[str] = fetch_page_html(current_page_url)
        if not html:
            print("Не удалось получить html!")
            return

        html_tenders: list[Tag] = parse_tenders(html)
        if not html_tenders:
            print("Нет данных о тендерах!")

        extract_tenders_data(html_tenders, count_tenders)

        offset += limit

    save_to_csv(TENDERS_LIST, output_filename)
