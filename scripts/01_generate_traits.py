import csv, json, random, os
random.seed(77)

N = 777

factions = ["Voltabees","Pyromiels","Floradrones","Nectarions"]
backgrounds = ["Neon Grid","Jungle Bio","Cyber Hive","Plasma Void"]
wings = ["Plasma","Holographic","Crystalline","Flame"]
armor = ["Honey Chrome","Dark Titanium","Floral Bio-suit","Plasma Shell"]
rarities = ["Common","Rare","Epic","Legendary"]

os.makedirs("traits", exist_ok=True)
rows = []
for i in range(N):
    rows.append({
        "id": i+1,
        "faction": random.choice(factions),
        "background": random.choice(backgrounds),
        "wings": random.choice(wings),
        "armor": random.choice(armor),
        "rarity": random.choices(rarities, weights=[70,20,8,2])[0]
    })

json.dump(rows, open("traits/traits.json","w"), indent=2)
print("✅ traits.json created with", len(rows), "entries")

