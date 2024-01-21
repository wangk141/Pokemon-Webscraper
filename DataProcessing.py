from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import NoSuchElementException, TimeoutException
import glob
import csv


def steal_data(url_input: str, set_name: str) -> None:
    """
    Scrapes data from tables on target, and places data
    into csv files

    url: str representation of url
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # for Chrome >= 109
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_input)

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
                set_n.append(set_name)
        except NoSuchElementException:
            print("value omitted")
    if len(name) > 0:
        dictt = pd.DataFrame({'name': name, 'PSA_9': PSA_9, 'PSA_10': PSA_10, 'set_name': set_n})
        dictt.to_csv("FOLDER FILEPATH" + url_input[46:] + ".csv", index=False)
        driver.quit()
    else:
        print("set omitted: " + set_name)


def search_raw(input_url: str, lst: list[list[str, str, str, str]]) -> list[list[str, str, str, str, str]]:
    """
    Returns the raw price of cards for comparisons
    """

    for line in lst:
        # for each name in list, search card name on google, look for tcgplayer link
        # click tcgplayer link, wait for resulting price
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # for Chrome >= 109
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.ca/")
        search = driver.find_element(By.NAME, "q")
        search.send_keys(line[0])
        search.send_keys(Keys.RETURN)

        try:
            # Wait for the search results container to be present in the DOM
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'search'))
            )

            # Assuming you are looking for a link to a specific website in the search results
            # Replace 'Your Target Website' with the actual name or URL of the website you are waiting for
            target_website_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, input_url))
            )

            # Click on the link to the target website
            target_website_link.click()
            find = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price"))
            )
            line.append(find.text[1:])
            print(line)
        except TimeoutException:
            print("some error occurred")
            line.append('0.00')

        finally:
            driver.quit()
    return lst


def combine_path(filepath: str) -> list[list[str, str, str, str]]:
    """
    Combines multiple csv files into one large csv file to make it easier to load into SQL
    database

    filepath: string representation of filepath
    """
    rows = []
    # Recursively searches all elements that match
    for name in glob.glob(filepath):
        with open(name, newline='') as csvfile:
            # Can change delimiter here to spaces or whatever, spell it correctly
            csvreader = csv.reader(csvfile, delimiter=',')
            counter = 0
            for row in csvreader:
                if counter == 0:
                    pass
                else:
                    rows.append([row[0], row[1], row[2], row[3]])
                counter += 1
    return rows
