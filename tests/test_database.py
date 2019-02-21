import pytest
import sys
import os
import sqlite3
sys.path.append('src')

import RSSParser as rssp
import RSSDatabase as rssd
from exceptions import InvalidDatabaseException, InvalidParserException, DatabaseAlreadyExistsException

global_parser = rssp.RSSParser('https://stackoverflow.com/jobs/feed')
overwrite_parser = rssp.RSSParser('https://stackoverflow.com/jobs/feed')


def test_rss_database_debug_mode():
    db = rssd.RSSDatabase(_debug=True)

    assert db.parser is None
    assert db.db is None
    assert db.connection is None
    assert db.cursor is None


def test__dev_set_parser():
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
    db = rssd.RSSDatabase(_debug=True)

    str_db = 'this is not a parser'
    db._dev_set_db(str_db)
    assert db.db == str_db

    num_db = 123456
    db._dev_set_db(num_db)
    assert db.db == 123456

    parser1 = rssp.RSSParser('')
    db._dev_set_db(parser1)
    assert db.db == parser1


def test__is_valid_parser():
    db = rssd.RSSDatabase(_debug=True)

    url2 = 'wont_work'
    parser2 = rssp.RSSParser(url2)

    db._dev_set_parser(global_parser)
    assert db._is_valid_parser(db.parser)

    db._dev_set_parser(parser2)
    assert not db._is_valid_parser(db.parser)


def test__is_valid_db():
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


def test__db_taken():
    db_name = 'test_db.sqlite'
    db = rssd.RSSDatabase(parser=global_parser, db=db_name)
    db.create_database()

    with pytest.raises(DatabaseAlreadyExistsException):
        db2 = rssd.RSSDatabase(parser=global_parser, db=db_name)
    db.disconnect_database()

    if os.path.isfile(db_name):
        os.remove(db_name)


def test_rss_database():
    with pytest.raises(InvalidParserException):
        db = rssd.RSSDatabase()

    with pytest.raises(InvalidDatabaseException):
        db = rssd.RSSDatabase(global_parser)

    db_name2 = 'cool_database.sqlite'
    db2 = rssd.RSSDatabase(parser=global_parser, db=db_name2)

    assert db2.parser == global_parser
    assert db2.db == db_name2
    assert db2.connection is None
    assert db2.cursor is None


def test_create_database():
    db_name = 'entries.sqlite'

    db = rssd.RSSDatabase(parser=global_parser, db=db_name)
    db.create_database()

    assert os.path.isfile(db_name)

    assert type(db.connection) == sqlite3.Connection
    assert type(db.cursor) == sqlite3.Cursor

    test_cursor = db.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    results = test_cursor.fetchall()
    assert len(results) == 1  # entry table
    assert results[0][0] == 'entry'

    db.disconnect_database()

    os.remove(db_name)
    assert not os.path.isfile(db_name)



