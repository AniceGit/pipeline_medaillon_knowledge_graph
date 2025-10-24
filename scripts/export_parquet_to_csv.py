#Export des fichiers Parquet (Silver) vers CSV au format Neo4j
"""
Convertit les fichiers Parquet (Silver) en CSV format Neo4j.
Nodes : id:ID, name, label
Edges : :START_ID, :END_ID, type
"""

import os
import glob
import pandas as pd

#Répertoires source (Silver) et destination (Gold)
SILVER_DIR = "data/silver"
GOLD_DIR = "data/gold"

#Création du dossier de sortie si nécessaire
os.makedirs(GOLD_DIR, exist_ok=True)

def export_nodes():
    """Exporte le fichier des noeuds Parquet en CSV Neo4j."""
    nodes_path = os.path.join(SILVER_DIR, "nodes.parquet")
    if not os.path.exists(nodes_path):
        raise FileNotFoundError(f"Fichier manquant : {nodes_path}")

    #Lecture et renommage des colonnes pour Neo4j
    df = pd.read_parquet(nodes_path)
    df = df.rename(columns={"id": "id:ID"})
    df = df[["id:ID", "name", "label"]]

    #Export CSV
    out_path = os.path.join(GOLD_DIR, "nodes.csv")
    df.to_csv(out_path, index=False)
    print(f"[+] nodes.csv généré ({len(df)} lignes)")

def export_edges():
    """Exporte les arêtes Parquet (shardées ou non) en CSV Neo4j."""
    #Recherche des fichiers shardés si présents
    shard_paths = sorted(glob.glob(os.path.join(SILVER_DIR, "shard=*/edges.parquet")))
    
    if shard_paths:
        #Concaténation des shards
        dfs = [pd.read_parquet(p) for p in shard_paths]
        df = pd.concat(dfs, ignore_index=True)
    else:
        #Sinon lecture du fichier unique
        edges_path = os.path.join(SILVER_DIR, "edges.parquet")
        if not os.path.exists(edges_path):
            raise FileNotFoundError(f"Fichier manquant : {edges_path}")
        df = pd.read_parquet(edges_path)

    #Renommage des colonnes pour le format Neo4j
    df = df.rename(columns={"src": ":START_ID", "dst": ":END_ID"})
    df = df[[":START_ID", ":END_ID", "type"]]

    #Export CSV
    out_path = os.path.join(GOLD_DIR, "edges.csv")
    df.to_csv(out_path, index=False)
    print(f"[+] edges.csv généré ({len(df)} lignes)")

def main():
    """Lance l’export des nœuds et arêtes vers le dossier Gold."""
    export_nodes()
    export_edges()
    print("[*] Export Parquet -> CSV terminé (dossier data/gold).")

if __name__ == "__main__":
    main()
