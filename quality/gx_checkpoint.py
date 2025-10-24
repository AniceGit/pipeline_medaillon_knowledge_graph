#Validation et nettoyage des données : passage en silver
import os
import pandas as pd

#Répertoires d'entrée et de sortie
BRONZE_DIR = "data/bronze"
SILVER_DIR = "data/silver"

#Création du répertoire de sortie si nécessaire
os.makedirs(SILVER_DIR, exist_ok=True)

def clean_nodes():
    """Nettoie les doublons dans le fichier des noeuds."""
    bronze_path = os.path.join(BRONZE_DIR, "nodes.parquet")
    silver_path = os.path.join(SILVER_DIR, "nodes.parquet")

    #Lecture du fichier source
    df = pd.read_parquet(bronze_path)
    original_count = len(df)

    #Suppression des doublons sur la colonne 'id'
    df_clean = df.drop_duplicates(subset=["id"])
    cleaned_count = len(df_clean)

    #Enregistrement et affichage du résultat
    if cleaned_count < original_count:
        print(f"X Nodes:{original_count - cleaned_count} doublon(s) trouvé(s) et supprimé(s)")
        df_clean.to_parquet(silver_path, index=False)
    else:
        df_clean.to_parquet(silver_path, index=False)
        print("O Nodes: Aucun doublon trouvé.")

def clean_edges():
    """Supprime les lignes contenant des valeurs nulles sur 'src' ou 'dst'."""
    bronze_path = os.path.join(BRONZE_DIR, "edges.parquet")
    silver_path = os.path.join(SILVER_DIR, "edges.parquet")

    #Lecture du fichier source
    df = pd.read_parquet(bronze_path)
    original_count = len(df)

    #Suppression des lignes avec des valeurs nulles
    df_clean = df.dropna(subset=["src", "dst"])
    cleaned_count = len(df_clean)

    #Enregistrement et affichage du résultat
    if cleaned_count < original_count:
        print(f"X Edges: {original_count - cleaned_count} ligne(s) contenant un ou plusieurs nulls trouvée(s).")
        df_clean.to_parquet(silver_path, index=False)
    else:
        df_clean.to_parquet(silver_path, index=False)
        print("O Edges: Aucun null trouvé sur les colonnes 'src' ou 'dst'.")

def main():
    """Nettoie les fichiers de noeuds et d’arêtes."""
    clean_nodes()
    clean_edges()

if __name__ == "__main__":
    main()
