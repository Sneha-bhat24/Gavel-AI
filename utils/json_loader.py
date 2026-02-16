import json
import os
from functools import lru_cache

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed")


# ---------------- Logging ----------------

def _log(msg):
    print(f"[DATA] {msg}")


# ---------------- Safe Loader ----------------

def _load_json_file(filename: str):
    path = os.path.join(DATA_PATH, filename)

    if not os.path.exists(path):
        _log(f"WARNING: {filename} not found")
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    _log(f"{filename} loaded ({len(data)} records)")
    return data


# ---------------- Quality Score ----------------

def _case_quality(case):
    score = 0

    if case["ratio"]: score += 0.4
    if case["summary"]: score += 0.2
    if case["legal_issue"]: score += 0.15
    if case["decision"]: score += 0.15
    if case["sections"] or case["acts"]: score += 0.1

    return round(score * 100, 2)


# ---------------- Normalization ----------------

def _normalize_case(raw, source):

    analysis = raw.get("analysis", {})
    metadata = raw.get("metadata", {})
    legal = raw.get("legal_elements", {})
    content = raw.get("content", {})

    case = {
        "id": metadata.get("case_number") or raw.get("source", ""),
        "title": metadata.get("case_title", ""),
        "court": metadata.get("court", ""),

        "summary": analysis.get("case_summary") or content.get("facts", ""),
        "legal_issue": analysis.get("legal_issue", ""),
        "ratio": analysis.get("ratio_decidendi", ""),
        "decision": analysis.get("final_judgment") or content.get("decision_or_order", ""),

        "sections": legal.get("sections", []),
        "acts": legal.get("acts", []),

        "source_file": source
    }

    case["quality_score"] = _case_quality(case)
    return case


def _normalize_constitution(raw):
    return {
        "article": raw.get("article") or raw.get("id"),
        "title": raw.get("title", ""),
        "text": raw.get("text", ""),
        "description": raw.get("description") or raw.get("explanation", "")
    }


# ---------------- Public APIs ----------------

@lru_cache(maxsize=1)
def load_all_cases():
    files = ["cases_sc.json", "cases_hc.json"]
    all_cases = []

    for file in files:
        raw_cases = _load_json_file(file)
        for c in raw_cases:
            all_cases.append(_normalize_case(c, file))

    # dataset stats
    if all_cases:
        avg_quality = sum(c["quality_score"] for c in all_cases) / len(all_cases)
        _log(f"Total cases: {len(all_cases)}")
        _log(f"Average dataset quality: {round(avg_quality,2)}%")

    return all_cases


@lru_cache(maxsize=1)
def load_constitution():
    raw = _load_json_file("constitution.json")
    articles = [_normalize_constitution(a) for a in raw]

    _log(f"Loaded {len(articles)} constitutional articles")
    return articles
