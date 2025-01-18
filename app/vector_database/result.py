import os
from dotenv import load_dotenv
from app.generate.gemini.reset_api_key import APIKeyManager
from app.generate.gemini.gemini import Gemini
from sentence_transformers import SentenceTransformer
from app.vector_database.vector_db import Qdrannt_VectorDB
from app.rerank.cohere import Cohere
from app.database.database_connection import DataBase_Connection
from app.articles.dao.articles_dao import Articles_Dao
from app.query.dao.query_dao import Query_Dao
from app.query.dto.query import Query
from langchain_huggingface import HuggingFaceEmbeddings
import os
load_dotenv()
MODEL_GENERATETOR = os.getenv("MODEL_GEMINI")
APIS_GEMINI_LIST = os.getenv('APIS_GEMINI_LIST').split(',')
MODEL_RERANKER = os.getenv("MODEL_RERANKER")
API_RERANKER=os.getenv("API_RERANKER").split(',')
EMBEDDING_QUERY=os.getenv("MODEL_EMBEDDING")

KEY_MANAGER_GEMINI = APIKeyManager(APIS_GEMINI_LIST)
KEY_MANAGER_COHERE=APIKeyManager(API_RERANKER)
URL_QDRANT=os.getenv("URL_QDRANT")
SERVER_NAME= os.getenv("SERVER_NAME")
DRIVER=os.getenv("DRIVER")
DATABASE_NAME=os.getenv("DATABASE_NAME")
# dbc=DataBase_Connection(SERVER_NAME,DRIVER,DATABASE_NAME)
# conn_string=dbc.open_connection()
# db=Articles_Dao(conn_string)
model_embedding_query=SentenceTransformer(EMBEDDING_QUERY)
embedding_search=HuggingFaceEmbeddings(model_name=EMBEDDING_QUERY)
model_reranker=Cohere(KEY_MANAGER_COHERE,MODEL_RERANKER,model_embedding_query)
model_gemini=Gemini(KEY_MANAGER_GEMINI,MODEL_GENERATETOR,model_embedding_query,model_reranker)


COLLECTION_NAME=os.getenv("COLLECTION_NAME")
keywords = [
        "không có nguyên lý", "không có quy luật mới", 
        "không đúc rút được", "trừu tượng hóa", "vận dụng", 
        "khái quát hóa", "khai thác", "công nhận", "sai lầm", 
        "chắp vá", "từ ngữ đời thường", "cóp nhặt", "mới mẻ", 
        "sáng tạo", "dân dã", "trừu tượng cao"
    ]
def result_query(original_query):
        vector_db=Qdrannt_VectorDB(COLLECTION_NAME,URL_QDRANT,embedding_search)
        query_obj=Query(original_query,keywords)
        query_dao=Query_Dao(vector_db)
        check_query_user=model_gemini.check_query(query_obj)
        print(type(check_query_user))
        if check_query_user=='0':
                generated_queries = model_gemini.generate_query(query_obj)
                print(generated_queries)
                check=""
                docs = query_dao.search_document_from_query(generated_queries,query_obj) 
                result_rerank=model_reranker.rerank_documents(query_obj, docs)
                if result_rerank==1:
                        response=model_gemini.generate_response_link(query_obj)
                        check="THÊM VÀO QDRANT"
                        return (f"{response}\n\n"
                                f"{check}")
                else:
                        response=model_gemini.generate_response(query_obj,result_rerank)
                        ranked_links = model_reranker.rerank_links(docs, response)
                        links_output = "\n".join([f"{link} (Điểm số liên quan: {score:.2f})" for link, score in ranked_links])
                        return (f"{response}\n\n"
                                f"Các đường link liên quan:\n{links_output}\n")
        elif check_query_user=='1':
                return f"""{model_gemini.generate_usually(query_obj)}"""
        elif check_query_user=='2' :
                return f"""{model_gemini.generate_introduction(query_obj)}"""
        elif check_query_user=='3':
                return f"""{'Xin lỗi bạn, tôi không được huấn luyện để trả lời câu hỏi này. Tôi chỉ hỗ trợ các câu hỏi liên quan đến chính trị Việt Nam và tư tưởng Hồ Chí Minh.'}"""