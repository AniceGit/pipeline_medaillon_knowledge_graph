#Import Neo4j
set -e

SILVER_DIR="data/silver"
GOLD_DIR="data/gold"
TMP_DIR="tmp"

mkdir -p "$GOLD_DIR" "$TMP_DIR"

echo "[*] Converting Parquet to CSV for Neo4j..."

# Convert nodes
echo "[+] Processing nodes..."
python3 -c "
import pandas as pd
df = pd.read_parquet('$SILVER_DIR/nodes.parquet')
df.rename(columns={'id': 'id:ID', 'name': 'name', 'label': 'label'}, inplace=True)
df.to_csv('$GOLD_DIR/nodes.csv', index=False)
"

# Convert edges from all shards
echo "[+] Processing edges from shards..."
> "$GOLD_DIR/edges.csv"  # Empty/create the file
echo ':START_ID,:END_ID,type' > "$GOLD_DIR/edges.csv"

for shard in "$SILVER_DIR"/shard=*/; do
    python3 -c "
import pandas as pd
df = pd.read_parquet('${shard}edges.parquet')
df.rename(columns={'src': ':START_ID', 'dst': ':END_ID'}, inplace=True)
df['type'] = 'REL'
df[[':START_ID', ':END_ID', 'type']].to_csv('$TMP_DIR/shard_edges.csv', index=False, mode='w')
"
    tail -n +2 "$TMP_DIR/shard_edges.csv" >> "$GOLD_DIR/edges.csv"
done

echo "[✓] CSVs ready in $GOLD_DIR/"
echo "Next step: Use 'neo4j-admin database import' with these files."
