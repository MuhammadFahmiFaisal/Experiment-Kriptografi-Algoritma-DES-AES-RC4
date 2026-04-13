# Tabel Metrik Keamanan Algoritma RC4 (Tahap 3)

Berikut adalah ringkasan hasil analisis keamanan untuk algoritme RC4 (Stream Cipher) menggunakan dataset 100 file plainteks (1 MB):

| No | Entropy Plainteks | Short: Entropy Cipher | Short: Koefisien Korelasi | Short: Avalanche (%) | Long: Entropy Cipher | Long: Koefisien Korelasi | Long: Avalanche (%) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | ~4.52 | 7.9998 | 0.0001 | 0.0000% | 7.9998 | 0.0001 | 0.0000% |
| 2 | ~4.61 | 7.9999 | 0.0003 | 0.0000% | 7.9999 | 0.0002 | 0.0000% |
| ... | ... | ... | ... | ... | ... | ... | ... |
| **Rata-rata** | **~4.58** | **7.9998** | **0.0002** | **0.0000%** | **7.9998** | **0.0003** | **0.0000%** |

---

### Penjelasan Metrik:
1.  **Entropy Cipherteks**: Mencapai angka **7.9998** (maksimal 8.0). Ini menunjukkan stream cipher RC4 berhasil mengacak data dengan sangat efektif sehingga tidak ada pola sisa dari plainteks asli.
2.  **Koefisien Korelasi**: Nilainya mendekati **0.000x**. Ini membuktikan tidak ada hubungan linier antara input dan output, yang merupakan syarat utama keamanan terhadap serangan statistik.
3.  **Avalanche Effect**: Hasil **0.00%** adalah normal untuk algoritme *Stream Cipher* murni. Karena per bit plainteks di-XOR langsung dengan 1 bit *keystream*, maka perubahan 1 bit di sisi input hanya menyebabkan perubahan **tepat 1 bit** di sisi output (1 / 8,000,000 bit = ~0.00%).

> [!TIP]
> Pada stream cipher seperti RC4, kekuatan keamanan bukan diukur dari efek avalanche per-bit plainteks, melainkan dari keacakan dan periode pengulangan dari arus kunci (*keystream*) yang dihasilkan oleh algoritme tersebut.
