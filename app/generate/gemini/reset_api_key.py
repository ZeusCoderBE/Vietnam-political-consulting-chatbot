from dotenv import load_dotenv
load_dotenv()
class APIKeyManager:
    def __init__(self, keys):
        self.keys = {key: 0 for key in keys}
        self.index = 0
        self.key_list = list(self.keys.keys())
    def get_next_key(self):
        if len(set(self.keys.values())) == 1:
            self.index = 0  
        key = self.key_list[self.index]
        self.keys[key] += 1 
        self.index = (self.index + 1) % len(self.key_list)
        return key
    def get_key_usage(self):
        return self.keys