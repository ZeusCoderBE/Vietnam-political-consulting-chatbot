from app.generate.gemini.reset_api_key import APIKeyManager
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from app.query.dto.query import Query
from app.etl.etl import ETL
from app.rerank.cohere import Cohere
from app.generate.google_service.google_service import GoogleSearchService

class LinkReranker:
    def __init__(self, key_manager: APIKeyManager, model: str,model_reranker:Cohere):
        self.key_manager = key_manager
        self.model = model
        self.model_reranker=model_reranker
    def built_response_prompt_links(self, original_query:Query, links):
        processed_links = "\n".join([f"{i+1}. {link}" for i, link in enumerate(links)])
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", 
                """
                Bạn là một trợ lý AI chuyên gia về chính trị Việt Nam. 
                Nhiệm vụ của bạn là đặt tiêu đề cho các đường link dựa trên tiêu đề đường link và câu hỏi. 
                """),
                ("human", f"""
                **Câu hỏi của người dùng**:  
                '{original_query.query}'  

                **Danh sách các đường link**:
                {processed_links}

                **Yêu cầu định dạng**:
                1. Hiển thị thông báo: 
                "Xin lỗi bạn, với kiến thức của tôi, câu hỏi của bạn chưa thể được giải quyết. Dưới đây là các nguồn thông tin mà tôi tìm thấy thông qua tìm kiếm Google liên quan đến câu hỏi của bạn:"
                2. Danh sách các link được trình bày với định dạng sau:
                "[Số thứ tự]. Tiêu đề bài viết: đường link"
                ví dụ : 1.Ai là người sáng lập ra google: https://fptshop.com.vn/tin-tuc/danh-gia/ai-la-nguoi-sang-lap-ra-google-161035
                3. Không được:
                - Sắp xếp lại danh sách.
                - Thêm ký tự đặc biệt hoặc ký hiệu không cần thiết.
                4. Đảm bảo mỗi đường link nằm trên **một dòng riêng biệt**.
                """)
            ]
        )
        return prompt
    def generate_response_links(self,original_query: Query) -> str:
        model_gemini = ChatGoogleGenerativeAI(
            google_api_key=self.key_manager.get_next_key(),
            model=self.model,  
            max_tokens=1000,
            temperature=0, 
        )
        print("ĐÃ VÀO ĐÂY ĐỂ SẮP HẠNG LINK")
        search=GoogleSearchService()
        links=search.search_google(original_query)
        print(links)
        etl=ETL(links)
        list_links_content=etl.extract_data_from_link()
        link_reranked=self.model_reranker.rerank_links_outside(original_query,list_links_content)
        response_chain=self.built_response_prompt_links(original_query,link_reranked) |  model_gemini | StrOutputParser()
        final_response = response_chain.invoke({"original_query": original_query.query}).strip()
        return final_response
        