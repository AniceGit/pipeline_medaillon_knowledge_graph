#Validation Great Expectations
import os
import pandas as pd
BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"

os.makedirs(SILVER_DIR, exist_ok=True)

def clean_nodes():
    bronze_path = os.path.join(BRONZE_DIR, "nodes.parquet")
    silver_path = os.path.join(SILVER_DIR, "nodes.parquet")
    df = pd.read_parquet(bronze_path)
    original_count = len(df)

    df_clean = df.drop_duplicates(subset=["id"])
    cleaned_count = len(df_clean)

    if cleaned_count < original_count:
        print(f"X Nodes:{original_count - cleaned_count} doublon(s) trouvé(s) et supprimé(s)")
        df_clean.to_parquet(silver_path, index=False)
    else:
        df_clean.to_parquet(silver_path, index=False)
        print("O Nodes: Aucun doublon trouvé.")

def clean_edges():
    bronze_path = os.path.join(BRONZE_DIR, "edges.parquet")
    silver_path = os.path.join(SILVER_DIR, "edges.parquet")
    df = pd.read_parquet(bronze_path)
    original_count = len(df)

    df_clean = df.dropna(subset=["src", "dst"])
    cleaned_count = len(df_clean)

    if cleaned_count < original_count:
        print(f"X Edges: {original_count - cleaned_count} ligne(s) contenant un ou plusieurs nulls trouvée(s).")
        df_clean.to_parquet(silver_path, index=False)
    else:
        df_clean.to_parquet(silver_path, index=False)
        print("O Edges: Aucun null trouvé sur les colonnes 'src' ou 'dst'.")

def main():
    clean_nodes()
    clean_edges()

if __name__ == "__main__":
    main()
