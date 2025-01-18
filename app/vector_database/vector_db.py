from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_huggingface import HuggingFaceEmbeddings

class Qdrannt_VectorDB:
    def __init__(self,collection_name:str,url:str,embedding_search:HuggingFaceEmbeddings) :
        self.collection_name=collection_name
        self.url=url
        self.embedding_search=embedding_search
    def create_qdrant_environment(self) -> QdrantVectorStore:
        return QdrantVectorStore.from_existing_collection(
            embedding=self.embedding_search,
            url= self.url,
            collection_name=self.collection_name,
            retrieval_mode=RetrievalMode.DENSE,
            metadata_payload_key="metadata"
        )