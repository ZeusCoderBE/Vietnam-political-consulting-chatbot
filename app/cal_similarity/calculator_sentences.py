import os
from sentence_transformers import SentenceTransformer,util
class Sentences:
    def __init__(self,sentences_a:str,sentences_b:str,embeddings_query:SentenceTransformer) :
        self.sentences_a=sentences_a
        self.sentences_b=sentences_b
        self.embeddings_query=embeddings_query
    def calculate_similarity(self) -> float:
            embedding1 = self.embeddings_query.encode(self.sentences_a, convert_to_tensor=True)
            embedding2 = self.embeddings_query.encode(self.sentences_b, convert_to_tensor=True)
            cosine_similarity = util.cos_sim(embedding1, embedding2).item()
            return cosine_similarity