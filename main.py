from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd


def steal_data(url_input: str, set_name: str) -> None:
    """
    Scrapes data off tables provided they are in simple HTML, and places data
    into csv files

    url: str representation of url surrounded with ""
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # for Chrome >= 109
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    searches = driver.find_elements(By.TAG_NAME, "tr")
    name = []
    PSA_9 = []
    PSA_10 = []
    set_n = []
    for search in searches:
        try:
            checker = search.find_element(By.XPATH, "./td[4]").text
            checker2 = search.find_element(By.XPATH, "./td[5]").text
            # This ensures the item has a graded price attached
            if checker != "" or checker2 != "":
                name.append(search.find_element(By.CLASS_NAME, "title").text)
                PSA_9.append(checker[1:])
                PSA_10.append(search.find_element(By.XPATH, "./td[5]").text[1:])
                set_n.append(a_set)
        except:
            print("value omitted")
    if len(name) > 0:
        dictt = pd.DataFrame({'name': name, 'PSA_9': PSA_9, 'PSA_10': PSA_10, 'set_name': set_n})
        dictt.to_csv("C:/Users/KAIXI/PycharmProjects/WebScraper/csvfiles/" + url_input[46:] + ".csv", index=False)
        driver.quit()
    else:
        print("set omitted: " + set_name)


# WE HAVE HEADLESS MODE
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # for Chrome >= 109
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.pikawiz.com/cards")

all_sets = []
searches = driver.find_elements(By.CLASS_NAME, "set-name")
for search in searches:
    if search.text.strip() != "":
        all_sets.append(search.text.replace(" ", "-"))

for a_set in all_sets:
    url = "https://www.pricecharting.com/console/pokemon-" + a_set
    try:
        steal_data(url, a_set)
    except:
        print("missing set: " + a_set)

