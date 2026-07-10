from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            score += 1.5
            reasons.append("genre match (+1.5)")

        if song.mood.lower() == user.favorite_mood.lower():
            score += 2.0
            reasons.append("mood match (+2.0)")

        energy_diff = abs(song.energy - user.target_energy)
        energy_points = round(1.5 * (1 - energy_diff), 2)
        if energy_points > 0:
            score += energy_points
            reasons.append(f"energy close (+{energy_points})")

        if user.likes_acoustic and song.acousticness > 0.6:
            score += 0.5
            reasons.append("acoustic bonus (+0.5)")

        return round(score, 2), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        scored = [(song, self._score(user, song)[0]) for song in self.songs]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)
        return [song for song, score in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        score, reasons = self._score(user, song)
        reason_str = ", ".join(reasons) if reasons else "no strong matches"
        return f"Score: {score} — {reason_str}"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            song['energy'] = float(row['energy'])
            song['tempo_bpm'] = float(row['tempo_bpm'])
            song['valence'] = float(row['valence'])
            song['danceability'] = float(row['danceability'])
            song['acousticness'] = float(row['acousticness'])
            songs.append(song)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    if song['genre'].lower() == user_prefs['favorite_genre'].lower():
        score += 1.5
        reasons.append("genre match (+1.5)")

    if song['mood'].lower() == user_prefs['favorite_mood'].lower():
        score += 2.0
        reasons.append("mood match (+2.0)")

    energy_diff = abs(song['energy'] - user_prefs['target_energy'])
    energy_points = round(1.5 * (1 - energy_diff), 2)
    if energy_points > 0:
        score += energy_points
        reasons.append(f"energy close (+{energy_points})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) if reasons else "no strong matches"
        scored.append((song, score, explanation))

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]