def test_populate_database():
    entries = [
        {   # Tags, location, and "(allows remote)"
            'id': 1,
            'title': 'job 1 (allows remote)',
            'author': 'company 1',
            'summary': 'summary 1',
            'link': 'link 1',
            'tags': [
                {'term': 'term1-1'},
                {'term': 'term1-2'},
                {'term': 'term1-3'}
            ],
            'location': 'city 1, state 1',
            'published': 'Wed, 06 Feb 2019 12:36:40 Z',
        },
        {   # Tags and location present, "(allows remote)" absent
            'id': 2,
            'title': 'job 2',
            'author': 'company 2',
            'summary': 'summary 2',
            'link': 'link 2',
            'tags': [
                {'term': 'term2-1'},
                {'term': 'term2-2'},
                {'term': 'term2-3'}
            ],
            'location': 'city 2, state 2',
            'published': 'Wed, 06 Feb 2019 12:36:42 Z',
        },
        {   # Tags and "(allows remote)", location absent
            'id': 3,
            'title': 'job 3 (allows remote)',
            'author': 'company 3',
            'summary': 'summary 3',
            'link': 'link 3',
            'tags': [
                {'term': 'term3-1'},
                {'term': 'term3-2'},
                {'term': 'term3-3'}
            ],
            'published': 'Wed, 06 Feb 2019 12:36:43 Z',
        },
        {   # Tags present, "(allows remote)" and location absent
            'id': 4,
            'title': 'job 4',
            'author': 'company 4',
            'summary': 'summary 4',
            'link': 'link 4',
            'tags': [
                {'term': 'term4-1'},
                {'term': 'term4-2'},
                {'term': 'term4-3'}
            ],
            'published': 'Wed, 06 Feb 2019 12:36:44 Z',
        },
        {   # Location and "(allows remote)", tags absent
            'id': 5,
            'title': 'job 5 (allows remote)',
            'author': 'company 5',
            'summary': 'summary 5',
            'link': 'link 5',
            'location': 'city 5, state 5',
            'published': 'Wed, 06 Feb 2019 12:36:45 Z',
        },
        {   # Location present, tags and "(allows remote)" absent
            'id': 6,
            'title': 'job 6',
            'author': 'company 6',
            'summary': 'summary 6',
            'link': 'link 6',
            'location': 'city 6, state 6',
            'published': 'Wed, 06 Feb 2019 12:36:46 Z',
        },
        {   # (allows remote)" present, tags and location absent
            'id': 7,
            'title': 'job 7 (allows remote)',
            'author': 'company 7',
            'summary': 'summary 7',
            'link': 'link 7',
            'published': 'Wed, 06 Feb 2019 12:36:47 Z',
        },
        {   # Tags, location, and "(allows remote)" absent
            'id': 8,
            'title': 'job 8',
            'author': 'company 8',
            'summary': 'summary 8',
            'link': 'link 8',
            'published': 'Wed, 06 Feb 2019 12:36:48 Z',
        },
    ]

    overwrite_parser._dev_set_entries(entries)

    db_name = 'test_db.sqlite'
    db = rssd.RSSDatabase(parser=overwrite_parser, db=db_name)
    db.create_database()

    db.populate_database()

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 1')
    test_results = test_query.fetchone()
    assert test_results[0] == 1
    assert test_results[1] == 'job 1 (allows remote)'
    assert test_results[2] == 'company 1'
    assert test_results[3] == 'summary 1'
    assert test_results[4] == 'link 1'
    assert test_results[5] == 'term1-1,term1-2,term1-3,'
    assert test_results[6] == 'city 1'
    assert test_results[7] == 'state 1'
    assert test_results[8] == 1

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 2')
    test_results = test_query.fetchone()
    assert test_results[0] == 2
    assert test_results[1] == 'job 2'
    assert test_results[2] == 'company 2'
    assert test_results[3] == 'summary 2'
    assert test_results[4] == 'link 2'
    assert test_results[5] == 'term2-1,term2-2,term2-3,'
    assert test_results[6] == 'city 2'
    assert test_results[7] == 'state 2'
    assert test_results[8] == 0

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 3')
    test_results = test_query.fetchone()
    assert test_results[0] == 3
    assert test_results[1] == 'job 3 (allows remote)'
    assert test_results[2] == 'company 3'
    assert test_results[3] == 'summary 3'
    assert test_results[4] == 'link 3'
    assert test_results[5] == 'term3-1,term3-2,term3-3,'
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 1

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 4')
    test_results = test_query.fetchone()
    assert test_results[0] == 4
    assert test_results[1] == 'job 4'
    assert test_results[2] == 'company 4'
    assert test_results[3] == 'summary 4'
    assert test_results[4] == 'link 4'
    assert test_results[5] == 'term4-1,term4-2,term4-3,'
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 0

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 5')
    test_results = test_query.fetchone()
    assert test_results[0] == 5
    assert test_results[1] == 'job 5 (allows remote)'
    assert test_results[2] == 'company 5'
    assert test_results[3] == 'summary 5'
    assert test_results[4] == 'link 5'
    assert test_results[5] == None
    assert test_results[6] == 'city 5'
    assert test_results[7] == 'state 5'
    assert test_results[8] == 1

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 6')
    test_results = test_query.fetchone()
    assert test_results[0] == 6
    assert test_results[1] == 'job 6'
    assert test_results[2] == 'company 6'
    assert test_results[3] == 'summary 6'
    assert test_results[4] == 'link 6'
    assert test_results[5] == None
    assert test_results[6] == 'city 6'
    assert test_results[7] == 'state 6'
    assert test_results[8] == 0

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 7')
    test_results = test_query.fetchone()
    assert test_results[0] == 7
    assert test_results[1] == 'job 7 (allows remote)'
    assert test_results[2] == 'company 7'
    assert test_results[3] == 'summary 7'
    assert test_results[4] == 'link 7'
    assert test_results[5] == None
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 1

    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 8')
    test_results = test_query.fetchone()
    assert test_results[0] == 8
    assert test_results[1] == 'job 8'
    assert test_results[2] == 'company 8'
    assert test_results[3] == 'summary 8'
    assert test_results[4] == 'link 8'
    assert test_results[5] == None
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 0

    db.disconnect_database()

    if os.path.isfile(db_name):
        os.remove(db_name)


