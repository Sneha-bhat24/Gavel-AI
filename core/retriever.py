from tools.case_law_tool import search_case_law
from tools.constitution_tool import search_constitution


def retrieve_legal_context(query: str):
    """
    Retrieval-first architecture.
    Always gathers evidence from all legal sources.
    No fragile intent detection.
    """

    # Retrieve both sources every time
    case_data = search_case_law(query, top_k=5)
    constitution_data = search_constitution(query, top_k=5)

    # confidence calculation
    confidence_scores = []

    if case_data and case_data["matches_found"] > 0:
        confidence_scores.append(case_data["confidence"])

    if constitution_data and constitution_data["matches_found"] > 0:
        confidence_scores.append(constitution_data["confidence"])

    overall_confidence = (
        round(sum(confidence_scores) / len(confidence_scores), 2)
        if confidence_scores else 0
    )

    # unified evidence
    evidence = {
        "intent": "auto",  # no manual intent
        "confidence": overall_confidence,
        "cases": case_data.get("cases", []),
        "constitution": constitution_data.get("articles", [])
    }

    print("Retrieved cases:", len(evidence["cases"]),
          "| articles:", len(evidence["constitution"]),
          "| confidence:", overall_confidence)

    return evidence
