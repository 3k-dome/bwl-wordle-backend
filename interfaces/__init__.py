from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

from flask import jsonify


def jsonify_interface(fun):
    def wrapper(*args, **kwargs):
        return jsonify(asdict(fun(*args, **kwargs)))

    # fixes overwriting endpoint ... flask already uses the
    # name 'wrapper' so we set it to the given functions name
    wrapper.__name__ = fun.__name__
    return wrapper


@dataclass
class WordInfo:
    text: str
    length: int
    date: datetime


@dataclass
class ForcedReset:
    old: WordInfo
    new: WordInfo


@dataclass
class WordLength:
    length: int
    session_start: datetime
    session_end: datetime


@dataclass
class DifficultyInfo:
    id: int
    name: str
    tries: int


@dataclass
class ValidatedLetter:
    letter: str
    is_in_word: bool
    is_at_index: bool
    count: int


@dataclass
class ValidatedWord:
    is_valid: bool
    is_word: bool
    letters: List[ValidatedLetter]


@dataclass
class AddedScore:
    score: int
    total_score: int


@dataclass
class ScoreSummary:
    no_played: int 
    no_won: int
    total_score: int
    avg_score: float
    total_taken_tries : int
    avg_taken_tries: float
    avg_hit_rate: float

@dataclass
class ScoreBoard:
    pass
