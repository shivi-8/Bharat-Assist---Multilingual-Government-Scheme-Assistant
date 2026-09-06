# Person 2 — Multilingual NLP & Retrieval — Step-by-Step Guide

This folder is self-contained: you don't need Person 1's real dataset yet.
`sample_schemes.json` is a small stand-in dataset so you can build and test
your whole module end to end, then swap in the real data later without
changing any code.

## Setup (do this once)

You'll need internet access to download model weights, so use Google Colab
if your machine doesn't have a reliable connection.

```bash
cd person2_retrieval
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Day 1 — Queries + pick an embedding model

Files: `data/queries_hi_en.json`, `scripts/embedding_model_test.py`

1. Open `data/queries_hi_en.json` — it already has 10 English + 10 Hindi
   test queries about common schemes (housing, health insurance, pensions,
   scholarships, LPG subsidy, skill training, maternity benefit, business
   loans). Read through them, tweak wording if you want, add a couple of
   your own if you think of good edge cases.
2. Run the model comparison script:
   ```bash
   python scripts/embedding_model_test.py
   ```
3. It tests two multilingual models by checking whether an English sentence
   and its Hindi translation land close together in vector space (they
   should) while an unrelated sentence lands far away. Whichever model
   shows the bigger gap between "matching" and "unrelated" similarity is
   the better pick.
4. Note down which model you picked — you'll hardcode it into
   `generate_embeddings.py` in Day 2.

**Commit your progress:**
```bash
git add data/queries_hi_en.json scripts/embedding_model_test.py
git commit -m "day1: added hindi+english test queries and embedding model comparison"
git push origin <your-branch-or-main>
```

## Day 2 — Sample dataset + generate embeddings

Files: `data/sample_schemes.json`, `scripts/generate_embeddings.py`

1. Look at `data/sample_schemes.json` — 8 real, well-known schemes (PM
   Awas Yojana, Ayushman Bharat, Ujjwala Yojana, old-age pension, Mudra
   Yojana, skill development, maternity benefit, SC/ST scholarship), each
   written in both English and Hindi. This stands in for Person 1's data
   until it's ready.
2. Open `scripts/generate_embeddings.py` and update `MODEL_NAME` to
   whichever model you picked on Day 1.
3. Run it:
   ```bash
   python scripts/generate_embeddings.py
   ```
   This creates `data/query_embeddings.npy` and `data/scheme_embeddings.npy`
   — the vector representations Day 3 will search over. These `.npy` files
   are git-ignored on purpose (they're regenerable and can get large);
   what you push is the *code* that produces them.

**Commit your progress:**
```bash
git add scripts/generate_embeddings.py
git commit -m "day2: sample dataset finalized and embeddings pipeline working"
git push origin <your-branch-or-main>
```

## Day 3 — Semantic similarity + Top-3 retrieval

Files: `scripts/retrieval.py`

1. Run it:
   ```bash
   python scripts/retrieval.py
   ```
2. For every one of the 20 test queries, it computes cosine similarity
   against all 8 sample schemes and prints the top 3 matches with scores.
3. **What to actually check:** does the top match make sense for each
   query? E.g. does q05 ("documents for Ayushman Bharat") return the
   Ayushman Bharat scheme at rank 1? Does a Hindi query about pensions
   (q14) correctly retrieve the English-language pension scheme entry,
   proving cross-lingual retrieval actually works?
4. Results are saved to `data/retrieval_results.json` — this is the file
   Person 3 will consume when wiring retrieval into the RAG prompt, so
   keep this format stable once it's working.

**Commit your progress:**
```bash
git add scripts/retrieval.py data/retrieval_results.json
git commit -m "day3: top-3 semantic retrieval implemented, tested across hindi and english"
git push origin <your-branch-or-main>
```

## If this is a brand-new git repo

If nobody has pushed anything yet:
```bash
git init
git remote add origin <your-repo-url>
git checkout -b person2-retrieval   # optional, if working on a branch per person
git add .
git commit -m "initial commit: person2 retrieval module skeleton"
git push -u origin person2-retrieval
```

If the repo already exists (shared with Person 1 and 3), just clone it and
work inside your `person2_retrieval/` folder so nobody's files collide:
```bash
git clone <your-repo-url>
cd <repo-name>
```

## What "done" looks like by Day 3

- `retrieval.py` runs without errors and prints sensible top-3 matches
- At least a few Hindi queries correctly retrieve schemes even though the
  scheme text you're testing against is a mix of Hindi and English
- `data/retrieval_results.json` exists and is committed — Person 3 needs it
- You can explain, in your own words, why cosine similarity between
  embeddings is what makes cross-lingual retrieval possible (this will
  come up when Sir checks progress)
