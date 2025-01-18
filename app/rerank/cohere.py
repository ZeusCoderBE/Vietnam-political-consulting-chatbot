import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import cohere
from app.query.dto.query import Query
import os
from app.generate.gemini.reset_api_key import APIKeyManager
load_dotenv()
class Cohere:
    def __init__(self,key:APIKeyManager,cohere_model:str,embedding_query:SentenceTransformer) :
        self.key=key
        self.cohere_model=cohere_model
        self.embeddings_query=embedding_query

    def rerank_documents(self, query: Query, documents: List[Tuple]) -> List[Tuple[str, float]]:
       
        doc_contents = [doc.page_content for doc,_ in documents]
        doc_links = [doc.metadata['link'] for doc, _ in documents]
        try:
            co = cohere.ClientV2(self.key.get_next_key())
            response = co.rerank(
                model=self.cohere_model,
                query=query.query,
                documents=doc_contents,
                top_n=5,
            )
            reranked_results = response.results
            ranked_documents = [
                (doc_contents[res.index],doc_links[res.index], res.relevance_score) for res in reranked_results
            ]
        except Exception as e:
            print(e)
        low_score_count = sum(1 for _,_, score in ranked_documents if score < 0.5)
        print(low_score_count)
        if low_score_count == 5:
            return 1
        return ranked_documents
    def rerank_links_outside(self,query:Query,documents:List[Tuple])->List[str]:
        doc_contents = [doc.page_content for doc in documents]
        links=[link.metadata['link'] for link in documents]
        try:
            co = cohere.ClientV2(self.key.get_next_key())
            response = co.rerank(
                model=self.cohere_model,
                query=query.query,
                documents=doc_contents,
                top_n=5,
            )
            reranked_results = response.results
            ranked_links = [
                (links[res.index]) for res in reranked_results
            ]
        except Exception as e:
            print(e)
        return ranked_links
    def rerank_links(self, docs: List[Tuple], response: str) -> List[Tuple[str, float]]:
        
        doc_contents = [doc.page_content for doc,_ in docs]
        doc_links = [doc.metadata['link'] for doc, _ in docs]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(doc_contents)
        response_tfidf = tfidf_vectorizer.transform([response])
        scores_tfidf = cosine_similarity(response_tfidf, tfidf_matrix).flatten()
        
        response_embedding = self.embeddings_query.encode(response, convert_to_tensor=True)
        doc_embeddings = self.embeddings_query.encode(doc_contents, convert_to_tensor=True)
        scores_cosine = util.pytorch_cos_sim(response_embedding, doc_embeddings).squeeze(0).cpu().numpy()
        
        combined_scores = 0.7 * scores_cosine + 0.3 * scores_tfidf
        link_with_scores = list(zip(doc_links, combined_scores))
        
        sorted_links = sorted(link_with_scores, key=lambda x: x[1], reverse=True)
        seen_links = set()
        unique_sorted_links = [
            (link, score) for link, score in sorted_links if link not in seen_links and not seen_links.add(link)
        ]
        return unique_sorted_links[:5]
    