from app.generate.gemini.reset_api_key import APIKeyManager
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from typing import List
from sentence_transformers import SentenceTransformer
from langchain.prompts import ChatPromptTemplate
from app.cal_similarity.calculator_sentences import Sentences
from app.query.dto.query import Query
class QueryGenerator:
    def __init__(self,key_manager:APIKeyManager,model:str,model_embedding_query:SentenceTransformer):
        self.key_manager=key_manager
        self.model = model
        self.model_embedding_query=model_embedding_query
    def build_query_prompt(self, original_query: Query):
        prompt = ChatPromptTemplate.from_messages(
            [("system", 
            "Bạn là một chuyên gia nghiên cứu về chính trị Việt Nam. Nhiệm vụ của bạn là tạo ra 4 câu truy vấn tìm kiếm có ngữ nghĩa gần giống nhất với một truy vấn gốc. "
            "Câu truy vấn tạo sinh phải đảm bảo không thay đổi ngữ nghĩa so với câu truy vấn gốc và đạt tỷ lệ giống ngữ nghĩa ít nhất 85%. "
            "Cấu trúc khi tạo câu truy vấn mới, bạn có thể thay đổi vị trí của các thành phần trong câu gốc, hoặc giữ nguyên các phần quan trọng như chủ ngữ, vị ngữ, động từ và tính từ. Bạn chỉ cần thêm các thành phần phụ vào câu để làm phong phú thêm nội dung, sao cho câu truy vấn mới không thay đổi ý nghĩa so với câu gốc."
            "Ví dụ: "
            "- 'Quan điểm của Hồ Chí Minh về khai thác di sản tư tưởng của Nho giáo?' có thể đổi thành:"
            "   + 'Về khai thác di sản tư tưởng của Nho giáo, Hồ Chí Minh quan điểm như thế nào?'"
            "   + 'Hồ Chí Minh có quan điểm như thế nào về việc khai thác di sản tư tưởng của Nho giáo?'"
            "   + 'Khai thác di sản tư tưởng của Nho giáo theo quan điểm của Hồ Chí Minh là như thế nào?'"
            "- 'Tính mới mẻ của tư tưởng Hồ Chí Minh là gì?' có thể đổi thành:"
            "   + 'Tính mới mẻ trong tư tưởng Hồ Chí Minh được hiểu như thế nào?'"
            "   + 'Hãy giải thích tính mới mẻ trong tư tưởng của Hồ Chí Minh?'"
            "   + 'Trong tư tưởng Hồ Chí Minh, tính mới mẻ có ý nghĩa như thế nào?'"
            "- 'Những phẩm chất thiên tài kết hợp với hoạt động thực tiễn của Hồ Chí Minh thể hiện ở đâu?' có thể đổi thành:"
            "   + 'Phẩm chất thiên tài và hoạt động thực tiễn của Hồ Chí Minh thể hiện như thế nào?'"
            "   + 'Hồ Chí Minh có phẩm chất thiên tài kết hợp với hoạt động thực tiễn được thể hiện ở đâu?'"
            "   + 'Sự kết hợp giữa phẩm chất thiên tài và hoạt động thực tiễn của Hồ Chí Minh được thể hiện như thế nào?'"
            "- 'Tư tưởng Hồ Chí Minh là gì?' có thể đổi thành:"
            "   + 'Hãy định nghĩa tư tưởng Hồ Chí Minh là gì?'"
            "   + 'Tư tưởng Hồ Chí Minh được định nghĩa như thế nào?'"
            "   + 'Ý nghĩa của tư tưởng Hồ Chí Minh là gì?'"
            "- 'Tính sáng tạo của tư tưởng Hồ Chí Minh thể hiện ở đâu?' có thể đổi thành:"
            "   + 'Trong tư tưởng Hồ Chí Minh, tính sáng tạo được thể hiện như thế nào?'"
            "   + 'Tính sáng tạo trong tư tưởng Hồ Chí Minh được biểu hiện ở đâu?'"
            "   + 'Hãy nêu rõ các điểm thể hiện tính sáng tạo của tư tưởng Hồ Chí Minh?'"),
            ("human", f"Vui lòng tạo ra 4 câu truy vấn tìm kiếm liên quan nhất đến: {original_query.query}. Chỉ trả về 4 câu truy vấn, không giải thích gì thêm.")]
        )
        return prompt


    def generate_query(self,original_query:Query) -> List[str]:
        prompt=self.build_query_prompt(original_query)
        print("Đã vô Đây")
        model_gemini = ChatGoogleGenerativeAI(
            google_api_key=self.key_manager.get_next_key(),
            model=self.model,  
            max_tokens=1000,
            temperature=0, 
        )
        query_generator_chain = prompt | model_gemini | StrOutputParser()  
        result = query_generator_chain.invoke({"original_query": original_query.query})
        generated_queries = result.strip().split('\n')
        cleaned_queries = [re.sub(r'^\d+\.\s*', '', query).strip() for query in generated_queries] 
        valid_queries=[]
        for query in cleaned_queries:
                sentences=Sentences(original_query.query, query,self.model_embedding_query)
                if sentences.calculate_similarity()>=0.5:
                    valid_queries.append(query)
                else :
                    continue
        valid_queries.append(original_query.query)
        return valid_queries