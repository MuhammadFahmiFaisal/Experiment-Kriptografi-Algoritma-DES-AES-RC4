import os
import time
import pandas as pd
import numpy as np
from Crypto.Cipher import DES, AES
from Crypto.Util import Counter
from Crypto.Util.Padding import pad, unpad

# Configuration
INPUT_FOLDER = "plaintext_files"
OUTPUT_EXCEL = "hasil_eksperimen_tahap2.xlsx"

# Long Keys from Stage 1
KEY_DES_LONG  = b"kryptos!"   # 8 bytes
KEY_AES_LONG  = b"thisisalongkey256bitversion!!!!!"  # 32 bytes

def run_experiment_tahap2():
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' tidak ditemukan.")
        return

    files = sorted([f for f in os.listdir(INPUT_FOLDER) if f.endswith(".txt")])
    print(f"Memulai Eksperimen Tahap 2 pada {len(files)} file...")

    results_aes = []
    results_des = []

    for i, filename in enumerate(files, 1):
        filepath = os.path.join(INPUT_FOLDER, filename)
        with open(filepath, "rb") as f:
            plaintext = f.read()
        
        size_mb = len(plaintext) / (1024 * 1024)

        # --- AES MODES (CBC, CTR, GCM) ---
        # 1. AES CBC
        iv_cbc = os.urandom(16)
        start = time.perf_counter()
        cipher_cbc = AES.new(KEY_AES_LONG, AES.MODE_CBC, iv_cbc)
        c_cbc = cipher_cbc.encrypt(pad(plaintext, 16))
        t_enc_cbc = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_dec_cbc = AES.new(KEY_AES_LONG, AES.MODE_CBC, iv_cbc)
        _ = unpad(cipher_dec_cbc.decrypt(c_cbc), 16)
        t_dec_cbc = (time.perf_counter() - start) * 1000

        # 2. AES CTR
        nonce_ctr = os.urandom(8)
        start = time.perf_counter()
        cipher_ctr = AES.new(KEY_AES_LONG, AES.MODE_CTR, nonce=nonce_ctr)
        c_ctr = cipher_ctr.encrypt(plaintext) # CTR doesn't need padding
        t_enc_ctr = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_dec_ctr = AES.new(KEY_AES_LONG, AES.MODE_CTR, nonce=nonce_ctr)
        _ = cipher_dec_ctr.decrypt(c_ctr)
        t_dec_ctr = (time.perf_counter() - start) * 1000

        # 3. AES GCM
        nonce_gcm = os.urandom(12)
        start = time.perf_counter()
        cipher_gcm = AES.new(KEY_AES_LONG, AES.MODE_GCM, nonce=nonce_gcm)
        c_gcm, tag = cipher_gcm.encrypt_and_digest(plaintext)
        t_enc_gcm = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_dec_gcm = AES.new(KEY_AES_LONG, AES.MODE_GCM, nonce=nonce_gcm)
        _ = cipher_dec_gcm.decrypt_and_verify(c_gcm, tag)
        t_dec_gcm = (time.perf_counter() - start) * 1000

        results_aes.append({
            "No": i,
            "Ukuran Plainteks (MB)": size_mb,
            "CBC: Enc (ms)": t_enc_cbc, "CBC: Dec (ms)": t_dec_cbc, "CBC: Size (MB)": len(c_cbc)/(1024*1024),
            "CTR: Enc (ms)": t_enc_ctr, "CTR: Dec (ms)": t_dec_ctr, "CTR: Size (MB)": len(c_ctr)/(1024*1024),
            "GCM: Enc (ms)": t_enc_gcm, "GCM: Dec (ms)": t_dec_gcm, "GCM: Size (MB)": len(c_gcm)/(1024*1024)
        })

        # --- DES MODES (CBC, CTR) ---
        # Note: GCM is not supported for 64-bit block ciphers like DES in PyCryptodome.
        # We will implement CBC and CTR for DES.
        
        # 1. DES CBC
        iv_des = os.urandom(8)
        start = time.perf_counter()
        cipher_des_cbc = DES.new(KEY_DES_LONG, DES.MODE_CBC, iv_des)
        c_des_cbc = cipher_des_cbc.encrypt(pad(plaintext, 8))
        t_enc_des_cbc = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_des_dec_cbc = DES.new(KEY_DES_LONG, DES.MODE_CBC, iv_des)
        _ = unpad(cipher_des_dec_cbc.decrypt(c_des_cbc), 8)
        t_dec_des_cbc = (time.perf_counter() - start) * 1000

        # 2. DES CTR
        nonce_des_ctr = os.urandom(4)
        start = time.perf_counter()
        cipher_des_ctr = DES.new(KEY_DES_LONG, DES.MODE_CTR, nonce=nonce_des_ctr)
        c_des_ctr = cipher_des_ctr.encrypt(plaintext)
        t_enc_des_ctr = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        cipher_des_dec_ctr = DES.new(KEY_DES_LONG, DES.MODE_CTR, nonce=nonce_des_ctr)
        _ = cipher_des_dec_ctr.decrypt(c_des_ctr)
        t_dec_des_ctr = (time.perf_counter() - start) * 1000

        results_des.append({
            "No": i,
            "Ukuran Plainteks (MB)": size_mb,
            "CBC: Enc (ms)": t_enc_des_cbc, "CBC: Dec (ms)": t_dec_des_cbc, "CBC: Size (MB)": len(c_des_cbc)/(1024*1024),
            "CTR: Enc (ms)": t_enc_des_ctr, "CTR: Dec (ms)": t_dec_des_ctr, "CTR: Size (MB)": len(c_des_ctr)/(1024*1024),
            "GCM": "N/A (Block size < 128 bit)"
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

    df_aes = add_avg(results_aes)
    df_des = add_avg(results_des)

    with pd.ExcelWriter(OUTPUT_EXCEL) as writer:
        df_aes.to_excel(writer, sheet_name="AES_Modes", index=False)
        df_des.to_excel(writer, sheet_name="DES_Modes", index=False)

    print(f"Eksperimen Tahap 2 Selesai! Hasil di {OUTPUT_EXCEL}")

if __name__ == "__main__":
    run_experiment_tahap2()
