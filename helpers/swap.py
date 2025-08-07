import json

input_file = "./assets/lyrics_dataset_cleaned.jsonl"
output_file = "lyrics_dataset_fixed.jsonl"

print("Fixing swapped artist/song fields...")

fixed_count = 0

with open(input_file, 'r', encoding='utf-8') as infile:
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line.strip())
            
            # Swap artist and song
            fixed_data = {
                "artist": data["song"],  # song becomes artist
                "song": data["artist"],  # artist becomes song
                "lyrics": data["lyrics"]
            }
            
            outfile.write(json.dumps(fixed_data, ensure_ascii=False) + '\n')
            fixed_count += 1
            
            if fixed_count % 100 == 0:
                print(f"Fixed {fixed_count} songs...")

print(f"✓ Fixed {fixed_count} songs")
print(f"✓ Output saved to: {output_file}")
print(f"✓ You can now delete the old file and rename this one")