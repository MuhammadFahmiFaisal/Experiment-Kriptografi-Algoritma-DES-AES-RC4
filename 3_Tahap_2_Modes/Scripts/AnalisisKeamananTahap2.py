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
OUTPUT_EXCEL = "analisis_keamanan_tahap2.xlsx"

# Long Keys from Stage 1
KEY_DES_LONG  = b"kryptos!"
KEY_AES_LONG  = b"thisisashortkey1thisisashortkey1" # Ensure 32 bytes

def calculate_entropy(data):
    if not data: return 0
    counts = Counter(data)
    total = len(data)
    return -sum((count/total) * math.log2(count/total) for count in counts.values())

def calculate_correlation(p_bytes, c_bytes):
    min_len = min(len(p_bytes), len(c_bytes))
    p_arr = np.frombuffer(p_bytes[:min_len], dtype=np.uint8)
    c_arr = np.frombuffer(c_bytes[:min_len], dtype=np.uint8)
    return np.corrcoef(p_arr, c_arr)[0, 1]

def calculate_avalanche_mode(plaintext, algorithm, key, mode, **kwargs):
    block_size = algorithm.block_size
    # Original
    if mode == AES.MODE_GCM:
        c1, tag1 = algorithm.new(key, mode, **kwargs).encrypt_and_digest(plaintext)
    elif mode == AES.MODE_CTR:
        c1 = algorithm.new(key, mode, **kwargs).encrypt(plaintext)
    else:
        c1 = algorithm.new(key, mode, **kwargs).encrypt(pad(plaintext, block_size))
        
    # Modified (Flip 1 bit)
    p2 = bytearray(plaintext)
    p2[0] ^= 0x01
    
    if mode == AES.MODE_GCM:
        c2, tag2 = algorithm.new(key, mode, **kwargs).encrypt_and_digest(bytes(p2))
    elif mode == AES.MODE_CTR:
        c2 = algorithm.new(key, mode, **kwargs).encrypt(bytes(p2))
    else:
        c2 = algorithm.new(key, mode, **kwargs).encrypt(pad(bytes(p2), block_size))
        
    # Count bit differences
    diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(c1, c2))
    
    # For GCM, also include tag differences? usually just ciphertext is fine
    # but GCM is CTR + Tag. CTR flip only flips 1 bit.
    
    total_bits = len(c1) * 8
    return (diff_bits / total_bits) * 100

def run_security_analysis_tahap2():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' tidak ditemukan.")
        return

    files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")])
    print(f"Memulai Analisis Keamanan Tahap 2 pada {len(files)} file...")

    results_aes = []
    results_des = []

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        with open(filepath, "rb") as f:
            p_bytes = f.read()
        
        ent_p = calculate_entropy(p_bytes)

        # --- AES MODES ---
        # 1. CBC
        iv = os.urandom(16)
        c_cbc = AES.new(KEY_AES_LONG, AES.MODE_CBC, iv).encrypt(pad(p_bytes, 16))
        
        # 2. CTR
        nonce_ctr = os.urandom(8)
        c_ctr = AES.new(KEY_AES_LONG, AES.MODE_CTR, nonce=nonce_ctr).encrypt(p_bytes)
        
        # 3. GCM
        nonce_gcm = os.urandom(12)
        c_gcm, _ = AES.new(KEY_AES_LONG, AES.MODE_GCM, nonce=nonce_gcm).encrypt_and_digest(p_bytes)

        results_aes.append({
            "No": i, "Entropy Plainteks": ent_p,
            "CBC: Entropy Cipher": calculate_entropy(c_cbc), "CBC: Korelasi": calculate_correlation(p_bytes, c_cbc), "CBC: Avalanche (%)": calculate_avalanche_mode(p_bytes, AES, KEY_AES_LONG, AES.MODE_CBC, iv=iv),
            "CTR: Entropy Cipher": calculate_entropy(c_ctr), "CTR: Korelasi": calculate_correlation(p_bytes, c_ctr), "CTR: Avalanche (%)": calculate_avalanche_mode(p_bytes, AES, KEY_AES_LONG, AES.MODE_CTR, nonce=nonce_ctr),
            "GCM: Entropy Cipher": calculate_entropy(c_gcm), "GCM: Korelasi": calculate_correlation(p_bytes, c_gcm), "GCM: Avalanche (%)": calculate_avalanche_mode(p_bytes, AES, KEY_AES_LONG, AES.MODE_GCM, nonce=nonce_gcm)
        })

        # --- DES MODES ---
        iv_des = os.urandom(8)
        c_des_cbc = DES.new(KEY_DES_LONG, DES.MODE_CBC, iv_des).encrypt(pad(p_bytes, 8))
        nonce_des_ctr = os.urandom(4)
        c_des_ctr = DES.new(KEY_DES_LONG, DES.MODE_CTR, nonce=nonce_des_ctr).encrypt(p_bytes)

        results_des.append({
            "No": i, "Entropy Plainteks": ent_p,
            "CBC: Entropy Cipher": calculate_entropy(c_des_cbc), "CBC: Korelasi": calculate_correlation(p_bytes, c_des_cbc), "CBC: Avalanche (%)": calculate_avalanche_mode(p_bytes, DES, KEY_DES_LONG, DES.MODE_CBC, iv=iv_des),
            "CTR: Entropy Cipher": calculate_entropy(c_des_ctr), "CTR: Korelasi": calculate_correlation(p_bytes, c_des_ctr), "CTR: Avalanche (%)": calculate_avalanche_mode(p_bytes, DES, KEY_DES_LONG, DES.MODE_CTR, nonce=nonce_des_ctr),
            "GCM": "N/A"
        })

        if i % 10 == 0:
            print(f"Dianalisis {i}/100 file...")

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

    df_aes = process_df(results_aes)
    df_des = process_df(results_des)

    with pd.ExcelWriter(OUTPUT_EXCEL) as writer:
        df_aes.to_excel(writer, sheet_name="Keamanan_AES_Modes", index=False)
        df_des.to_excel(writer, sheet_name="Keamanan_DES_Modes", index=False)

    print(f"Analisis Keamanan Selesai! Hasil di {OUTPUT_EXCEL}")

if __name__ == "__main__":
    run_security_analysis_tahap2()
