import sqlite3
import os
from exceptions import InvalidParserException, InvalidDatabaseException, DatabaseAlreadyExistsException
from dateutil import parser
from functools import reduce


class RSSDatabase:
    def __init__(self, parser=None, db=None, _debug=False):
        """
        Constructor for RSSDatabase class
            parser (RSSParser.RSSParser, optional): Defaults to None. parser to read job entries from
            db (str, optional): Defaults to None. Database name to use
            _debug (bool, optional): Defaults to False. Used exclusively for testing.

        Raises:
            InvalidParserException: if the parser is not of the right type and _debug is set to false
            InvalidDatabaseException: if the database name is incorrect and _debug is set to false
        """

        if not _debug:
            if self._is_valid_parser(parser):
                self.parser = parser
            else:
                raise InvalidParserException(parser, 'Something is wrong with your parser.')

            if self._is_valid_db(db):
                if not self._db_taken(db):
                    self.db = db
                else:
                    raise DatabaseAlreadyExistsException(db, 'The database name is already taken.')
            else:
                raise InvalidDatabaseException(db, 'Something is wrong with your database name: ' + str(db))
        else:
            self.parser = None
            self.db = None

        self.connection = None
        self.cursor = None

    def _is_valid_parser(self, parser):
        """
        Determines whether the provided parser is valid

        Args:
            parser (RSSParser.RSSParser): parser to test validity

        Returns:
            bool: True if parser is valid, false otherwise
        """

        if parser is None:
            return False
        else:
            return parser.is_valid_parser()

    def _is_valid_db(self, db):
        """
        Determines whether the provided database name is valid

        Args:
            db (str): string to test validity of

        Raises:
            DatabaseAlreadyExistsException: If the provided name already exists in the file system

        Returns:
            bool: True if db has valid name, false otherwise
        """

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

    def _db_taken(self, db):
        """
        Determines whether the provided database name is already taken

        Args:
            db (str): String to test if it exists

        Returns:
            bool: True if db doesn't already exist, false otherwise
        """

        if os.path.isfile(db):
            return True
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
        """ Populates the database with the entries from the provided parser. """

        try:
            entry = self.parser.entry()
            while True:
                current_entry = next(entry)
                self.process_entry(current_entry)
        except StopIteration:
            self.connection.commit()

    def process_entry(self, entry):
        """
        Add an entry dictionary to a SQLite database

        Args:
            entry (dict): Dictionary containing information on job entry
        """
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
        """
        Connects to a database with the given name

        Args:
            db (str): database name to connect to

        Raises:
            InvalidDatabaseException: If db has an invalid name
        """

        if self._is_valid_db(db):
            self.db = db
            self.connection = sqlite3.connect(db)
            self.cursor = self.connection.cursor()
        else:
            raise InvalidDatabaseException(db, 'Something is wrong with your database name: ' + str(db))

    def disconnect_database(self, commit=True):
        """
        Disconnects from a database and may commit changes.

        Args:
            commit (bool, optional): Defaults to True. If true, commits all changes, else changes are ignore
        """

        if commit:
            self.connection.commit()
            self.connection.close()
        else:
            self.connection.close()

    def _dev_set_parser(self, parser):
        self.parser = parser

    def _dev_set_db(self, db):
        self.db = db