def test_title_has_remote_option():
    db = rssd.RSSDatabase(_debug=True)

    has_remote = 'This text has a remote option (allows remote)'
    not_has_remote = 'This text does not have a remote option'

    assert db.title_has_remote_option(has_remote)
    assert not db.title_has_remote_option(not_has_remote)


def test_process_entry():
    db_name = 'test_db.sqlite'
    db = rssd.RSSDatabase(_debug=True)
    db.connect_database(db_name)
    db.create_database()
    test_connection = db.connection
    test_cursor = db.cursor

    entries = [
        {   # Tags, location, and "(allows remote)"
            'id': 1,
            'title': 'job 1 (allows remote)',
            'author': 'company 1',
            'summary': 'summary 1',
            'link': 'link 1',
            'tags': [
                {'term': 'term1-1'},
                {'term': 'term1-2'},
                {'term': 'term1-3'}
            ],
            'location': 'city 1, state 1',
            'published': 'Wed, 06 Feb 2019 12:36:40 Z',
        },
        {   # Tags and location present, "(allows remote)" absent
            'id': 2,
            'title': 'job 2',
            'author': 'company 2',
            'summary': 'summary 2',
            'link': 'link 2',
            'tags': [
                {'term': 'term2-1'},
                {'term': 'term2-2'},
                {'term': 'term2-3'}
            ],
            'location': 'city 2, state 2',
            'published': 'Wed, 06 Feb 2019 12:36:42 Z',
        },
        {   # Tags and "(allows remote)", location absent
            'id': 3,
            'title': 'job 3 (allows remote)',
            'author': 'company 3',
            'summary': 'summary 3',
            'link': 'link 3',
            'tags': [
                {'term': 'term3-1'},
                {'term': 'term3-2'},
                {'term': 'term3-3'}
            ],
            'published': 'Wed, 06 Feb 2019 12:36:43 Z',
        },
        {   # Tags present, "(allows remote)" and location absent
            'id': 4,
            'title': 'job 4',
            'author': 'company 4',
            'summary': 'summary 4',
            'link': 'link 4',
            'tags': [
                {'term': 'term4-1'},
                {'term': 'term4-2'},
                {'term': 'term4-3'}
            ],
            'published': 'Wed, 06 Feb 2019 12:36:44 Z',
        },
        {   # Location and "(allows remote)", tags absent
            'id': 5,
            'title': 'job 5 (allows remote)',
            'author': 'company 5',
            'summary': 'summary 5',
            'link': 'link 5',
            'location': 'city 5, state 5',
            'published': 'Wed, 06 Feb 2019 12:36:45 Z',
        },
        {   # Location present, tags and "(allows remote)" absent
            'id': 6,
            'title': 'job 6',
            'author': 'company 6',
            'summary': 'summary 6',
            'link': 'link 6',
            'location': 'city 6, state 6',
            'published': 'Wed, 06 Feb 2019 12:36:46 Z',
        },
        {   # (allows remote)" present, tags and location absent
            'id': 7,
            'title': 'job 7 (allows remote)',
            'author': 'company 7',
            'summary': 'summary 7',
            'link': 'link 7',
            'published': 'Wed, 06 Feb 2019 12:36:47 Z',
        },
        {   # Tags, location, and "(allows remote)" absent
            'id': 8,
            'title': 'job 8',
            'author': 'company 8',
            'summary': 'summary 8',
            'link': 'link 8',
            'published': 'Wed, 06 Feb 2019 12:36:48 Z',
        },
    ]

    db.process_entry(entries[0])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 1')
    test_results = test_query.fetchone()
    assert test_results[0] == 1
    assert test_results[1] == 'job 1 (allows remote)'
    assert test_results[2] == 'company 1'
    assert test_results[3] == 'summary 1'
    assert test_results[4] == 'link 1'
    assert test_results[5] == 'term1-1,term1-2,term1-3,'
    assert test_results[6] == 'city 1'
    assert test_results[7] == 'state 1'
    assert test_results[8] == 1

    db.process_entry(entries[1])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 2')
    test_results = test_query.fetchone()
    assert test_results[0] == 2
    assert test_results[1] == 'job 2'
    assert test_results[2] == 'company 2'
    assert test_results[3] == 'summary 2'
    assert test_results[4] == 'link 2'
    assert test_results[5] == 'term2-1,term2-2,term2-3,'
    assert test_results[6] == 'city 2'
    assert test_results[7] == 'state 2'
    assert test_results[8] == 0

    db.process_entry(entries[2])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 3')
    test_results = test_query.fetchone()
    assert test_results[0] == 3
    assert test_results[1] == 'job 3 (allows remote)'
    assert test_results[2] == 'company 3'
    assert test_results[3] == 'summary 3'
    assert test_results[4] == 'link 3'
    assert test_results[5] == 'term3-1,term3-2,term3-3,'
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 1

    db.process_entry(entries[3])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 4')
    test_results = test_query.fetchone()
    assert test_results[0] == 4
    assert test_results[1] == 'job 4'
    assert test_results[2] == 'company 4'
    assert test_results[3] == 'summary 4'
    assert test_results[4] == 'link 4'
    assert test_results[5] == 'term4-1,term4-2,term4-3,'
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 0

    db.process_entry(entries[4])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 5')
    test_results = test_query.fetchone()
    assert test_results[0] == 5
    assert test_results[1] == 'job 5 (allows remote)'
    assert test_results[2] == 'company 5'
    assert test_results[3] == 'summary 5'
    assert test_results[4] == 'link 5'
    assert test_results[5] == None
    assert test_results[6] == 'city 5'
    assert test_results[7] == 'state 5'
    assert test_results[8] == 1

    db.process_entry(entries[5])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 6')
    test_results = test_query.fetchone()
    assert test_results[0] == 6
    assert test_results[1] == 'job 6'
    assert test_results[2] == 'company 6'
    assert test_results[3] == 'summary 6'
    assert test_results[4] == 'link 6'
    assert test_results[5] == None
    assert test_results[6] == 'city 6'
    assert test_results[7] == 'state 6'
    assert test_results[8] == 0

    db.process_entry(entries[6])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 7')
    test_results = test_query.fetchone()
    assert test_results[0] == 7
    assert test_results[1] == 'job 7 (allows remote)'
    assert test_results[2] == 'company 7'
    assert test_results[3] == 'summary 7'
    assert test_results[4] == 'link 7'
    assert test_results[5] == None
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 1

    db.process_entry(entries[7])
    db.connection.commit()
    test_query = db.cursor.execute('SELECT * FROM entry WHERE id = 8')
    test_results = test_query.fetchone()
    assert test_results[0] == 8
    assert test_results[1] == 'job 8'
    assert test_results[2] == 'company 8'
    assert test_results[3] == 'summary 8'
    assert test_results[4] == 'link 8'
    assert test_results[5] == None
    assert test_results[6] == None
    assert test_results[7] == None
    assert test_results[8] == 0

    db.disconnect_database()

    if os.path.isfile(db_name):
        os.remove(db_name)


