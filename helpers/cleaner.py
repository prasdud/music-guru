import json

input_file = "lyrics_dataset.jsonl"
output_file = "lyrics_dataset_cleaned.jsonl"

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        try:
            data = json.loads(line)
            original_lyrics = data.get("lyrics", [])
            cleaned_lyrics = [lyric_line for lyric_line in original_lyrics if "read more" not in lyric_line.lower()]
            data["lyrics"] = cleaned_lyrics
            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
        except json.JSONDecodeError:
            continue  # skip malformed lines
