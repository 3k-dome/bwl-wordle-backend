from dataclasses import replace
import random
from datetime import datetime, timedelta
from typing import List

from flask import Flask
from interfaces import GameDifficultyInfo, DebugResetInfo, ValidatedLetter, ValidatedWord, DebugWordInfo, GameWordLength
from models import Word, Difficulty
from sqlalchemy import desc

from .resettable_base import ResettableBase, depends_on_reset


class GameService(ResettableBase):
    """Handles anything about a the main game loop."""

    def __init__(self, app: Flask, daily: bool, interval: int) -> None:
        super().__init__(daily, interval)
        self.selected_word: Word
        self.app = app
        self.reset()

    def reset(self) -> None:
        """Implementation of this services reset method.

        When ever e reset happens this service needs to set a new usable word for the
        new cycle, if all words are used the reset will also reset all usd words and
        call itself again.
        """
        self.updated = datetime.now()
        try:
            with self.app.app_context():
                # update and select can not be in the same 'request' because we need to
                # expunge our selected word so we modify it first ...
                word = random.choice(Word.query.filter_by(usable=True).filter_by(used=False).all())
                word.used = True
                word.date = datetime.now()
                self.app.db.session.commit()
                # and then select it again ...
                self.selected_word = Word.query.order_by(desc(Word.date)).first()
                self.app.db.session.expunge(self.selected_word)
                self.app.db.session.commit()
        except:
            # eventually all words are used and 'random.choice' throws, then we simply
            # recycle all our words and call 'self.reset' again
            with self.app.app_context():
                for word in Word.query.filter_by(usable=True).filter_by(used=True).all():
                    word.used = True
                self.app.db.session.commit()
            self.reset()

    def force_reset(self) -> DebugResetInfo:
        """Debug method to force a reset."""
        old = self.get_word_info()
        self.reset()
        return DebugResetInfo(old, self.get_word_info())

    @depends_on_reset
    def get_word_info(self) -> DebugWordInfo:
        """Debug method to see the current state."""
        return DebugWordInfo(self.selected_word.text, len(self.selected_word.text), self.selected_word.date)

    @depends_on_reset
    def get_word_length(self) -> GameWordLength:
        """Returns everything to start a new game, i.e. word length and session times."""
        return GameWordLength(
            len(self.selected_word.text),
            self.daily,
            self.updated,
            (
                (self.updated + timedelta(days=1)).replace(hour=0, minute=0, second=0)
                if self.daily
                else self.updated + timedelta(seconds=self.interval)
            ),
        )

    @depends_on_reset
    def get_validated_word(self, word: str = "", **kwargs) -> ValidatedWord:
        """Returns the input validation for a given words."""
        word = word.lower()
        # cache the current words as set, and count each letter beforehand
        cache = set(self.selected_word.text)
        count = {letter: self.selected_word.text.count(letter) for letter in word}
        with self.app.app_context():
            return ValidatedWord(
                # wether the word is in our db and equals the current word
                True if Word.query.filter_by(text=word).all() else False,
                word == self.selected_word.text,
                [
                    # letter based validation: letter, in word, at position, count
                    ValidatedLetter(letter, letter in cache, letter == self.selected_word.text[i], count[letter] or 0)
                    for i, letter in enumerate(word[: self.selected_word.text.__len__()])
                ],
            )

    def get_difficulties(self) -> List[GameDifficultyInfo]:
        """Returns a simple overview of all available difficulties."""
        with self.app.app_context():
            return [GameDifficultyInfo(record.id, record.name, record.tries) for record in Difficulty.query.all()]
