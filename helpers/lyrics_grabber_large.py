import os
import lyricsgenius
from dotenv import load_dotenv
import csv
import json
import re
import string
import time
from concurrent.futures import ThreadPoolExecutor
import threading

# === Setup ===
load_dotenv(".env")
token = os.getenv("GENIUS_API_TOKEN")

genius = lyricsgenius.Genius(token)
genius.verbose = False
genius.remove_section_headers = True

# === Config ===
csv_file = "./assets/1000songswithartistname.csv"  # Your input CSV
output_file = "lyrics_dataset.jsonl"
max_workers = 3

# Pre-compile regex for cleaning
punct_to_remove = ''.join(c for c in string.punctuation if c not in {"'", "-"})
punct_pattern = re.compile(f"[{re.escape(punct_to_remove)}]")

# Thread-safe counter
class Counter:
    def __init__(self):
        self.value = 0
        self.success = 0
        self.lock = threading.Lock()
    
    def increment(self, success=False):
        with self.lock:
            self.value += 1
            if success:
                self.success += 1

counter = Counter()
file_lock = threading.Lock()

def clean_lyrics(lyrics):
    if not lyrics:
        return []
    
    cleaned_lines = []
    for line in lyrics.split('\n')[1:]:  # Skip first line
        line = line.lower().strip()
        # Skip common non-lyric lines
        if any(skip in line for skip in ['embed', 'you might also like', '[verse', '[chorus', '[bridge']):
            continue
        
        line = punct_pattern.sub("", line)
        line = re.sub(r'\s+', ' ', line).strip()
        
        if line and len(line) > 3:
            cleaned_lines.append(line)
    
    return cleaned_lines

def get_song_lyrics(artist, song_title, total_songs):
    try:
        # Search for the specific song
        song = genius.search_song(song_title, artist)
        
        if song and song.lyrics:
            cleaned = clean_lyrics(song.lyrics)
            
            if cleaned:  # Only save if we got actual lyrics
                result = {
                    "artist": artist,
                    "song": song_title,
                    "lyrics": cleaned
                }
                
                # Thread-safe file writing
                with file_lock:
                    with open(output_file, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(result, ensure_ascii=False) + '\n')
                
                counter.increment(success=True)
                print(f"✓ {counter.success}/{total_songs} - {artist} - {song_title}")
                return True
        
        counter.increment()
        print(f"✗ {counter.value}/{total_songs} - Failed: {artist} - {song_title}")
        return False
        
    except Exception as e:
        counter.increment()
        print(f"✗ {counter.value}/{total_songs} - Error: {artist} - {song_title}")
        return False

def main():
    # Read CSV file
    songs = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    songs.append((row[0], row[1]))  # (artist, song)
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        return
    
    total_songs = len(songs)
    print(f"Found {total_songs} songs in CSV")
    print(f"Starting lyrics collection with {max_workers} workers...")
    print("=" * 60)
    
    # Clear output file
    with open(output_file, 'w', encoding='utf-8') as f:
        pass
    
    # Process songs concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        for artist, song in songs:
            future = executor.submit(get_song_lyrics, artist, song, total_songs)
            futures.append(future)
            time.sleep(0.1)  # Small delay between submissions
        
        # Wait for all to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                counter.increment()
    
    print("\n" + "=" * 60)
    print(f"Complete!")
    print(f"Total processed: {counter.value}")
    print(f"Successfully scraped: {counter.success}")
    print(f"Failed: {counter.value - counter.success}")
    print(f"Output saved to: {output_file}")

if __name__ == "__main__":
    main()