from collections import ChainMap
from configparser import ConfigParser, Interpolation
from typing import Any

from expandvars import expandvars


class EnvInterpolation(Interpolation):
    def before_get(
        self,
        parser: ConfigParser,
        section: str,
        option: str,
        value: Any,
        defaults: ChainMap,
    ) -> Any:
        return expandvars(value)
