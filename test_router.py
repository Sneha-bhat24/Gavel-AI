from core.query_router import route_query

queries = [
    "What is Article 21?",
    "Give me a similar dowry harassment case",
    "Can in-laws be arrested under 498A?",
    "Hello"
]

for q in queries:
    print(q, "→", route_query(q))
