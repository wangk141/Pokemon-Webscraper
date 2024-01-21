import mysql
from mysql.connector import ProgrammingError


def should_invest():
    """
    Returns pokemon cards where if you grade them, you can earn money, and break even in the worst case
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="YOUR DATABASE PASSWORD",
        database="pokemon"
    )
    mycursor = mydb.cursor()
    query = "SELECT * FROM pokemon WHERE PSA9 >= RAW + 24 and PSA10 >= RAW * 2 + 24"
    mycursor.execute(query)

    result = mycursor.fetchall()
    for res in result:
        print(res)


def clean_data_set():
    """
    Cleans data when errors are returned
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="YOUR DATABASE PASSWORD",
        database="pokemon"
    )
    mycursor = mydb.cursor()
    query = "DELETE FROM pokemon WHERE raw = 0"
    mycursor.execute(query)
    mydb.commit()

