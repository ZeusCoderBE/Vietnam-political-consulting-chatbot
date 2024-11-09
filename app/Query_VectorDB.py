import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple
from qdrant_client.models import Filter, FieldCondition, MatchValue
from googlesearch import search
from qdrant_client import QdrantClient
from app.VectorDBConnection import create_qdrant_environment
import shutil
import time
from app.Extract_Data import crawl_and_save_to_file
from app.Load_VectorDB import load_qdrant
from app.Transform_VectorDB import transform_data
load_dotenv()
MODEL_GENERATETOR = os.getenv("MODEL_GEMINI")
MODEL_EMBEDDING=os.getenv("MODEL_EMBEDDING")
MODEL_RERANK=os.getenv("MODEL_RERANK")
embeddings_query = SentenceTransformer(MODEL_EMBEDDING)
rerank_model = SentenceTransformer(MODEL_RERANK)
keywords = [
        "không có nguyên lý", "không có quy luật mới", 
        "không đúc rút được", "trừu tượng hóa", "vận dụng", 
        "khái quát hóa", "khai thác", "công nhận", "sai lầm", 
        "chắp vá", "từ ngữ đời thường", "cóp nhặt", "mới mẻ", 
        "sáng tạo", "dân dã", "trừu tượng cao"
    ]
def calculate_similarity(query1: str, query2: str) -> float:
    embedding1 = embeddings_query.encode(query1, convert_to_tensor=True)
    embedding2 = embeddings_query.encode(query2, convert_to_tensor=True)
    return util.pytorch_cos_sim(embedding1, embedding2).item()

def query_generator(original_query: str,API_GENERATETOR) -> List[str]:
    print(API_GENERATETOR)
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Bạn là một trợ lý chuyên gia về chính trị Việt Nam, có nhiệm vụ tạo ra nhiều truy vấn tìm kiếm dựa trên một truy vấn gốc."),
         ("human", f"Tạo 5 truy vấn tìm kiếm liên quan nhất đến: {original_query}. Mỗi truy vấn trên một dòng mới, và đảm bảo chỉ trả về các truy vấn, không có thêm bất kỳ giải thích hay văn bản nào khác.")] 
    )
    print("Đã Vào Đây")
    model = ChatGoogleGenerativeAI(
        google_api_key=API_GENERATETOR,
        model=MODEL_GENERATETOR,
        temperature=0.1,
        max_tokens=1000,
        top_p=0.3,
    )
    query_generator_chain = prompt | model | StrOutputParser()

    result = query_generator_chain.invoke({"original_query": original_query})
    generated_queries = result.strip().split('\n')
    valid_queries = [query for query in generated_queries if calculate_similarity(original_query, query) 
                     > 0.6]
    valid_queries.append(original_query)  
    return valid_queries
def create_should_filter(user_keywords: List[str], metadata_fields: str) -> Filter:
    should_conditions = []
    for keyword_condition in user_keywords:
        should_conditions.append(FieldCondition(
            key=metadata_fields, 
            match=MatchValue(value=keyword_condition)
        ))

    return Filter(
        should=should_conditions
    )
def rerank_documents(top_documents: List[Tuple], query_embedding) -> List[Tuple]:
    docs_with_scores = []
    doc_contents = [doc.page_content for doc, _ in top_documents if doc.page_content]
    if not doc_contents:
        raise ValueError("Không có nội dung tài liệu hợp lệ để xử lý TF-IDF.")
    tfidf_vectorizer = TfidfVectorizer() 
    tfidf_matrix = tfidf_vectorizer.fit_transform(doc_contents)
    query_tfidf = tfidf_vectorizer.transform([query_embedding])
    tfidf_scores = cosine_similarity(query_tfidf, tfidf_matrix).flatten()
    
    query_embedding = rerank_model.encode(query_embedding, convert_to_tensor=True)
    
    for (doc, _), tfidf_score in zip(top_documents, tfidf_scores):
        doc_embedding = rerank_model.encode(doc.page_content, convert_to_tensor=True)
        cosine_sim = util.pytorch_cos_sim(query_embedding, doc_embedding).item()
        combined_score = 0.8 * cosine_sim + 0.2 * tfidf_score
        docs_with_scores.append((doc, combined_score))
    
    return sorted(docs_with_scores, key=lambda x: x[1], reverse=True)
