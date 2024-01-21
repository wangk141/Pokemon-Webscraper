import mysql
from mysql.connector import ProgrammingError
import mysql.connector
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from DataProcessing import steal_data, combine_path, search_raw


# Web scrape all pokemon sets into csv files
def load_data():
    """
    Initialize the most recent n sets to our database

    n: nth most recent set
    """

    # Headless mode doesn't display the browser
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # for Chrome >= 109
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.pikawiz.com/cards")

    # Simple replace to match fragment identifier in URL
    all_sets = []
    searches = driver.find_elements(By.CLASS_NAME, "set-name")
    for search in searches:
        if search.text.strip() != "":
            all_sets.append(search.text.replace(" ", "-"))

    # Counter to do n sets as without threading it currently takes too long
    # Cannot thread due to fear of DDOSing sites
    print(all_sets)
    a = input("Type [all] if you want to load all sets or [set-name] for a specific set: ")
    if a.lower() == "all":
        for a_set in all_sets:
            url = "https://www.pricecharting.com/console/pokemon-" + a_set
            try:
                steal_data(url, a_set)
            except NoSuchElementException:
                print("missing set: " + a_set)
    elif a in all_sets:
        url = "https://www.pricecharting.com/console/pokemon-" + a
        try:
            steal_data(url, a)
        except NoSuchElementException:
            print("missing set: " + a)
    else:
        print("Must be an existing set or all")
        load_data()


def initialize_db():
    """
    Initialize the database and table if this is the first time accessing database
    """
    a = combine_path('FOLDER FILEPATH/*.csv')
    data = search_raw("tcgplayer.com", a)
    query = "INSERT INTO `pokemon`(`Name`, `PSA9`, `PSA10`, `SETNAME`, `RAW`) VALUES (%s, %s, %s, %s, %s)"
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="YOUR DATABASE PASSWORD",
        database="pokemon"
    )

    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS pokemon")
    mycursor.execute("USE pokemon")
    mycursor.execute("CREATE TABLE IF NOT EXISTS pokemon (Name VARCHAR(255), PSA9 FLOAT, PSA10 FLOAT, "
                     "SETNAME VARCHAR(100), RAW FLOAT)")
    mycursor.executemany(query, data)
    mydb.commit()
