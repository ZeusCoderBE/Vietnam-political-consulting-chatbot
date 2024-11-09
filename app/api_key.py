
from dotenv import load_dotenv

# Tải biến môi trường từ tệp .env
load_dotenv()

class APIKeyManager:
    def __init__(self, keys):
        # Danh sách API keys
        self.keys = keys
        self.index = 0  # Chỉ số của key hiện tại

    def get_next_key(self):
        """
        Lấy API key tiếp theo trong danh sách và tăng chỉ số.
        """
        key = self.keys[self.index]
        self.index = (self.index + 1) % len(self.keys)  # Chuyển đến key tiếp theo
        return key

    def rotate_keys_on_error(self):
        """
        Nếu gặp lỗi với key hiện tại, chuyển sang key tiếp theo.
        """
        self.index = (self.index + 1) % len(self.keys)  # Chuyển đến key tiếp theo
        print(f"Chuyển sang sử dụng key mới: {self.keys[self.index]}")