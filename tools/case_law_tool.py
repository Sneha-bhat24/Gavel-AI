import re
from utils.json_loader import load_all_cases


# -------- text helpers --------

def _tokenize(text):
    """Safely convert any field (str/list/None) into tokens"""
    if not text:
        return set()

    if isinstance(text, list):
        text = " ".join(str(t) for t in text)

    text = str(text).lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)

    return set(text.split())


def _match_score(query_tokens, case_tokens):
    if not case_tokens:
        return 0
    return len(query_tokens & case_tokens) / max(len(query_tokens), 1)


# -------- duplicate merge --------

def _merge_duplicate_cases(results):
    """
    Merge multiple chunks belonging to same judgment safely.
    Always converts key into a string.
    """
    merged = {}

    for score, case in results:

        title = case.get("title")
        ratio = case.get("ratio", "")

        # normalize title
        if isinstance(title, list):
            title = " ".join(str(t) for t in title)

        # fallback if title empty
        key = title if title else str(ratio)[:120]

        # ensure string key
        key = str(key)

        if key not in merged:
            merged[key] = (score, case)
        else:
            if score > merged[key][0]:
                merged[key] = (score, case)

    return list(merged.values())



# -------- scoring --------

def _score_case(query, case):
    query_tokens = _tokenize(query)

    summary_tokens = _tokenize(case.get("summary"))
    ratio_tokens = _tokenize(case.get("ratio"))
    issue_tokens = _tokenize(case.get("legal_issue"))
    section_tokens = _tokenize(case.get("sections"))

    score = 0

    # weighted semantic matching
    score += 0.35 * _match_score(query_tokens, ratio_tokens)
    score += 0.25 * _match_score(query_tokens, issue_tokens)
    score += 0.20 * _match_score(query_tokens, summary_tokens)
    score += 0.20 * _match_score(query_tokens, section_tokens)

    # combine with dataset quality (balanced)
    score = score * 0.8 + (case.get("quality_score", 0) / 100) * 0.2

    return round(score, 4)


# -------- public tool --------

def search_case_law(query: str, top_k: int = 3):

    cases = load_all_cases()

    scored = []
    for case in cases:
        relevance = _score_case(query, case)
        if relevance > 0.05:  # ignore weak matches
            scored.append((relevance, case))

    # sort by relevance
    scored.sort(key=lambda x: x[0], reverse=True)

    # merge duplicate judgments
    scored = _merge_duplicate_cases(scored)

    # prepare output
    results = []
    for score, case in scored[:top_k]:
        results.append({
            "case_title": case.get("title", "Unknown Case"),
            "court": case.get("court", "Unknown Court"),
            "legal_issue": case.get("legal_issue", ""),
            "ratio": case.get("ratio", ""),
            "decision": case.get("decision", ""),
            "relevance": round(score * 100, 2)
        })

    confidence = round(
        sum(r["relevance"] for r in results) / max(len(results), 1),
        2
    )

    return {
        "matches_found": len(results),
        "confidence": confidence,
        "cases": results
    }
