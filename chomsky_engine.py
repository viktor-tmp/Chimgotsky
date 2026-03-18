import sqlite3
import random
import os

class ChomskyPC:
    def __init__(self, db_name="lexicon.db"):
        # Tự động xác định đường dẫn tuyệt đối đến file database nằm cùng thư mục với script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_name)
        
        self.conn = None
        self.cursor = None
        self._connect()

        # Dữ liệu phục vụ Grammar Injection
        self.determiners = ['the', 'a', 'some', 'this', 'that']
        self.prepositions = ['in', 'on', 'at', 'with', 'by', 'from', 'to', 'under']
        self.vowels = ('a', 'e', 'i', 'o', 'u')

    def _connect(self):
        """Khởi tạo kết nối tới database."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Không tìm thấy file database tại: {self.db_path}")
        
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        """Đóng kết nối khi không còn sử dụng."""
        if self.conn:
            self.conn.close()

    def get_word(self, pos):
        """Truy vấn ngẫu nhiên một thực từ từ database."""
        pos_map = {'N': 'n', 'V': 'v', 'A': 'a', 'ADJ': 'a'}
        mapped_pos = pos_map.get(pos.upper(), pos.lower())
        
        if mapped_pos not in ['n', 'v', 'a']:
            return f"[{pos}]"

        self.cursor.execute('SELECT word FROM words WHERE pos = ? ORDER BY RANDOM() LIMIT 1', (mapped_pos,))
        result = self.cursor.fetchone()
        
        return result[0] if result else f"[{pos}]"

    def _conjugate_verb(self, verb):
        """Chia động từ theo ngôi thứ 3 số ít."""
        if verb.endswith(('s', 'ss', 'sh', 'ch', 'x', 'z', 'o')):
            return verb + 'es'
        elif verb.endswith('y') and len(verb) > 1 and verb[-2] not in self.vowels:
            return verb[:-1] + 'ies'
        else:
            return verb + 's'

    def generate_sentence(self, pattern):
        """Sinh câu dựa trên cấu trúc cho trước (VD: "DET ADJ N V")."""
        tokens = pattern.strip().split()
        words = []
        
        for token in tokens:
            token_upper = token.upper()
            
            if token_upper == 'DET':
                words.append(random.choice(self.determiners))
            elif token_upper == 'PREP':
                words.append(random.choice(self.prepositions))
            elif token_upper in ['N', 'V', 'ADJ']:
                word = self.get_word(token_upper)
                if token_upper == 'V':
                    word = self._conjugate_verb(word)
                words.append(word)
            else:
                words.append(token)
                
        # Xử lý mạo từ a/an
        for i in range(len(words) - 1):
            if words[i].lower() == 'a':
                next_word = words[i+1].lower()
                if next_word.startswith(self.vowels):
                    words[i] = 'an' if words[i].islower() else 'An'

        if words:
            sentence = " ".join(words)
            return sentence.capitalize() + "."
            
        return ""

# ----- CHẾ ĐỘ TƯƠNG TÁC TRÊN PC (INTERACTIVE MODE) -----
if __name__ == "__main__":
    try:
        engine = ChomskyPC()
        print("-" * 50)
        print("🦜 CHIMGOTSKY ENGINE - INTERACTIVE TERMINAL")
        print(f"Database: {engine.db_path}")
        print("-" * 50)
        print("HƯỚNG DẪN:")
        print("1. Nhấn [ENTER]      : Sinh câu ngẫu nhiên (mặc định)")
        print("2. Gõ 'N', 'V', 'ADJ' : Lấy 1 thực từ ngẫu nhiên")
        print("3. Gõ pattern tự chọn : Ví dụ 'DET N V DET N'")
        print("4. Gõ 'exit' hoặc 'q' : Thoát chương trình")
        print("-" * 50)

        while True:
            # Nhận input từ người dùng
            user_input = input("Chimgotsky > ").strip()
            
            # Lệnh thoát
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Tạm biệt Viktor! Đang đóng kết nối...")
                break
            
            # Xử lý lệnh lấy từ đơn
            cmd = user_input.upper()
            if cmd in ['N', 'V', 'ADJ', 'A']:
                word = engine.get_word(cmd)
                print(f"-> Result [{cmd}]: {word}")
            
            # Xử lý sinh câu
            else:
                # Nếu chỉ nhấn Enter, dùng pattern mặc định
                pattern = user_input if user_input else "DET ADJ N V PREP DET N"
                sentence = engine.generate_sentence(pattern)
                print(f"-> {sentence}")

        engine.close()

    except Exception as e:
        print(f"LỖI HỆ THỐNG: {e}")
