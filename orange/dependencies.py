from orange.core.parser.abstract_parser import AbstractParser
from orange.core.source.abstract_source import AbstractSource
from orange.dev_config import *
from orange.parser.tmdb.tmdb_parser import TmdbParser
from orange.source.mikan.mikan_source import MikanSource

class AppDependency:

    registed_source = {
        "mikan": MikanSource
    }

    registed_parser = {
        "tmdb": TmdbParser
    }

    def getSource(self) -> AbstractSource:
        source_type = self.registed_source.get(source, MikanSource)
        return source_type()

    def getParser(self) -> AbstractParser:
        parser_type = self.registed_parser.get(parser, TmdbParser)
        return parser_type()

appDependency = AppDependency()