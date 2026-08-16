import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from genai.query_parser import QueryParser
from engine.retrieval import RetrievalEngine
from engine.ranking import RankingEngine

query = "pizza"

parser = QueryParser()
parsed = parser.parse_query(query, context={})
print("Parsed Query:", parsed)

retriever = RetrievalEngine()
candidates = retriever.retrieve_candidates(parsed)
print("Candidates found:", len(candidates))
for c in candidates:
    print(c['name'], c.get('cuisines'))