def test_connect_database():
    db_name = 'test_db.sqlite'
    db = rssd.RSSDatabase(_debug=True)
    db.connect_database(db_name)

    test_connection = db.connection
    test_cursor = db.cursor
    test_cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name VARCHAR(10) NOT NULL);')
    test_connection.commit()

    test_cursor.execute('SELECT name FROM sqlite_master WHERE type = "table"')
    tables = test_cursor.fetchall()
    assert len(tables) == 1
    assert tables[0][0] == 'test'

    with pytest.raises(InvalidDatabaseException):
        db.connect_database('wont_work')

    db.disconnect_database()

    if os.path.isfile(db_name):
        os.remove(db_name)


def test_disconnect_database():
    db_name = 'test_db.sqlite'
    db = rssd.RSSDatabase(_debug=True)
    db.connect_database(db_name)

    test_cursor = db.cursor
    test_cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, name VARCHAR(10) NOT NULL);')

    test_cursor.execute('INSERT INTO test (id, name) VALUES (1, "a");')

    db.disconnect_database(commit=False)

    db.connect_database(db_name)

    test_cursor = db.cursor
    test_cursor.execute('SELECT COUNT(*) FROM test;')
    count = test_cursor.fetchall()
    assert len(count) == 1
    assert count[0][0] == 0

    test_cursor.execute('INSERT INTO test (id, name) VALUES (1, "a");')

    db.disconnect_database(commit=True)
    db.connect_database(db_name)

    test_cursor = db.cursor
    test_cursor.execute('SELECT COUNT(*) FROM test;')
    count = test_cursor.fetchall()
    assert len(count) == 1
    assert count[0][0] == 1

    db.disconnect_database()

    if os.path.isfile(db_name):
        os.remove(db_name)
