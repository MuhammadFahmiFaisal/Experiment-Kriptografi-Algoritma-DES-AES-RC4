import pandas as pd

def consolidate():
    print("Menggabungkan data berdasarkan algoritme...")

    # --- DES CONSOLIDATION ---
    with pd.ExcelWriter("LAPORAN_FINAL_DES.xlsx") as writer:
        # Stage 1: ECB (Combine Perf and Security if possible, or separate sheets)
        df_p1 = pd.read_excel("hasil_eksperimen.xlsx", sheet_name="DES_Results")
        df_s1 = pd.read_excel("analisis_metrik_keamanan.xlsx", sheet_name="Keamanan_DES")
        df_p1.to_excel(writer, sheet_name="Tahap1_ECB_Performa", index=False)
        df_s1.to_excel(writer, sheet_name="Tahap1_ECB_Keamanan", index=False)
        
        # Stage 2: Modes
        df_p2 = pd.read_excel("hasil_eksperimen_tahap2.xlsx", sheet_name="DES_Modes")
        df_s2 = pd.read_excel("analisis_keamanan_tahap2.xlsx", sheet_name="Keamanan_DES_Modes")
        df_p2.to_excel(writer, sheet_name="Tahap2_Modes_Performa", index=False)
        df_s2.to_excel(writer, sheet_name="Tahap2_Modes_Keamanan", index=False)

    # --- AES CONSOLIDATION ---
    with pd.ExcelWriter("LAPORAN_FINAL_AES.xlsx") as writer:
        # Stage 1: ECB
        df_p1_aes = pd.read_excel("hasil_eksperimen.xlsx", sheet_name="AES_Results")
        df_s1_aes = pd.read_excel("analisis_metrik_keamanan.xlsx", sheet_name="Keamanan_AES")
        df_p1_aes.to_excel(writer, sheet_name="Tahap1_ECB_Performa", index=False)
        df_s1_aes.to_excel(writer, sheet_name="Tahap1_ECB_Keamanan", index=False)
        
        # Stage 2: Modes
        df_p2_aes = pd.read_excel("hasil_eksperimen_tahap2.xlsx", sheet_name="AES_Modes")
        df_s2_aes = pd.read_excel("analisis_keamanan_tahap2.xlsx", sheet_name="Keamanan_AES_Modes")
        df_p2_aes.to_excel(writer, sheet_name="Tahap2_Modes_Performa", index=False)
        df_s2_aes.to_excel(writer, sheet_name="Tahap2_Modes_Keamanan", index=False)

    # --- RC4 CONSOLIDATION ---
    with pd.ExcelWriter("LAPORAN_FINAL_RC4.xlsx") as writer:
        df_rc4 = pd.read_excel("hasil_eksperimen_tahap3_rc4.xlsx")
        df_rc4.to_excel(writer, sheet_name="Tahap3_RC4_Lengkap", index=False)

    print("Konsolidasi Selesai!")
    print("File Dibuat: LAPORAN_FINAL_DES.xlsx, LAPORAN_FINAL_AES.xlsx, LAPORAN_FINAL_RC4.xlsx")

if __name__ == "__main__":
    consolidate()
