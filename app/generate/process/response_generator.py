from app.generate.gemini.reset_api_key import APIKeyManager
from langchain.prompts import ChatPromptTemplate
from app.query.dto.query import Query
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Tuple
from langchain_core.output_parsers import StrOutputParser
class ResponseGenerator:
    def __init__(self,key_manager:APIKeyManager,model:str):
        self.key_manager=key_manager
        self.model=model
    def build_response_prompt(self, original_query, context):
        context = "\n".join([doc for doc, _,_ in context])
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                "Bạn là một chuyên gia hàng đầu về chính trị Việt Nam, với nhiệm vụ cung cấp các câu trả lời chính xác, logic và mạch lạc dựa trên thông tin được cung cấp. Hãy đảm bảo câu trả lời tuân thủ hướng dẫn chi tiết sau."),

                ("human", f"""
                
                **Câu hỏi**:  
                '{original_query}'  

                **Thông tin cung cấp**:  
                {context}  

                **Yêu cầu trả lời**:  
                1. **Phân tích câu hỏi**:  
                - Hiểu rõ ý nghĩa câu hỏi, bao gồm các từ đồng nghĩa hoặc cách diễn đạt tương tự.  
                - Xác định các yếu tố chính cần giải đáp, tránh lạc đề hoặc bỏ sót thông tin.  
                
                2. **Cấu trúc câu trả lời**:  
                - Khi trả lời thì bắt buộc không lặp lại câu hỏi
                - Trả lời trực tiếp và ngắn gọn, mở đầu bằng câu khái quát ngắn thể hiện trọng tâm của câu trả lời. Ví dụ: khi hỏi "tư tường hồ chí minh là gì ?" thì câu mở đầu sẽ là: "Tư tưởng Hồ Chí Minh là nền tảng tư tưởng của cách mạng Việt Nam...".
                - Trả lời được tổ chức thành các mục đánh số, mỗi mục đề cập một khía cạnh chính,các ý trong cùng một mục phải liên quan đến tiêu đề mục đó,ghi trên trên cùng một dòng và sử dụng định dạng:  
                    **[Số thứ tự]. Tiêu đề mục**: Nội dung giải thích chi tiết trong cùng dòng không cần xuống dòng.  
                - Ví dụ:  
                    **1. Tư tưởng Hồ Chí Minh về độc lập dân tộc**: Tư tưởng Hồ Chí Minh khẳng định...  
                    **2. Vai trò cách mạng của Đảng Cộng sản Việt Nam**: Đảng đóng vai trò...  
                3. **Sử dụng thông tin cung cấp**:  
                - Chỉ dựa vào nội dung cung cấp. Không tự thêm thông tin bên ngoài.   

                4. **Xử lý trường hợp thiếu thông tin**:  
                - Nếu nội dung cung cấp không đủ để trả lời câu hỏi, hãy ghi: "Trong bộ dữ liệu không có thông tin."  

                5. **Chất lượng và phong cách trình bày**:  
                - Sử dụng ngôn từ chính xác, chuyên nghiệp và phù hợp với ngữ cảnh chính trị Việt Nam .
                - Bám sát nội dung được cung cấp không được thêm ý khác không liên quan vào.
                - Câu trả lời cần ngắn gọn, dễ hiểu, đồng thời phải đầy đủ và hợp lý.  
                - Các mục trả lời phải mạch lạc, có tính kết nối, tránh dư thừa.  
                - Kết thúc bằng một câu tóm tắt khái quát các ý chính trong câu trả lời.   
                 Hãy trả lời theo hướng dẫn trên. 
                    """)
            ]
        )
        return prompt
    def generate_response(self,origin_query:Query,docs:List[Tuple]):
        model_gemini=ChatGoogleGenerativeAI (
           google_api_key=self.key_manager.get_next_key(),
           model=self.model,
           temperature=0.1,
           max_tokens=3000,
           top_p=0.5
           
        )
        response=self.build_response_prompt(origin_query.query,docs)|model_gemini | StrOutputParser()
        final_response=response.invoke({"original_query": origin_query.query}).strip()
        return final_response
    
    