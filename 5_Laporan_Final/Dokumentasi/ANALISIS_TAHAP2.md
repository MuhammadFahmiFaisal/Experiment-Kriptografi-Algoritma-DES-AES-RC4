# Analisis Eksperimen Tahap 2: Mode Operasi Cipher Blok
## Perbandingan CBC, CTR, dan GCM

Tahap ini mengevaluasi bagaimana mode operasi yang berbeda mempengaruhi performa, ukuran data, dan fitur keamanan (Confidentiality vs Integrity).

---

### 1. Mengenal Mode Operasi Cipher Blok

| Mode | Mekanisme Enkripsi | Mekanisme Dekripsi | Mendukung Paralelisme (Y/N) | Integrity Protection (Y/N) |
| :--- | :--- | :--- | :---: | :---: |
| **ECB** | Setiap blok dienkripsi independen dengan kunci yang sama. | Setiap blok didekripsi independen. | **Y** | **N** |
| **CBC** | Setiap blok plainteks di-XOR dengan cipherteks sebelumnya sebelum dienkripsi (menggunakan IV untuk blok pertama). | Cipherteks didekripsi lalu di-XOR dengan cipherteks sebelumnya. | **N** (Enkripsi sekuensial) | **N** |
| **CTR** | Mengenkripsi nilai Counter (Nonce + Counter) lalu hasilnya di-XOR dengan plainteks. | Sama dengan enkripsi (mengenkripsi Counter lalu XOR dengan cipherteks). | **Y** | **N** |
| **GCM** | Menggunakan mode CTR untuk enkripsi dan menambahkan mekanisme GHASH untuk autentikasi. | Melakukan dekripsi CTR dan memverifikasi tag autentikasi (MAC). | **Y** | **Y** (Authenticated Encryption) |

---

### 2. Analisis Hasil Eksperimen

#### Performa Relatif Antar Mode
*   **CTR** biasanya adalah yang tercepat karena mekanisme XOR-nya sangat efisien dan mendukung paralelisme penuh. CTR juga tidak memerlukan *padding*, sehingga menghindari overhead pada data.
*   **CBC** sedikit lebih lambat karena sifatnya yang berantai (*chaining*), yang berarti blok berikutnya tidak bisa diproses sebelum blok sebelumnya selesai dienkripsi.
*   **GCM** memberikan performa yang sangat baik pada prosesor modern. Meskipun melakukan tugas tambahan (menghitung tag integritas), GCM tetap cepat karena berbasis CTR dan mendukung paralelisme.

#### Perubahan Ukuran Cipherteks
*   **ECB & CBC**: Ukuran cipherteks bertambah sedikit karena adanya **Padding** (agar sesuai dengan ukuran blok 8 atau 16 byte).
*   **CTR**: Ukuran cipherteks **identik** dengan plainteks karena berperan sebagai *stream cipher* (tidak perlu padding).
*   **GCM**: Ukuran cipherteks sama dengan plainteks, namun ada tambahan **Tag Autentikasi** (biasanya 16 byte per proses) yang disimpan untuk keperluan verifikasi integritas.

#### Perbedaan Keamanan: Confidentiality vs Integrity
*   **ECB, CBC, CTR**: Hanya memberikan **Confidentiality** (Kerahasiaan). Jika penyerang mengubah satu bit pada cipherteks, kita mungkin mendapatkan data sampah saat dekripsi, tapi kita tidak tahu secara otomatis bahwa data telah dimanipulasi.
*   **GCM**: Memberikan **Confidentiality AND Integrity** (Authenticated Encryption). Jika satu bit saja diubah oleh penyerang, proses dekripsi akan gagal pada tahap verifikasi tag (`MAC check failed`), sehingga memberikan perlindungan terhadap serangan manipulasi data.

---

### 3. Catatan Khusus Algoritme
*   **DES**: Standar industri dan library modern (PyCryptodome) tidak mendukung GCM untuk DES karena GCM dirancang khusus untuk blok cipher 128-bit (seperti AES). Penggunaan GCM pada blok 64-bit (DES) dianggap tidak aman dan tidak standar.
*   **AES**: Mendukung seluruh mode dengan sangat baik dan GCM adalah pilihan standar untuk aplikasi modern karena fitur keamanannya yang lengkap.

---

### 4. Analisis Metrik Keamanan Tahap 2

Hasil analisis keamanan pada file `analisis_keamanan_tahap2.xlsx` menunjukkan beberapa temuan krusial:

#### Entropi & Korelasi
*   Seluruh mode (**CBC, CTR, GCM**) berhasil mempertahankan nilai **Entropi** yang sangat tinggi (mendekati **8.0**), menunjukkan pengacakan data yang maksimal.
*   **Koefisien Korelasi** tetap mendekati **0.0**, membuktikan bahwa perubahan mode operasi tidak mengurangi kemampuan algoritme dalam memutus hubungan statistik antara plainteks dan cipherteks.

#### Fenomena Avalanche Effect (Penting)
Terdapat perbedaan mencolok pada metrik Avalanche Effect antar mode:
1.  **Mode CBC**: Menghasilkan Avalanche Effect yang sangat tinggi (~50%). Hal ini karena sifat *Chaining*; satu bit yang berubah di awal blok akan merambat (*propagate*) ke seluruh blok-blok berikutnya dalam satu file.
2.  **Mode CTR & GCM**: Menghasilkan nilai Avalanche Effect yang **sangat rendah** (hanya beberapa bit yang berubah). 
    *   **Penjelasan**: Ini bukan berarti algoritmenya lemah. Mode CTR bekerja seperti *Stream Cipher* di mana plainteks di-XOR langsung dengan *keystream*. Sifat XOR mengakibatkan perubahan 1 bit pada plainteks **hanya** akan mengubah 1 bit yang bersesuaian pada cipherteks.
    *   **Kesimpulan**: Untuk mode CTR/GCM, metrik Avalanche Effect "per-bit plainteks" memang secara desain rendah, namun keamanan integritasnya (pada GCM) dijamin oleh **Auth Tag** yang akan berubah total jika ada satu bit pun yang dimanipulasi.
