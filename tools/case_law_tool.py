import re
from utils.json_loader import load_all_cases


# -------- text helpers --------

def _tokenize(text: str):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return set(text.split())


def _match_score(query_tokens, case_text_tokens):
    if not case_text_tokens:
        return 0
    return len(query_tokens & case_text_tokens) / len(query_tokens)


# -------- scoring --------

def _score_case(query, case):
    query_tokens = _tokenize(query)

    summary_tokens = _tokenize(case["summary"])
    ratio_tokens = _tokenize(case["ratio"])
    issue_tokens = _tokenize(case["legal_issue"])
    section_tokens = set(" ".join(case["sections"]).lower().split())

    score = 0

    score += 0.35 * _match_score(query_tokens, ratio_tokens)
    score += 0.25 * _match_score(query_tokens, issue_tokens)
    score += 0.20 * _match_score(query_tokens, summary_tokens)
    score += 0.20 * _match_score(query_tokens, section_tokens)

    # boost using dataset quality
    score *= (0.5 + case["quality_score"] / 200)

    return round(score, 4)


# -------- public tool --------

def search_case_law(query: str, top_k: int = 3):

    cases = load_all_cases()

    scored = []
    for case in cases:
        relevance = _score_case(query, case)
        if relevance > 0.05:  # ignore weak matches
            scored.append((relevance, case))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []
    for score, case in scored[:top_k]:
        results.append({
            "case_title": case["title"],
            "court": case["court"],
            "legal_issue": case["legal_issue"],
            "ratio": case["ratio"],
            "decision": case["decision"],
            "relevance": round(score * 100, 2)
        })

    confidence = round(sum(r["relevance"] for r in results) / (len(results) or 1), 2)

    return {
        "matches_found": len(results),
        "confidence": confidence,
        "cases": results
    }
