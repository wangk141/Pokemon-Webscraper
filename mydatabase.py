import mysql.connector
import glob
import csv


def combine_path(filepath: str) -> list[tuple[str, str, str, str]]:
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
                    rows.append((row[0], row[1], row[2], row[3]))
                counter += 1
    return rows


# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="YOUR PASSWORD",
    database="pokemondb"
)

data = combine_path('C:/Users/KAIXI/PycharmProjects/WebScraper/csvfiles/*.csv')
print(data)
query = "INSERT INTO `pokemondb`(`Name`, `PSA9`, `PSA10`, `SETNAME`) VALUES (%s, %s, %s, %s)"

mymouse = mydb.cursor()
mymouse.executemany(query, data)
mydb.commit()



