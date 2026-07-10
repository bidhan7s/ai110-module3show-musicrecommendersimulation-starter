# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a simplified content-based music recommender, similar
in spirit to how platforms like Spotify suggest songs — but using only a
song's own attributes (genre, mood, energy) rather than other users'
listening behavior. A user "taste profile" is compared against a small song
catalog, each song is scored for how well it matches, and the top-ranked
results are returned as recommendations.

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
- +1.5 points if the song's genre matches the user's favorite genre
- +2.0 points if the song's mood matches the user's favorite mood
- Up to +1.5 points based on how *close* the song's energy is to the
  user's target energy (closer = more points, not just "higher energy")

I initially weighted genre higher than mood (2.0 vs 1.0), but testing
revealed this let energy closeness override a wrong mood match too easily.
I rebalanced the weights to give mood more influence, which is reflected
in the numbers above — see "Experiments You Tried" below for details.

Every song in the catalog is scored this way, then the list is sorted from
highest to lowest score. The top K songs are returned as the final
recommendations, along with a plain-language list of "reasons" explaining
why each song scored the way it did (e.g. "genre match (+1.5)").

This mirrors real systems in a simplified way: real recommenders also
turn raw attributes into scores and rank across a catalog — just with far
more features and far more users' behavior data feeding in.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
```

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

=== Recommendations for: High-Energy Pop ===
Sunrise City - Score: 4.88
Because: genre match (+1.5), mood match (+2.0), energy close (+1.38)
Rooftop Lights - Score: 3.29
Because: mood match (+2.0), energy close (+1.29)
Gym Hero - Score: 2.96
Because: genre match (+1.5), energy close (+1.46)
Storm Runner - Score: 1.48
Because: energy close (+1.48)
Fuego Tropical - Score: 1.46
Because: energy close (+1.46)

=== Recommendations for: Chill Lofi ===
Library Rain - Score: 2.78
Because: genre match (+1.5), energy close (+1.28)
Focus Flow - Score: 2.70
Because: genre match (+1.5), energy close (+1.2)
Midnight Coding - Score: 2.67
Because: genre match (+1.5), energy close (+1.17)
Spacewalk Thoughts - Score: 1.38
Because: energy close (+1.38)
Moonlight Meditation - Score: 1.38
Because: energy close (+1.38)

=== Recommendations for: Deep Intense Rock ===
Storm Runner - Score: 4.91
Because: genre match (+1.5), mood match (+2.0), energy close (+1.41)
Midnight Cipher - Score: 3.50
Because: mood match (+2.0), energy close (+1.5)
Gym Hero - Score: 3.38
Because: mood match (+2.0), energy close (+1.38)
Fuego Tropical - Score: 1.47
Because: energy close (+1.47)
Sunrise City - Score: 1.46
Because: energy close (+1.46)

=== Recommendations for: Adversarial (conflicting prefs) ===
Storm Runner - Score: 2.98
Because: genre match (+1.5), energy close (+1.48)
Gym Hero - Score: 1.46
Because: energy close (+1.46)
Fuego Tropical - Score: 1.46
Because: energy close (+1.46)
Thunder Forge - Score: 1.44
Because: energy close (+1.44)
Neon Rush - Score: 1.43
Because: energy close (+1.43)
```

---

## Experiments You Tried

I ran an adversarial test profile — rock genre, "sad" mood, 0.9 target
energy — a combination that doesn't really exist cleanly in my dataset.
"Storm Runner" (rock/intense/0.91 energy) ranked #1 despite not matching
mood at all, because its genre and energy match were strong enough to
compensate.

To test this, I changed the weights: genre from 2.0 → 1.5, mood from
1.0 → 2.0, and energy's max from 2.0 → 1.5, to make mood matter more.
Storm Runner's adversarial score dropped from 3.98 to 2.98 and correctly
lost its mood bonus — but it still ranked #1 overall, because there's no
high-energy "sad" rock song anywhere in the catalog to take its place.

This showed me the issue wasn't purely the weighting formula — it was
also a data coverage gap. Reweighting fixed *how much* a wrong-mood song
was penalized, but couldn't produce a better option that didn't exist.

---

## Limitations and Risks

- The catalog only has 18 songs, so many genre/mood/energy combinations
  (like "sad high-energy rock") simply don't exist, no matter how the
  scoring is tuned.
- The system doesn't understand lyrics, language, or cultural context —
  it only compares numeric/categorical attributes.
- Mood and genre are tightly coupled in this dataset (e.g. "happy" is
  almost always pop), which risks pushing users toward the same narrow
  slice of the catalog regardless of their actual taste.
- Energy contributes as much or more than genre/mood, so a strong energy
  match can override a mismatched mood — this is discussed in more depth
  in the model card.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender showed me that turning data into predictions is
really just a matter of designing a point system and trusting it to rank
consistently — there's no "magic," just weighted comparisons applied at
scale. The more surprising lesson was that bias doesn't only come from
bad weighting; it can come from the dataset itself. Even after I
rebalanced my scoring to fix an obvious flaw (mood being too easy to
override), the system still produced an imperfect result because the
right song simply wasn't in my catalog. That distinction — an algorithm
problem versus a data problem — is exactly the kind of unfairness real
recommender systems can have at a much larger scale, where missing or
underrepresented data quietly limits what certain users ever get shown.