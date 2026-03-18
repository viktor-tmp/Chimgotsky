package com.example.chimgotskyapp

import android.os.Bundle
import android.widget.Button
import android.widget.TextView
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