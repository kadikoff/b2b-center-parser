import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from src.core.models import db_helper
from src.core.models.model_tenders import Tenders

BASE_URL = "https://www.b2b-center.ru"
BASE_MARKET_URL = "https://www.b2b-center.ru/market/"
TENDERS_LIST: list[Tenders] = []


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

        TENDERS_LIST.append(Tenders(
            tender_id=tender_id,
            organizer=tender_organizer,
            url=tender_full_url,
            description=tender_description,
            end_date=tender_date_of_end
        ))

        if len(TENDERS_LIST) == count_tenders:
            break


async def save_to_db(tenders: list[Tenders]) -> None:
    """Сохраняет данные о тендерах в базу данных"""

    if not tenders:
        print("Нет данных для сохранения.")
        return

    async for session in db_helper.session_dependency():
        session.add_all(tenders)
        await session.commit()

    print(f"\nВ базу данных добавлено тендеров: {len(tenders)}")


async def main(count_tenders: int) -> None:
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

    await save_to_db(TENDERS_LIST)
