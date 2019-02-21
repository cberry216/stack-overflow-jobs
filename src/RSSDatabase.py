import sqlite3
import os
import RSSParser as rssp
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
            parser (object): parser to test validity

        Returns:
            bool: True if parser is valid, false otherwise
        """

        if type(parser) is not rssp.RSSParser:
            return False
        else:
            return parser.is_valid_parser()

    def _is_valid_db(self, db):
        """
        Determines whether the provided database name is valid

        Args:
            db (str): string to test validity of

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
                city VARCHAR(256),
                state VARCHAR(256),
                allows_remote INT NOT NULL,
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
            # only commit once all entries are processed
            self.connection.commit()

    def process_entry(self, entry):
        """
        Add an entry dictionary to the SQLite database

        Args:
            entry (dict): Dictionary containing information on job entry
        """
        entry_id = entry['id']
        entry_title = entry['title']
        entry_company = entry['author']
        entry_summary = entry['summary']
        entry_link = entry['link']

        if 'tags' in entry:
            # convert dict of terms to comma-seperated string of terms
            entry_tags = reduce(lambda x, y: x + y['term'] + ',', entry['tags'], '')
        else:
            entry_tags = None
        if 'location' in entry:
            entry_location_city_state = entry['location'].split(',')
            entry_city = entry_location_city_state[0].strip()
            entry_state = entry_location_city_state[1].strip()
        else:
            entry_city = None
            entry_state = None

        entry_allows_remote = 1 if self.title_has_remote_option(entry_title) else 0

        entry_published = parser.parse(entry['published'])

        self.cursor.execute(
            """INSERT INTO entry (id, title, company, summary, link, tags, city, state, allows_remote, published) VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (entry_id, entry_title, entry_company, entry_summary, entry_link, entry_tags, entry_city, entry_state, entry_allows_remote, entry_published))

    def title_has_remote_option(self, title):
        """
        Determines whether the given title contains the option to work remotely.    

        Args:
            title (str): title string that may contain remote
        """
        REMOTE_OFFSET = -15  # This is the slice which will be (allows remote) or gibberishSE
        return title[REMOTE_OFFSET:] == '(allows remote)'

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
            commit (bool, optional): Defaults to True. If true, commits all changes, else changes are ignored
        """

        if commit:
            self.connection.commit()
        self.connection.close()

    def _dev_set_parser(self, parser):
        self.parser = parser

    def _dev_set_db(self, db):
        self.db = db
