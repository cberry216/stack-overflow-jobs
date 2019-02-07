import pytest
import sys
sys.path.append('src')


def test_rss_database_debug_mode():
    import RSSDatabase as rssd

    db = rssd.RSSDatabase(_debug=True)

    assert db.parser is None
    assert db.db is None
    assert db.connection is None
    assert db.cursor is None


def test__dev_set_parser():
    import RSSDatabase as rssd
    import RSSParser as rssp
    from exceptions import InvalidParserException, InvalidDatabaseException

    db = rssd.RSSDatabase(_debug=True)

    str_parser = 'this is not a parser'
    db._dev_set_parser(str_parser)
    assert db.parser == str_parser

    num_parser = 123456
    db._dev_set_parser(num_parser)
    assert db.parser == 123456

    parser1 = rssp.RSSParser('')
    db._dev_set_parser(parser1)
    assert db.parser.url == parser1.url
    assert db.parser == parser1


def test__dev_set_db():
    import RSSDatabase as rssd
    import RSSParser as rssp
    from exceptions import InvalidParserException, InvalidDatabaseException

    db = rssd.RSSDatabase(_debug=True)

    str_parser = 'this is not a parser'
    db._dev_set_db(str_parser)
    assert db.db == str_parser

    num_parser = 123456
    db._dev_set_db(num_parser)
    assert db.db == 123456

    parser1 = rssp.RSSParser('')
    db._dev_set_db(parser1)
    assert db.db == parser1


def test__is_valid_parser():
    import RSSDatabase as rssd
    import RSSParser as rssp

    db = rssd.RSSDatabase(_debug=True)

    url = 'https://stackoverflow.com/jobs/feed'
    parser = rssp.RSSParser(url)

    url2 = 'wont_work'
    parser2 = rssp.RSSParser(url2)

    db._dev_set_parser(parser)
    assert db._is_valid_parser(db.parser)

    db._dev_set_parser(parser2)
    assert not db._is_valid_parser(db.parser)


def test__is_valid_db():
    import RSSDatabase as rssd

    db = rssd.RSSDatabase(_debug=True)
    db_name1 = 'db.sqlite'
    db_name2 = 'ajsdasjhgakjsdf.sqlite3'
    db_name3 = 'random.db'
    db_name4 = 'invalid_database'

    db._dev_set_db(db_name1)
    assert db._is_valid_db(db.db)

    db._dev_set_db(db_name2)
    assert db._is_valid_db(db.db)

    db._dev_set_db(db_name3)
    assert db._is_valid_db(db.db)

    db._dev_set_db(db_name4)
    assert not db._is_valid_db(db.db)


def test_rss_database():
    import RSSDatabase as rssd
    import RSSParser as rssp
    from exceptions import InvalidParserException, InvalidDatabaseException

    with pytest.raises(InvalidParserException):
        db = rssd.RSSDatabase()

    parser = rssp.RSSParser('https://stackoverflow.com/jobs/feed')
    with pytest.raises(InvalidDatabaseException):
        db = rssd.RSSDatabase(parser)

    db_name2 = 'cool_database.sqlite'
    db2 = rssd.RSSDatabase(parser=parser, db=db_name2)

    assert db2.parser == parser
    assert db2.db == db_name2
    assert db2.connection is None
    assert db2.cursor is None


def test_create_database():
    import RSSDatabase as rssd
    import RSSParser as rssp
    import sqlite3
    import os

    parser = rssp.RSSParser('https://stackoverflow.com/jobs/feed')
    db_name = 'entries.sqlite'

    db = rssd.RSSDatabase(parser=parser, db=db_name)
    db.create_database()

    assert os.path.isfile(db_name)

    assert type(db.connection) == sqlite3.Connection
    assert type(db.cursor) == sqlite3.Cursor

    test_cursor = db.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    results = test_cursor.fetchall()
    assert len(results) == 2  # entry table + auto increment table from sqlite
    assert results[0][0] == 'entry'

    os.remove(db_name)
    assert not os.path.isfile(db_name)


def test_populate_database():
    import RSSDatabase as rssd
    import RSSParser as rssp
    import sqlite3
    import os

    parser = rssp.RSSParser('https://stackoverflow.com/jobs/feed')

    entries = [
        {   # Both tags and location present
            'id': 1,
            'title': 'job 1',
            'author': 'company 1',
            'summary': 'summary 1',
            'link': 'link 1',
            'tags': [
                {'term': 'term1-1'},
                {'term': 'term1-2'},
                {'term': 'term1-3'}
            ],
            'location': 'location 1',
            'published': 'Wed, 06 Feb 2019 12:36:40 Z',
            'updated': '2019-02-06T12:36:40Z'
        },
        {   # Location present, tags absent
            'id': 2,
            'title': 'job 2',
            'author': 'company 2',
            'summary': 'summary 2',
            'link': 'link 2',
            'location': 'location 2',
            'published': 'Wed, 06 Feb 2019 12:36:40 Z',
            'updated': '2019-02-06T12:36:40Z'
        },
        {   # Tags present, location absent
            'id': 3,
            'title': 'job 3',
            'author': 'company 3',
            'summary': 'summary 3',
            'link': 'link 3',
            'tags': [
                {'term': 'term3-1'},
                {'term': 'term3-2'},
                {'term': 'term3-3'}
            ],
            'published': 'Wed, 06 Feb 2019 12:36:40 Z',
            'updated': '2019-02-06T12:36:40Z'
        },
        {   # Both tags and location absent
            'id': 4,
            'title': 'job 4',
            'author': 'company 4',
            'summary': 'summary 4',
            'link': 'link 4',
            'published': 'Wed, 06 Feb 2019 12:36:40 Z',
            'updated': '2019-02-06T12:36:40Z'
        },
    ]

    parser._dev_set_entries(entries)

    db_name = 'entries.sqlite'
    db = rssd.RSSDatabase(parser=parser, db=db_name)
    db.create_database()
    db.populate_database()

    test_cursor = db.cursor.execute('SELECT * FROM entry WHERE id = 1')
    test_results = test_cursor.fetchone()
    assert test_results[0] == 1
    assert test_results[1] == 'job 1'
    assert test_results[2] == 'company 1'
    assert test_results[3] == 'summary 1'
    assert test_results[4] == 'link 1'
    assert test_results[5] == 'term1-1,term1-2,term1-3'
    assert test_results[6] == 'location 1'
    assert test_results[7] == ''                            # Published
    assert test_results[8] == ''                            # Updated
    assert test_results[9] == ''                            # Timestamp

    assert False


def test_disconnect_database():
    assert False


def test_delete_database():
    assert False
