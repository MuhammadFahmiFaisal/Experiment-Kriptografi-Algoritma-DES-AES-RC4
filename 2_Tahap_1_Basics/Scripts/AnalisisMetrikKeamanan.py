import os
import time
import pandas as pd
import numpy as np
import math
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad
from collections import Counter

# Configuration
INPUT_FOLDER = "plaintext_files"
OUTPUT_EXCEL = "analisis_metrik_keamanan.xlsx"

# Keys (Same as previous stage for consistency)
KEY_DES_SHORT = b"key12345"
KEY_DES_LONG  = b"kryptos!"
KEY_AES_SHORT = b"thisisashortkey1"
KEY_AES_LONG  = b"thisisalongkey256bitversion!!!!!"

def calculate_entropy(data):
    """Calculates Shannon Entropy of a byte sequence."""
    if not data:
        return 0
    entropy = 0
    counts = Counter(data)
    total = len(data)
    for count in counts.values():
        p = count / total
        entropy -= p * math.log2(p)
    return entropy

def calculate_correlation(p_bytes, c_bytes):
    """Calculates Pearson Correlation Coefficient between plaintext and ciphertext bytes."""
    # Ensure same length (ciphertext might be padded, so we truncate/pad P to match C)
    # Actually, for ECB, C length = padded P length.
    if len(p_bytes) != len(c_bytes):
        min_len = min(len(p_bytes), len(c_bytes))
        p_bytes = p_bytes[:min_len]
        c_bytes = c_bytes[:min_len]
        
    p_arr = np.frombuffer(p_bytes, dtype=np.uint8)
    c_arr = np.frombuffer(c_bytes, dtype=np.uint8)
    
    correlation_matrix = np.corrcoef(p_arr, c_arr)
    return correlation_matrix[0, 1]

def calculate_avalanche(plaintext, algorithm, key, mode=AES.MODE_ECB):
    """Calculates Avalanche Effect % by flipping 1 bit in plaintext."""
    block_size = algorithm.block_size
    padded_p1 = pad(plaintext, block_size)
    
    # Original Encryption
    cipher1 = algorithm.new(key, mode)
    c1 = cipher1.encrypt(padded_p1)
    
    # Flip 1 bit in P (e.g., first bit of first byte)
    p2 = bytearray(plaintext)
    p2[0] ^= 0x01  # Flip LSB of first byte
    padded_p2 = pad(bytes(p2), block_size)
    
    # Modified Encryption
    cipher2 = algorithm.new(key, mode)
    c2 = cipher2.encrypt(padded_p2)
    
    # Count bit differences (Hamming Distance)
    diff_bits = 0
    for b1, b2 in zip(c1, c2):
        diff_bits += bin(b1 ^ b2).count('1')
        
    total_bits = len(c1) * 8
    return (diff_bits / total_bits) * 100

def run_security_analysis():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' tidak ditemukan.")
        return

    files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")])
    print(f"Memulai Analisis Metrik Keamanan pada {len(files)} file...")

    des_results = []
    aes_results = []

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        with open(filepath, "rb") as f:
            p_bytes = f.read()

        ent_p = calculate_entropy(p_bytes)

        # --- DES ANALYSIS ---
        # Short Key
        c1_des_s = DES.new(KEY_DES_SHORT, DES.MODE_ECB).encrypt(pad(p_bytes, DES.block_size))
        ent_c_des_s = calculate_entropy(c1_des_s)
        corr_des_s = calculate_correlation(p_bytes, c1_des_s)
        aval_des_s = calculate_avalanche(p_bytes, DES, KEY_DES_SHORT)
        
        # Long Key
        c1_des_l = DES.new(KEY_DES_LONG, DES.MODE_ECB).encrypt(pad(p_bytes, DES.block_size))
        ent_c_des_l = calculate_entropy(c1_des_l)
        corr_des_l = calculate_correlation(p_bytes, c1_des_l)
        aval_des_l = calculate_avalanche(p_bytes, DES, KEY_DES_LONG)

        des_results.append({
            "No": i,
            "Entropy Plainteks": ent_p,
            "C_Short: Entropy Cipher": ent_c_des_s,
            "C_Short: Koefisien Korelasi": corr_des_s,
            "C_Short: Avalanche Effect (%)": aval_des_s,
            "C_Long: Entropy Cipher": ent_c_des_l,
            "C_Long: Koefisien Korelasi": corr_des_l,
            "C_Long: Avalanche Effect (%)": aval_des_l
        })

        # --- AES ANALYSIS ---
        # Short Key
        c1_aes_s = AES.new(KEY_AES_SHORT, AES.MODE_ECB).encrypt(pad(p_bytes, AES.block_size))
        ent_c_aes_s = calculate_entropy(c1_aes_s)
        corr_aes_s = calculate_correlation(p_bytes, c1_aes_s)
        aval_aes_s = calculate_avalanche(p_bytes, AES, KEY_AES_SHORT)

        # Long Key
        c1_aes_l = AES.new(KEY_AES_LONG, AES.MODE_ECB).encrypt(pad(p_bytes, AES.block_size))
        ent_c_aes_l = calculate_entropy(c1_aes_l)
        corr_aes_l = calculate_correlation(p_bytes, c1_aes_l)
        aval_aes_l = calculate_avalanche(p_bytes, AES, KEY_AES_LONG)

        aes_results.append({
            "No": i,
            "Entropy Plainteks": ent_p,
            "C_Short: Entropy Cipher": ent_c_aes_s,
            "C_Short: Koefisien Korelasi": corr_aes_s,
            "C_Short: Avalanche Effect (%)": aval_aes_s,
            "C_Long: Entropy Cipher": ent_c_aes_l,
            "C_Long: Koefisien Korelasi": corr_aes_l,
            "C_Long: Avalanche Effect (%)": aval_aes_l
        })

        if i % 10 == 0:
            print(f"Dianalisis {i}/100 file...")

    # DataFrames and Averages
    def process_df(data):
        df = pd.DataFrame(data)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if "No" in numeric_cols: numeric_cols.remove("No")
        
        averages = df[numeric_cols].mean()
        avg_row = {col: averages[col] for col in numeric_cols}
        avg_row["No"] = "RATA-RATA"
        for col in df.columns:
            if col not in avg_row: avg_row[col] = ""
            
        return pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    df_des = process_df(des_results)
    df_aes = process_df(aes_results)

    # Save to Excel
    with pd.ExcelWriter(OUTPUT_EXCEL) as writer:
        df_des.to_excel(writer, sheet_name="Keamanan_DES", index=False)
        df_aes.to_excel(writer, sheet_name="Keamanan_AES", index=False)

    print(f"Analisis Selesai! Hasil disimpan di {OUTPUT_EXCEL}")

if __name__ == "__main__":
    run_security_analysis()
