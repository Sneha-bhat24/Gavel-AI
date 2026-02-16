from utils.json_loader import load_all_cases, load_constitution

cases = load_all_cases()
print("Cases:", len(cases))
print(cases[0])

articles = load_constitution()
print("Articles:", len(articles))
print(articles[0])
