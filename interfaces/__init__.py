from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List

from flask import jsonify


def jsonify_interface(fun):
    """Converts the dataclass output of a function to a simple dictionary."""

    def wrapper(*args, **kwargs):
        return jsonify(asdict(fun(*args, **kwargs)))

    # fixes overwriting endpoint ... flask already uses the
    # name 'wrapper' so we set it to the given functions name
    wrapper.__name__ = fun.__name__
    return wrapper


@dataclass
class DebugWordInfo:
    """Returned by debug route '/debug/get_word'."""

    text: str
    length: int
    date: datetime


@dataclass
class DebugResetInfo:
    """Returned by debug route '/debug/set_word'."""

    old: DebugWordInfo
    new: DebugWordInfo


@dataclass
class GameWordLength:
    """Returned by '/api/game/new_game'.

    This holds all the information that is send to the client
    to start a new game. We only send the current words length
    since the actual word should not be stored on the clients side.
    """

    length: int
    daily: bool
    session_start: datetime
    session_end: datetime


@dataclass
class GameDifficultyInfo:
    """Returned by '/api/game/difficulties'.

    Basically wraps all the information the client needs about
    all the provided difficulties to access other routes later.
    """

    id: int
    name: str
    tries: int


@dataclass
class ValidatedLetter:
    """Returned by '/api/game/validate_input'.

    Wraps the validation data about each letter in a given
    input word. Is wrapped by 'ValidatedWord'.
    """

    letter: str
    is_in_word: bool
    is_at_index: bool
    count: int


@dataclass
class ValidatedWord:
    """Returned by '/api/game/validate_input'.

    Holds the full validation data for any given
    input word.
    """

    is_valid: bool
    is_word: bool
    letters: List[ValidatedLetter]


@dataclass
class AddedScore:
    """Returned by '/api/score/add'.

    Holds the newly added score and the new total score by
    the difficulty the user played on.
    """

    score: int
    total_score: int


@dataclass
class ScoreSummary:
    """Returned by '/api/score/summary'.

    Holds the summary information for one difficulty.
    Is returned as a list of each difficulty.
    """

    no_played: int
    no_won: int
    total_score: int
    avg_score: float
    total_taken_tries: int
    avg_taken_tries: float
    avg_hit_rate: float
