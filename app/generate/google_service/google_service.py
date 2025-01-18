from googlesearch import search
from app.query.dto.query import Query
class GoogleSearchService:
    def search_google(self,query: Query, num_results: int = 10) -> str:
            results = search(query.query, num_results=num_results)
            links = []
            for result in results:
                links.append(result)
            if links:
                return links
            return 0