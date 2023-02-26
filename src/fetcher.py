from urllib.parse import urljoin
import requests
from dataclasses import dataclass


@dataclass
class Scores:
    username: str
    easy: int
    medium: int
    hard: int


class ScoresFetcher:
    def __init__(self, stats_url: str):
        self.stats_url = stats_url

    def fetch_stats(self, username: str) -> Scores:
        url = urljoin(self.stats_url, username)
        r = requests.get(url)
        if r.status_code != 200:
            return None
        
        return Scores(
            username,
            r.json()["easySolved"],
            r.json()["mediumSolved"],
            r.json()["hardSolved"],
        )
