import sqlite3 as sql
import os
import sys
from dateutil import parser

sys.path.append('src')
from RSSDatabase import RSSDatabase
from RSSParser import RSSParser

PARSE_URL = 'https://stackoverflow.com/jobs/feed'

class DBInterface:
    def __init__(self, db):
        self.db = db
        self.connection = sql.connect(self.db)
        self.cursor = self.connection.cursor()
        self.all_entries = self.get_all_entries()

    def purge_database(self):
        self.connection.close()
        if os.path.isfile('db.sqlite'):
            os.remove('db.sqlite')
        parser = RSSParser(PARSE_URL)
        rss_db = RSSDatabase(parser=parser, db=self.db)
        rss_db.create_database()
        rss_db.populate_database()
        rss_db.disconnect_database()
        self.connection = sql.connect(self.db)
        self.cursor = self.connection.cursor()
        self.all_entries = self.get_all_entries()

    def concat_database(self):
        max_date_query = self.cursor.execute("SELECT MAX(published) FROM entry;").fetchone()
        max_date = parser.parse(max_date_query[0])
        parser = RSSParser(PARSE_URL)
        rss_db = RSSDatabase(parser=parser, db=self.db)
        rss_db.connect_database(self.db)
        entry = parser.entry()
        try:
            while True:
                current_entry = next(entry)
                if current_entry['published'] > max_date:
                    rss_db.process_entry(current_entry)
        except StopIteration:
            self.connection.commit()
            rss_db.disconnect_database()
        self.connection = sql.connect(self.db)
        self.cursor = self.connection.cursor()
        self.all_entries = self.get_all_entries()


    def get_all_entries(self):
        return self.cursor.execute("SELECT * FROM entry;").fetchall()

    def get_single_entry(self, id):
        return self.cursor.execute(f"SELECT * FROM entry WHERE id = {id}").fetchone()

    def filter_entries(self, filter_dict, and_results):
        filter_string = "WHERE "
        first_item = True

        if filter_dict['location'] == False:
            if not first_item:
                if and_results:
                    filter_string += 'AND '
                else:
                    filter_string += 'OR '
            else:
                first_item = False
            filter_string += '(city IS NOT NULL AND state IS NOT NULL) '

        if filter_dict['state'] != '':
            state_string = filter_dict['state']
            if not first_item:
                if and_results:
                    filter_string += 'AND '
                else:
                    filter_string += 'OR '
            else:
                first_item = False
            filter_string += f'LOWER(state) = LOWER("{state_string}") '

        if filter_dict['city'] != '':
            city_string = filter_dict['city']
            if not first_item:
                if and_results:
                    filter_string += 'AND '
                else:
                    filter_string += 'OR '
            else:
                first_item = False
            filter_string += f'LOWER(city) = LOWER("{city_string}") '

        if filter_dict['tags'] != '':
            for tag in filter_dict['tags'].split(','):
                if not first_item:
                    if and_results:
                        filter_string += 'AND '
                    else:
                        filter_string += 'OR '
                else:
                    first_item = False
                filter_string += f'LOWER(tags) LIKE "%{tag}%" '

        if filter_dict['title'] != '':
            title_string = filter_dict['title']
            if not first_item:
                if and_results:
                    filter_string += 'AND '
                else:
                    filter_string += 'OR '
            else:
                first_item = False
            filter_string += f'LOWER(title) LIKE "%{title_string}%" '

        if filter_dict['company'] != '':
            company_string = filter_dict['company']
            if not first_item:
                if and_results:
                    filter_string += 'AND '
                else:
                    filter_string += 'OR '
            else:
                first_item = False
            filter_string += f'LOWER(company) = LOWER("{company_string}") '

        # if filter_dict['remote']

        filter_string += ";"

        if filter_string == 'WHERE ;':
            filter_string = ';'
        print(and_results)
        print(filter_string)
        self.all_entries = self.cursor.execute('SELECT * FROM entry ' + filter_string).fetchall()
