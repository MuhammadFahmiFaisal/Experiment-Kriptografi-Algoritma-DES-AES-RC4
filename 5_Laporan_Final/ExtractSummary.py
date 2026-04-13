import pandas as pd

# Load averages
def get_avg(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)
    # Find row where 'No' is 'RATA-RATA'
    avg_row = df[df['No'] == 'RATA-RATA'].iloc[0]
    return avg_row

# Data extraction
# Tahap 1 (ECB)
try:
    perf_des_ecb = get_avg("hasil_eksperimen.xlsx", "DES_Results")
    perf_aes_ecb = get_avg("hasil_eksperimen.xlsx", "AES_Results")
    sec_des_ecb = get_avg("analisis_metrik_keamanan.xlsx", "Keamanan_DES")
    sec_aes_ecb = get_avg("analisis_metrik_keamanan.xlsx", "Keamanan_AES")

    # Tahap 2 (CBC, CTR, GCM)
    perf_des_modes = get_avg("hasil_eksperimen_tahap2.xlsx", "DES_Modes")
    perf_aes_modes = get_avg("hasil_eksperimen_tahap2.xlsx", "AES_Modes")
    sec_des_modes = get_avg("analisis_keamanan_tahap2.xlsx", "Keamanan_DES_Modes")
    sec_aes_modes = get_avg("analisis_keamanan_tahap2.xlsx", "Keamanan_AES_Modes")

    print("Data extracted successfully.")
except Exception as e:
    print(f"Error reading files: {e}")

# Build the summary table for DES
def format_table():
    # DES
    des_data = {
        "ECB": [
            "Ada (Padding)", 
            f"{perf_des_ecb['Waktu Enkripsi Long (ms)']:.2f}", 
            f"{perf_des_ecb['Waktu Dekripsi Long (ms)']:.2f}",
            f"{sec_des_ecb['C_Long: Entropy Cipher']:.4f}",
            f"{sec_des_ecb['C_Long: Koefisien Korelasi']:.4f}",
            f"{sec_des_ecb['C_Long: Avalanche Effect (%)']:.2f}%"
        ],
        "CBC": [
            "Ada (Padding)", 
            f"{perf_des_modes['CBC: Enc (ms)']:.2f}", 
            f"{perf_des_modes['CBC: Dec (ms)']:.2f}",
            f"{sec_des_modes['CBC: Entropy Cipher']:.4f}",
            f"{sec_des_modes['CBC: Korelasi']:.4f}",
            f"{sec_des_modes['CBC: Avalanche (%)']:.2f}%"
        ],
        "CTR": [
            "Tidak Ada", 
            f"{perf_des_modes['CTR: Enc (ms)']:.2f}", 
            f"{perf_des_modes['CTR: Dec (ms)']:.2f}",
            f"{sec_des_modes['CTR: Entropy Cipher']:.4f}",
            f"{sec_des_modes['CTR: Korelasi']:.4f}",
            f"{sec_des_modes['CTR: Avalanche (%)']:.4f}%" # CTR bit flip is small
        ],
        "GCM": ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
    }

    # AES
    aes_data = {
        "ECB": [
            "Ada (Padding)", 
            f"{perf_aes_ecb['Waktu Enkripsi Long (ms)']:.2f}", 
            f"{perf_aes_ecb['Waktu Dekripsi Long (ms)']:.2f}",
            f"{sec_aes_ecb['C_Long: Entropy Cipher']:.4f}",
            f"{sec_aes_ecb['C_Long: Koefisien Korelasi']:.4f}",
            f"{sec_aes_ecb['C_Long: Avalanche Effect (%)']:.2f}%"
        ],
        "CBC": [
            "Ada (Padding)", 
            f"{perf_aes_modes['CBC: Enc (ms)']:.2f}", 
            f"{perf_aes_modes['CBC: Dec (ms)']:.2f}",
            f"{sec_aes_modes['CBC: Entropy Cipher']:.4f}",
            f"{sec_aes_modes['CBC: Korelasi']:.4f}",
            f"{sec_aes_modes['CBC: Avalanche (%)']:.2f}%"
        ],
        "CTR": [
            "Tidak Ada", 
            f"{perf_aes_modes['CTR: Enc (ms)']:.2f}", 
            f"{perf_aes_modes['CTR: Dec (ms)']:.2f}",
            f"{sec_aes_modes['CTR: Entropy Cipher']:.4f}",
            f"{sec_aes_modes['CTR: Korelasi']:.4f}",
            f"{sec_aes_modes['CTR: Avalanche (%)']:.4f}%"
        ],
        "GCM": [
            "Tidak Ada (Tag)", 
            f"{perf_aes_modes['GCM: Enc (ms)']:.2f}", 
            f"{perf_aes_modes['GCM: Dec (ms)']:.2f}",
            f"{sec_aes_modes['GCM: Entropy Cipher']:.4f}",
            f"{sec_aes_modes['GCM: Korelasi']:.4f}",
            f"{sec_aes_modes['GCM: Avalanche (%)']:.4f}%"
        ]
    }

    print("\n| Algoritma | Metrik Evaluasi | ECB | CBC | CTR | GCM |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")
    metrics = ["Perubahan Ukuran File", "Waktu Enkripsi (ms)", "Waktu Dekripsi (ms)", "Entropy Cipher", "Koefisien Korelasi", "Avalanche Effect"]
    
    for i, m in enumerate(metrics):
        line = f"| **DES** | {m} | {des_data['ECB'][i]} | {des_data['CBC'][i]} | {des_data['CTR'][i]} | {des_data['GCM'][i]} |"
        print(line)
    
    for i, m in enumerate(metrics):
        line = f"| **AES** | {m} | {aes_data['ECB'][i]} | {aes_data['CBC'][i]} | {aes_data['CTR'][i]} | {aes_data['GCM'][i]} |"
        print(line)

format_table()
