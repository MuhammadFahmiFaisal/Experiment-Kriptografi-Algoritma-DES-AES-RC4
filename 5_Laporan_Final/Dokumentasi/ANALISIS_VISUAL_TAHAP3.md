# Analisis Visual Perbandingan DES vs AES vs RC4 (Tahap 3)

Berikut adalah visualisasi perbandingan antara algoritme *Block Cipher* (DES, AES) dan *Stream Cipher* (RC4).

---

### Grafik Perbandingan Kinerja

| Metrik | Grafik | Deskripsi Fenomena |
| :--- | :--- | :--- |
| **Ukuran Plainteks vs Cipherteks** | ![Ukuran](grafik_tahap3/ukuran_file.png) | **Fenomena:** RC4 (Stream Cipher) mempertahankan ukuran file yang sama persis dengan plainteks. Berbeda dengan DES/AES dalam mode blok (seperti ECB/CBC) yang menunjukkan sedikit penambahan ukuran akibat mekanisme *padding*. |
| **Waktu Enkripsi & Dekripsi** | ![Waktu](grafik_tahap3/kecepatan_enc.png) | **Fenomena:** RC4 menunjukkan kecepatan yang sangat tinggi karena operasinya yang sederhana (XOR bitstream). Namun, AES juga menunjukkan performa yang sangat kompetitif, bahkan mengungguli algoritme DES lama secara signifikan. |
| **Entropy Plainteks vs Cipherteks** | ![Entropy](grafik_tahap3/entropy.png) | **Fenomena:** Semua algoritme (DES, AES, RC4) berhasil mencapai nilai entropi mendekati 8.0. Ini membuktikan bahwa ketiganya sangat efektif dalam menghilangkan pola statistik dari plainteks asli. |
| **Koefisien Korelasi** | ![Korelasi](grafik_tahap3/correlation.png) | **Fenomena:** Nilai korelasi mendekati nol untuk semua algoritme, menunjukkan tidak adanya hubungan linier antara plainteks dan cipherteks yang dihasilkan. |
| **Avalanche Effect** | ![Avalanche](grafik_tahap3/avalanche.png) | **Fenomena:** Efek longsor (Avalanche) pada **RC4** terlihat sangat rendah (mendekati 0%) dibandingkan mode CBC pada DES/AES. Hal ini dikarenakan karakteristik *stream cipher* di mana manipulasi 1 bit input hanya berakibat pada 1 bit output yang bersesuaian tanpa perambatan error. |

---

### Pertanyaan Analisis

#### 1) Mengapa stream cipher lebih cepat pada beberapa arsitektur?
Stream cipher (seperti RC4 atau ChaCha20) lebih cepat karena mekanisme kerjanya yang sangat sederhana. Proses enkripsi hanya berupa operasi XOR antara bit plainteks dengan arus kunci (*keystream*). Tidak diperlukan proses pemecahan data ke dalam blok-blok besar atau proses substitusi dan permutasi yang berulang-ulang (*multiple rounds*) seperti pada algoritme blok, sehingga mengonsumsi siklus CPU yang jauh lebih sedikit.

#### 2) Mengapa AES tetap menjadi standar industri?
Meskipun stream cipher bisa lebih cepat, AES tetap menjadi standar karena:
*   **Hardware Acceleration**: Hampir semua prosesor modern memiliki instruksi **AES-NI** yang membuat enkripsi AES sangat cepat di level perangkat keras.
*   **Keamanan Teruji**: AES telah melalui pengujian keamanan yang sangat ketat selama puluhan tahun (kompetisi NIST).
*   **Fleksibilitas**: Melalui mode operasi seperti CTR atau GCM, AES dapat memiliki keunggulan stream cipher (tidak perlu padding & paralel) sekaligus memberikan proteksi integritas (AEAD).

#### 3) Pada kondisi apa ChaCha20 / RC4 lebih unggul dibanding AES?
Algoritme stream (khususnya ChaCha20 yang modern) lebih unggul pada:
*   **Perangkat Tanpa Akselerasi Hardware**: Pada ponsel lama atau perangkat IoT murah yang tidak memiliki instruksi AES-NI, stream cipher jauh lebih cepat daripada AES.
*   **Implementasi Software Murni**: Ketika pengembang tidak bisa mengandalkan fitur CPU tertentu, stream cipher memberikan performa yang lebih konsisten cepat di berbagai platform.
*   **Koneksi Latensi Rendah**: Untuk transmisi data yang mengalir terus menerus (audio/video streaming) di mana overhead block-chaining dapat menambah latensi.
