set -e

GOLD_DIR="data/gold"

echo "[*] Conversion des Parquet Silver -> CSV (Gold)..."
python3 scripts/export_parquet_to_csv.py

echo "[*] Arrêt de Neo4j pour import offline..."
docker stop neo4j || true

echo "[*] Import des données dans Neo4j (bulk)..."
# On monte directement data/gold dans /import pour éviter les problèmes de permission
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
docker start neo4j

echo "[✓] Import terminé avec succès !"
