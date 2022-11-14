import dataclasses
import json
import unittest

from orange.source.mikan.mikan_source import MikanSource
from orange.source.model import Bangumi, Season, TimeTable, WeekDay


class MikanSourceTest(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.source = MikanSource()

    def test_get_bangumi(self):
        flag,data = self.source.query_season(2020, Season.SPRING)
        self.assertTrue(flag)
        with open('orange_test/mock_file/source/mikan_season.json') as f:
           self.assertEqual(json.dumps(dataclasses.asdict(data)), f.read())