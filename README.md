# Greek Parliament Speeches — Information Retrieval

A web application that applies Information Retrieval techniques to the proceedings of the Hellenic Parliament (1989–2020), featuring keyword extraction, speaker similarity, and topic modeling via LSI.

---

## Features

- **Keyword Extraction** — Identifies the most significant terms per speech, per MP, or per party using TF-IDF weights
- **Speaker Similarity** — Computes pairwise similarity between MPs based on their speech vectors
- **Latent Semantic Indexing (LSI)** — Uncovers thematic topics across parliamentary speeches using SVD
- **Search** — Query speeches using TF-IDF dot product scoring
- **Web Interface** — Local Flask app with a Jinja + Bootstrap frontend

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Backend | Flask |
| Frontend | Jinja2 + Bootstrap |
| Database | SQLite |
| NLP | `greek_stemmer_plus` |
| IR / ML | `scikit-learn` (SVD), `scipy` (sparse matrices) |
| Dataset | Greek Parliament Proceedings 1989–2020 |

---

## How It Works

### Text Processing (`text_processor.py`)
Raw speech text is cleaned with regular expressions, then stemmed using `greek_stemmer_plus`. A stem-to-word map is maintained to keep results human-readable.

### TF-IDF (`tfidf.py`)
Custom TF-IDF implementation using:

```
tf(t, d)  = 1 + log(f_td)
idf(t)    = log((N + 1) / df(t))
weight    = tf(t, d) * idf(t)
```

Weights are stored in a `scipy` sparse matrix. Search uses raw dot product (found to outperform cosine similarity for this dataset).

### Keywords (`keywords.py`)
Top-weighted terms are extracted per speech, MP, or party from the TF-IDF matrix.

### LSI (`lsi.py`)
Each speech is projected into a latent semantic space via SVD. A mean vector is computed per MP and used for pairwise similarity comparisons.

---

## Getting Started

### Prerequisites
- Python 3.13 (not compatible with 3.14+)
- The dataset file: `Greek_Parliament_Proceedings_1989_2020.csv` placed in the project root

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

The app will open automatically in your browser. If not, navigate to [http://localhost:5000](http://localhost:5000).

Note: The first launch may be slow due to initial computations. Results are cached for faster subsequent runs.

---

## Author

- Άγγελος Μανουσέλης — [manousela@csd.auth.gr](mailto:manousela@csd.auth.gr)

*Department of Computer Science, Aristotle University of Thessaloniki*