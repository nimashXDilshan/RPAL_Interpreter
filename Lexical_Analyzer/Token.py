class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value
    
    def __repr__(self):
        return f"<Token(type={self.type}, value={self.value})>"
