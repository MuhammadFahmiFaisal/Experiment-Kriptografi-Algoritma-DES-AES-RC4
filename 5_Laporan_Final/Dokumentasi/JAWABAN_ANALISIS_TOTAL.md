# Kumpulan Jawaban dan Penjelasan Analisis Eksperimen Kriptografi
**Eksperimen: Perbandingan DES vs AES vs RC4 (Tahap 1 - 3)**

Dokumen ini merangkum seluruh jawaban analisis teoretis berdasarkan hasil eksperimen mandiri yang telah dilakukan.

---

### BAGIAN 1: Perbandingan Dasar (DES vs AES)

#### 1. Mengapa AES menghasilkan tingkat keamanan lebih tinggi dibanding DES?
*   **Ruang Kunci (Key Space)**: DES memiliki panjang kunci efektif hanya 56-bit, yang dapat ditembus dengan *brute-force* dalam waktu singkat menggunakan komputer modern. AES mendukung kunci 128, 192, dan 256-bit yang secara eksponensial lebih kuat.
*   **Ukuran Blok**: AES menggunakan blok 128-bit, meminimalkan risiko serangan berbasis tabrakan (*birthday attacks*) dibandingkan blok 64-bit pada DES.
*   **Struktur Algoritme**: AES menggunakan struktur *Substitution-Permutation Network* (SPN) yang lebih tahan terhadap analisis diferensial dan linier dibandingkan struktur *Feistel* pada DES.

#### 2. Bagaimana panjang kunci mempengaruhi avalanche effect?
Secara teoretis, panjang kunci tidak secara langsung mengubah nilai ideal *avalanche effect* (tetap 50%). Namun, kunci yang lebih panjang pada AES berarti jumlah putaran (*rounds*) yang lebih banyak (misal 14 putaran untuk AES-256 vs 10 putaran untuk AES-128). Hal ini memastikan bahwa data diacak lebih dalam, memberikan ketahanan lebih kuat terhadap analisis kriptografi tingkat lanjut.

#### 3. Apakah terdapat perbedaan signifikan performa terhadap ukuran file besar?
**Ya.** Pada file besar (1MB ke atas), AES umumnya jauh lebih cepat daripada DES. Ini terjadi karena AES dirancang untuk operasi matriks/byte yang sangat efisien pada prosesor modern, serta dukungan instruksi **AES-NI** pada perangkat keras, sedangkan DES banyak menggunakan operasi bit-level yang relatif lambat diproses oleh software.

---

### BAGIAN 2: Analisis Mode Operasi (ECB, CBC, CTR, GCM)

#### 4. Apakah ECB paling aman? Mengapa?
**Tidak.** ECB adalah mode yang paling tidak aman. 
**Alasannya**: Dalam mode ECB, blok plainteks yang identik akan menghasilkan blok cipherteks yang identik pula. Hal ini membocorkan pola informasi (seperti visual "ECB Penguin"), sehingga penyerang dapat mengenali struktur data asli meskipun data tersebut terenkripsi.

#### 5. Apakah CTR paling cepat? Mengapa?
**Ya.** CTR adalah salah satu mode tercepat.
**Alasannya**: Mode CTR mendukung **paralelisme penuh**. Karena enkripsi setiap blok hanya bergantung pada nilai counter yang bisa dihitung di awal, komputer dapat memproses banyak blok secara bersamaan. Selain itu, CTR tidak memerlukan *padding*, sehingga prosesnya lebih ringkas.

#### 6. Mengapa GCM menjadi standar TLS modern?
GCM (*Galois/Counter Mode*) menjadi standar (seperti pada TLS 1.3) karena:
*   **AEAD (Authenticated Encryption)**: Memberikan kerahasiaan sekaligus integritas data dalam satu langkah efisien.
*   **Tahan Serangan Padding**: Karena tidak menggunakan padding, GCM kebal terhadap serangan *Padding Oracle*.
*   **Kinerja Tinggi**: Berbasis mode CTR yang paralel, GCM sangat cepat dan optimal untuk transmisi data kecepatan tinggi di internet.

---

### BAGIAN 3: Block Cipher vs Stream Cipher (RC4)

#### 7. Mengapa stream cipher lebih cepat pada beberapa arsitektur?
Stream cipher seperti RC4 atau ChaCha20 lebih cepat dalam implementasi perangkat lunak murni karena operasinya sangat sederhana (hanya XOR antara plainteks dengan arus kunci bit-demi-bit). Tidak ada struktur blok kompleks atau substitusi berlapis yang membebani siklus CPU.

#### 8. Mengapa AES tetap menjadi standar industri dibandingkan stream cipher murni?
AES tetap menjadi standar karena keseimbangan antara keamanan ekstrem dan performa. Adanya fitur **AES-NI** (akselerasi hardware) pada CPU modern membuat AES seringkali lebih cepat atau menyamai stream cipher, sambil memberikan jaminan keamanan yang jauh lebih teruji melalui kompetisi NIST selama bertahun-tahun.

#### 9. Pada kondisi apa ChaCha20 / RC4 lebih unggul dibanding AES?
*   **Perangkat Tanpa Akselerasi Hardware**: Pada prosesor ponsel murah atau perangkat IoT yang tidak memiliki unit instruksi AES khusus.
*   **Streaming Data Latensi Rendah**: Untuk kebutuhan transfer audio atau video *real-time* di mana kecepatan pemrosesan per-byte lebih diutamakan daripada overhead manajemen blok.
*   **Resource Terbatas**: Pada mikrokontroler kecil dengan memori RAM yang sangat terbatas untuk menyimpan tabel S-Box AES yang besar.
