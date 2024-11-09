from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
import os
from langchain.docstore.document import Document
from dotenv import load_dotenv
import json
MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
load_dotenv()
def load_qdrant(path, collection_name='temp'):
    with open(path, 'r', encoding='utf-8') as json_file:
        documents = json.load(json_file)
    text_splitter = SemanticChunker(
        embeddings=HuggingFaceBgeEmbeddings(model_name=MODEL_EMBEDDING),
        buffer_size=4,
        breakpoint_threshold_type="gradient",
        breakpoint_threshold_amount=0.5,
        min_chunk_size=400,
    )
    documents_with_embeddings = []
    for doc in documents:
        content = doc["content"] 
        metadata = {
            "id": doc["id"],
            "link": doc["link"]
        }
        document = Document(page_content=content, metadata=metadata)
        chunks = text_splitter.split_documents([document])
        documents_with_embeddings.extend(
            Document(page_content=chunk.page_content, metadata=metadata) for chunk in chunks
        )
    QdrantVectorStore.from_documents(
        documents=documents_with_embeddings,
        embedding=HuggingFaceBgeEmbeddings(model_name=MODEL_EMBEDDING),  # Mô hình nhúng
        url="http://localhost:6333",
        collection_name=collection_name,
        retrieval_mode=RetrievalMode.DENSE,
        prefer_grpc=True,
        metadata_payload_key="metadata"
    )
    return 1

