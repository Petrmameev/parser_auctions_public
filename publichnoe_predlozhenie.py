import csv
import datetime
import json
import os
import time

import lxml
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()
current_data = datetime.date.today()

def extract_auction_data(item):
    image = item.find("img")
    if image is not None:
        image_file = image.get("src")
        if not image_file.startswith("https"):
            image_file = "https://m-ets.ru/" + image_file
    else:
        image_file = None
    title = item.find("div", class_="comp-title")
    title_text = title.text
    item_text = item.text
    item_href = "https://m-ets.ru/" + item.get("href")
    deadline = item.find("div", class_="comp-dates")
    deadline_text = deadline.text
    start_price = item.find("div", class_="price current")
    start_price_text = start_price.text
    subtext = item.find_all("div", class_="subtext")
    subtext_list = []
    for single_text in subtext:
        subtext_text = single_text.text
        subtext_list.append(subtext_text)
    if not item.find("div", class_="price step"):
        step_or_min_price = item.find("div", class_="price min")
    else:
        step_or_min_price = item.find("div", class_="price step")
    step_or_min_price_text = (
        step_or_min_price.text if step_or_min_price else None
    )
    auction_dict = {
        "Url": item_href,
        "Title": title_text,
        "Image": image_file,
        "Subtext_1": subtext_list[0],
        "Start_price": start_price_text,
        "Subtext_2": subtext_list[1] if len(subtext_list) > 1 else None,
        "Step_or_min_price": step_or_min_price_text,
        "Deadline": deadline_text,
    }
    hernya = ["\xa0", "\n"]
    cleaned_auction_dict = {
        k: (
            v.replace(hernya[0], " ").replace(hernya[1], " ")
            if isinstance(v, str)
            else v
        )
        for k, v in auction_dict.items()
    }
    cleaned_auction_dict = {
        k: v for k, v in cleaned_auction_dict.items() if v is not None
    }
    return cleaned_auction_dict


def fetch_pub_pred_data(url, geo, category):
    s = requests.Session()
    page_number = 1
    all_auctions = []

    while True:
        page_url = f"{url}&page={page_number}"
        response = requests.get(url=page_url, headers={"user-agent": f"{ua.random}"}, verify=False)

        # Сохранение HTML-страницы
        with open(
                f"Data_files/{geo}/publichnoe_predlozhenie/data_html/{category}_page_{page_number}.html",
                "w",
                encoding="utf-8",
        ) as file:
            file.write(response.text)

        # Парсинг HTML-страницы
        with open(
                f"Data_files/{geo}/publichnoe_predlozhenie/data_html/{category}_page_{page_number}.html",
                encoding="utf-8",
        ) as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        if soup.find("div", class_="empty-search"):
            print("По Вашему запросу ничего не найдено!")
            return

        all_auctions_on_page = soup.find("div", class_="soc_body list").find_all(
            "a", class_="search-comp-item"
        )

        for item in all_auctions_on_page:
            cleaned_auction_dict = extract_auction_data(item)
            all_auctions.append(cleaned_auction_dict)

        print(all_auctions)
        page_number += 1

        # Сохранение данных в JSON
        with open(
                f"Data_files/{geo}/publichnoe_predlozhenie/data_json/{category}.json",
                "w",
                encoding="utf-8",
        ) as file:
            json.dump(
                all_auctions,
                file,
                ensure_ascii=False,
                indent=4,
            )

    return all_auctions

