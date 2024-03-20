import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By

BASE_URL = "http://www-cast3m.cea.fr/index.php?page=notices&notice="


def main():
    driver.get("http://www-cast3m.cea.fr/index.php?page=notices")
    tables = driver.find_elements(By.CSS_SELECTOR, "table.tabaffichage")

    # Use the variable in your script
    lang = getLanguage()

    docs: list = []
    for table in tables:
        for row in table.find_elements(By.CSS_SELECTOR, "tr"):
            for cell in row.find_elements(By.TAG_NAME, "td"):
                name: str = cell.text
                if len(name) == 0:
                    continue
                tag = cell.find_element(By.TAG_NAME, "a")
                url: str = tag.get_attribute("href")
                if not (url is None or url.endswith("#debut")):
                    docs.append(
                        {
                            "name": name,
                            "url": url.replace(BASE_URL, ""),
                            "documentation": "",
                        }
                    )

    with open("data.json", "w") as outfile:
        json.dump(docs, outfile)

    with open("data.json", "r") as infile:
        docs = json.load(infile)

    for doc in docs:
        documentation = getDocumentation(f'{BASE_URL}{doc["url"]}')
        doc["documentation"] = documentation

    with open("data.json", "w") as outfile:
        json.dump(docs, outfile)


def getDocumentation(url: str):
    driver.get(url)
    pre = driver.find_element(By.TAG_NAME, "pre")
    return pre.text


def getLanguage() -> str:
    with open("package.json") as f:
        data = json.load(f)
        return data["gibiane-vscode.lange"]["default"]


if __name__ == "__main__":
    CHROMEDRIVER_PATH = "./chromedriver"
    if os.name == "nt":
        CHROMEDRIVER_PATH += ".exe"
    with webdriver.Chrome(CHROMEDRIVER_PATH) as driver:
        main()
