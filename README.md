# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a simplified content-based music recommender, similar
in spirit to how platforms like Spotify suggest songs — but using only a
song's own attributes (genre, mood, energy) rather than other users'
listening behavior. A user "taste profile" is compared against a small song
catalog, each song is scored for how well it matches, and the top-ranked
results are returned as recommendations
---

## How The System Works

Each `Song` in this system has the following features:
- **genre** — e.g. pop, rock, lofi
- **mood** — e.g. happy, intense, calm
- **energy** — a 0.0-1.0 scale representing intensity
- **tempo_bpm** — beats per minute

A `UserProfile` stores target preferences for these same fields:
- **favorite_genre**
- **favorite_mood**
- **target_energy**

The `Recommender` scores each song against the user profile using a
weighted rule:
- +2.0 points if the song's genre matches the user's favorite genre
- +1.0 point if the song's mood matches the user's favorite mood
- Up to +2.0 points based on how *close* the song's energy is to the
  user's target energy (closer = more points, not just "higher energy")

Every song in the catalog is scored this way, then the list is sorted from
highest to lowest score. The top K songs are returned as the final
recommendations, along with a plain-language list of "reasons" explaining
why each song scored the way it did (e.g. "genre match (+2.0)").

This mirrors real systems in a simplified way: real recommenders also
turn raw attributes into scores and rank across a catalog — just with far
more features and far more users' behavior data feeding in.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 18

Top recommendations:

Storm Runner - Score: 4.88
Because: genre match (+2.0), mood match (+1.0), energy close (+1.88)

Midnight Cipher - Score: 3.00
Because: mood match (+1.0), energy close (+2.0)

Gym Hero - Score: 2.84
Because: mood match (+1.0), energy close (+1.84)

Fuego Tropical - Score: 1.96
Because: energy close (+1.96)

Sunrise City - Score: 1.94
Because: energy close (+1.94)
```

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



