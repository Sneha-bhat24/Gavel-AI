from core.query_router import route_query
from tools.case_law_tool import search_case_law
from tools.constitution_tool import search_constitution


def retrieve_legal_context(query: str):
    """
    Main retrieval pipeline.
    Decides which knowledge sources to use and gathers evidence.
    """

    intent = route_query(query)

    case_data = None
    constitution_data = None

    # ---------- routing ----------
    if intent in ["case", "mixed"]:
        case_data = search_case_law(query)

    if intent in ["constitution", "mixed"]:
        constitution_data = search_constitution(query)

    # ---------- confidence ----------
    confidence_scores = []

    if case_data:
        confidence_scores.append(case_data["confidence"])

    if constitution_data:
        confidence_scores.append(constitution_data["confidence"])

    overall_confidence = (
        round(sum(confidence_scores) / len(confidence_scores), 2)
        if confidence_scores else 0
    )

    # ---------- structured evidence ----------
    evidence = {
        "intent": intent,
        "confidence": overall_confidence,
        "cases": case_data["cases"] if case_data else [],
        "constitution": constitution_data["articles"] if constitution_data else []
    }

    return evidence
