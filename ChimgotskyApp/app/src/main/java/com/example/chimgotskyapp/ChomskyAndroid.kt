package com.example.chimgotskyapp

import android.content.Context
import android.database.sqlite.SQLiteDatabase

class ChomskyAndroid(context: Context) {
    private val dbHelper = DatabaseHelper(context)
    private var database: SQLiteDatabase? = null

    private val determiners = listOf("the", "a", "some", "this", "that")
    private val prepositions = listOf("in", "on", "at", "with", "by", "from", "to", "under")
    private val vowels = listOf('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')

    init {
        dbHelper.prepareDatabase()
        // Tối ưu bộ nhớ (Nhiệm vụ 3.3): Mở kết nối 1 lần và giữ nguyên để dùng lại
        database = dbHelper.readableDatabase
    }

    fun close() {
        database?.close()
        dbHelper.close()
    }

    // Nhiệm vụ 3.2: Tái cấu trúc logic sinh từ
    fun getWord(pos: String): String {
        val mappedPos = when (pos.uppercase()) {
            "N" -> "n"
            "V" -> "v"
            "A", "ADJ" -> "a"
            else -> return "[$pos]"
        }

        var word = "[$pos]"
        val query = "SELECT word FROM words WHERE pos = ? ORDER BY RANDOM() LIMIT 1"

        // Tối ưu bộ nhớ (Nhiệm vụ 3.3): Hàm use {} đảm bảo Cursor luôn bị đóng (close)
        // ngay sau khi dùng xong, chống rò rỉ bộ nhớ (Memory Leak) làm treo app.
        database?.rawQuery(query, arrayOf(mappedPos))?.use { cursor ->
            if (cursor.moveToFirst()) {
                word = cursor.getString(0)
            }
        }
        return word
    }

    private fun conjugateVerb(verb: String): String {
        return when {
            verb.endsWith("s") || verb.endsWith("ss") || verb.endsWith("sh") ||
                    verb.endsWith("ch") || verb.endsWith("x") || verb.endsWith("z") || verb.endsWith("o") -> verb + "es"
            verb.endsWith("y") && verb.length > 1 && verb[verb.length - 2] !in vowels -> verb.dropLast(1) + "ies"
            else -> verb + "s"
        }
    }

    // Nhiệm vụ 3.2: Tái cấu trúc logic sinh câu
    fun generateSentence(pattern: String): String {
        val tokens = pattern.trim().split("\\s+".toRegex())
        val words = mutableListOf<String>()

        for (token in tokens) {
            when (val tokenUpper = token.uppercase()) {
                "DET" -> words.add(determiners.random())
                "PREP" -> words.add(prepositions.random())
                "N", "ADJ" -> words.add(getWord(tokenUpper))
                "V" -> words.add(conjugateVerb(getWord("V")))
                else -> words.add(token) // Văn bản tĩnh
            }
        }

        // Morphology: Xử lý mạo từ a/an
        for (i in 0 until words.size - 1) {
            if (words[i].equals("a", ignoreCase = true)) {
                val nextWord = words[i + 1]
                if (nextWord.isNotEmpty() && nextWord.first() in vowels) {
                    words[i] = "an"
                }
            }
        }

        // Viết hoa chữ cái đầu và thêm dấu chấm
        if (words.isNotEmpty()) {
            val sentence = words.joinToString(" ")
            return sentence.replaceFirstChar { it.uppercase() } + "."
        }

        return ""
    }
}