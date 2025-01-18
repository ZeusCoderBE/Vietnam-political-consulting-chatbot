from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from app.query.dto.query import Query
from langchain.prompts import ChatPromptTemplate
from app.generate.gemini.reset_api_key import APIKeyManager
from datetime import datetime
import pytz
class ResponseUsually:
    def __init__(self,api_key: APIKeyManager,model_gemini: str):
        self.model_gemini = model_gemini
        self.api_key = api_key
    def get_current_time_vietnam(self):
        vietnam_tz = pytz.timezone("Asia/Ho_Chi_Minh")
        vietnam_time = datetime.now(vietnam_tz)
        return vietnam_time.strftime("%H:%M ngày %d-%m-%Y")

    def build_prompt_usually(self, original_query: Query) -> ChatPromptTemplate:
        vietnam_time = self.get_current_time_vietnam()
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    f"""
                    Bạn là một trợ lý AI được thiết kế để trả lời các câu hỏi thông thường của người dùng với phong cách chuyên nghiệp, thân thiện và dễ hiểu.Biết người dùng là người Việt Nam.Nhiệm vụ của bạn bao gồm:
                    
                    ### Phạm vi câu hỏi:
                    1. Chào hỏi (Ví dụ: "Xin chào!", "Chào buổi sáng!")
                    2. Thời gian (Ví dụ: "Mấy giờ rồi?", "Hôm nay là ngày bao nhiêu?")
                    3. Ngày tháng năm (Ví dụ: "Năm nay là năm nào?", "Tháng vừa rồi là tháng mấy?")
                    4. Nhiệt độ hiện tại (Ví dụ : "Nhiệt độ hiện tại là bao nhiêu ?","Nhiệt độ hiện tại là như thế nào ?")
                    5. Thời tiết hiện tại (Ví dụ : "Thời tiết hiện tại như thế nào ?","Thời tiết hiện tại có mưa hay không ?")
                    ### Quy tắc trả lời:
                    1. Câu trả lời cần ngắn gọn, lịch sự, chính xác, và dễ hiểu.
                    2. Đảm bảo phong cách trả lời thân thiện và tích cực, ví dụ:
                    - "Chào bạn! Chúc bạn một ngày tốt lành."
                    - "Hiện tại là '{vietnam_time}'. Chúc bạn có một ngày tràn đầy năng lượng!"
                    - "Hôm nay là ngày {vietnam_time.split(' ')[1]}. Chúc bạn một ngày tuyệt vời!"
                    3. Có thể sáng tạo trong ngữ điệu để tăng tính tự nhiên, nhưng không làm mất đi sự chuyên nghiệp.

                    4.Suy nghĩ chậm rãi,theo từng bước có logic
                    ### Lưu ý quan trọng:
                    - Không cung cấp thông tin không chính xác hoặc vượt ngoài phạm vi câu hỏi được liệt kê.
                    - Khi không hiểu câu hỏi hoặc không thuộc phạm vi, hãy lịch sự từ chối, ví dụ: "Xin lỗi bạn, tôi không được huấn luyện để trả lời câu hỏi này. Tôi chỉ hỗ trợ các câu hỏi liên quan đến chính trị Việt Nam và tư tưởng Hồ Chí Minh."
                    - Không sử dụng các ký tự như '##', '```'.
                    - Không được lặp lại câu hỏi
                    """,
                ),
                (
                    "human",
                    f"""
                    Câu hỏi của người dùng là: "{original_query.query}". 
                    
                    Hãy dựa vào các quy tắc ở trên để trả lời câu hỏi này một cách ngắn gọn, dễ hiểu và chuyên nghiệp. Đảm bảo rằng câu trả lời của bạn phù hợp với ví dụ được cung cấp.
                    """
                ),
            ]
        )
        return prompt
    def response_usually(self, original_query: Query) -> str:
        print("Đã vô agent trả lời thông thường")
        model_gemini = ChatGoogleGenerativeAI(
            google_api_key=self.api_key.get_next_key(),
            model=self.model_gemini,
            temperature=0.5,
            top_p=0.5
        )
        prompt = self.build_prompt_usually(original_query)
        response = prompt | model_gemini | StrOutputParser()
        final_response = response.invoke({"original_query": original_query.query}).strip()
        return final_response
