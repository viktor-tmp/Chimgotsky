import sqlite3
import collections

def stress_test(db_path="lexicon.db", sample_size=10000):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Lấy mẫu ngẫu nhiên 10,000 dòng
        print(f"--- Đang rút trích {sample_size} mẫu ngẫu nhiên từ database... ---")
        cursor.execute("SELECT word, pos FROM words ORDER BY RANDOM() LIMIT ?", (sample_size,))
        results = cursor.fetchall()
        conn.close()

        if not results:
            print("Lỗi: Không tìm thấy dữ liệu trong database!")
            return

        words_only = [r[0] for r in results]
        pos_only = [r[1] for r in results]
        
        # 1. Kiểm tra trạng từ (pos = 'r')
        adverbs = [p for p in pos_only if p == 'r']
        
        # 2. Kiểm tra từ ghép (có dấu - hoặc _)
        compounds = [w for w in words_only if '-' in w or '_' in w]
        
        # 3. Kiểm tra độ trùng lặp (Collision)
        counter = collections.Counter(words_only)
        duplicates = {word: count for word, count in counter.items() if count > 1}
        
        print(f"\n✅ KẾT QUẢ KIỂM THỬ:")
        print(f"------------------------------------------")
        print(f"- Trạng từ lọt lưới: {len(adverbs)} (Yêu cầu: 0)")
        print(f"- Từ ghép lọt lưới: {len(compounds)} (Yêu cầu: 0)")
        print(f"- Tỷ lệ trùng lặp: {(len(duplicates)/sample_size)*100:.2f}% (Yêu cầu: < 0.1%)")
        print(f"- Số từ độc nhất trong mẫu: {len(set(words_only))}")
        print(f"------------------------------------------")
        
        if len(adverbs) == 0 and len(compounds) == 0:
            print("=> ĐÁNH GIÁ: DATABASE ĐẠT CHUẨN SẠCH.")
        else:
            print("=> ĐÁNH GIÁ: CẦN KIỂM TRA LẠI BỘ LỌC Ở GIAI ĐOẠN 1.")

    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")

if __name__ == "__main__":
    stress_test()
