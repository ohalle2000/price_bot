import re
import time
from _utils import *
from bs4 import BeautifulSoup
from _secrets import BOT_TOKEN, ADMIN_ID
from typing import List
from urllib.parse import quote
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def extract_links_from_cars_response(html_content: str, base_url: str, target_class: str, max_price: int) -> List[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all("a", class_=target_class)

    links = []
    for element in elements:
        href = element.get("href")
        if href and re.search(r"a\d{10}", href):
            continue

        title = element.find("img").get("title", "").strip()
        atrtributes = (
            element.find("div", class_="hz-Listing-attributes hz-Text hz-Text--bodyRegularStrong").get_text(strip=True)
            if element.find("div", class_="hz-Listing-attributes hz-Text hz-Text--bodyRegularStrong")
            else ""
        )
        description = element.find("p", class_="hz-Listing-description hz-text-paragraph").get_text(strip=True)
        price = element.find("div", class_="hz-Listing-price").get_text(strip=True)

        link = base_url.split("/l")[0] + href if href else f"{base_url}#q:{quote(title)}"

        if "€" in price:
            actual_price = int(price[2:-2].replace(".", ""))
            if actual_price > max_price:
                continue

        links.append(" ".join(part for part in [link, title, atrtributes, description, price] if part))

    return links


def cars_main(
    driver: webdriver.Chrome, urls: List[str], base_url: str, target: str, max_price: int, links: List[str]
) -> List[str]:
    for url in urls:
        try:
            driver.get(url)
            time.sleep(20)
            html_content = driver.page_source

            new_links = extract_links_from_cars_response(html_content, base_url, target, max_price)

            for link in new_links:
                if link not in links:
                    console.print(f"[bold green]New link found![/bold green] {link}")
                    send_telegram_message(
                        bot_token=BOT_TOKEN,
                        admin_id=ADMIN_ID,
                        message=link,
                    )
                    links.append(link)

        except WebDriverException as e:
            console.print(f"[bold red]WebDriver error: {e}[/bold red]")

    # driver.quit()

    return links
