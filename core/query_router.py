import re

# ---------------- keyword banks ----------------

CONSTITUTION_WORDS = [
    "article", "constitution", "fundamental right", "legal provision",
    "ipc", "crpc", "section", "act", "law says", "under law",
    "meaning of", "define", "explain law"
]

CASE_WORDS = [
    "case", "judgment", "precedent", "court held", "court ruled",
    "similar case", "high court", "supreme court", "citation",
    "quashed", "appeal", "petition", "order passed"
]

ADVICE_WORDS = [
    "can i", "can we", "is it legal", "what happens if",
    "what should i do", "am i liable", "punishment", "arrest",
    "file complaint", "police", "charged", "falsely accused",
    "harassment", "dowry", "divorce", "bail", "fir"
]

NON_LEGAL = [
    "hello", "hi", "thanks", "thank you", "who are you"
]


# ---------------- helpers ----------------

def _score(text, keywords):
    score = 0
    for word in keywords:
        if word in text:
            score += 1
    return score


# ---------------- classifier ----------------

def route_query(query: str):
    q = query.lower()

    if any(x in q for x in NON_LEGAL):
        return "general"

    constitution_score = _score(q, CONSTITUTION_WORDS)
    case_score = _score(q, CASE_WORDS)
    advice_score = _score(q, ADVICE_WORDS)

    # boost if section/article number present
    if re.search(r'\b\d+[a-zA-Z]?\b', q):
        constitution_score += 1

    # decision logic
    scores = {
        "constitution": constitution_score,
        "case": case_score,
        "advice": advice_score
    }

    intent = max(scores, key=scores.get)

    if scores[intent] == 0:
        return "general"

    if intent == "advice":
        return "mixed"  # advice needs both law + case

    return intent
