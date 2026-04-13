import pandas as pd
import matplotlib.pyplot as plt
import os

# Files
FILE_DES = "LAPORAN_FINAL_DES.xlsx"
FILE_AES = "LAPORAN_FINAL_AES.xlsx"
FILE_RC4 = "LAPORAN_FINAL_RC4.xlsx"
OUTPUT_DIR = "grafik_tahap3"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Extract Averages
def get_avg(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)
    return df[df['No'] == 'RATA-RATA'].iloc[0]

# For stage 3 comparison, we use Long Keys
avg_des = get_avg(FILE_DES, "Tahap1_ECB_Keamanan") # We take security metrics for ECB DES as baseline
perf_des = get_avg(FILE_DES, "Tahap1_ECB_Performa")
avg_aes = get_avg(FILE_AES, "Tahap1_ECB_Keamanan")
perf_aes = get_avg(FILE_AES, "Tahap1_ECB_Performa")
avg_rc4 = get_avg(FILE_RC4, "Tahap3_RC4_Lengkap")

def save_plot(title, filename):
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename))
    plt.close()

# 1. Waktu Enkripsi (ms)
plt.figure(figsize=(8, 6))
labels = ['DES (ECB)', 'AES (ECB)', 'RC4']
times = [perf_des['Waktu Enkripsi Long (ms)'], perf_aes['Waktu Enkripsi Long (ms)'], avg_rc4['Long: Waktu Enc (ms)']]
plt.bar(labels, times, color=['lightcoral', 'lightskyblue', 'lightgreen'])
plt.ylabel('Waktu (ms)')
save_plot('Perbandingan Kecepatan Enkripsi', 'kecepatan_enc.png')

# 2. Ukuran Cipherteks
plt.figure(figsize=(8, 6))
# 1MB is baseline
sizes = [perf_des['Ukuran Cipherteks Long (MB)'], perf_aes['Ukuran Cipherteks Long (MB)'], avg_rc4['Long: Ukuran Cipher (MB)']]
plt.bar(labels, sizes, color=['coral', 'skyblue', 'green'])
plt.ylabel('Ukuran (MB)')
plt.ylim(1.0, 1.0001) # Zoom to see padding (very small for 1MB)
save_plot('Perbandingan Ukuran File', 'ukuran_file.png')

# 3. Entropy
plt.figure(figsize=(8, 6))
entropies = [avg_des['C_Long: Entropy Cipher'], avg_aes['C_Long: Entropy Cipher'], avg_rc4['Long: Entropy Cipher']]
plt.bar(labels, entropies, color='orchid')
plt.ylabel('Entropy')
plt.ylim(7.9, 8.1)
save_plot('Perbandingan Entropy', 'entropy.png')

# 4. Korelasi
plt.figure(figsize=(8, 6))
corrs = [avg_des['C_Long: Koefisien Korelasi'], avg_aes['C_Long: Koefisien Korelasi'], avg_rc4['Long: Korelasi']]
plt.bar(labels, corrs, color='orange')
plt.ylabel('Correlation Coefficient')
plt.axhline(0, color='black', linewidth=0.8)
save_plot('Koefisien Korelasi', 'correlation.png')

# 5. Avalanche Effect
plt.figure(figsize=(8, 6))
# For DES/AES we use CBC from Stage 2 which has propagation vs RC4
perf_des_cbc = get_avg(FILE_DES, "Tahap2_Modes_Keamanan")
perf_aes_cbc = get_avg(FILE_AES, "Tahap2_Modes_Keamanan")

labels_aval = ['DES (CBC)', 'AES (CBC)', 'RC4']
avals = [perf_des_cbc['CBC: Avalanche (%)'], perf_aes_cbc['CBC: Avalanche (%)'], avg_rc4['Long: Avalanche (%)']]
plt.bar(labels_aval, avals, color='gold')
plt.ylabel('Avalanche Effect (%)')
plt.axhline(50, color='red', linestyle='--', label='Ideal (50%)')
plt.legend()
save_plot('Perbandingan Avalanche Effect', 'avalanche.png')

print("Grafik Tahap 3 berhasil dibuat di folder 'grafik_tahap3'.")
