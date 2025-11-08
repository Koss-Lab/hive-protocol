import json, os
from pathlib import Path

# on crée le dossier de sortie s'il n'existe pas
os.makedirs("pfp_images", exist_ok=True)

# on charge la liste des 777 combinaisons
traits = json.load(open("traits/traits.json","r",encoding="utf-8"))

# modèle de prompt pour chaque image
TEMPLATE = (
    "portrait NFT d'une abeille cybernétique {faction}, ailes {wings}, armure {armor}, fond {background}, "
    "style cyberpunk + sacred geometry + néon organique, rendu 3D stylisé, honey-chrome reflections, "
    "éclairage néon bleu, pfp centré, qualité 4K, sans texte."
)

# on crée un fichier texte par PFP
for row in traits:
    pid = row["id"]
    prompt = TEMPLATE.format(**row)
    Path(f"pfp_images/{pid}.txt").write_text(prompt, encoding="utf-8")

print("✅ Prompts prêts dans pfp_images/ — un fichier par abeille.")