def search_qdrant(generated_queries: List[str], original_query: str,collection_name,check) -> List[Tuple]:
    qdrant_exit = create_qdrant_environment(collection_name)
    all_top_documents = []
    seen_documents = set()
    total_documents_searched = 0
    
    for query in generated_queries:
        if query:
            user_matched_keywords = [keyword for keyword in keywords if keyword in query.lower()]
            filter_condition = create_should_filter(user_matched_keywords, 'metadata.keyword_sub') if user_matched_keywords else None
            if filter_condition and check == 1:
                top_documents = qdrant_exit.similarity_search_with_score(query, k=5, filter=filter_condition)
            else:
                top_documents = qdrant_exit.similarity_search_with_score(query, k=5) 
            total_documents_searched += len(top_documents)
            for doc, score in top_documents:
                if hasattr(doc, 'page_content'):
                    doc_content = doc.page_content
                    if doc_content not in seen_documents:
                        seen_documents.add(doc_content)
                        all_top_documents.append((doc, score))
    reranked_docs = rerank_documents(all_top_documents, original_query)
    return reranked_docs[:5]
def rerank_links(docs: List[Tuple], response: str) -> List[str]:
    link_with_scores = []
    doc_contents = [doc.page_content for doc, _ in docs]

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(doc_contents)
    response_tfidf = tfidf_vectorizer.transform([response])
    scores_tfidf = cosine_similarity(response_tfidf, tfidf_matrix).flatten()

    response_embedding = rerank_model.encode(response, convert_to_tensor=True)

    for (doc, _), tfidf_score in zip(docs, scores_tfidf):
        doc_embedding = rerank_model.encode(doc.page_content, convert_to_tensor=True)
        cosine_score = util.pytorch_cos_sim(response_embedding, doc_embedding).item()
        combined_score = 0.7 * cosine_score + 0.3 * tfidf_score
        link_with_scores.append((doc.metadata['link'], combined_score))
    sorted_links = sorted(link_with_scores, key=lambda x: x[1], reverse=True)
    seen_links = set()
    unique_sorted_links = []
    for link, score in sorted_links:
        if link not in seen_links:
            seen_links.add(link)
            unique_sorted_links.append((link, score))

    return unique_sorted_links 
def prompt_template(docs: List[Tuple], original_query: str) -> str:
    context = "\n".join([doc.page_content for doc, _ in docs])
    response_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Bạn là một trợ lý chuyên gia về chính trị Việt Nam, có nhiệm vụ trả lời câu hỏi về chính trị Việt Nam nói chung hay tư tưởng Hồ Chí Minh nói riêng."),
            ("human", f"""
                Bạn hãy trả lời câu hỏi '{original_query}' dựa vào nội dung đã được cung cấp.
                Hãy lấy toàn bộ ý trong nội dung sau để trả lời:
                {context}
                Đảm bảo câu trả lời phải dài nhưng không thêm bất kỳ thông tin mới nào.Nếu không có câu trả lời trong nội dung đã được cung cấp, chỉ cần phản hồi "trong bộ dữ liệu không có thông tin".
            """)
        ]
    )
    return response_prompt
def generate_response(original_query: str, docs: List[Tuple],API_GENERATETOR) -> str:
    response_model = ChatGoogleGenerativeAI(
        google_api_key=API_GENERATETOR,
        model=MODEL_GENERATETOR,
        temperature=0.1,
        max_tokens=6000,
        top_p=0.6,
    )
    response_chain = prompt_template(docs, original_query) | response_model | StrOutputParser()
    final_response = response_chain.invoke({"original_query": original_query}).strip()
    ranked_links = rerank_links(docs, final_response)
    links_output = "\n".join([f"{link} (Điểm số liên quan: {score:.2f})" for link, score in ranked_links])
    return (f"{final_response}\n\n"
            f"Các đường link liên quan:\n{links_output}\n"
    )

