# Dokumentasi Step-by-Step Eksperimen Kriptografi
## Perbandingan DES vs AES (ECB Mode)

Dokumen ini menjelaskan langkah-langkah detail pelaksanaan eksperimen untuk memenuhi tugas mata kuliah Kriptografi.

---

### Langkah 1: Persiapan Lingkungan (Environment)
Pastikan Python telah terinstal di sistem Anda. Instal library yang diperlukan (dependencies) dengan menjalankan perintah berikut di Terminal/CMD:

```bash
pip install pycryptodome pandas numpy openpyxl
```

**Fungsi Library:**
*   `pycryptodome`: Implementasi algoritma DES dan AES.
*   `pandas`: Mengelola data hasil eksperimen ke dalam tabel.
*   `numpy`: Digunakan untuk analisis statistik distribusi karakter (varians).
*   `openpyxl`: Digunakan untuk menyimpan hasil ke format Excel (.xlsx).

---

### Langkah 2: Pembuatan Dataset Plainteks
Jalankan script generator data untuk membuat 100 file teks unik dalam Bahasa Indonesia.

**Perintah:**
```bash
python generate_data.py
```

**Detail Proses:**
1.  Program akan membuat folder bernama `plaintext_files`.
2.  Setiap file berukuran tepat **1 MB**.
3.  Konten setiap file adalah teks bermakna tentang kriptografi dalam Bahasa Indonesia.
4.  Setiap file memiliki urutan paragraf dan ID yang berbeda agar dataset bervariasi.

---

### Langkah 3: Konfigurasi Script Eksperimen (`Tahap1.py`)
Buka file `Tahap1.py` untuk melihat parameter yang digunakan:

*   **Algoritma & Mode**: DES-ECB dan AES-ECB.
*   **Kunci DES**: Menggunakan 8-byte (64-bit) karena batasan standar algoritma.
*   **Kunci AES**: 
    *   Kunci Pendek: 128-bit (16 byte).
    *   Kunci Panjang: 256-bit (32 byte).
*   **Metrik yang Dicatat**:
    *   Waktu Enkripsi (ms)
    *   Waktu Dekripsi (ms)
    *   Ukuran Cipherteks
    *   Varians Distribusi Karakter (untuk analisis pengacakan).

---

### Langkah 4: Menjalankan Eksperimen
Setelah dataset siap, jalankan proses enkripsi dan dekripsi massal.

**Perintah:**
```bash
python Tahap1.py
```

**Proses:**
1.  Program akan membaca 100 file dari `plaintext_files`.
2.  Melakukan pengujian DES (Short & Long Key) dan AES (Short & Long Key) pada setiap file.
3.  Menghitung kecepatan proses dalam milidetik.
4.  Menghitung sebaran karakter sebelum dan sesudah enkripsi.

---

### Langkah 5: Analisis Hasil
Hasil akhir akan disimpan ke dalam:
`hasil_eksperimen.xlsx` (Performa) dan `analisis_metrik_keamanan.xlsx` (Keamanan).

**Cara Membaca Hasil:**
1.  **Tab DES**: Berisi data hasil tes DES.
2.  **Tab AES**: Berisi data hasil tes AES.
3.  **Kolom Var (Varians)**: 
    *   `Var Plain`: Varians tinggi (teks bermakna memiliki pola/pengulangan).
    *   `Var Cipher`: Varians rendah (mendekati 0) menunjukkan enkripsi berhasil mengacak data secara merata ke seluruh spektrum byte (0-255).

---

### Analisis & Penjelasan Hasil Tahap 1

Pada tahap ini, kita telah berhasil mengumpulkan dataset performa dari 100 sampel file. Berikut adalah poin-poin penjelasan penting untuk laporan:

1.  **Signifikansi Statistik (100 Sampel)**:
    Penggunaan 100 sampel bertujuan untuk mendapatkan rata-rata yang stabil. Waktu pemrosesan pada komputer dapat bervariasi tergantung pada beban sistem saat itu (background processes). Dengan mengambil rata-rata (baris 101), kita mendapatkan angka performa yang lebih akurat dan objektif.

2.  **Rata-rata (Baris 101)**:
    Baris terakhir pada file Excel menampilkan rata-rata waktu enkripsi/dekripsi. Umumnya, Anda akan melihat bahwa **AES-128** cenderung sangat efisien bahkan dibandingkan dengan DES, karena AES dirancang untuk optimal pada arsitektur prosesor modern.

3.  **Kunci Pendek vs Panjang**:
    *   Pada **AES**, Anda dapat membandingkan apakah kunci 256-bit (Kunci Panjang) mengakibatkan penurunan kecepatan yang signifikan dibanding 128-bit. Secara teori, AES-256 melakukan lebih banyak putaran (*rounds*), sehingga waktu enkripsi akan sedikit lebih lama.
    *   Pada **DES**, karena kedua kunci tetap 8-byte, perbedaan waktu seharusnya sangat kecil atau tidak ada (hanya dipengaruhi fluktuasi sistem).

4.  **Distribusi Karakter (Efek Difusi)**:
    Perhatikan perubahan nilai **Variance**.
    *   Plainteks memiliki varians yang **tinggi** karena distribusi karakter yang tidak merata (karakter bahasa manusia).
    *   Cipherteks harus memiliki varians yang **sangat rendah** (mendekati nol). Ini menunjukkan algoritma berhasil melakukan *diffusion* (pengacakan) sehingga frekuensi pemunculan setiap byte (0-255) menjadi hampir sama rata.

