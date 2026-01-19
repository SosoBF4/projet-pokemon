import sqlite3
import requests
import os
import re

DB_PATH = "./sql/Pokemon.db"
SAVE_DIR = "image"
BASE_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon"

os.makedirs(SAVE_DIR, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT image FROM pokemon")
rows = cursor.fetchall()

for (image_path,) in rows:
    match = re.search(r"(\d+)\.png$", image_path)
    if not match:
        continue

    pokemon_id = match.group(1)
    url = f"{BASE_URL}/{pokemon_id}.png"
    local_path = f"{SAVE_DIR}/{pokemon_id}.png"

    if os.path.exists(local_path):
        print(f"⏭️ {pokemon_id}.png déjà téléchargé")
        continue

    r = requests.get(url)
    if r.status_code == 200:
        with open(local_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Pokémon {pokemon_id} téléchargé")
    else:
        print(f"❌ Erreur pour Pokémon {pokemon_id}")

conn.close()
