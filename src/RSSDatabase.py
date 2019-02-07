import sqlite3
from exceptions import InvalidParserException, InvalidDatabaseException


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
                raise InvalidDatabaseException(db, 'Something is wrong with your database name.')
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(256) NOT NULL,
                company VARCHAR(256) NOT NULL,
                summary TEXT NOT NULL,
                link TEXT NOT NULL,
                tags TEXT,
                location VARCHAR(256),
                published DATETIME NOT NULL,
                updated DATETIME NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.connection.commit()

    def populate_database(self):
        pass

    def disconnect_database(self, commit=True):
        pass

    def delete_database(self, commit=True):
        pass

    def _dev_set_parser(self, parser):
        self.parser = parser

    def _dev_set_db(self, db):
        self.db = db
