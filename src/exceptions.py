class InvalidParserException(ValueError):
    def __init__(self, parser, message='An error occured'):
        """
        Overwrites __init__ function for ValueError.

        Args:
          parser (object): Object to provide error reporting on.
          message (str, optional): Defaults to 'An error occured'. Error message to report.
        """

        super().__init__()
        self.parser = parser
        self.message = message

    def __str__(self):
        """
        Overwrites the default stacktrace with custom message.

        Returns:
          str: Error message to report.
        """

        error_string = self.message + \
            '\n\tThe parser provided is invalid.\n\tThe parser is of type: ' + str(type(self.parser))
        try:
            error_string += '\n\tparser.url: \'' + self.parser.url + '\'\n\tparser.count: ' + str(self.parser.count)
        except Exception:
            pass
        return error_string


class InvalidDatabaseException(ValueError):
    def __init__(self, db, message='An error occurred'):
        """
        Overwrites __init__ function for ValueError.

        Args:
          db (str): String to provide error reporting on.
          message (str, optional): Defaults to 'An error occurred'. Error message to report.
        """

        super().__init__()
        self.db = db
        self.message = message

    def __str__(self):
        """
        Overwrites the default stacktrace with custom message.

        Returns:
          str: Error message to report.
        """

        error_string = self.message + \
            '\n\tThe database name provided is invalid.\n\tThe database should have one of the follow extensions:\n\t\t.db\n\t\t.sqlite\n\t\t.sqlite3\n\tCurrent database name: ' + \
            str(self.db)
        return error_string


class DatabaseAlreadyExistsException(ValueError):
    def __init__(self, db, message='An error occured.'):
        """
        Overwrites __init__ function for ValueError.

        Args:
          db (str): String to provide error reporting on.
          message (str, optional): Defaults to 'An error occurred'. Error message to report.
        """
        super().__init__()
        self.db = db
        self.message = message

    def __str__(self):
        """
        Overwrites the default stacktrace with custom message.

        Returns:
          str: Error message to report.
        """
        error_string = self.message + \
            '\n\tThe database with the name \'%s\' is already initiliazed.\n\tPlease change the name of the database to something different.' % self.db
        return error_string
