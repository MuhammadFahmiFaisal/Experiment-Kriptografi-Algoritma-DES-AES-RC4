# Analisis Visual dan Deskripsi Fenomena Eksperimen
## Perbandingan Kinerja & Keamanan: DES vs AES

Berikut adalah visualisasi hasil eksperimen berdasarkan rata-rata dari 100 sampel plainteks (1MB).

---

### 1. Perbandingan Ukuran Plainteks vs Cipherteks
| Grafik | Deskripsi Fenomena |
| :--- | :--- |
| ![Ukuran File](grafik_hasil/ukuran_file.png) | **Fenomena:** Ukuran cipherteks sedikit lebih besar daripada plainteks pada semua algoritme. Hal ini disebabkan oleh mekanisme **Padding** (PKCS7) yang menambahkan byte ekstra agar panjang data menjadi kelipatan ukuran blok (8 byte untuk DES, 16 byte untuk AES). Perbedaan antara DES dan AES sangat minimal karena file berukuran besar (1MB). |

### 2. Waktu Enkripsi & Dekripsi
| Grafik | Deskripsi Fenomena |
| :--- | :--- |
| ![Waktu Eksekusi](grafik_hasil/waktu_eksekusi.png) | **Fenomena:** AES menunjukkan efisiensi waktu yang lebih baik atau kompetitif dibandingkan DES meskipun memiliki kunci yang lebih kompleks. Proses dekripsi biasanya memakan waktu yang hampir sama dengan enkripsi pada mode ECB. Pengaruh panjang kunci pada AES (128 vs 256) terlihat pada sedikit peningkatan waktu untuk kunci 256 karena jumlah putaran (*rounds*) yang bertambah. |

### 3. Entropy Plainteks vs Cipherteks
| Grafik | Deskripsi Fenomena |
| :--- | :--- |
| ![Entropy](grafik_hasil/entropy_comparison.png) | **Fenomena:** Terjadi lonjakan signifikan nilai entropi dari plainteks (~4.0) ke cipherteks (~7.99). Ini membuktikan bahwa algoritme berhasil mengacak pola bahasa manusia menjadi distribusi yang tampak acak sempurna (maksimal 8.0). AES dan DES keduanya mencapai entropi tinggi, namun AES seringkali lebih konsisten mendekati angka 8. |

### 4. Koefisien Korelasi
| Grafik | Deskripsi Fenomena |
| :--- | :--- |
| ![Korelasi](grafik_hasil/correlation.png) | **Fenomena:** Nilai korelasi berada di kisaran yang sangat rendah (mendekati 0.0), baik positif maupun negatif. Hal ini menunjukkan tidak ada hubungan linier antara input dan output. Rendahnya korelasi adalah indikator kuat bahwa serangan statistik akan sangat sulit dilakukan terhadap hasil enkripsi ini. |

### 5. Avalanche Effect
| Grafik | Deskripsi Fenomena |
| :--- | :--- |
| ![Avalanche](grafik_hasil/avalanche.png) | **Fenomena:** Semua konfigurasi menghasilkan nilai Avalanche Effect di kisaran 50% (ideal). Artinya, perubahan **1 bit** pada plainteks mengakibatkan perubahan sekitar setengah dari total bit cipherteks. Hal ini menunjukkan sifat *diffusion* yang sangat baik pada DES maupun AES. |

---

## Jawaban Pertanyaan Analisis

### 1. Mengapa AES menghasilkan tingkat keamanan lebih tinggi dibanding DES?
AES dianggap lebih aman karena beberapa alasan teknis utama:
*   **Panjang Kunci**: DES hanya memiliki panjang kunci efektif 56-bit (mudah ditembus dengan *brute-force* modern), sedangkan AES mendukung hingga 256-bit yang secara matematis mustahil ditembus dengan teknologi saat ini.
*   **Ukuran Blok**: AES menggunakan blok 128-bit, sedangkan DES hanya 64-bit. Ukuran blok yang lebih besar mengurangi risiko serangan berbasis tabrakan (*birthday attacks*).
*   **Arsitektur**: AES menggunakan *Substitution-Permutation Network* (SPN) yang lebih resisten terhadap *linear* dan *differential cryptanalysis* dibandingkan struktur *Feistel* pada DES.

### 2. Bagaimana panjang kunci mempengaruhi avalanche effect?
Secara teoretis, peningkatan panjang kunci (misal AES-128 ke AES-256) meningkatkan jumlah putaran (*rounds*) dalam algoritme. Semakin banyak putaran, semakin dalam data "dikocok". Meskipun kunci 128-bit sudah cukup untuk mencapai nilai avalanche 50%, kunci yang lebih panjang memastikan properti ini tetap terjaga bahkan di bawah analisis kriptografi yang lebih kompleks, tanpa mengubah nilai ideal 50% tersebut.

### 3. Apakah terdapat perbedaan signifikan performa terhadap ukuran file besar?
Ya. Pada file berukuran besar, **AES umumnya jauh lebih cepat** daripada DES karena:
*   **Optimasi Hardware**: Prosesor modern (Intel/AMD) memiliki instruksi khusus **AES-NI** yang mempercepat enkripsi AES langsung di level perangkat keras.
*   **Efisiensi Software**: DES banyak menggunakan operasi tingkat bit dan permutasi yang lambat jika dijalankan melalui simulasi perangkat lunak dibandingkan operasi matriks/tabel yang digunakan oleh AES.
