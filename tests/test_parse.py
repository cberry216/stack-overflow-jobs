import pytest
import sys
sys.path.append('src')

import RSSParser as rssp

global_parser = rssp.RSSParser('https://stackoverflow.com/jobs/feed')

def test_rss_parser_init():
    parser = rssp.RSSParser('this_is_the_url')

    assert type(parser) == rssp.RSSParser
    assert parser.url == 'this_is_the_url'


def test_parse_rss_feed():               # parse_rss_feed() is automatically called when an RSSParser is initialized
    assert global_parser.feed.status == 200
    assert 'bozo_exception' not in global_parser.keys
    assert type(global_parser.entries) == type([])


def test_is_valid_parser():
    url2 = 'thisurlwillnotwork'
    parser_fail = rssp.RSSParser(url2)

    assert global_parser.is_valid_parser()
    assert not parser_fail.is_valid_parser()


def test__dev_set_entries():
    import RSSParser as rssp
    url = 'https://stackoverflow.com/jobs/feed'
    parser = rssp.RSSParser(url)

    test_entries = [
        {'id': 100, 'author': 'abc', 'title': 'good job'},
        {'id': 200, 'author': 'def', 'title': 'okay job'},
        {'id': 300, 'author': 'hij', 'title': 'bad job'},
        {'id': 400, 'author': 'klm', 'title': 'hell job'},
        {'id': 500, 'author': 'nop', 'title': 'ugh job'},
        {'id': 600, 'author': 'qrs', 'title': 'your job'},
    ]

    parser._dev_set_entries(test_entries)
    assert parser.entries[0] == {'id': 100, 'author': 'abc', 'title': 'good job'}
    assert parser.entries[1] == {'id': 200, 'author': 'def', 'title': 'okay job'}
    assert parser.entries[2] == {'id': 300, 'author': 'hij', 'title': 'bad job'}
    assert parser.entries[3] == {'id': 400, 'author': 'klm', 'title': 'hell job'}
    assert parser.entries[4] == {'id': 500, 'author': 'nop', 'title': 'ugh job'}
    assert parser.entries[5] == {'id': 600, 'author': 'qrs', 'title': 'your job'}


def test_entry():
    import RSSParser as rssp
    url = 'https://stackoverflow.com/jobs/feed'
    parser = rssp.RSSParser(url)

    test_entries = [
        {'id': 100, 'author': 'abc', 'title': 'good job'},
        {'id': 200, 'author': 'def', 'title': 'okay job'},
        {'id': 300, 'author': 'hij', 'title': 'bad job'},
        {'id': 400, 'author': 'klm', 'title': 'hell job'},
        {'id': 500, 'author': 'nop', 'title': 'ugh job'},
        {'id': 600, 'author': 'qrs', 'title': 'your job'},
    ]

    parser._dev_set_entries(test_entries)

    entry = parser.entry()

    next_entry = next(entry)
    assert next_entry == {'id': 100, 'author': 'abc', 'title': 'good job'}
    next_entry = next(entry)
    assert next_entry == {'id': 200, 'author': 'def', 'title': 'okay job'}
    next_entry = next(entry)
    assert next_entry == {'id': 300, 'author': 'hij', 'title': 'bad job'}
    next_entry = next(entry)
    assert next_entry == {'id': 400, 'author': 'klm', 'title': 'hell job'}
    next_entry = next(entry)
    assert next_entry == {'id': 500, 'author': 'nop', 'title': 'ugh job'}
    next_entry = next(entry)
    assert next_entry == {'id': 600, 'author': 'qrs', 'title': 'your job'}

    with pytest.raises(StopIteration):
        next_entry = next(entry)
