import os
import random

def generate_indonesian_content(file_index, target_size_mb=1):
    # Kumpulan paragraf tentang Kriptografi dalam Bahasa Indonesia
    paragraphs = [
        "Kriptografi adalah ilmu dan seni menjaga keamanan pesan. Dalam dunia teknologi informasi, kriptografi menjadi pilar utama untuk melindungi data dari akses yang tidak sah.",
        "Algoritma DES (Data Encryption Standard) merupakan salah satu algoritma simetris yang sempat menjadi standar global. Namun, karena ukuran kuncinya yang hanya 56-bit, DES kini dianggap rentan terhadap brute force.",
        "AES (Advanced Encryption Standard) hadir sebagai pengganti DES dengan keamanan yang lebih tinggi. AES mendukung kunci 128, 192, dan 256 bit, menjadikannya standar enkripsi pemerintah Amerika Serikat dan dunia saat ini.",
        "Mode operasi ECB (Electronic Codebook) adalah mode paling sederhana di mana setiap blok plainteks dienkripsi secara independen menggunakan kunci yang sama. Kelemahannya adalah pola pada plainteks masih bisa terlihat pada cipherteks.",
        "Dalam mata kuliah Kriptografi, mahasiswa belajar mengenai perbandingan antara block cipher dan stream cipher. Block cipher memproses data dalam blok tetap, sedangkan stream cipher memproses data bit demi bit.",
        "Keamanan sistem informasi tidak hanya bergantung pada algoritma, tetapi juga pada manajemen kunci. Kunci pendek lebih mudah ditebak, sedangkan kunci panjang memberikan perlindungan lebih kuat namun memerlukan sumber daya komputasi lebih besar.",
        "Metrik keamanan yang sering diuji dalam eksperimen kriptografi meliputi waktu enkripsi, waktu dekripsi, dan perubahan distribusi karakter. Distribusi karakter yang merata pada cipherteks menunjukkan kualitas enkripsi yang baik.",
        "Implementasi kriptografi modern menggunakan library seperti PyCryptodome di Python. Hal ini memudahkan pengembang untuk menerapkan standar keamanan tinggi tanpa harus membangun algoritma dari awal.",
        "Penting bagi mahasiswa Teknik Informatika untuk memahami risiko penggunaan mode ECB. Tanpa IV (Initialization Vector), data yang berulang akan menghasilkan pola yang sama pada hasil enkripsi.",
        "Eksperimen ini bertujuan untuk menganalisis kekuatan dan kelemahan DES vs AES melalui pengujian langsung terhadap 100 sampel data bermakna."
    ]
    
    # Tambahkan variasi dengan mengacak urutan paragraf untuk setiap file
    random.seed(file_index) # Pastikan setiap file unik tapi reprodusibel jika dijalankan ulang
    shuffled_paragraphs = paragraphs.copy()
    random.shuffle(shuffled_paragraphs)
    
    base_text = "\n\n".join(shuffled_paragraphs)
    
    # Jadikan 1MB
    target_bytes = int(target_size_mb * 1024 * 1024)
    base_bytes = base_text.encode('utf-8')
    
    repetitions = target_bytes // len(base_bytes)
    content = (base_bytes + b"\n\n") * repetitions
    
    # Pastikan ukuran tepat 1MB
    if len(content) > target_bytes:
        content = content[:target_bytes]
    else:
        content += b" " * (target_bytes - len(content))
        
    return content

def main():
    folder_name = "plaintext_files"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    print(f"Memulai pembuatan 100 file plainteks (Bahasa Indonesia) di '{folder_name}'...")
    
    for i in range(1, 101):
        filename = f"plaintext_{i:03d}.txt"
        filepath = os.path.join(folder_name, filename)
        
        # Buat konten unik untuk setiap file
        content = generate_indonesian_content(i, 1)
        
        # Tambahkan header unik di awal agar konten setiap file benar-benar berbeda dari baris pertama
        header = f"DOKUMEN EKSPERIMEN KRIPTOGRAFI #{i:03d}\n==================================\n\n".encode('utf-8')
        final_content = header + content[len(header):]
        
        with open(filepath, "wb") as f:
            f.write(final_content)
            
        if i % 10 == 0:
            print(f"Berhasil membuat {i}/100 file...")

    print("Selesai! 100 file plainteks bermakna Bahasa Indonesia telah siap.")

if __name__ == "__main__":
    main()
