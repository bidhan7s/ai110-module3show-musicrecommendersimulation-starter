"""
Command line runner for the Music Recommender Simulation.
"""

from src.recommender import load_songs, recommend_songs


PROFILES = {
    "High-Energy Pop": {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.9},
    "Chill Lofi": {"favorite_genre": "lofi", "favorite_mood": "calm", "target_energy": 0.2},
    "Deep Intense Rock": {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.85},
    "Adversarial (conflicting prefs)": {"favorite_genre": "rock", "favorite_mood": "sad", "target_energy": 0.9},
}


def print_recommendations(profile_name, user_prefs, songs, k=5):
    print(f"\n=== Recommendations for: {profile_name} ===")
    recommendations = recommend_songs(user_prefs, songs, k)
    for rec in recommendations:
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")


def main() -> None:
    songs = load_songs("./data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()