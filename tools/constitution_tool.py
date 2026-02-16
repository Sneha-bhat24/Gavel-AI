import re
from utils.json_loader import load_constitution


# ---------- helpers ----------

def _tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return set(text.split())


def _match_score(query_tokens, text_tokens):
    if not text_tokens:
        return 0
    return len(query_tokens & text_tokens) / len(query_tokens)


def _extract_numbers(query):
    return re.findall(r'\d+[a-zA-Z]*', query)


# ---------- scoring ----------

def _score_article(query, article):
    query_tokens = _tokenize(query)

    title_tokens = _tokenize(article["title"])
    text_tokens = _tokenize(article["text"])
    desc_tokens = _tokenize(article["description"])

    score = 0

    # keyword similarity
    score += 0.4 * _match_score(query_tokens, title_tokens)
    score += 0.3 * _match_score(query_tokens, text_tokens)
    score += 0.3 * _match_score(query_tokens, desc_tokens)

    # strong boost if number mentioned (Article 21 etc.)
    numbers = _extract_numbers(query)
    for num in numbers:
        if num in str(article["article"]):
            score += 0.5

    return round(score, 4)


# ---------- public tool ----------

def search_constitution(query: str, top_k: int = 3):

    articles = load_constitution()

    scored = []
    for article in articles:
        relevance = _score_article(query, article)
        if relevance > 0.05:
            scored.append((relevance, article))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, art in scored[:top_k]:
        results.append({
            "article": art["article"],
            "title": art["title"],
            "description": art["description"][:400],
            "relevance": round(score * 100, 2)
        })

    confidence = round(sum(r["relevance"] for r in results) / (len(results) or 1), 2)

    return {
        "matches_found": len(results),
        "confidence": confidence,
        "articles": results
    }
