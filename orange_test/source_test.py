import unittest

from orange.dependencies import appDependency
from orange.core.source.model import Season, WeekDay, Bangumi


class MikanSourceTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.source = appDependency.getSource()

    def test_get_bangumi(self):
        data = self.source.query_season(2020, Season.SPRING)
        self.assertIsNotNone(data)
        for day in WeekDay:
            self.assertTrue(data.table.get(str(day.value)) is not None)