import os
import time
import pandas as pd
import numpy as np
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
from collections import Counter

# Configuration
INPUT_FOLDER = "plaintext_files"
OUTPUT_EXCEL = "hasil_eksperimen.xlsx"

# Keys
# DES keys must be 8 bytes
KEY_DES_SHORT = b"key12345"  # 8 bytes
KEY_DES_LONG  = b"kryptos!"   # 8 bytes (DES only supports 8 bytes, so we use different ones)

# AES keys can be 16, 24, or 32 bytes
KEY_AES_SHORT = b"thisisashortkey1"  # 16 bytes (AES-128)
KEY_AES_LONG  = b"thisisalongkey256bitversion!!!!!"  # 32 bytes (AES-256)

def calculate_char_dist_variance(data):
    """Calculates the variance of byte frequencies to measure distribution flatness."""
    counts = Counter(data)
    # Ensure all 256 bytes are considered
    freqs = [counts.get(i, 0) for i in range(256)]
    return np.var(freqs)

def encrypt_process(data, algorithm, key, mode=AES.MODE_ECB):
    block_size = algorithm.block_size
    padded_data = pad(data, block_size)
    
    cipher = algorithm.new(key, mode)
    
    start_time = time.perf_counter()
    ciphertext = cipher.encrypt(padded_data)
    end_time = time.perf_counter()
    
    enc_time_ms = (end_time - start_time) * 1000
    return ciphertext, enc_time_ms

def decrypt_process(ciphertext, algorithm, key, mode=AES.MODE_ECB):
    cipher = algorithm.new(key, mode)
    
    start_time = time.perf_counter()
    decrypted_padded = cipher.decrypt(ciphertext)
    end_time = time.perf_counter()
    
    dec_time_ms = (end_time - start_time) * 1000
    plaintext = unpad(decrypted_padded, algorithm.block_size)
    return plaintext, dec_time_ms

def perform_experiment():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' not found. Please run generate_data.py first.")
        return

    files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")])
    if not files:
        print(f"Error: No files found in '{INPUT_FOLDER}'.")
        return

    des_data = []
    aes_data = []

    print(f"Starting experiment on {len(files)} files...")

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        with open(filepath, "rb") as f:
            plaintext = f.read()

        size_mb = len(plaintext) / (1024 * 1024)
        var_plain = calculate_char_dist_variance(plaintext)

        # --- DES EXPERIMENT ---
        # Short Key
        c_des_s, t_enc_des_s = encrypt_process(plaintext, DES, KEY_DES_SHORT)
        _, t_dec_des_s = decrypt_process(c_des_s, DES, KEY_DES_SHORT)
        var_des_s = calculate_char_dist_variance(c_des_s)
        
        # Long Key
        c_des_l, t_enc_des_l = encrypt_process(plaintext, DES, KEY_DES_LONG)
        _, t_dec_des_l = decrypt_process(c_des_l, DES, KEY_DES_LONG)
        var_des_l = calculate_char_dist_variance(c_des_l)

        des_data.append({
            "No": i,
            "Ukuran File Plainteks (MB)": size_mb,
            "Waktu Enkripsi Short (ms)": t_enc_des_s,
            "Waktu Dekripsi Short (ms)": t_dec_des_s,
            "Ukuran Cipherteks Short (MB)": len(c_des_s) / (1024 * 1024),
            "Waktu Enkripsi Long (ms)": t_enc_des_l,
            "Waktu Dekripsi Long (ms)": t_dec_des_l,
            "Ukuran Cipherteks Long (MB)": len(c_des_l) / (1024 * 1024),
            "Var Plain": var_plain,
            "Var Cipher Short": var_des_s,
            "Var Cipher Long": var_des_l
        })

        # --- AES EXPERIMENT ---
        # Short Key (AES-128)
        c_aes_s, t_enc_aes_s = encrypt_process(plaintext, AES, KEY_AES_SHORT)
        _, t_dec_aes_s = decrypt_process(c_aes_s, AES, KEY_AES_SHORT)
        var_aes_s = calculate_char_dist_variance(c_aes_s)

        # Long Key (AES-256)
        c_aes_l, t_enc_aes_l = encrypt_process(plaintext, AES, KEY_AES_LONG)
        _, t_dec_aes_l = decrypt_process(c_aes_l, AES, KEY_AES_LONG)
        var_aes_l = calculate_char_dist_variance(c_aes_l)

        aes_data.append({
            "No": i,
            "Ukuran File Plainteks (MB)": size_mb,
            "Waktu Enkripsi Short (ms)": t_enc_aes_s,
            "Waktu Dekripsi Short (ms)": t_dec_aes_s,
            "Ukuran Cipherteks Short (MB)": len(c_aes_s) / (1024 * 1024),
            "Waktu Enkripsi Long (ms)": t_enc_aes_l,
            "Waktu Dekripsi Long (ms)": t_dec_aes_l,
            "Ukuran Cipherteks Long (MB)": len(c_aes_l) / (1024 * 1024),
            "Var Plain": var_plain,
            "Var Cipher Short": var_aes_s,
            "Var Cipher Long": var_aes_l
        })

        if i % 10 == 0:
            print(f"Processed {i}/100 files...")

    # Create DataFrames
    df_des = pd.DataFrame(des_data)
    df_aes = pd.DataFrame(aes_data)

    # Add Average Row (Row 101)
    def add_average_row(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        # Remove 'No' from average calculation if it's just an index
        if "No" in numeric_cols:
            numeric_cols.remove("No")
        
        averages = df[numeric_cols].mean()
        avg_row = {col: averages[col] for col in numeric_cols}
        avg_row["No"] = "RATA-RATA"
        # Fill non-numeric columns with empty string or relevant label if any exist
        for col in df.columns:
            if col not in avg_row:
                avg_row[col] = ""
        
        return pd.concat([df, pd.DataFrame([avg_row])], ignore_index=True)

    df_des = add_average_row(df_des)
    df_aes = add_average_row(df_aes)

    # Save to Excel
    with pd.ExcelWriter(OUTPUT_EXCEL) as writer:
        df_des.to_excel(writer, sheet_name="DES_Results", index=False)
        df_aes.to_excel(writer, sheet_name="AES_Results", index=False)

    print(f"Experiment complete! Results saved to {OUTPUT_EXCEL}")

if __name__ == "__main__":
    perform_experiment()