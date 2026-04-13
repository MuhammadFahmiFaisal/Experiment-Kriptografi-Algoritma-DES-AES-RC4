import pandas as pd
import matplotlib.pyplot as plt
import os

# Files
FILE_PERF = "hasil_eksperimen.xlsx"
FILE_SEC = "analisis_metrik_keamanan.xlsx"
OUTPUT_DIR = "grafik_hasil"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Load data
df_perf_des = pd.read_excel(FILE_PERF, sheet_name="DES_Results")
df_perf_aes = pd.read_excel(FILE_PERF, sheet_name="AES_Results")
df_sec_des = pd.read_excel(FILE_SEC, sheet_name="Keamanan_DES")
df_sec_aes = pd.read_excel(FILE_SEC, sheet_name="Keamanan_AES")

# Get Averages (Last row)
avg_perf_des = df_perf_des.iloc[-1]
avg_perf_aes = df_perf_aes.iloc[-1]
avg_sec_des = df_sec_des.iloc[-1]
avg_sec_aes = df_sec_aes.iloc[-1]

def save_plot(title, filename):
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()
    print(f"Saved: {filename}")

# 1. Chart: Waktu Enkripsi & Dekripsi (ms)
plt.figure(figsize=(10, 6))
labels = ['DES Short', 'DES Long', 'AES Short', 'AES Long']
enc_times = [avg_perf_des['Waktu Enkripsi Short (ms)'], avg_perf_des['Waktu Enkripsi Long (ms)'], 
             avg_perf_aes['Waktu Enkripsi Short (ms)'], avg_perf_aes['Waktu Enkripsi Long (ms)']]
dec_times = [avg_perf_des['Waktu Dekripsi Short (ms)'], avg_perf_des['Waktu Dekripsi Long (ms)'], 
             avg_perf_aes['Waktu Dekripsi Short (ms)'], avg_perf_aes['Waktu Dekripsi Long (ms)']]

x = range(len(labels))
plt.bar([i - 0.2 for i in x], enc_times, width=0.4, label='Enkripsi', color='skyblue')
plt.bar([i + 0.2 for i in x], dec_times, width=0.4, label='Dekripsi', color='salmon')
plt.xticks(x, labels)
plt.ylabel('Waktu (ms)')
save_plot('Perbandingan Waktu Eksekusi (Rata-rata)', 'waktu_eksekusi.png')

# 2. Chart: Ukuran Plainteks vs Cipherteks (MB)
plt.figure(figsize=(8, 6))
labels_size = ['Plainteks', 'DES Short', 'DES Long', 'AES Short', 'AES Long']
sizes = [avg_perf_des['Ukuran File Plainteks (MB)'], 
         avg_perf_des['Ukuran Cipherteks Short (MB)'], avg_perf_des['Ukuran Cipherteks Long (MB)'],
         avg_perf_aes['Ukuran Cipherteks Short (MB)'], avg_perf_aes['Ukuran Cipherteks Long (MB)']]
plt.bar(labels_size, sizes, color='lightgreen')
plt.ylabel('Ukuran (MB)')
plt.ylim(0.9, 1.1) # Zoom in to see padding differences
save_plot('Perbandingan Ukuran File', 'ukuran_file.png')

# 3. Chart: Entropy (Rata-rata)
plt.figure(figsize=(8, 6))
labels_ent = ['Plain', 'DES S', 'DES L', 'AES S', 'AES L']
entropies = [avg_sec_des['Entropy Plainteks'], 
             avg_sec_des['C_Short: Entropy Cipher'], avg_sec_des['C_Long: Entropy Cipher'],
             avg_sec_aes['C_Short: Entropy Cipher'], avg_sec_aes['C_Long: Entropy Cipher']]
plt.bar(labels_ent, entropies, color='orchid')
plt.ylabel('Entropy Value')
plt.ylim(0, 9)
save_plot('Perbandingan Entropy (Randomness)', 'entropy_comparison.png')

# 4. Chart: Koefisien Korelasi
plt.figure(figsize=(8, 6))
labels_corr = ['DES Short', 'DES Long', 'AES Short', 'AES Long']
corrs = [avg_sec_des['C_Short: Koefisien Korelasi'], avg_sec_des['C_Long: Koefisien Korelasi'],
         avg_sec_aes['C_Short: Koefisien Korelasi'], avg_sec_aes['C_Long: Koefisien Korelasi']]
plt.bar(labels_corr, corrs, color='orange')
plt.ylabel('Correlation Coefficient')
plt.axhline(0, color='black', linewidth=0.8)
save_plot('Koefisien Korelasi Plain-Cipher', 'correlation.png')

# 5. Chart: Avalanche Effect (%)
plt.figure(figsize=(8, 6))
labels_aval = ['DES Short', 'DES Long', 'AES Short', 'AES Long']
avals = [avg_sec_des['C_Short: Avalanche Effect (%)'], avg_sec_des['C_Long: Avalanche Effect (%)'],
         avg_sec_aes['C_Short: Avalanche Effect (%)'], avg_sec_aes['C_Long: Avalanche Effect (%)']]
plt.bar(labels_aval, avals, color='gold')
plt.ylabel('Avalanche Effect (%)')
plt.axhline(50, color='red', linestyle='--', label='Ideal (50%)')
plt.legend()
save_plot('Perbandingan Avalanche Effect', 'avalanche.png')

print("Semua grafik berhasil dibuat di folder 'grafik_hasil'.")
