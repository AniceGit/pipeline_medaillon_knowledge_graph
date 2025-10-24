#Partitionnement
import os
import pandas as pd

SILVER_DIR = "data/silver"
N_SHARDS = 8

os.makedirs(SILVER_DIR, exist_ok=True)

def partition_edges():
    df = pd.read_parquet(os.path.join(SILVER_DIR, "edges.parquet"))
    df["shard"] = df["src"] % N_SHARDS  
    for shard_id in range(N_SHARDS):
        shard_dir = os.path.join(SILVER_DIR, f"shard={shard_id}")
        os.makedirs(shard_dir, exist_ok=True)
        shard_df = df[df["shard"] == shard_id].drop(columns=["shard"])
        shard_df.to_parquet(os.path.join(shard_dir, "edges.parquet"), index=False)
        print(f"[+] Shard {shard_id} généré. Contient {len(shard_df)} edges.")

def main():
    partition_edges()

if __name__ == "__main__":
    main()
