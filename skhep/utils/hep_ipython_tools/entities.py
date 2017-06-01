# Licensed under a 3-clause BSD style license, see LICENSE.


class StoreContent:
    """
    Data class for an entry in a store content list.
    """

    def __init__(self, name, number):
        """
        Create a new entry in a Store Content List.
        :param name: The name of the store content.
        :param number: The number of items in this store content.
        """
        #: The name of the store content.
        self.name = name
        #: The number of items in this store content.
        self.number = number


class StoreContentList:
    """
    Data class for the content of the storage for one event.
    """

    def __init__(self, content, event_number):
        """
        Create a new content fr one event.
        :param content: A list of StoreContents.
        :param event_number: The event number this element describes.
        """
        #: A list of StoreContents.
        self.content = content
        #: The event number this element describes.
        self.event_number = event_number


class StatisticsColumn:
    """
    Data class for a column in the statistics view.
    """

    def __init__(self, name, display_name=None, three_column_format=False):
        """
        Create a new column for the statistics view.
        :param name: The name of this column.
        :param display_name: The display name of this column.
        :param three_column_format: If the column has one or three columns.
        """
        #: The name of this column.
        self.name = name
        #: If the column has one or three columns.
        self.three_column_format = three_column_format

        if not display_name:
            #: The name to show
            self.display_name = self.name
        else:
            #: The name to show
            self.display_name = display_name


class Statistics:
    """
    Data class for the statistics.
    """

    def __init__(self, columns, modules):
        """
        Create a new Statistics object.
        :param columns: The list of StatisticsColumns.
        :param modules: A list of dictionaries, each one with the same names as there are columns.
        """
        #: The list of StatisticsColumns.
        self.columns = columns
        #: A list of dictionaries, each one with the same names as there are columns.
        self.modules = modules
