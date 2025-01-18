from typing import List, Tuple
from app.generate.gemini.reset_api_key import APIKeyManager
from app.rerank.cohere import Cohere
from app.generate.google_service.google_service import GoogleSearchService
from app.generate.process.link_reranker import LinkReranker
from app.generate.process.query_generator import QueryGenerator
from app.generate.process.response_generator import ResponseGenerator
from app.query.dto.query import Query
from sentence_transformers import SentenceTransformer
from app.generate.process.check_query import QueryRouter
from app.generate.process.response_introduction import ResponseIntroduction
from app.generate.process.response_usually import ResponseUsually

class Gemini: 
    def __init__(self, key_manager: APIKeyManager, model: str,model_embedding_query:SentenceTransformer,model_reranker:Cohere):
        self.query_generator = QueryGenerator(key_manager, model,model_embedding_query)
        self.response_generator = ResponseGenerator(key_manager, model)
        self.link_reranker = LinkReranker(key_manager, model,model_reranker)
        self.query_router=QueryRouter(key_manager,model)
        self.response_usually=ResponseUsually(key_manager,model)
        self.response_introduction=ResponseIntroduction(key_manager,model)
    def check_query(self,original_query:Query):
        return self.query_router.response_router(original_query)
    def generate_usually(self,original_query:Query):
        return self.response_usually.response_usually(original_query)
    def generate_introduction(self,original_query:Query):
        return self.response_introduction.response_introduction(original_query)
    def generate_query(self,original_query:Query):
        return self.query_generator.generate_query(original_query)
    def generate_response(self, original_query: Query, docs: List[Tuple]) -> str:
        return self.response_generator.generate_response(original_query, docs)
    def generate_response_link(self,original_query:Query):
        return self.link_reranker.generate_response_links(original_query)
    