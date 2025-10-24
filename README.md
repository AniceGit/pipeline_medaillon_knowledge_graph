
---

# 🧱 Architecture Médaillon x Neo4j Knowledge Graph

## 🎯 Objectif

Ce projet met en place une **pipeline de données complète** suivant l’architecture **médaillon** *(Bronze → Silver → Gold)* pour ingérer, transformer et charger un **graphe de connaissances** (Knowledge Graph) dans une base **Neo4j conteneurisée**.

L’ensemble du pipeline s’exécute **par scripts Python**, sans orchestrateur externe, et permet de générer, nettoyer et importer des données simulées à grande échelle.

---

## 🏗️ Architecture du projet

```
projet/
├── docker-compose.yaml           # Conteneur Neo4j
├── README.md                     # Documentation
├── data/
│   ├── raw/                      # Données CSV brutes
│   ├── bronze/                   # Données converties en Parquet
│   ├── silver/                   # Données nettoyées et partitionnées
│   └── gold/                     # CSV finaux pour import Neo4j
├── scripts/
│   ├── generate_sample_data.py   # Génération de données simulées
│   ├── to_parquet.py             # Conversion CSV → Parquet (Bronze)
│   ├── quality_gx_checkpoint.py  # Validation et nettoyage (Silver)
│   ├── partition_edges.py        # Partitionnement des arêtes (Silver)
│   ├── export_parquet_to_csv.py  # Export Parquet → CSV (Gold)
│   └── neo4j_bulk_import.sh      # Import des CSV dans Neo4j
└── neo4j/
    └── data/                     # Stockage persistant Neo4j
```

---

## ⚙️ Pipeline de traitement

### 🥉 **Bronze** — Données brutes

* Génération aléatoire de **1 million de nœuds** (`Person`, `Org`, `Paper`)
* Création de **5 millions d’arêtes** aléatoires (`REL`)
* Fichiers produits :

  * `data/raw/nodes.csv`
  * `data/raw/edges.csv`

### 🥈 **Silver** — Données nettoyées et partitionnées

* Conversion des CSV en **Parquet** (`scripts/to_parquet.py`)
* Nettoyage avec **pandas** :

  * Suppression des doublons dans les nœuds
  * Suppression des arêtes contenant des valeurs nulles
* Partitionnement des arêtes en **8 shards** selon `src % N_SHARDS`

Structure :

```
data/silver/
├── nodes.parquet
├── edges.parquet
└── shard=0..7/edges.parquet
```

### 🥇 **Gold** — Données prêtes à l’import

* Export des fichiers Silver en **CSV format Neo4j**

  * `nodes.csv` → colonnes `id:ID, name, label`
  * `edges.csv` → colonnes `:START_ID, :END_ID, type`
* Import automatisé dans Neo4j via le script `neo4j_bulk_import.sh`

---

## 🐳 Conteneur Neo4j

Le service Neo4j est défini dans `docker-compose.yaml` :

```yaml
services:
  neo4j:
    image: neo4j:5.13
    container_name: neo4j
    environment:
      NEO4J_AUTH: "none"
    ports:
      - "7474:7474"   # Interface Web
      - "7687:7687"   # Protocole Bolt
    volumes:
      - ./neo4j/data:/data
      - ./neo4j/import:/var/lib/neo4j/import
    restart: unless-stopped
```

### Lancer Neo4j

```bash
docker compose up -d
```

Interface : [http://localhost:7474](http://localhost:7474)

---

## 🚀 Exécution du pipeline

### 1️⃣ Génération de données brutes

```bash
python3 scripts/generate_sample_data.py
```

### 2️⃣ Conversion en Parquet (Bronze)

```bash
python3 scripts/to_parquet.py
```

### 3️⃣ Nettoyage et validation (Silver)

```bash
python3 scripts/quality_gx_checkpoint.py
```

### 4️⃣ Partitionnement des arêtes

```bash
python3 scripts/partition_edges.py
```

### 5️⃣ Export vers CSV et import dans Neo4j

```bash
bash scripts/neo4j_bulk_import.sh
```

---

## 🧩 Résultat final

Une base Neo4j peuplée à partir de données simulées, consultable via l’interface web :
📍 [http://localhost:7474/browser](http://localhost:7474/browser)

Vous pouvez ensuite exécuter des requêtes **Cypher**, par exemple :

```cypher
MATCH (p:Person)-[r:REL]->(o)
RETURN p, r, o
LIMIT 25;
```

---

## 📚 Références utiles

* [Architecture Médaillon (Databricks)](https://www.databricks.com/glossary/medallion-architecture)
* [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/)
* [Apache Parquet Documentation](https://parquet.apache.org/docs/overview/)

---
