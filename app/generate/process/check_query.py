from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from app.query.dto.query import Query
from langchain.prompts import ChatPromptTemplate
from app.generate.gemini.reset_api_key import APIKeyManager

class QueryRouter:
    def __init__(self, api_key: APIKeyManager,model_gemini: str):
        self.model_gemini = model_gemini
        self.api_key = api_key

    def build_prompt_router(self, original_query: Query) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """Bạn là một chuyên gia phân loại câu hỏi của người dùng.Biết người dùng là người Việt Nam.
                Nhiệm vụ của bạn là phân loại câu hỏi của người dùng vào 3 lớp sau:
                1. Chính trị Việt Nam
                2. Chào hỏi thông thường
                3. Hỏi thông tin về bản thân bạn
                """),
                ("human", f"""Câu hỏi của người dùng là: "{original_query.query}".
                Nếu câu hỏi liên quan đến lĩnh vực chính trị Việt Nam, ví dụ:
                - "Tư tưởng Hồ Chí Minh là gì?"
                - "Tính sáng tạo của tư tưởng Hồ Chí Minh?"
                - "Quan điểm của Hồ Chí Minh về việc khai thác tư tưởng Nho giáo?"
                - "Tính mới mẻ trong tư tưởng Hồ Chí Minh?"
                - "Đổi mới trong tư tưởng Hồ Chí Minh là gì?"

                Thì trả ra 0.

                Nếu câu hỏi là chào hỏi thông thường, hỏi giờ, hỏi ngày, hỏi tháng, hỏi năm, ví dụ:
                - "Xin chào!"
                - "Chào"
                - "Mấy giờ rồi?"
                - "Ngày hiện tại là ngày bao nhiêu?"
                - "Tháng vừa rồi là tháng mấy?"
                - "Năm sau là năm mấy?"

                Thì trả ra 1.

                Nếu câu hỏi là hỏi thông tin về bạn như:
                - "Bạn là ai?"
                - "Ai đã tạo ra bạn?"
                - "Bạn có thể hỗ trợ tôi trong lĩnh vực nào?"
                - "Bạn được sinh ra vào năm nào?"
                - "Giới thiệu về bạn cho tôi biết"

                Thì trả ra 2.
                
                Cuối cùng nếu câu hỏi không thuộc tất cả các phạm vi đã nêu ở trên.
                
                thì trả ra 3.

                **Lưu ý**: Chỉ trả ra '0', '1' hoặc '2'. Không được thêm bất kỳ ký tự nào hay lời giải thích nào!
                """)
            ]
        )
        return prompt

    def response_router(self, original_query: Query) -> str:
        model_gemini = ChatGoogleGenerativeAI(
            google_api_key=self.api_key.get_next_key(),
            model=self.model_gemini,
            temperature=0,
        )
        prompt = self.build_prompt_router(original_query)
        response = prompt |model_gemini | StrOutputParser()
        final_response = response.invoke({"original_query": original_query.query}).strip()
        return final_response
