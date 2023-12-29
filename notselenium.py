from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import pandas as pd


def steal_data(url: str) -> None:
    """
    Scrapes data off tables provided they are in simple HTML, and places data
    into csv files

    url: str representation of url surrounded with ""
    """
    driver = webdriver.Chrome()
    driver.get(url)

    searches = driver.find_elements(By.TAG_NAME, "tr")
    name = []
    PSA_9 = []
    PSA_10 = []
    for search in searches:
        try:
            name.append(search.find_element(By.CLASS_NAME, "title").text)
            PSA_9.append(search.find_element(By.XPATH, "./td[4]").text)
            PSA_10.append(search.find_element(By.XPATH, "./td[5]").text)
        except NoSuchElementException as e:
            print("value omitted")

    dict = pd.DataFrame({'name': name, 'PSA_9': PSA_9, 'PSA_10': PSA_10})
    dict.to_csv(url[46:] + ".csv", index=False)
    driver.quit()


driver = webdriver.Chrome()
driver.get("https://www.pikawiz.com/cards")

all_sets = []
searches = driver.find_elements(By.CLASS_NAME, "set-name")
for search in searches:
    if search.text.strip() != "":
        all_sets.append(search.text.replace(" ", "-"))

for a_set in all_sets:
    url = "https://www.pricecharting.com/console/pokemon-" + a_set
    try:
        steal_data(url)
    except:
        print("missing set: " + a_set)


