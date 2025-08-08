import json


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
        w1 = pair['word1_rhyme_ending']
        w2 = pair['word2_rhyme_ending']
        if(w1==w2):
            exact_match = 1
        else:
            exact_match = 0
        ending_length_min = min(len(w1), len(w2))

        #ADD PHENOME EDIT DISTANCE
        #ADD STRESS PATTERN MATCH
        #ADD SYLLABLE COUNT DIFFERENCE FOR BETTER NUANCES
        
        features.append({
            'exact_match': exact_match,
            'ending_length_min': ending_length_min,
            'label': pair['label']
        })
        


### -------------------------------
# 5. Store in List
### -------------------------------
def store_in_list():
    


### -------------------------------
# 6. Save to CSV
### -------------------------------
def save_to_csv(pairs, output_path):
    


### -------------------------------
# 7. Check Balance
### -------------------------------
def check_balance():
    

### -------------------------------
# 8. Main Pipeline
### -------------------------------
def main():
    input_path = "./assets/rhyme_annotated.jsonl"
    output_path = "./assets/rhyme_pairs.csv"

    songs = load_jsonl(input_path)
    all_pairs = []

    for song in songs:
        last_words = collect_last_words(song)
        pairs = generate_pairs(last_words)
        for w1, w2, label in pairs:
            features = compute_features(w1, w2)
            all_pairs.append((*features, label))

    balanced_pairs = check_balance(all_pairs)
    save_to_csv(balanced_pairs, output_path)





### -------------------------------
# Entry Point
### -------------------------------
if __name__ == "__main__":
    main()
