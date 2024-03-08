import re
import time
from _utils import *
from bs4 import BeautifulSoup
from _secrets import BOT_TOKEN, ADMIN_ID
from typing import List
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def extract_links_from_macbook_response(html_content: str, target_class: str) -> List[str]:
    soup = BeautifulSoup(html_content, "html.parser")
    elements = soup.find_all("a", class_=target_class)

    links = []
    for element in elements:
        href = element.get("href")
        if href and re.search(r"a\d{10}", href):
            continue

        link_parts = [
            f"https://www.marktplaats.nl{href}",
            element.find("img").get("title", "").strip(),
            element.find("p", class_="hz-Listing-description hz-text-paragraph").get_text(strip=True),
            element.find("div", class_="hz-Listing-group--price-date-feature").get_text(strip=True),
        ]

        links.append(" ".join(part for part in link_parts if part))

    return links


def macbook_main(driver: webdriver.Chrome, urls: List[str], target: str, links: List[str]) -> List[str]:
    for idx, url in enumerate(urls):
        try:
            driver.get(url)
            time.sleep(20)
            html_content = driver.page_source

            # with open(f"./macbook{idx}.html", "w") as file:
            #     # use soup to pretify the html
            #     soup = BeautifulSoup(html_content, "html.parser")
            #     file.write(soup.prettify())

            new_links = extract_links_from_macbook_response(html_content, target)

            for link in new_links:
                if link not in links:
                    console.print(f"[bold green]New link found![/bold green] {link}")
                    # if (
                    #     any(
                    #         keyword in link.lower()
                    #         for keyword in ["m1", "m2", "2021", "2023"]
                    #     )
                    #     and all(
                    #         year not in link
                    #         for year in [str(y) for y in range(2012, 2021)]
                    #     )
                    #     and "pro 13" not in link.lower()
                    # ):
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
