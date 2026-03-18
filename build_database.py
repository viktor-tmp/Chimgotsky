import sqlite3
import nltk
from nltk.corpus import wordnet as wn

# Tải dữ liệu WordNet nếu chưa có
nltk.download('wordnet')

def create_lexicon_db(db_name="lexicon.db"):
    # Nhiệm vụ 1.3: Kết nối và khởi tạo SQLite
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Tạo bảng lưu trữ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            pos TEXT NOT NULL,
            UNIQUE(word, pos)
        )
    ''')

    # Xóa dữ liệu cũ nếu chạy lại script để tránh lỗi
    cursor.execute('DELETE FROM words')

    # Sử dụng tập hợp (set) để loại bỏ các từ trùng lặp cùng từ loại
    lexicon_set = set()

    # Nhiệm vụ 1.2: Các nhãn POS được phép (Danh từ, Động từ, Tính từ)
    allowed_pos = {'n', 'v', 'a'}

    print("Đang quét WordNet và lọc dữ liệu...")

    # Nhiệm vụ 1.1: Quét toàn bộ synsets trong WordNet
    for synset in wn.all_synsets():
        pos = synset.pos()
        
        # WordNet phân loại thêm 's' (satellite adjective), ta gộp chung vào 'a' (adjective)
        if pos == 's':
            pos = 'a'

        if pos in allowed_pos:
            for lemma in synset.lemmas():
                word = lemma.name().lower()

                # Nhiệm vụ 1.2: Lọc bỏ từ ghép (có '_' hoặc '-') và đảm bảo chỉ chứa chữ cái
                if '_' not in word and '-' not in word and word.isalpha():
                    lexicon_set.add((word, pos))

    print(f"Đã trích xuất thành công {len(lexicon_set)} thực từ đơn độc lập.")
    print("Đang ghi vào cơ sở dữ liệu SQLite...")

    # Đưa dữ liệu vào bảng
    cursor.executemany('''
        INSERT OR IGNORE INTO words (word, pos)
        VALUES (?, ?)
    ''', list(lexicon_set))

    # Nhiệm vụ 1.3: Tạo chỉ mục (Index) theo cột 'pos' để tăng tốc độ truy vấn ngẫu nhiên (ORDER BY RANDOM)
    print("Đang thiết lập Indexing...")
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_pos ON words(pos);')

    conn.commit()
    conn.close()
    print(f"Hoàn tất! Cơ sở dữ liệu đã được lưu tại file: {db_name}")

if __name__ == "__main__":
    create_lexicon_db()
