# Tabel Ringkasan Rata-Rata Hasil Eksperimen (Kunci Panjang)

Berikut adalah tabel perbandingan performa dan keamanan algoritma kriptografi pada empat mode operasi yang berbeda:

| Algoritma | Metrik Evaluasi | ECB | CBC | CTR | GCM |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **DES** | Perubahan Ukuran File | Ada (Padding) | Ada (Padding) | Tidak Ada | N/A |
| **DES** | Waktu Enkripsi (ms) | 20.86 | 26.05 | 22.28 | N/A |
| **DES** | Waktu Dekripsi (ms) | 20.47 | 24.90 | 21.80 | N/A |
| **DES** | Entropy Cipher | 7.9856 | 7.9998 | 7.9998 | N/A |
| **DES** | Koefisien Korelasi | -0.0017 | -0.0001 | 0.0001 | N/A |
| **DES** | Avalanche Effect | 0.00% | 50.00% | 0.00% | N/A |
| **AES** | Perubahan Ukuran File | Ada (Padding) | Ada (Padding) | Tidak Ada | Tidak Ada (Tag) |
| **AES** | Waktu Enkripsi (ms) | 1.53 | 12.48 | 3.54 | 6.04 |
| **AES** | Waktu Dekripsi (ms) | 1.42 | 5.60 | 2.18 | 2.81 |
| **AES** | Entropy Cipher | 7.9939 | 7.9998 | 7.9998 | 7.9998 |
| **AES** | Koefisien Korelasi | 0.0048 | 0.0001 | 0.0000 | 0.0001 |
| **AES** | Avalanche Effect | 0.00% | 50.00% | 0.00% | 0.00% |

> [!NOTE]
> *N/A pada DES-GCM dikarenakan algoritma DES (blok 64-bit) tidak mendukung mode GCM secara standar.*

---

### Deskripsi Perbandingan Kinerja

1.  **Efisiensi Waktu**: **AES-ECB** menunjukkan waktu tercepat karena sifatnya yang sangat sederhana dan optimal pada perangkat keras modern. Namun, dari sisi mode keamanan yang "aman", **AES-CTR** adalah yang paling efisien karena mendukung paralelisme penuh.
2.  **Ukuran File**: Mode **CTR** dan **GCM** lebih unggul dalam efisiensi ruang karena tidak memerlukan *padding* (ciphertext memiliki panjang yang sama dengan plainteks). GCM hanya menambahkan sedikit overhead untuk *authentication tag*.
3.  **Pengacakan Data**: Seluruh mode memberikan nilai **Entropy** yang sangat baik (mendekati 8.0). Namun, **CBC** menunjukkan nilai **Korelasi** yang paling konsisten rendah dan **Avalanche Effect** paling tinggi (50%) karena adanya efek perambatan (*chaining*) perubahan bit antar blok.

---

### Jawaban Pertanyaan Analisis

#### 1. Apakah ECB paling aman? Mengapa?
**Tidak.** ECB adalah mode operasi yang paling tidak aman. 
**Alasannya:** ECB mengenkripsi setiap blok plainteks yang identik menjadi blok cipherteks yang identik pula. Hal ini mengakibatkan pola data asli masih dapat terlihat pada cipherteks (disebut *pattern leakage*). Ini mempermudah penyerang untuk melakukan analisis statistik dan visual (seperti fenomena ECB Penguin).

#### 2. Apakah CTR paling cepat? Mengapa?
**Ya.** CTR umumnya adalah salah satu mode tercepat.
**Alasannya:**
*   **Paralelisme**: Tidak seperti CBC yang harus menunggu proses blok sebelumnya selesai, CTR dapat mengenkripsi semua blok secara bersamaan karena setiap blok hanya bergantung pada nilai counter/nonce yang unik.
*   **No Padding**: Tidak ada waktu yang terbuang untuk proses padding atau unpadding.
*   **Efisiensi Operasi**: Proses utama hanya melibatkan XOR antara plainteks dengan *keystream* yang dihasilkan dari enkripsi counter.

#### 3. Mengapa GCM menjadi standar TLS modern?
GCM (*Galois/Counter Mode*) menjadi standar utama untuk keamanan web (TLS 1.2 & 1.3) karena:
*   **Authenticated Encryption (AEAD)**: Memberikan kerahasiaan (*confidentiality*) sekaligus integritas (*integrity*) dan keaslian (*authenticity*) dalam satu proses.
*   **Efisiensi Tinggi**: Mendukung paralelisme (berbasis mode CTR) sehingga sangat cepat pada prosesor modern.
*   **Keamanan Terhadap Serangan Padding**: GCM tidak menggunakan padding, sehingga kebal terhadap serangan *Padding Oracle* yang sering menyerang mode CBC.
*   **Satu Paket**: Menghilangkan kebutuhan untuk menggabungkan enkripsi dan MAC secara terpisah (seperti AES-CBC + HMAC), yang sering kali salah diimplementasikan oleh pengembang.
