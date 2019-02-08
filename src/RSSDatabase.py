import sqlite3
from exceptions import InvalidParserException, InvalidDatabaseException
from dateutil import parser
from functools import reduce


class RSSDatabase:
    def __init__(self, parser=None, db=None, _debug=False):
        if not _debug:
            if self._is_valid_parser(parser):
                self.parser = parser
            else:
                raise InvalidParserException(parser, 'Something is wrong with your parser.')

            if self._is_valid_db(db):
                self.db = db
            else:
                raise InvalidDatabaseException(db, 'Something is wrong with your database name: ' + str(db))
        else:
            self.parser = None
            self.db = None

        self.connection = None
        self.cursor = None

    def _is_valid_parser(self, parser):
        if parser is None:
            return False
        else:
            return parser.is_valid_parser()

    def _is_valid_db(self, db):
        if db is None:
            return False
        else:
            db_split = db.split('.')
            if len(db_split) < 2:
                return False
            db_ext = db_split[len(db_split) - 1]
            if db_ext in ['db', 'sqlite', 'sqlite3']:
                return True
            else:
                return False

    def create_database(self):
        """ Sets up database connection and cursor, and adds the 'entry' table """

        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE entry (
                id INTEGER PRIMARY KEY,
                title VARCHAR(256) NOT NULL,
                company VARCHAR(256) NOT NULL,
                summary TEXT NOT NULL,
                link TEXT NOT NULL,
                tags TEXT,
                location VARCHAR(256),
                published DATETIME NOT NULL,
                timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def populate_database(self):
        try:
            entry = self.parser.entry()
            while True:
                current_entry = next(entry)
                self.process_entry(current_entry)
        except StopIteration:
            self.connection.commit()

    def process_entry(self, entry):
        entry_id = entry['id']
        entry_title = entry['title']
        entry_company = entry['author']
        entry_summary = entry['summary']
        entry_link = entry['link']

        if 'tags' in entry:
            entry_tags = reduce(lambda x, y: x + y['term'] + ',', entry['tags'], '')
        else:
            entry_tags = None
        if 'location' in entry:
            entry_location = entry['location']
        else:
            entry_location = 'Remote'

        entry_datetime = parser.parse(entry['published'])
        entry_published = 'DATETIME(%s-%s-%s %s:%s:%s)' % (entry_datetime.year, entry_datetime.month,
                                                           entry_datetime.day, entry_datetime.hour, entry_datetime.minute, entry_datetime.second)

        self.cursor.execute(
            """INSERT INTO entry (id, title, company, summary, link, tags, location, published) VALUES (?,?,?,?,?,?,?,?)""",
            (entry_id, entry_title, entry_company, entry_summary, entry_link, entry_tags, entry_location, entry_published))

    def connect_database(self, db):
        if self._is_valid_db(db):
            self.db = db
            self.connection = sqlite3.connect(db)
            self.cursor = self.connection.cursor()
        else:
            raise InvalidDatabaseException(db, 'Something is wrong with your database name: ' + str(db))

    def disconnect_database(self, commit=True):
        if commit:
            self.connection.commit()
            self.connection.close()
        else:
            self.connection.close()

    def _dev_set_parser(self, parser):
        self.parser = parser

    def _dev_set_db(self, db):
        self.db = db
