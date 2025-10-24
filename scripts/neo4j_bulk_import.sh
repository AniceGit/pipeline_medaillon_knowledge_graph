#Pipeline d’import Neo4j : conversion Parquet -> CSV -> import bulk

set -e #Arrêt immédiat en cas d'erreur

GOLD_DIR="data/gold"

echo "[*] Conversion des Parquet Silver -> CSV (Gold)..."

#Exécute le script Python qui exporte les fichiers au format Neo4j
python3 scripts/export_parquet_to_csv.py

echo "[*] Arrêt de Neo4j pour import offline..."
#Stoppe le conteneur Neo4j s’il est en cours d’exécution (ignore l’erreur sinon)
docker stop neo4j || true

echo "[*] Import des données dans Neo4j (bulk)..."
#Exécute l’import bulk depuis les CSV générés
#Monte data/gold dans /import pour éviter les problèmes de permission lors d'une copie
docker run --rm \
  -v $(pwd)/neo4j/data:/data \
  -v $(pwd)/data/gold:/import \
  neo4j:5.13 \
  neo4j-admin database import full \
    --overwrite-destination=true \
    --nodes=/import/nodes.csv \
    --relationships=/import/edges.csv \
    neo4j

echo "[*] Redémarrage de Neo4j..."

#Relance le conteneur Neo4j
docker start neo4j

echo "[✓] Import terminé avec succès !"
