#Génération de données
import csv
import os
import random

# Paramètres de génération
OUT_DIR = "data/raw"
NUM_NODES = 1_000_000
NUM_EDGES = 5_000_000
NODE_CHUNK = 100_000
EDGE_CHUNK = 200_000
LABELS = ["Person", "Org", "Paper"]

def generate_nodes():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "nodes.csv"), "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "label", "name"])
        for i in range(NUM_NODES):
            label = random.choice(LABELS)
            writer.writerow([i, label, f"name_{i}"])
    print("[+] nodes.csv written")

def generate_edges():
    with open(os.path.join(OUT_DIR, "edges.csv"), "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["src", "dst", "type"])
        for _ in range(NUM_EDGES):
            src = random.randint(0, NUM_NODES - 1)
            dst = random.randint(0, NUM_NODES - 1)
            writer.writerow([src, dst, "REL"])
    print("[+] edges.csv written")

def main():
    generate_nodes()
    generate_edges()

if __name__ == "__main__":
    main()
