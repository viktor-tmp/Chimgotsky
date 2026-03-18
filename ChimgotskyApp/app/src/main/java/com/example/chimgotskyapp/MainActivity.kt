package com.example.chimgotskyapp

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.os.Bundle
import android.widget.Button
import android.widget.ImageButton
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var engine: ChomskyAndroid
    private val historyList = mutableListOf<String>() // Lưu trữ lịch sử

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        engine = ChomskyAndroid(this)

        val tvResult = findViewById<TextView>(R.id.tvResult)
        val tvHistory = findViewById<TextView>(R.id.tvHistory)
        val btnCopy = findViewById<ImageButton>(R.id.btnCopy) // Nút Copy mới

        val btnN = findViewById<Button>(R.id.btnWordN)
        val btnV = findViewById<Button>(R.id.btnWordV)
        val btnA = findViewById<Button>(R.id.btnWordA)
        val btnSentence = findViewById<Button>(R.id.btnGenerateSentence)

        // Hàm hỗ trợ cập nhật kết quả và lịch sử
        fun updateOutput(content: String) {
            tvResult.text = content
            historyList.add(0, content) // Thêm vào đầu danh sách
            tvHistory.text = historyList.joinToString("\n---\n")
        }

        // --- XỬ LÝ SAO CHÉP (COPY) ---
        btnCopy.setOnClickListener {
            val textToCopy = tvResult.text.toString()

            // Chỉ sao chép nếu có văn bản và không phải là dòng gợi ý ban đầu
            if (textToCopy.isNotEmpty() && textToCopy != "Tap to generate...") {
                val clipboard = getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
                val clip = ClipData.newPlainText("Chimgotsky Output", textToCopy)
                clipboard.setPrimaryClip(clip)

                // Hiện thông báo dạng bong bóng (Toast) để chắc chắn là đã bấm được
                Toast.makeText(this, "Đã sao chép vào bộ nhớ tạm! 🦜", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Chưa có nội dung để sao chép!", Toast.LENGTH_SHORT).show()
            }
        }

        // Sự kiện tạo từ đơn Noun
        btnN.setOnClickListener {
            val word = engine.getWord("N")
            updateOutput("[Noun]: $word")
        }

        // Sự kiện tạo từ đơn Verb
        btnV.setOnClickListener {
            val word = engine.getWord("V")
            updateOutput("[Verb]: $word")
        }

        // Sự kiện tạo từ đơn Adjective
        btnA.setOnClickListener {
            val word = engine.getWord("ADJ")
            updateOutput("[Adj]: $word")
        }

        // Sự kiện tạo câu
        btnSentence.setOnClickListener {
            val sentence = engine.generateSentence("DET ADJ N V")
            updateOutput(sentence)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        engine.close()
    }
}