5.  **Risiko ECB pada Data Bermakna**:
    Karena kita menggunakan teks Bahasa Indonesia yang bermakna (memiliki pola kalimat berulang), mode **ECB** akan menghasilkan blok cipherteks yang sama untuk blok plainteks yang identik. Meskipun metrik performa kita bagus, secara keamanan mode ini sangat berisiko karena tidak menyembunyikan pola data dengan sempurna.

---

### Langkah 6: Analisis Metrik Keamanan
Tahap ini mengukur kekuatan algoritme berdasarkan teori informasi dan statistik.

**Perintah:**
```bash
python AnalisisMetrikKeamanan.py
```

**Metrik yang Diukur:**
1.  **Entropy (Entropi)**: Mengukur keacakan data. Nilai ideal untuk cipherteks 8-bit adalah mendekati **8.0**. Semakin tinggi entropi, semakin sulit data diprediksi.
2.  **Koefisien Korelasi**: Mengukur hubungan linier antara plainteks dan cipherteks. Nilai ideal adalah mendekati **0.0**, yang berarti tidak ada hubungan sisa yang dapat dieksploitasi.
3.  **Avalanche Effect**: Persentase perubahan bit pada cipherteks jika **1 bit** plainteks diubah. Nilai ideal adalah **50%**. Ini menunjukkan sifat *confusion* dan *diffusion* algoritme yang kuat.

**Output:**
File `analisis_metrik_keamanan.xlsx` dengan baris rata-rata di akhir (baris 101).

---

### Langkah 7: Eksperimen Mode Operasi (Tahap 2)
Tahap ini menguji mode operasi yang lebih kompleks: **CBC, CTR, dan GCM**.

**Perintah:**
```bash
python Tahap2_Modes.py
```

**Proses:**
1.  Melakukan pengujian performa hanya menggunakan **Kunci Panjang** dari Tahap 1.
2.  Membandingkan kecepatan proses (ms) dan overhead ukuran (MB) antara mode operasi.
3.  **GCM** diuji khusus pada AES sebagai standar *Authenticated Encryption*.

**Output:**
File `hasil_eksperimen_tahap2.xlsx`.

---

### Langkah 8: Analisis Keamanan Mode Operasi (Tahap 2)
Mengukur metrik keamanan pada mode CBC, CTR, dan GCM.

**Perintah:**
```bash
python AnalisisKeamananTahap2.py
```

**Poin Penting Analisis:**
1.  **Chaining Effect (CBC)**: Perhatikan bagaimana perubahan bit merambat ke blok-blok berikutnya.
2.  **Streaming Effect (CTR/GCM)**: Memahami mengapa perubahan 1 bit plainteks hanya mengubah 1 bit cipherteks yang bersesuaian.
3.  **Auth Tag (GCM)**: Memahami peran tag tambahan dalam menjamin integritas data.

**Output:**
File `analisis_keamanan_tahap2.xlsx`.

---

### Penjelasan Hasil Metrik Keamanan

Berdasarkan hasil eksekusi `AnalisisMetrikKeamanan.py`, berikut adalah cara menjelaskan temuan Anda:

1.  **Analisis Entropi (Entropy)**:
    *   **Plainteks**: Nilainya biasanya rendah (sekitar 3.0 - 5.0) karena bahasa manusia memiliki banyak pengulangan dan pola.
    *   **Cipherteks**: Harus memberikan nilai mendekati **8.0** (seperti 7.99xx). Hal ini menunjukkan bahwa algoritme berhasil menghilangkan pola bahasa dan mengubahnya menjadi data yang tampak acak (random-looking data). Jika AES memiliki entropi lebih tinggi dari DES, maka AES lebih baik dalam pengacakan.

2.  **Analisis Koefisien Korelasi**:
    *   Idealnya nilai ini mendekati **0.0** (baik positif maupun negatif kecil, misal 0.001).
    *   Nilai yang mendekati 0 menunjukkan bahwa tidak ada hubungan linier antara input (plainteks) dan output (cipherteks). Penyerang tidak bisa menebak plainteks hanya dengan melihat perubahan pada cipherteks secara statistik.

3.  **Analisis Avalanche Effect**:
    *   Inilah ujian terpenting. Nilai ideal adalah **50%**.
    *   Jika Anda mengubah hanya 1 bit pada 1MB data, dan hasilnya adalah ~50% bit pada cipherteks berubah, maka algoritme tersebut memiliki tingkat *diffusion* yang sangat tinggi.
    *   **AES** umumnya memiliki nilai Avalanche yang sangat stabil mendekati 50%. **DES** juga memiliki efek ini, namun secara teoretis AES lebih efisien dalam mencapainya dengan ukuran blok yang lebih besar (128-bit vs 64-bit).

4.  **Kesimpulan Performa vs Keamanan**:
    *   Melalui tabel rata-rata, Anda dapat menyimpulkan bahwa **AES tidak hanya lebih cepat (efisiensi) tetapi juga memberikan metrik keamanan yang lebih solid** (entropi lebih tinggi dan korelasi lebih rendah) dibandingkan DES. 
    *   Perbedaan antara **Kunci Pendek dan Panjang** pada AES akan menunjukkan bahwa meskipun kunci lebih panjang menambah sedikit beban komputasi, tingkat keamanan (entropi) yang dihasilkan relatif konsisten tinggi.
