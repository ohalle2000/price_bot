import time
from _utils import *
from _macbook import macbook_main
from selenium import webdriver

SLEEP_TIME = 5 * 60


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
)
browser = webdriver.Chrome(options=options)


# use without cookies
def main():
    mac_book_config = get_website_config("macbook-marketplaats")
    macbook_base_url = mac_book_config["url"]
    macbook_target = mac_book_config["target"]
    macbook_urls = expand_link_with_pages(macbook_base_url)
    while True:
        with open("./macbook-links.txt", "r") as file:
            links = file.read().splitlines()

        macbook_links = macbook_main(browser, macbook_urls, macbook_target, links)

        # Sort links alphabetically
        macbook_links.sort(key=custom_sort)

        # Limit to the last 50 links
        # existing_links = existing_links[-50:]

        with open("./macbook-links.txt", "w") as file:
            file.write("\n".join(macbook_links))

        console.print("[bold blue]Sleeping...[/bold blue]")
        time.sleep(SLEEP_TIME)

    browser.quit()


if __name__ == "__main__":
    main()