def determine_user_query(original_query: str,API_GENERATETOR) -> int:
    examples: List[str] = [
        "Cho tôi thêm thông tin ngoài những ý bạn nói ở trên? : 1",
        "Cho tôi biết thêm một số khái niệm? : 1",
        "Ngoài những điều đã đề cập, còn có gì khác không? : 1",
        "Có thông tin nào khác liên quan đến chủ đề này không? : 1",
        "Có bạn hãy cho tôi thêm thông tin về vấn đề này? : 1",
        "Bạn có thể cung cấp thêm thông tin về vấn đề này không? : 1",
        "Có những khía cạnh nào khác mà tôi nên biết không? : 1",
        "Bạn có thể giải thích thêm về chủ đề này không? : 1",
        "Xin hãy cho tôi biết thêm về các giải pháp khả thi? : 1",
        "Có nguồn thông tin nào khác về điều này không? : 1",
        "Hãy cho tôi biết tính sáng tạo của tư tưởng Hồ Chí Minh? : 0",
        "Tư tưởng Hồ Chí Minh là gì? : 0",
        "Tính mới mẻ của tư tưởng Hồ Chí Minh? : 0",
        "Tính khai thác của tư tưởng Hồ Chí Minh thể hiện ở khía cạnh nào? : 0",
        "Bạn hãy khái quát hoá về tư tưởng Hồ Chí Minh? : 0",
        "Hãy mô tả về những điểm chính trong tư tưởng Hồ Chí Minh? : 0",
        "Tại sao tư tưởng Hồ Chí Minh lại quan trọng trong lịch sử Việt Nam? : 0",
        "Làm thế nào để áp dụng tư tưởng Hồ Chí Minh vào thực tiễn hiện nay? : 0",
        "Bạn có thể cho tôi biết những thành tựu nổi bật trong tư tưởng Hồ Chí Minh? : 0",
        "Tư tưởng Hồ Chí Minh có ảnh hưởng gì đến các chính sách hiện tại không? : 0"
    ]
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Bạn là một trợ lý hữu ích, có nhiệm vụ phân loại câu hỏi của người dùng vào một trong hai lớp: yêu cầu thêm thông tin hoặc yêu cầu giải thích cụ thể."),
            ("human", f"Hãy xác định xem câu hỏi sau đây: '{original_query}' thuộc vào lớp nào dựa vào các ví dụ này: {examples}. "
                     f"Nếu câu hỏi thuộc lớp yêu cầu thêm thông tin, hãy trả ra 1; nếu không, hãy trả ra 0. "
                     f"Tuyệt đối không trả lời bằng bất kỳ giá trị nào khác ngoài 0 hoặc 1.")
        ]
    )
    print("Da Vao Day")
    model = ChatGoogleGenerativeAI(
        google_api_key=API_GENERATETOR,
        model=MODEL_GENERATETOR,
        temperature=0,
        max_tokens=10,
    )
    query_generator_chain = prompt | model | StrOutputParser()
    result = query_generator_chain.invoke({"original_query": original_query})
    return int(result)  
def search_google(query: str, num_results: int = 5) -> str:
    results = search(query, num_results=num_results)
    links = []
    for result in results:
        links.append(result)
    if links:
        return links
    return 0
def execute_function(query):
    links = search_google(query)
    if links==0:
        print("Không tìm thấy thông tin")
    output_files=[]
    output_dir = '../data/data_temp/'
    for i, link in enumerate(links, start=1):
        output_file = os.path.join(output_dir, f'data_{i}.txt')  
        output_files.append(output_file)
        crawl_and_save_to_file(link, output_file)  # Gọi hàm lưu nội dung
    transform_data(output_files,links)
    load_qdrant('../data/data_temp/data_temp.json')
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir, exist_ok=True)
def result_query(original_query,API_GENERATETOR):
    generated_queries=query_generator(original_query,API_GENERATETOR)
    if determine_user_query(original_query,API_GENERATETOR) == 1:
       execute_function(original_query)
       docs = search_qdrant(generated_queries, original_query,'temp',check=0)
       final_response = generate_response(original_query, docs,API_GENERATETOR)
       client = QdrantClient(url="http://localhost:6333")
       client.delete_collection("temp")
       return final_response
    else:
       docs = search_qdrant(generated_queries, original_query,"document_embeddings_400_word_4",check=1)
       final_response = generate_response(original_query, docs,API_GENERATETOR)
       return final_response