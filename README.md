# Eksperimen Analisis Kriptografi Modern: DES, AES, dan RC4
**Tugas Eksperimen Mata Kuliah Kriptografi - Mahasiswa Teknik Informatika**

Repository ini berisi rangkaian eksperimen komprehensif untuk menganalisis dan membandingkan algoritme kriptografi modern (DES dan AES) serta representasi stream cipher (RC4) berdasarkan metrik performa dan keamanan.

---

## 📂 Struktur Proyek

Proyek ini disusun secara sistematis dalam folder berikut:

1.  **[`1_Dataset/`](./1_Dataset)**: Generator data dan kumpulan 100 file plainteks (Bahasa Indonesia) berukuran 1MB sebagai sampel uji.
2.  **[`2_Tahap_1_Basics/`](./2_Tahap_1_Basics)**: Perbandingan dasar antara DES dan AES menggunakan mode **ECB**. Berisi script performa, metrik keamanan, dan visualisasi dasar.
3.  **[`3_Tahap_2_Modes/`](./3_Tahap_2_Modes)**: Eksperimen mendalam mengenai berbagai **Mode Operasi** blok cipher (**CBC, CTR, GCM**) untuk menganalisis aspek kerahasiaan (*confidentiality*) dan integritas (*integrity*).
4.  **[`4_Tahap_3_Stream/`](./4_Tahap_3_Stream)**: Perbandingan antara **Block Cipher** (DES/AES) dengan **Stream Cipher** (**RC4**) untuk memahami perbedaan unit pemrosesan dan efisiensi waktu.
5.  **[`5_Laporan_Final/`](./5_Laporan_Final)**: Kumpulan laporan dokumentasi lengkap (.md), jawaban atas pertanyaan analisis, serta file Excel konsolidasi hasil akhir.

---

## 📋 Alur Eksperimen

Eksperimen dilakukan dalam 3 tahap utama:

### Tahap 1: Pengujian Baseline (ECB)
Menganalisis performa kecepatan dan keacakan (Entropi) pada mode paling dasar. Ditemukan bahwa sementara AES lebih cepat, mode ECB memiliki risiko keamanan tinggi (*pattern leakage*).

### Tahap 2: Eksperimen Mode Operasi
Menguji mode **CBC, CTR, dan GCM**. 
*   **CBC**: Menunjukkan efek longsor (*avalanche effect*) yang kuat (50%).
*   **CTR**: Menunjukkan performa tercepat karena paralelisme.
*   **GCM**: Terpilih sebagai standar keamanan modern karena fitur **Authenticated Encryption** (kerahasiaan + integritas).

### Tahap 3: Block vs Stream Cipher
Memasukkan **RC4** sebagai perbandingan. RC4 unggul dalam kecepatan software murni namun memiliki karakteristik keamanan yang berbeda (tidak ada perambatan error).

---

## 🚀 Cara Menjalankan

1.  **Persiapan Lingkungan**:
    Install dependencies: `pip install pycryptodome pandas numpy openpyxl matplotlib`
2.  **Generate Data**:
    Jalankan `python 1_Dataset/generate_data.py` untuk menghasilkan 100 file uji.
3.  **Eksekusi Analisis**:
    Jalankan script di setiap folder `Scripts` sesuai urutan tahapan (1, 2, dan 3).
4.  **Review Laporan**:
    Hasil akhir yang sudah dirangkum dapat dilihat di folder `5_Laporan_Final/Dokumentasi`.

---

## 📊 Hasil Utama
*   **Algoritme Tercepat**: AES (terutama dengan dukungan hardware) dan RC4.
*   **Algoritme Paling Aman**: **AES-GCM** (Keamanan terbaik untuk data modern).
*   **Metrik Keamanan**: Rata-rata Entropi cipherteks berhasil mencapai **~7.99**, membuktikan efektivitas pengacakan algoritme.

---

## 🛡️ Kesimpulan Keamanan
Hasil eksperimen merekomendasikan penggunaan **AES dalam mode GCM atau CTR** untuk aplikasi modern. Penggunaan **ECB (semua algoritme)** dan **DES (ukuran kunci kecil)** sudah tidak direkomendasikan untuk standar keamanan saat ini.

---
*Dibuat untuk memenuhi Tugas Eksperimen Kriptografi MG-6.*
