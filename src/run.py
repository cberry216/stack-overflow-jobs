import RSSParser as rssp
import RSSDatabase as rssd
import sys


def main():
    if len(sys.argv) != 2:
        print('usage: python[3] run.py <database name>')
        sys.exit(1)
    else:
        db_name = sys.argv[1]

    stackoverflow_rss_feed_url = 'https://stackoverflow.com/jobs/feed'

    print('Generating parser...')
    rss_parser = rssp.RSSParser(stackoverflow_rss_feed_url)
    rss_database = rssd.RSSDatabase(parser=rss_parser, db=db_name)

    print('Creating Database...')
    rss_database.create_database()
    print('Populating Database...')
    rss_database.populate_database()
    print('Disconnecting Database...')
    rss_database.disconnect_database(commit=True)


if __name__ == '__main__':
    main()
