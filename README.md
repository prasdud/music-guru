# music-guru
The ultimate music analyser software from profanity detection to in-depth rhyme scheme analysis plus a little extra.

MVP scope:

Core features:
– Search for a song by title/artist.
– Check local cache (DB + Redis).
– If not found, fetch lyrics from lyricsgenius API.
– Store lyrics, metadata, and analysis results.
– Run text analysis: profanity count, unique-word count, lexical diversity, readability metrics.
– Save results to user account.
– Public caching so repeated searches avoid API calls.
– Basic auth: signup, login, logout.
– Simple UI for searching and viewing results.
- Store all (maybe some) statistics in a global leaderboard that can be sorted by, ex- artist with most unique words, most profane words etc

Non-MVP (later):
– Background workers for heavy analysis.
– Dashboard for trends.
– Recommendations.
– Versioned analysis pipeline.

Project architecture:

Apps:

core: settings, middleware, utilities.

accounts: user model, auth flows, quotas.

catalog: Song, Artist, AnalysisResult models, caching logic, lyrics retrieval.

analysis: text-processing code, profanity lists, NLP utilities.

api: endpoints for search, results, and user actions.

dashboard (optional later): staff tools.

Models:
Artist(id, name, normalized_name, created_at)
Song(id, artist FK, title, normalized_title, lyrics_text, lyrics_fetched_at, api_source, cache_version, created_at)
AnalysisResult(id, song FK, version, profanity_count, unique_word_count, lexical_diversity, readability_score, computed_at)
UserSavedItem(id, user FK, song FK, saved_at)

Caching strategy:
Redis keys:
song:<artist>:<title> → song primary key
lyrics:<song_id>:<version> → lyrics text
analysis:<song_id>:<version> → analysis result blob
Expiry: lyrics long-lived; analysis tied to version; metadata short-lived.
Concurrency: lock key to avoid duplicate API calls.

Flow for search request:
– Normalize input.
– Check Redis for song key.
– If exists, load from DB + cached blobs.
– If not, check DB by normalized fields.
– If not present, acquire lock; call lyricsgenius; store lyrics; trigger analysis; store output.
– Return data to client.

Analysis pipeline:
– Tokenization.
– Profanity filter pass.
– Word-frequency calculation.
– Diversity metric (unique/total).
– Readability index formula.
– Pack into AnalysisResult.
– Version field ensures future upgrades don’t mix metrics.

Auth and permissions:
– Django user model with custom fields for quotas.
– Session-based login.
– User can save results; saved items appear in profile.
– Rate limiting middleware for anonymous users.

Middleware:
– request throttling for API abuse.
– cache bypass logic for staff.
– logging of external API requests.

Admin customizations:
– list filters for songs missing analysis.
– bulk re-analysis action.
– cache inspection page.
– API error log page.

API endpoints (MVP):
GET /search?query=
GET /song/<id>/
POST /song/<id>/save
GET /account/saved

Templates:
– search page
– song detail page with analysis
– profile page for saved songs
– basic login/signup

Deployment:
– Django + Gunicorn
– Redis for cache + locks
– Postgres for DB
– Celery/RQ optional for async tasks later
– Environment variables for API keys

MVP acceptance:
– Searching any song returns lyrics and analysis without failure.
– Repeated searches use cache.
– Logged-in users can save items.
– No duplicate external API calls during concurrency.
– Admin can view and fix entries.
