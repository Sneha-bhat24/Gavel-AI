from tools.case_law_tool import search_case_law

query = "Can in-laws be prosecuted under 498A without specific allegations?"

result = search_case_law(query)

from pprint import pprint
pprint(result)
