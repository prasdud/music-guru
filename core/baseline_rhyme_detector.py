import json
from collections import defaultdict
from itertools import product
from string import ascii_uppercase

### -------------------------------
# 1. Load JSONL Dataset
### -------------------------------
def load_jsonl(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


### -------------------------------
# 2. Phoneme Similarity (for slant/multi rhymes)
### -------------------------------
def phoneme_similarity(p1, p2):
    """
    Compares two phoneme lists backwards.
    Returns number of matching trailing phonemes.
    """
    matches = 0
    for a, b in zip(reversed(p1), reversed(p2)):
        if a == b:
            matches += 1
        else:
            break
    return matches


### -------------------------------
# 3. Rhyme Group ID Generator
### -------------------------------
def generate_rhyme_group():
    """
    Yields rhyme group labels: A, B, ..., Z, AA, AB, ..., ZZ, AAA, ...
    """
    length = 1
    while True:
        for group in product(ascii_uppercase, repeat=length):
            yield ''.join(group)
        length += 1


### -------------------------------
# 4. Detect Rhymes for a Song
### -------------------------------
def detect_rhyme_groups(song, min_match_phonemes=2):
    rhyme_groups = {}  # key: rhyme_ending tuple, value: group ID (A, B, C...)
    rhyme_group_gen = generate_rhyme_group()

    # Map rhyme endings to group labels
    for line in song["lines"]:
        if not line["words"]:
            continue
        last_word = line["words"][-1]
        rhyme_key = tuple(last_word["rhyme_ending"].split())

        # Try to find an existing group
        assigned = False
        for key, group in rhyme_groups.items():
            if phoneme_similarity(rhyme_key, key) >= min_match_phonemes:
                line["rhyme_id"] = group
                assigned = True
                break

        # If no match, assign new group
        if not assigned:
            group_id = next(rhyme_group_gen)
            rhyme_groups[rhyme_key] = group_id
            line["rhyme_id"] = group_id

    return song


### -------------------------------
# 5. Save Output JSONL
### -------------------------------
def save_jsonl(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")


### -------------------------------
# 6. Main Pipeline
### -------------------------------
def main():
    input_path = "preprocessed.jsonl"
    output_path = "rhyme_annotated.jsonl"

    songs = load_jsonl(input_path)
    annotated_songs = []

    for song in songs:
        annotated_song = detect_rhyme_groups(song)
        annotated_songs.append(annotated_song)

    save_jsonl(annotated_songs, output_path)
    print(f"Saved annotated songs to {output_path}")


### -------------------------------
# Entry Point
### -------------------------------
if __name__ == "__main__":
    main()
