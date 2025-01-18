import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
from typing import List
from selenium import webdriver
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore,RetrievalMode
import os
from langchain.docstore.document import Document
from selenium.webdriver.chrome.options import Options
import requests
from dotenv import load_dotenv
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
COLLECTION_NAME=os.getenv("COLLECTION_NAME")
model_embeddings=HuggingFaceEmbeddings(model_name=MODEL_EMBEDDING)
class ETL:
    def __init__(self,links:List) :
        self.links=links
    def extract_data_from_link(self):
        contents = []
        edge_options = Options()
        edge_options.add_argument("--headless")
        edge_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
        driver = webdriver.Edge(options=edge_options)
        for link in self.links:
            try:
                response = requests.get(link, headers={"User-Agent": edge_options.arguments[-1]}, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    content = soup.get_text(strip=True)
                    contents.append(Document(page_content=content, metadata={"link": link}))
                    continue  
                driver.get(link)
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                content = soup.get_text(strip=True)
                contents.append(Document(page_content=content, metadata={"link": link}))
            except Exception as e:
                print(f"Lỗi khi truy cập link {link}: {e}")
                contents.append(Document(page_content="", metadata={"link": link}))
        driver.quit()
        return contents
    def load_qdrant(self,documents):
        print("Vào load")
        text_splitter = SemanticChunker(
            embeddings=model_embeddings,  
            buffer_size=4,  
            breakpoint_threshold_type="gradient", 
            breakpoint_threshold_amount=0.7,  
            min_chunk_size=500, 
        )
        documents_with_embeddings = []
        try:
            for doc in documents:
                chunks = text_splitter.split_documents([doc])
                documents_with_embeddings.extend(
                    Document(page_content=chunk.page_content, metadata=doc.metadata) for chunk in chunks
                )
            QdrantVectorStore.from_documents(
                            documents=documents_with_embeddings,
                            embedding=model_embeddings,  
                            url="http://localhost:6333",
                            collection_name=COLLECTION_NAME,
                            retrieval_mode=RetrievalMode.DENSE,
                            metadata_payload_key="metadata",
                            batch_size=128,
                            timeout=1000 ,
                )
            print(f"Đã thêm {len(documents_with_embeddings)} tài liệu mới vào collection '{COLLECTION_NAME}'.")
        except Exception as e:
                print(f"có lỗi gì đó {e}")
        return len(documents_with_embeddings)

    