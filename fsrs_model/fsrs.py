from .card import Card
from .log import Log, Rating
from datetime import datetime, timedelta
from math import log

class FSRS:
    def get_recommended_state(self, card: Card, now: datetime):
        if len(card.review_log) == 0:
            return 'learning'
        return 'review'

    def create_card(self):
        return Card()

    def create_log(self, card: Card, state: str, now: datetime, rating: Rating):
        return Log(now, rating)

    def repeat(self, card: Card, state: str, now: datetime):
        days = {0: 1, 1: 3, 2: 7, 3: 14}
        rating = card.review_log[-1].rating.value
        card.due = now.date() + timedelta(days=days[rating])
        return card