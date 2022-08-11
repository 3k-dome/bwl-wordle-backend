import imp
import re
from typing import Dict
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect


class SerializableModelBase:
    """Provides an easy to use base class to convert db models to json."""

    def __dict__(self) -> Dict:
        return {key: getattr(self, key) for key in inspect(self).attrs.keys()}

    def as_json(self, indent: int = 4) -> str:
        return json.dumps(self.__dict__(), indent=indent)

    def __repr__(self) -> str:
        return str(self.__dict__())

    def __str__(self) -> str:
        return repr(self)


db = SQLAlchemy()
