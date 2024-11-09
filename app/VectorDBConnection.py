from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
def create_qdrant_environment(collection_name) -> QdrantVectorStore:
    return QdrantVectorStore.from_existing_collection(
        embedding=HuggingFaceBgeEmbeddings(model_name=MODEL_EMBEDDING),
        url="http://localhost:6333",
        collection_name=collection_name,
        retrieval_mode=RetrievalMode.DENSE,
        prefer_grpc=True,
        metadata_payload_key="metadata"
    )
