from mainCommands import load_data, initialize_db
from SQLcommands import clean_data_set, should_invest
"""
Usage:

load_data: Web Scrapes specific set data
initialize_db: Initializes db in mySQL
clean_data_set: Removes values from data where Raw card price could not be found
should_invest: Returns list of cards you should invest in to grade 

"""
if __name__ == '__main__':
    load_data()
    initialize_db()
    clean_data_set()
    should_invest()

