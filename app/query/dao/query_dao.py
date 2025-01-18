from qdrant_client.models import Filter, FieldCondition, MatchValue
from typing import List,Tuple
from app.vector_database.vector_db import Qdrannt_VectorDB
from app.query.dto.query import Query
class Query_Dao:
    def __init__(self,qdrant_exit:Qdrannt_VectorDB):
        self.qdrant_exit=qdrant_exit.create_qdrant_environment()
    def create_filter_query(self,user_keywords:List[str], metadata_fields: str) -> Filter:
            should_conditions = []
            for keyword_condition in user_keywords:
                should_conditions.append(FieldCondition(
                    key=metadata_fields, 
                    match=MatchValue(value=keyword_condition)
                ))

            return Filter(
                should=should_conditions
            )
    def search_document_from_query(self,generated_queries: List[str], keywords:Query) -> List[Tuple]:
            all_top_documents = []
            seen_documents = set()
            try:
                for query in generated_queries:
                    if query:
                        user_matched_keywords = [keyword for keyword in keywords.keyword if keyword in query.lower()]
                        filter_condition = self.create_filter_query(user_matched_keywords, 'metadata.keyword_sub') if user_matched_keywords else None
                        if filter_condition:
                            top_documents = self.qdrant_exit.similarity_search_with_score(query, k=5, filter=filter_condition)
                        else:
                            top_documents = self.qdrant_exit.similarity_search_with_score(query, k=5)
                        for doc, score in top_documents:
                            if hasattr(doc, 'page_content'):
                                doc_content = doc.page_content
                                if doc_content not in seen_documents:
                                    seen_documents.add(doc_content)
                                    all_top_documents.append((doc, score))
            except Exception as e:
                    print("co loi xay ra ",e)
            return all_top_documents