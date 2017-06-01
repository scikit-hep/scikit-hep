# Licensed under a 3-clause BSD style license, see LICENSE.
from unittest import TestCase

from skhep.utils.ipythontools.entities import StoreContent, StoreContentList, StatisticsColumn, Statistics


class TestStoreContent(TestCase):

    def test_init(self):
        store_content = StoreContent("Name", 42)

        self.assertEqual(store_content.name, "Name")
        self.assertEqual(store_content.number, 42)


class TestStoreContentList(TestCase):

    def test_init(self):
        content_list = [StoreContent("First", 1), StoreContent("Second", 2)]
        store_content_list = StoreContentList(content_list, 21)

        self.assertEqual(store_content_list.content, content_list)
        self.assertEqual(store_content_list.event_number, 21)


class TestStatisticsColumn(TestCase):

    def test_init(self):
        statistics_column = StatisticsColumn("Name")

        self.assertEqual(statistics_column.name, "Name")
        self.assertEqual(statistics_column.display_name, "Name")
        self.assertEqual(statistics_column.three_column_format, False)

        statistics_column = StatisticsColumn("Name", "DisplayName")

        self.assertEqual(statistics_column.name, "Name")
        self.assertEqual(statistics_column.display_name, "DisplayName")
        self.assertEqual(statistics_column.three_column_format, False)

        statistics_column = StatisticsColumn("Name", "DisplayName", True)

        self.assertEqual(statistics_column.name, "Name")
        self.assertEqual(statistics_column.display_name, "DisplayName")
        self.assertEqual(statistics_column.three_column_format, True)


class TestStatistics(TestCase):

    def test_init(self):
        test_columns = [StatisticsColumn("Name"), StatisticsColumn("OtherName")]
        test_modules = [1, 2, 3]
        statistics = Statistics(test_columns, test_modules)

        self.assertEqual(statistics.columns, test_columns)
        self.assertEqual(statistics.modules, test_modules)
