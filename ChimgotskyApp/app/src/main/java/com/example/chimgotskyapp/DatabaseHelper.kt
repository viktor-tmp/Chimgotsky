package com.example.chimgotskyapp

import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import java.io.File
import java.io.FileOutputStream

class DatabaseHelper(private val context: Context) : SQLiteOpenHelper(context, DB_NAME, null, DB_VERSION) {

    companion object {
        private const val DB_NAME = "lexicon.db"
        private const val DB_VERSION = 1
    }

    private val dbFile: File = context.getDatabasePath(DB_NAME)

    // Nhiệm vụ 3.1: Đọc và chép file từ assets
    fun prepareDatabase() {
        if (!dbFile.exists()) {
            dbFile.parentFile?.mkdirs()
            context.assets.open(DB_NAME).use { inputStream ->
                FileOutputStream(dbFile).use { outputStream ->
                    inputStream.copyTo(outputStream)
                }
            }
        }
    }

    override fun onCreate(db: SQLiteDatabase?) {
        // Không dùng đến vì DB đã được tạo sẵn từ Python
    }

    override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
        // Xử lý cập nhật DB nếu cần trong tương lai
    }
}