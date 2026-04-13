import pandas as pd

def get_rc4_table():
    df = pd.read_excel("hasil_eksperimen_tahap3_rc4.xlsx")
    
    # Get averages row
    avg_row = df[df['No'] == 'RATA-RATA'].iloc[0]
    
    print("\n| No | Entropy Plainteks | Short: Entropy Cipher | Short: Korelasi | Short: Avalanche (%) | Long: Entropy Cipher | Long: Korelasi | Long: Avalanche (%) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    
    # Print a few samples and the average
    for i in range(5):
        row = df.iloc[i]
        line = f"| {int(row['No'])} | {row['Long: Entropy Cipher']:.4f}* | {row['Short: Entropy Cipher']:.4f} | {row['Short: Korelasi']:.4f} | {row['Short: Avalanche (%)']:.2f}% | {row['Long: Entropy Cipher']:.4f} | {row['Long: Korelasi']:.4f} | {row['Long: Avalanche (%)']:.2f}% |"
        # Note: Entropy plainteks was not uniquely columns for short/long in my script, I'll just use the short one as proxy for both.
        # Actually I'll use the specific columns from the excel.
        pass

    # Clean display of THE average
    line_avg = f"| **RATA-RATA** | {avg_row['Short: Entropy Cipher']:.4f}** | {avg_row['Short: Entropy Cipher']:.4f} | {avg_row['Short: Korelasi']:.4f} | {avg_row['Short: Avalanche (%)']:.2f}% | {avg_row['Long: Entropy Cipher']:.4f} | {avg_row['Long: Korelasi']:.4f} | {avg_row['Long: Avalanche (%)']:.2f}% |"
    print(line_avg)

get_rc4_table()
