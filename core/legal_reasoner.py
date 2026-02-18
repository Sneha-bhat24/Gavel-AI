from core.llm import generate_text
from utils.prompt_loader import load_prompt


# ---------------- Formatting Helpers ----------------

def _format_cases(cases: list) -> str:
    """Convert case retrieval results into readable context for LLM."""
    if not cases:
        return "No relevant precedents found."

    formatted = []
    for c in cases:
        formatted.append(f"""
CASE: {c.get('case_title', 'Unknown Case')}
Court: {c.get('court', 'Unknown Court')}
Legal Issue: {c.get('legal_issue', 'Not specified')}
Principle (Ratio): {c.get('ratio', 'Not available')}
Decision: {c.get('decision', 'Not available')}
Relevance: {c.get('relevance', 0)}%
""")

    return "\n-------------------------\n".join(formatted)


def _format_constitution(articles: list) -> str:
    """Convert constitutional retrieval results into readable context."""
    if not articles:
        return "No specific statutory provisions found."

    formatted = []
    for a in articles:
        formatted.append(f"""
Article/Section: {a.get('article', 'Unknown')}
Title: {a.get('title', '')}
Description: {a.get('description', '')}
Relevance: {a.get('relevance', 0)}%
""")

    return "\n-------------------------\n".join(formatted)


# ---------------- Main Reasoning Function ----------------

def generate_legal_answer(query: str, evidence: dict) -> str:
    """
    Final reasoning step.
    Takes retrieved evidence and generates grounded legal response.
    Only ONE Gemini call happens here.
    """

    # Load external prompt template
    template = load_prompt("generation.txt")

    # Safely extract evidence
    cases = evidence.get("cases", [])
    constitution = evidence.get("constitution", [])

    # Format context
    cases_text = _format_cases(cases)
    constitution_text = _format_constitution(constitution)

    # Build final prompt
    prompt = template.format(
        question=query,
        cases=cases_text,
        constitution=constitution_text
    )

    # Call Gemini once
    response = generate_text(prompt)
    return response.strip()

