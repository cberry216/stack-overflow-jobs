import RSSParser as rssp
import RSSDatabase as rssd
from exceptions import InvalidParserException, InvalidDatabaseException, DatabaseAlreadyExistsException
import sys

DB_NAME = 'db.sqlite'

def main():
    stackoverflow_rss_feed_url = 'https://stackoverflow.com/jobs/feed'

    print('Generating parser...')
    rss_parser = rssp.RSSParser(stackoverflow_rss_feed_url)
    try:
        rss_database = rssd.RSSDatabase(parser=rss_parser, db=DB_NAME)
    except InvalidParserException as e:
        print(str(e))
        sys.exit(1)
    except InvalidDatabaseException as e:
        print(str(e))
        sys.exit(1)
    except DatabaseAlreadyExistsException as e:
        print(str(e))
        sys.exit(1)

    print('Creating Database...')
    rss_database.create_database()
    print('Populating Database...')
    rss_database.populate_database()
    print('Disconnecting Database...')
    rss_database.disconnect_database(commit=True)
    print(f'\nDatabase is populated. To explore run \n\t\'$ sqlite3 {DB_NAME}\'')
    print('The only table in the database is:\n\t\'entry\'')
    print('Attribute names for the entry table are:')
    print('\tid | title | company | summary | link | tags | location | allows_remote | published | timestamp')


if __name__ == '__main__':
    main()
