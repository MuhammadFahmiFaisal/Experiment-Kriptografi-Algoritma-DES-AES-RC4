# LAPORAN EKSPERIMEN KRIPTOGRAFI MODERN
**Mata Kuliah: Kriptografi (MG-6)**

---

## 1. Pendahuluan & Objektif
Eksperimen ini bertujuan untuk menganalisis algoritme kriptografi modern (DES dan AES) berdasarkan karakteristik performa dan metrik keamanan. Pengujian dilakukan menggunakan berbagai mode operasi (ECB, CBC, CTR, GCM) untuk mengevaluasi kekuatan dan kelemahan masing-masing metode.

## 2. Metodologi Eksperimen
*   **Dataset**: 100 file plainteks bermakna (Bahasa Indonesia) dengan ukuran masing-masing tepat 1 MB.
*   **Algoritme**: 
    *   DES (Data Encryption Standard)
    *   AES (Advanced Encryption Standard)
*   **Mode Operasi**: ECB, CBC, CTR, GCM.
*   **Parameter Kunci**: Menggunakan kunci panjang (AES-256 dan DES-64bit).

## 3. Ringkasan Hasil Eksperimen (Rata-rata)

| Algoritma | Metrik Evaluasi | ECB | CBC | CTR | GCM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DES** | Waktu Enkripsi (ms) | 20.86 | 26.05 | 22.28 | N/A |
| **DES** | Waktu Dekripsi (ms) | 20.47 | 24.90 | 21.80 | N/A |
| **DES** | Avalanche Effect | 0.00% | 50.00% | 0.00% | N/A |
| **AES** | Waktu Enkripsi (ms) | 1.53 | 12.48 | 3.54 | 6.04 |
| **AES** | Waktu Dekripsi (ms) | 1.42 | 5.60 | 2.18 | 2.81 |
| **AES** | Avalanche Effect | 0.00% | 50.00% | 0.00% | 0.00% |
| **RC4** | Waktu Enkripsi (ms) | - | - | - | ~1.40 (Stream) |

> [!NOTE]
> *RC4 adalah stream cipher, sehingga tidak menggunakan mode operasi blok (ECB/CBC/GCM). Angka yang ditunjukkan adalah performa murni stream.*

## 4. Analisis Visual & Fenomena
*   **Performa**: AES secara signifikan lebih cepat daripada DES, terutama pada mode ECB dan CTR karena desain arsitektur yang lebih efisien dan dukungan perangkat keras modern.
*   **Overhead Ukuran**: Mode ECB dan CBC menambah ukuran file karena *padding*, sedangkan CTR dan GCM mempertahankan ukuran asli (CTR) atau hanya menambah *tag* autentikasi minimal (GCM).
*   **Randomness (Entropy)**: Semua cipherteks menunjukkan nilai entropi mendekati 8.0, membuktikan bahwa algoritme berhasil mengubah data bermakna menjadi pola acak.
*   **Efek Longsor (Avalanche)**: Mode **CBC** memberikan efek difusi terbaik antar blok (50%), sedangkan mode **CTR/GCM** memiliki avalanche rendah per-bit plainteks namun diimbangi dengan keamanan integritas yang kuat.

---

## 5. Pertanyaan Analisis

### 5.1 Mengapa AES lebih aman dibanding DES?
AES memiliki ukuran kunci yang jauh lebih besar (hingga 256-bit vs 56-bit DES) yang membuatnya aman dari *brute force*. Selain itu, AES menggunakan blok 128-bit dan struktur SPN yang lebih resisten terhadap analisis kriptografi canggih dibanding struktur Feistel pada DES.

### 5.2 Mengapa CTR paling cepat?
CTR memungkinkan proses enkripsi dan dekripsi dilakukan secara **paralel**. Setiap blok diproses secara mandiri menggunakan counter, sehingga tidak ada ketergantungan antar blok (berbeda dengan CBC yang bersifat sekuensial).

### 5.3 Mengapa GCM menjadi standar TLS modern?
GCM adalah mode **AEAD** yang memberikan kerahasiaan sekaligus integritas data. GCM sangat efisien (paralel), tidak memerlukan padding (aman dari *Padding Oracle*), dan relatif mudah diimplementasikan dengan performa tinggi pada standar web modern.

---

## 7. Tahap 3: Perbandingan Block Cipher vs Stream Cipher (RC4)

Pada tahap akhir, kita membandingkan algoritme berbasis blok (DES/AES) dengan algoritme berbasis aliran atau **Stream Cipher** (RC4).

### Tabel Performa RC4 (Rata-rata 100 File)
| Metrik | RC4 (Short Key) | RC4 (Long Key) |
| :--- | :--- | :--- |
| Waktu Enkripsi (ms) | ~1.42 | ~1.45 |
| Ukuran Cipherteks | 1.00 MB (No Padding) | 1.00 MB (No Padding) |
| Entropy Cipher | ~7.999 | ~7.999 |
| Avalanche Effect | 0.00% | 0.00% |

### Perbandingan Karakteristik:
1.  **Unit Pemrosesan**: 
    *   **Block Cipher (AES/DES)**: Memproses data dalam unit blok tetap (64/128 bit). Memerlukan padding jika data tidak pas.
    *   **Stream Cipher (RC4)**: Memproses data bit-per-bit atau byte-per-byte. Tidak memerlukan padding, sehingga ukuran output selalu sama dengan input.
2.  **Kecepatan**:
    *   RC4 secara historis sangat cepat dalam implementasi perangkat lunak murni. Namun, AES modern dengan dukungan instruksi CPU (AES-NI) dapat menyaingi atau melampaui kecepatan RC4.
3.  **Avalanche Effect**:
    *   Sama seperti mode CTR, **RC4 memiliki Avalanche Effect rendah (per-bit plainteks)** karena satu bit perubahan di input hanya mengubah satu bit di output (sifat XOR). Keamanannya bergantung pada keacakan arus kunci (*keystream*), bukan pada perambatan error.

---

## 8. Kesimpulan Akhir
Berdasarkan eksperimen, **AES dalam mode GCM atau CTR adalah pilihan terbaik** untuk penggunaan umum modern. GCM sangat direkomendasikan jika integritas data (proteksi dari manipulasi) menjadi prioritas, sedangkan CTR menawarkan kecepatan maksimal. Penggunaan **ECB sangat dilarang** untuk data nyata karena kerentanan pola grafisnya, dan **DES sudah tidak layak** digunakan untuk keamanan jangka panjang karena ukuran kuncinya yang terlalu kecil. Untuk kebutuhan streaming sederhana dengan resource rendah, RC4 pernah populer, namun kini sudah digantikan oleh stream cipher yang lebih kuat seperti ChaCha20.
