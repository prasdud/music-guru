import json
import csv
from collections import Counter
import Levenshtein


master_feature_list = []


### -------------------------------
# 1. Load JSONL Dataset
### -------------------------------
def load_jsonl(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]



### -------------------------------
# 2. Collect Last Words
### -------------------------------
def collect_last_words(song):
    last_words = []
    for line in song['lines']:
        if not line['words']:
            continue
        last_word = line['words'][-1]

        tempdict = {
            "text": last_word['text'],
            "phonemes": last_word['phonemes'],
            "syllables": last_word['syllables'],
            "stress": last_word['stress'],
            "rhyme_ending": last_word['rhyme_ending'],
            "rhyme_id": line['rhyme_id'],
        }

        last_words.append(tempdict)
    return last_words

        

### -------------------------------
# 3. Generate Pairs
### -------------------------------
def generate_pairs(last_words):
    pairs = []
    for i in range(0, len(last_words)):
        for j in range(i+1, len(last_words)):
            if((last_words[i]['rhyme_id']) == (last_words[j]['rhyme_id'])):
                label = 1
            else:
                label = 0
            pairs.append({
                "word1_text": last_words[i]['text'],
                "word1_phonemes": last_words[i]['phonemes'],
                "word1_syllables": last_words[i]['syllables'],
                "word1_stress": last_words[i]['stress'],
                "word1_rhyme_ending": last_words[i]['rhyme_ending'],

                "word2_text": last_words[j]['text'],
                "word2_phonemes": last_words[j]['phonemes'],
                "word2_syllables": last_words[j]['syllables'],
                "word2_stress": last_words[j]['stress'],
                "word2_rhyme_ending": last_words[j]['rhyme_ending'],

                "label": label
            })

    return pairs


### -------------------------------
# 4. Compute Features
### -------------------------------
def compute_features(pairs):
    features = []
    for pair in pairs:
        w1 = pair['word1_rhyme_ending'].lower().strip()
        w2 = pair['word2_rhyme_ending'].lower().strip()
        p1 = ''.join(pair.get('word1_phonemes', []))
        p2 = ''.join(pair.get('word2_phonemes', []))
        s1 = pair.get('word1_stress', '')
        s2 = pair.get('word2_stress', '')
        syl1 = int(pair.get('word1_syllables') or 0)
        syl2 = int(pair.get('word2_syllables') or 0)


        # Exact match
        exact_match = 1 if w1 == w2 else 0

        # Minimum ending length
        ending_length_min = min(len(w1), len(w2))

        # Phoneme edit distance (normalized similarity)
        if p1 and p2:
            max_len = max(len(p1), len(p2))
            phoneme_similarity = 1 - (Levenshtein.distance(p1, p2) / max_len) if max_len > 0 else 0
        else:
            phoneme_similarity = 0.0


        # Stress pattern match (binary)
        stress_match = 1 if s1 and s2 and s1 == s2 else 0

        # Stress pattern sequence similarity
        if s1 and s2:
            stress_similarity = 1 - (Levenshtein.distance(s1, s2) / max(len(s1), len(s2)))
        else:
            stress_similarity = 0.0

        # Syllable count difference
        syllable_diff = abs(syl1 - syl2)

        features.append({
            'exact_match': exact_match,
            'ending_length_min': ending_length_min,
            'phoneme_similarity': phoneme_similarity,
            'stress_match': stress_match,
            'stress_similarity': stress_similarity,
            'syllable_diff': syllable_diff,
            'label': pair['label']
        })
    
    return features



### -------------------------------
# 5. Store in List
### -------------------------------
def store_in_list(features):
    global master_feature_list
    master_feature_list.extend(features)


    


### -------------------------------
# 6. Save to CSV
### -------------------------------
def save_to_csv(features, output_path):
    if not features:
        print("NO FEATURES TO SAVE")
        return
    
    field_names = features[0].keys()

    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(features)
    
    print(f"✅ Saved {len(features)} rows to {output_path}")


### -------------------------------
# 7. Check Balance
### -------------------------------
def check_balance(features):
    if not features:
        print("NO FEATURES TO CHECK")
        return

    labels = [f['label'] for f in features]
    counts = Counter(labels)
    
    total = sum(counts.values())
    for label, count in counts.items():
        percentage = (count / total) * 100
        print(f"Label {label}: {count} samples ({percentage:.2f}%)")



### -------------------------------
# HELPER. For verifying rhyme stats
### -------------------------------
def rhyme_stats_per_song(songs):
    for idx, song in enumerate(songs):
        last_words = collect_last_words(song)
        pairs = generate_pairs(last_words)
        
        rhyme_count = sum(1 for p in pairs if p['label'] == 1)
        non_rhyme_count = len(pairs) - rhyme_count
        total = len(pairs)
        
        rhyme_percent = (rhyme_count / total * 100) if total > 0 else 0
        
        print(f"Song {idx+1}: Total pairs={total}, Rhymes={rhyme_count} ({rhyme_percent:.2f}%)")



### -------------------------------
# 8. Main Pipeline
### -------------------------------
def main():
    input_path = "./assets/rhyme_annotated.jsonl"
    output_path = "./assets/rhyme_pairs.csv"

    songs = load_jsonl(input_path)
    rhyme_stats_per_song(songs)
    all_pairs = []

    for song in songs:
        last_words = collect_last_words(song)
        pairs = generate_pairs(last_words)
        features = compute_features(pairs)
        all_pairs.extend(features)

    check_balance(all_pairs)
    save_to_csv(all_pairs, output_path)






### -------------------------------
# Entry Point
### -------------------------------
if __name__ == "__main__":
    main()
