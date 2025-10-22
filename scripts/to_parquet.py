#Conversion CSV -> Parquet
import os
import pandas as pd

RAW_DIR = "data/raw"
BRONZE_DIR = "data/bronze"

os.makedirs(BRONZE_DIR, exist_ok=True)

def convert_csv_to_parquet(filename):
    csv_path = os.path.join(RAW_DIR, filename)
    parquet_path = os.path.join(BRONZE_DIR, filename.replace(".csv", ".parquet"))
    df = pd.read_csv(csv_path)
    df.to_parquet(parquet_path, index=False)
    print(f"[+] Converted {filename} -> {parquet_path}")

def main():
    convert_csv_to_parquet("nodes.csv")
    convert_csv_to_parquet("edges.csv")

if __name__ == "__main__":
    main()
