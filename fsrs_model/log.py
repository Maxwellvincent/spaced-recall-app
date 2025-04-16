from enum import Enum
from datetime import datetime

class Rating(Enum):
    Again = 0
    Hard = 1
    Good = 2
    Easy = 3

class Log:
    def __init__(self, time: datetime, rating: Rating):
        self.time = time
        self.rating = rating