# 🦜 Chimgotsky Engine: Minimalist Offline NLG

**Chimgotsky** là một công cụ sinh ngôn ngữ tự nhiên (NLG) tối giản, lấy cảm hứng từ chủ nghĩa cấu trúc ngôn ngữ của Noam Chomsky. Hệ thống hoạt động **offline 100%**, sử dụng cơ sở dữ liệu SQLite được tối ưu hóa từ WordNet với hơn **80.000 thực từ**.

&lt;p align="center"&gt; &lt;img src="assets/ic_parrot.png" width="150" alt="Chimgotsky Mascot"&gt;

&lt;i&gt;"Linguistic Structuralism for Developers"&lt;/i&gt; &lt;/p&gt;

* * *

## 🚀 Tính năng nổi bật (Key Features)

- **Offline First:** Không cần Internet, không cần API Key, không phụ thuộc GPU/NPU.
    
- **Siêu nhẹ:** Toàn bộ "bộ não" 80.000 từ gói gọn trong file `.db` khoảng 20MB.
    
- **Đa nền tảng:** Chạy mượt mà trên cả Linux/Windows (Python) và Android (Kotlin).
    
- **Tốc độ cao:** Truy xuất trung bình **0.001s** nhờ hệ thống B-Tree Indexing.
    
- **Tự động hóa Ngữ pháp:** Tích hợp logic xử lý mạo từ (a/an) và chia động từ cơ bản.
    

* * *

## 🧩 1. Hệ thống Token & Cấu trúc Pattern

Engine giải mã các chuỗi mẫu (Pattern) để tạo ra câu. Bạn có thể chèn văn bản tĩnh xen kẽ các Token động.

| Token | Ý nghĩa | Ví dụ |
| --- | --- | --- |
| **N** | Danh từ (Noun) | *theory, system, parrot* |
| **V** | Động từ (Verb) | *analyzes, creates, flies* |
| **ADJ** | Tính từ (Adjective) | *dialectical, complex, teal* |
| **DET** | Định từ (Determiner) | *the, a, some, every* |
| **PREP** | Giới từ (Preposition) | *in, on, with, under* |


> **Ví dụ:** `"DET ADJ N V PREP DET N"` **Kết quả:** `"The dialectical system works with every theory."`

* * *

## 🐍 2. Tích hợp Python (PC Platform)

**Yêu cầu:** `chomsky_engine.py` và `lexicon.db` nằm cùng thư mục.

Python

```
from chomsky_engine import ChomskyPC

# 1. Khởi tạo Engine
engine = ChomskyPC("lexicon.db")

# 2. Lấy một thực từ ngẫu nhiên
noun = engine.get_word("N")

# 3. Sinh câu hoàn chỉnh
pattern = "DET ADJ N V"
sentence = engine.generate_sentence(pattern)

print(f"Output: {sentence}")
```

* * *

## 🤖 3. Tích hợp Android (Kotlin)

**Yêu cầu:** Đặt file `lexicon.db` vào thư mục `app/src/main/assets/`.

Kotlin

```
// 1. Khởi tạo Engine (Tự động sao chép DB từ assets)
val engine = ChomskyAndroid(this)

// 2. Lấy một từ đơn lẻ
val randomWord = engine.getWord("V")

// 3. Sinh câu hoàn chỉnh (Auto Capitalization & A/An Logic)
val finalSentence = engine.generateSentence("DET ADJ N V")

// 4. Giải phóng tài nguyên
engine.close()
```

* * *

## 🛠️ 4. Đặc tả Kỹ thuật (Technical Specs)

- **Data Source:** WordNet 3.1 Lexical Database.
    
- **Optimization:** SQLite Indexing trên cột `pos`.
    
- **Morphology:** Xử lý hậu tố ngôi thứ 3 số ít (`-s`, `-es`, `-ies`) và mạo từ tương thích nguyên âm.
    
- **Extensibility:** Dễ dàng mở rộng vốn từ bằng cách cập nhật bảng `words` trong SQLite mà không cần sửa code.
    

* * *

## 📄 Giấy phép (License)

Dự án phát hành dưới giấy phép **MIT**. Tự do sử dụng, chỉnh sửa và phân phối.

* * *

**© 2026 Chimgotsky Project** | Developed by **Viktor** on Ubuntu 24.04.

* * *
