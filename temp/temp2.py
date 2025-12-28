import requests
from bs4 import BeautifulSoup
from typing import List, Set

WIKI_URL = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"

def get_unique_splashdata_passwords(timeout: float = 20.0) -> List[str]:
    """
    Возвращает отсортированный список уникальных паролей,
    собранных из секции Top 25 most common passwords by year according to SplashData
    на странице Википедии.
    Требует: pip install requests beautifulsoup4
    """
    resp = requests.get(WIKI_URL, timeout=timeout, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # Находим заголовок секции
    header = None
    for h in soup.find_all(["h2", "h3", "h4"]):
        span = h.find("span", class_="mw-headline")
        if span and "Top 25 most common passwords by year according to SplashData" in span.get_text():
            header = h
            break
    if header is None:
        raise RuntimeError("Секция SplashData не найдена на странице")

    passwords: Set[str] = set()

    # Проходим по узлам секции до следующего заголовка того же уровня
    node = header.next_sibling
    while node:
        if getattr(node, "name", None) == "table":
            # собираем все строки таблицы
            rows = []
            for tr in node.find_all("tr"):
                cells = [cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])]
                if cells:
                    rows.append(cells)
            if not rows:
                node = node.next_sibling
                continue

            # Попытка: если первая строка содержит года — используем её как заголовок колонок
            first_row = rows[0]
            is_year_header = any(cell.startswith("20") or cell.isdigit() for cell in first_row)
            if is_year_header:
                # Для каждой колонки (год) собираем до 25 значений из следующих строк
                for col_idx in range(len(first_row)):
                    for r in rows[1:26]:
                        if col_idx < len(r):
                            v = r[col_idx].strip()
                            if v:
                                passwords.add(v)
            else:
                # Иначе предположим формат Rank | 2011 | 2012 | ...
                # Найдём строку заголовка, содержащую года
                header_row = None
                for r in rows:
                    if any(cell.startswith("20") or cell.isdigit() for cell in r):
                        header_row = r
                        break
                if header_row:
                    start_idx = 0
                    if header_row and (header_row[0].lower().startswith("rank") or header_row[0].lower() == "rank"):
                        start_idx = 1
                    # индекс колонок годов в матрице соответствует позиции в header_row
                    # соберём для каждой из этих колонок значения из строк ниже
                    for col_offset, year in enumerate(header_row[start_idx:], start=start_idx):
                        for r in rows:
                            # пропускаем строку заголовка
                            if r is header_row:
                                continue
                            if col_offset < len(r):
                                v = r[col_offset].strip()
                                if v:
                                    passwords.add(v)
                        else:
                            # как крайний случай: собираем все ячейки таблицы, кроме ранжировочных чисел
                            for r in rows[1:]:
                                for cell in r:
                                    # пропускаем чисто числовые значения ранга
                                    if cell and not cell.isdigit():
                                        passwords.add(cell)
                        if getattr(node, "name", None) in ["h2", "h3", "h4"]:
                            break
                        node = node.next_sibling

                        # Очистка: убрать возможные заголовки/метки, оставить уникальные пароли
                        cleaned = set()
                        for p in passwords:
                            # Иногда в ячейках могут быть номера ранга или пометки через пробелы/скобки — оставим строку как есть, но уберём пустые
                            s = p.strip()
                            if s:
                                cleaned.add(s)

                        return sorted(cleaned)

# Пример использования
if __name__ == "__main__":
    pw_list = get_unique_splashdata_passwords()
    print(f"Всего уникальных паролей: {len(pw_list)}")
    print(pw_list[:50])
