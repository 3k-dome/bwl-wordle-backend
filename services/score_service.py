from datetime import datetime
from typing import List

import requests
from flask import Flask
from interfaces import AddedScore, ScoreSummary
from models import Difficulty, Score, User
from sqlalchemy import desc

from services.user_service import Status

from .resettable_base import ResettableBase, depends_on_reset


class ScoreService(ResettableBase):
    def __init__(self, app: Flask, ip: str, port: str, daily: bool, interval: int) -> None:
        super().__init__(daily, interval)
        self.app = app
        self.ip = ip if ip != "0.0.0.0" else "127.0.0.1"
        self.port = port

    # we only need the properties and the decorator since we have no reset
    def reset(self) -> None:
        self.updated = datetime.now()

    @staticmethod
    def calculate_score(word_length: int, max_tries: int, taken_tries: int, found_letters: int) -> int:
        hit_rate = found_letters / word_length
        tries_rate = taken_tries / max_tries
        return int((50 * hit_rate) + (50 * tries_rate))

    def can_add_score(self, username: str) -> Status:
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            latest_score = Score.query.filter_by(user_id=user.id).order_by(desc(Score.date)).first()
            if latest_score:
                # if a latest score was found we need to make sure it was placed within the last
                # game session i.e. on another day or outside the current interval
                if self.daily and latest_score.date.day == datetime.now().day:
                    return Status.Error
                if not self.daily and (latest_score.date - self.updated).seconds < self.interval:
                    return Status.Error
        return Status.Ok

    @depends_on_reset
    def add_score(self, username: str, max_tries: int = None, taken_tries: int = None, found_letters: int = None, **kwargs) -> Status:
        # we need all of those
        if not username or not max_tries or not taken_tries or not found_letters:
            return Status.Empty
        # check the last score of this user
        can_add_score_status = self.can_add_score(username)
        if can_add_score_status != Status.Ok:
            return can_add_score_status
        # if we are still here calculate and add the score
        word_length = requests.get(f"http://{self.ip}:{self.port}/api/game/new_game").json()["length"]
        with self.app.app_context():
            difficultly = Difficulty.query.filter_by(tries=max_tries).first()
            user = User.query.filter_by(username=username).first()
            # calculate metrics
            score = ScoreService.calculate_score(word_length, max_tries, taken_tries, found_letters)
            won = found_letters == word_length
            hit_rate = found_letters / word_length

            # add the new score
            self.app.db.session.add(
                Score(
                    user_id=user.id,
                    difficulty_id=difficultly.id,
                    score=score,
                    won=won,
                    taken_tries=taken_tries,
                    hit_rate=hit_rate,
                )
            )
            self.app.db.session.commit()
        return Status.Ok

    def get_latest_score(self, username: str) -> AddedScore:
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            records = Score.query.filter_by(user_id=user.id).order_by(desc(Score.date)).all()
            return AddedScore(records[0].score, sum([record.score for record in records]))

    def get_summery_by_records(self, records: List[Score], tries: int = 0) -> ScoreSummary:
        won_games = sum([record.won for record in records])
        win_rate = won_games / len(records) if records else 0
        avg_taken_tries = sum([record.taken_tries for record in records]) / len(records) if records else 0
        avg_hit_rate = sum([record.hit_rate for record in records]) / len(records) if records else 0
        return ScoreSummary(tries, avg_taken_tries, len(records), won_games, win_rate, avg_hit_rate)

    def get_summery(self, username: str) -> List[ScoreSummary]:
        results = []
        with self.app.app_context():
            user = User.query.filter_by(username=username).first()
            # summary by difficulty
            for difficulty in Difficulty.query.all():
                records = Score.query.filter_by(user_id=user.id).filter_by(difficulty_id=difficulty.id).all()
                results.append(self.get_summery_by_records(records, difficulty.tries))
        return results
