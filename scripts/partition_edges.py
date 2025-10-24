#Partitionnement des données d’arêtes en plusieurs shards
import os
import pandas as pd

#Répertoire source et nombre de partitions
SILVER_DIR = "data/silver"
N_SHARDS = 8

#Création du répertoire de sortie si nécessaire
os.makedirs(SILVER_DIR, exist_ok=True)

def partition_edges():
    """Partitionne le fichier edges.parquet en plusieurs shards selon la colonne 'src'."""
    #Lecture du fichier des arêtes nettoyé
    df = pd.read_parquet(os.path.join(SILVER_DIR, "edges.parquet"))

    #Calcul du shard pour chaque ligne
    df["shard"] = df["src"] % N_SHARDS  

    #Création et écriture des fichiers shardés
    for shard_id in range(N_SHARDS):
        shard_dir = os.path.join(SILVER_DIR, f"shard={shard_id}")
        os.makedirs(shard_dir, exist_ok=True)

        #Sélection des lignes appartenant à ce shard
        shard_df = df[df["shard"] == shard_id].drop(columns=["shard"])
        shard_df.to_parquet(os.path.join(shard_dir, "edges.parquet"), index=False)
        print(f"[+] Shard {shard_id} généré. Contient {len(shard_df)} edges.")

def main():
    """Exécute le partitionnement des arêtes."""
    partition_edges()

if __name__ == "__main__":
    main()
