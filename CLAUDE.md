# CLAUDE.md

## Project Name
Music Guru — Computational Lyric & Music Intelligence Engine

## Purpose
Generic system that ingests an artist name and outputs a mathematical, linguistic, and structural analysis of their music and albums.

Not a recommendation engine.  
Not sentiment-based.  
Pure measurement.

---

## Core Philosophy

Raw Art  
→ Structured Language  
→ Numerical Features  
→ Mathematical Objects  
→ Comparative Distributions

Claims must be supported by metrics.

---

## System Architecture

Client (Next.js)  
→ FastAPI Gateway  
→ Job Queue (Celery + Redis)  
→ Analysis Engine (Python)  
→ PostgreSQL (metadata + results)  
→ DuckDB (analytics)

---

## Input

- Artist name  
- Optional album filter  
- Optional comparison set  

---

## Output

- Per-song metrics  
- Per-album aggregates  
- Cross-artist percentiles  
- Visualizations  
- JSON API  

---

## Analysis Modules

### 1. Text Processing
- Normalize  
- Tokenize  
- Lemmatize  
- POS tagging  
- Phonetic transcription  

### 2. Lexical Metrics
- Word frequency  
- Unique word ratio  
- Shannon entropy  
- Zipf slope  

### 3. Syllabic Metrics
- Syllables per word  
- Syllables per bar  
- Variance  

### 4. Rhyme Analysis
- Perfect rhyme detection  
- Near rhyme detection  
- Multisyllable chains  
- Rhyme graph  

### 5. Semantic Analysis
- Sentence embeddings  
- Cosine similarity  
- Topic clustering  

### 6. Flow Analysis
- BPM detection  
- Syllables per beat  
- Cadence FFT  

### 7. Statistical Layer
- Z-score normalization  
- Percentiles  
- Composite indices  

---

## Folder Structure

/apps/web  
/apps/api  
/engine  
  /ingest  
  /nlp  
  /rhyme  
  /audio  
  /semantic  
  /stats  
  /pipeline  
/db  
/scripts  

---

## Data Contracts

All modules accept:

{
  "song_id": "uuid",
  "text": "string",
  "audio_path": "string | null"
}

All modules output:

{
  "metric_name": number,
  "metadata": {}
}

---

## Composite Score Formula

technical_score =  
w1 * entropy +  
w2 * rhyme_density +  
w3 * multisyllable_rate +  
w4 * syllable_variance +  
w5 * semantic_coherence  

Weights configurable.

---

## Engineering Principles

- Deterministic outputs  
- No hidden heuristics  
- Every metric reproducible  
- Logs for every pipeline stage  

---

## Guardrails

- No subjective labels  
- No rankings without comparison set  
- No training proprietary models  

---

## MVP Milestones

1. Lyrics ingestion  
2. Tokenization + entropy  
3. Syllable counting  
4. Rhyme density  
5. Embeddings  
6. Simple frontend  

---

## Stretch Goals

- Audio cadence  
- Flow stress patterns  
- Metaphor detection  

---

## Success Criteria

System produces stable, reproducible metrics that place elite artists as statistical outliers across multiple dimensions.

---

## Example CLI

musicguru analyze --artist "J. Cole" --album "The Fall Off"

---

## Non-Goals

- Recommendation engine  
- Playlist generator  
- Opinionated reviews  

---

## License

MIT

