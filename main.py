import mysql.connector
from selenium.webdriver.chrome.options import Options
import pandas as pd
import glob
import csv

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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


def combine_path(filepath: str) -> list[list[str, str, str, str]]:
    """
    Combines multiple csv files into one large csv file to make it easier to load into sql
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


def search_raw(input_url: str, lst: list[list[str, str, str, str]]) -> list[list[str, str, str, str, str]]:
    """

    :param input_url:
    :param lst:
    :return:
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
        except:
            print("some error occurred")
            line.append('0.00')
        finally:
            driver.quit()
    return lst


# Web scrape all pokemon sets into csv files
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

myurl = 'C:/Users/KAIXI/PycharmProjects/WebScraper/csvfiles/*.csv'
search_raw("tcgplayer.com", combine_path(myurl))

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="readinghorsecrackspizza",
    database="pokemondb"
)

a = combine_path('C:/Users/KAIXI/PycharmProjects/WebScraper/csvfiles/*.csv')
data = search_raw("tcgplayer.com", a)
print(data)
query = "INSERT INTO `pokemondb`(`Name`, `PSA9`, `PSA10`, `SETNAME`, `RAW`) VALUES (%s, %s, %s, %s, %s)"

mymouse = mydb.cursor()
mymouse.executemany(query, data)
mydb.commit()
