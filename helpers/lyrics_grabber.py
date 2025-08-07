import os
import lyricsgenius
from dotenv import load_dotenv
import re
import string


load_dotenv(".env")
token = os.getenv("GENIUS_API_TOKEN")


genius = lyricsgenius.Genius(token)

print("enter name of the artist")
artistName = input()

print("enter name of the song")
songName = input()

genius.verbose = False # Turn off status messages
genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
genius.skip_non_songs = False # Include hits thought to be non-songs (e.g. track lists)
genius.excluded_terms = ["(Remix)", "(Live)"] # Exclude songs with these words in their title
genius.album_comments = False

song = genius.search_song(songName, artistName)

cleaned_lines = []
punct_to_remove = ''.join(c for c in string.punctuation if c not in {"'", "-"})

for line in song.lyrics.split('\n')[1:]:  # Skip first line
    line = line.lower()
    line = re.sub(f"[{re.escape(punct_to_remove)}]", "", line)
    line = re.sub(r'\s+', ' ', line).strip()
    if line:  # Skip empty lines
        cleaned_lines.append(line)

# Now cleaned_lines is a list of cleaned lyric lines
for line in cleaned_lines:
    print(line)