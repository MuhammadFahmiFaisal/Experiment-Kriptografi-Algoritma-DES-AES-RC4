import os
import time
import pandas as pd
import numpy as np
import math
from Crypto.Cipher import ARC4
from collections import Counter

# Configuration
INPUT_FOLDER = "plaintext_files"
OUTPUT_EXCEL = "hasil_eksperimen_tahap3_rc4.xlsx"

# Keys for RC4
KEY_RC4_SHORT = b"secretkeyshort1"  # 16 bytes
KEY_RC4_LONG  = b"thisisareallylongsecretkeyforrc4" # 32 bytes

def calculate_entropy(data):
    if not data: return 0
    counts = Counter(data)
    total = len(data)
    return -sum((count/total) * math.log2(count/total) for count in counts.values())

def calculate_correlation(p_bytes, c_bytes):
    p_arr = np.frombuffer(p_bytes, dtype=np.uint8)
    c_arr = np.frombuffer(c_bytes, dtype=np.uint8)
    return np.corrcoef(p_arr, c_arr)[0, 1]

def calculate_avalanche_rc4(plaintext, key):
    # Original
    cipher1 = ARC4.new(key)
    c1 = cipher1.encrypt(plaintext)
    
    # Flip 1 bit in P
    p2 = bytearray(plaintext)
    p2[0] ^= 0x01
    
    # Modified
    cipher2 = ARC4.new(key)
    c2 = cipher2.encrypt(bytes(p2))
    
    # Count bit differences
    diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(c1, c2))
    total_bits = len(c1) * 8
    return (diff_bits / total_bits) * 100

def run_experiment_tahap3():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' tidak ditemukan.")
        return

    files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")])
    print(f"Memulai Eksperimen Tahap 3 (RC4) pada {len(files)} file...")

    results = []

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        with open(filepath, "rb") as f:
            plaintext = f.read()
        
        size_mb = len(plaintext) / (1024 * 1024)

        # 1. RC4 Short Key
        start = time.perf_counter()
        cipher_s = ARC4.new(KEY_RC4_SHORT)
        c_s = cipher_s.encrypt(plaintext)
        t_enc_s = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_dec_s = ARC4.new(KEY_RC4_SHORT)
        _ = cipher_dec_s.decrypt(c_s)
        t_dec_s = (time.perf_counter() - start) * 1000

        # 2. RC4 Long Key
        start = time.perf_counter()
        cipher_l = ARC4.new(KEY_RC4_LONG)
        c_l = cipher_l.encrypt(plaintext)
        t_enc_l = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_dec_l = ARC4.new(KEY_RC4_LONG)
        _ = cipher_dec_l.decrypt(c_l)
        t_dec_l = (time.perf_counter() - start) * 1000

        results.append({
            "No": i,
            "Ukuran Plainteks (MB)": size_mb,
            "Short: Waktu Enc (ms)": t_enc_s,
            "Short: Waktu Dec (ms)": t_dec_s,
            "Short: Ukuran Cipher (MB)": len(c_s) / (1024 * 1024),
            "Short: Entropy Cipher": calculate_entropy(c_s),
            "Short: Korelasi": calculate_correlation(plaintext, c_s),
            "Short: Avalanche (%)": calculate_avalanche_rc4(plaintext, KEY_RC4_SHORT),
            "Long: Waktu Enc (ms)": t_enc_l,
            "Long: Waktu Dec (ms)": t_dec_l,
            "Long: Ukuran Cipher (MB)": len(c_l) / (1024 * 1024),
            "Long: Entropy Cipher": calculate_entropy(c_l),
            "Long: Korelasi": calculate_correlation(plaintext, c_l),
            "Long: Avalanche (%)": calculate_avalanche_rc4(plaintext, KEY_RC4_LONG)
        })

        if i % 10 == 0:
            print(f"Processed {i}/100 files...")

    # Averages
    def add_avg(data):
        df = pd.DataFrame(data)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if "No" in numeric_cols: numeric_cols.remove("No")
        averages = df[numeric_cols].mean()
        avg_row = {col: averages[col] for col in numeric_cols}
        avg_row["No"] = "RATA-RATA"
        for col in df.columns:
            if col not in avg_row: avg_row[col] = ""
        return pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    df_final = add_avg(results)
    df_final.to_excel(OUTPUT_EXCEL, index=False)

    print(f"Eksperimen Tahap 3 Selesai! Hasil di {OUTPUT_EXCEL}")

if __name__ == "__main__":
    run_experiment_tahap3()
