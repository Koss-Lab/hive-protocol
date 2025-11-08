# Hive Protocol — Starter Kit (v0.1)

This is a practical, end‑to‑end scaffold to launch **Hive Protocol – Les Gardiens du Miel Cosmique** on **Solana** with **777 PFPs**, lore, XP, and airdrops.

---

## 0) Project Structure

```
hive-protocol/
├─ README.md
├─ .env.example
├─ assets/
│  ├─ logo/
│  ├─ banners/
│  └─ fonts/
├─ pfp_images/              # output images {id}.png
├─ metadata/                # output metadata {id}.json
├─ traits/
│  ├─ traits.json           # 777 combo list
│  └─ traits.csv
├─ scripts/
│  ├─ 01_generate_traits.py
│  ├─ 02_render_batch_example.py
│  ├─ 03_generate_metadata.py
│  ├─ 04_upload_ipfs_pinata.ts
│  ├─ 05_metaplex_sugar_config.json
│  ├─ 06_airdrop_rewards.ts
│  ├─ 07_create_spl_token.sh
│  └─ 08_distribute_tokens.ts
├─ web/
│  ├─ mint-site/            # simple Next.js site scaffold
│  └─ public/
├─ backend/
│  ├─ supabase.sql          # schema for XP/missions
│  ├─ edge_functions/
│  │  └─ weekly_rewards.ts  # cron: compute top wallets & enqueue rewards
│  └─ README.md
└─ docs/
   ├─ lore.md
   ├─ roadmap.md
   └─ marketing_copy.md
```

Populate `.env` from `.env.example` for API keys (Pinata/NFT.Storage, RPC URL, private key).

---

## 1) Traits & Rarity (source of truth)

**Factions:** Voltabees, Pyromiels, Floradrones, Nectarions

**Attributes:**
- Background: Neon Grid, Jungle Bio, Cyber Hive, Plasma Void
- Wings: Plasma, Holographic, Crystalline, Flame
- Armor: Honey Chrome, Dark Titanium, Floral Bio-suit, Plasma Shell
- Rarity: Common, Rare, Epic, Legendary

**Recommended rarity weights (sum to 1.0):**
- Rarity: Common 0.70, Rare 0.20, Epic 0.08, Legendary 0.02
- Background (balanced): 0.25 each
- Wings (slight bias): Plasma 0.30, Holographic 0.30, Crystalline 0.25, Flame 0.15
- Armor (balanced): 0.25 each
- Faction (balanced): 0.25 each

### scripts/01_generate_traits.py
```python
import csv, json, random, os
random.seed(77)

N = 777

factions = ["Voltabees","Pyromiels","Floradrones","Nectarions"]
factions_w = [0.25,0.25,0.25,0.25]

backgrounds = ["Neon Grid","Jungle Bio","Cyber Hive","Plasma Void"]
backgrounds_w = [0.25,0.25,0.25,0.25]

wings = ["Plasma","Holographic","Crystalline","Flame"]
wings_w = [0.30,0.30,0.25,0.15]

armor = ["Honey Chrome","Dark Titanium","Floral Bio-suit","Plasma Shell"]
armor_w = [0.25,0.25,0.25,0.25]

rarities = ["Common","Rare","Epic","Legendary"]
rarities_w = [0.70,0.20,0.08,0.02]

os.makedirs("traits", exist_ok=True)

seen = set()
rows = []

while len(rows) < N:
    f = random.choices(factions, factions_w)[0]
    b = random.choices(backgrounds, backgrounds_w)[0]
    w = random.choices(wings, wings_w)[0]
    a = random.choices(armor, armor_w)[0]
    r = random.choices(rarities, rarities_w)[0]
    key = (f,b,w,a,r)
    if key in seen:
        continue
    seen.add(key)
    idx = len(rows) + 1
    rows.append({
        "id": idx,
        "faction": f,
        "background": b,
        "wings": w,
        "armor": a,
        "rarity": r
    })

with open("traits/traits.json","w",encoding="utf-8") as f:
    json.dump(rows,f,ensure_ascii=False,indent=2)

with open("traits/traits.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id","faction","background","wings","armor","rarity"])
    writer.writeheader()
    writer.writerows(rows)

print("✅ Generated:", len(rows), "unique combos -> traits/traits.json & traits/traits.csv")
```

---

## 2) Image Generation (prompt modularity)

**Master prompt template (French):**
```
portrait NFT d'une abeille cybernétique {faction}, ailes {wings}, armure {armor}, fond {background},
"cyberpunk + sacred geometry + neon organic forms", "bee‑armored entities with light wings and honey‑chrome reflections",
rendu 3D stylisé, focus visage 1:1, ultra-détaillé, reflets miel‑chrome, rim light néon bleu,
techno-organic, DOF subtil, qualité 4K, style cohérent, pfp centré, sans texte.
```

**English variant (if needed):**
```
cybernetic bee portrait NFT, {faction} faction, {wings} wings, {armor} armor, {background} background,
cyberpunk + sacred geometry + neon organic forms, honey‑chrome reflections, 3D stylized render, centered PFP, 4K.
```

### scripts/02_render_batch_example.py
*Example stub* (replace `CALL_YOUR_IMAGE_API()` with your generator — local SDXL, Leonardo, etc.).
```python
import json, os
from pathlib import Path

os.makedirs("pfp_images", exist_ok=True)
traits = json.load(open("traits/traits.json","r",encoding="utf-8"))

TPL = (
    "portrait NFT d'une abeille cybernétique {faction}, ailes {wings}, armure {armor}, fond {background}, "
    "cyberpunk + sacred geometry + neon organic forms, bee‑armored entities with light wings and honey‑chrome reflections, "
    "rendu 3D stylisé, focus visage 1:1, ultra-détaillé, reflets miel‑chrome, rim light néon bleu, techno-organic, DOF subtil, 4K, pfp centré, sans texte."
)

for row in traits:
    pid = row["id"]
    prompt = TPL.format(**row)
    out_path = Path(f"pfp_images/{pid}.png")
    if out_path.exists():
        continue
    # image_bytes = CALL_YOUR_IMAGE_API(prompt)
    # out_path.write_bytes(image_bytes)
    open(out_path, "wb").write(b"")  # placeholder; replace with actual bytes
print("✅ Render stubs written to pfp_images/. Replace stub with real generator output.")
```

---

## 3) Metadata JSON generation

### scripts/03_generate_metadata.py
```python
import os, json
from pathlib import Path

IPFS_IMG_CID = os.getenv("IPFS_IMG_CID", "QmREPLACE_ME_IMAGE_CID")
os.makedirs("metadata", exist_ok=True)
rows = json.load(open("traits/traits.json","r",encoding="utf-8"))

for row in rows:
    pid = row["id"]
    meta = {
      "name": f"Hive Guardian #{pid}",
      "description": f"A cyber-bee from faction {row['faction']} defending the Cosmic Hive.",
      "image": f"ipfs://{IPFS_IMG_CID}/{pid}.png",
      "attributes": [
        {"trait_type":"Faction","value":row['faction']},
        {"trait_type":"Armor","value":row['armor']},
        {"trait_type":"Wings","value":row['wings']},
        {"trait_type":"Rarity","value":row['rarity']},
        {"trait_type":"Background","value":row['background']}
      ]
    }
    Path(f"metadata/{pid}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print("✅ Metadata ready in metadata/ (set IPFS_IMG_CID before final build)")
```

---

## 4) IPFS Upload (Pinata example)

Install deps in project root:
```bash
npm i pinata-web3 @pinata/sdk dotenv
```

`.env.example` keys:
```
PINATA_JWT=eyJhbGciOi...
PINATA_GATEWAY=https://gateway.pinata.cloud/ipfs/
```

### scripts/04_upload_ipfs_pinata.ts
```ts
import "dotenv/config";
import { PinataSDK } from "@pinata/sdk";
import fs from "fs";
import path from "path";

const pinata = new PinataSDK({ pinataJWTKey: process.env.PINATA_JWT! });

async function uploadDir(dir: string, name: string){
  const res = await pinata.pinFromFS(dir, { pinataMetadata: { name } });
  console.log(`✅ ${name} CID:`, res.IpfsHash);
  return res.IpfsHash;
}

(async ()=>{
  const imagesCID = await uploadDir("pfp_images","HivePFP_Images");
  const metadata = JSON.parse(fs.readFileSync("traits/traits.json","utf-8"));
  // patch metadata with final images CID
  for(const row of metadata){
    const p = path.join("metadata", `${row.id}.json`);
    const m = JSON.parse(fs.readFileSync(p,"utf-8"));
    m.image = `ipfs://${imagesCID}/${row.id}.png`;
    fs.writeFileSync(p, JSON.stringify(m, null, 2));
  }
  const metaCID = await uploadDir("metadata","HivePFP_Metadata");
  console.log("Images:", imagesCID, "Metadata:", metaCID);
})();
```

---

## 5) Mint Setup (Metaplex Candy Machine v3 via `sugar`)

Install sugar: https://docs.metaplex.com/tools/sugar/installation

### scripts/05_metaplex_sugar_config.json
```json
{
  "number": 777,
  "symbol": "HIVE",
  "sellerFeeBasisPoints": 500,
  "isMutable": true,
  "uploadMethod": "bundlr",
  "creators": [{"address": "REPLACE_YOUR_WALLET","share": 100}],
  "collection": {"name": "Hive Protocol – Guardians","family": "Hive"},
  "price": 0.02,
  "solTreasuryAccount": "REPLACE_TREASURY_WALLET",
  "goLiveDate": "2025-11-15T18:00:00Z",
  "retainAuthority": true,
  "guards": {"default": {"startDate": {"date": "2025-11-15T18:00:00Z"}}}
}
```

**Preparation:**
```bash
# 1) Prepare the assets folder Metaplex expects
mkdir -p cache/assets
# copy images & metadata to sequential filenames
for i in $(seq 1 777); do cp pfp_images/$i.png cache/assets/$((i-1)).png; done
for i in $(seq 1 777); do cp metadata/$i.json  cache/assets/$((i-1)).json; done

# 2) Sugar commands
sugar validate
sugar upload
sugar deploy
sugar mint one   # test mint
```

---

## 6) SPL Token ($HNYX)

### scripts/07_create_spl_token.sh
```bash
#!/usr/bin/env bash
set -e
NAME=HNYX
DECIMALS=6
SUPPLY=7770000      # 7,770,000 with 6 decimals -> mint 7,770,000 * 10^6

# Create mint
TOKEN=$(spl-token create-token --decimals $DECIMALS | awk '/Creating/ {print $3}')
echo "TOKEN MINT: $TOKEN"
# Create associated account for treasury
TREASURY=$(spl-token create-account $TOKEN | awk '/Creating/ {print $3}')
echo "TREASURY: $TREASURY"
# Mint supply
spl-token mint $TOKEN $((SUPPLY*10**DECIMALS))
# Set mint authority to a secure key (or multisig)
# spl-token authorize $TOKEN mint --disable
```

### scripts/08_distribute_tokens.ts (simple airdropper)
```ts
import { Connection, Keypair, PublicKey, LAMPORTS_PER_SOL } from "@solana/web3.js";
import { getOrCreateAssociatedTokenAccount, transfer, getMint } from "@solana/spl-token";
import fs from "fs";

const RPC = process.env.RPC_URL!;
const MINT = new PublicKey(process.env.HNYX_MINT!);
const SECRET = Uint8Array.from(JSON.parse(fs.readFileSync(process.env.PRIVKEY_PATH!, "utf-8")));
const payer = Keypair.fromSecretKey(SECRET);

(async ()=>{
  const conn = new Connection(RPC, "confirmed");
  const list = JSON.parse(fs.readFileSync("backend/airdrop_list.json","utf-8"));
  for(const {wallet, amount} of list){
    const owner = new PublicKey(wallet);
    const ata = await getOrCreateAssociatedTokenAccount(conn, payer, MINT, owner);
    await transfer(conn, payer, (await getOrCreateAssociatedTokenAccount(conn, payer, MINT, payer.publicKey)).address, ata.address, payer, amount);
    console.log(`✅ sent ${amount} HNYX to ${wallet}`);
  }
})();
```

---

## 7) XP + Missions (Supabase schema)

### backend/supabase.sql
```sql
-- Users & wallets
create table profiles (
  id uuid primary key default gen_random_uuid(),
  handle text unique,
  created_at timestamptz default now()
);
create table wallets (
  id uuid primary key default gen_random_uuid(),
  profile_id uuid references profiles(id) on delete cascade,
  address text unique not null,
  created_at timestamptz default now()
);

-- Missions & participation
create table missions (
  id bigserial primary key,
  title text not null,
  starts_at timestamptz,
  ends_at timestamptz,
  faction text check (faction in ('Voltabees','Pyromiels','Floradrones','Nectarions')),
  base_xp int default 10
);

create table mission_participations (
  id bigserial primary key,
  wallet text not null,
  mission_id bigint references missions(id) on delete cascade,
  success boolean,
  bonus_xp int default 0,
  created_at timestamptz default now()
);

-- XP ledger (denormalized)
create view xp_leaderboard as
select wallet,
       sum(case when success then coalesce(m.base_xp,10) else 0 end + coalesce(bonus_xp,0)) as xp
from mission_participations mp
left join missions m on m.id=mp.mission_id
group by wallet
order by xp desc;
```

### backend/edge_functions/weekly_rewards.ts (pseudo)
```ts
// 1) Read xp_leaderboard, 2) pick top N, 3) write backend/airdrop_list.json used by 08_distribute_tokens.ts
```

---

## 8) Airdrop NFTs (legendary raffle for first 77)

### scripts/06_airdrop_rewards.ts (NFT example)
```ts
// Use Metaplex JS SDK to mint/transfer selected legendary IDs to early wallets.
```

Keep a CSV `early_supporters.csv` with wallet addresses; script selects random legendary `id` and sends.

---

## 9) Website Copy (mint page)

- **Title:** Hive Protocol — Les Gardiens du Miel Cosmique
- **Tagline:** Rejoignez la ruche. Devenez Gardien.
- **Pitch:** 777 PFPs génératifs sur Solana. 4 factions. Missions hebdomadaires. XP, airdrops, et token $HNYX.
- **Mint CTA:** « Frapper un Gardien » (0.02 SOL)
- **Sections:**
  - Collection • Roadmap • Factions • Leaderboard • FAQ • Docs
- **FAQ snippets:**
  - *C’est quoi HNYX ?* Un token SPL utilisé pour boosters, missions et avantages.
  - *Comment gagner de l’XP ?* Participez aux missions hebdo, votez, partagez des créations.

---

## 10) Lore (extracts)

**Cosmic Hive Network** — Entre les galaxies, le Miel Cosmique pulse comme un chant ancien. Quand le Nœud Source se fissure, la Reine Primordiale appelle 777 Gardiens.

**Factions:**
- **Voltabees:** navigateurs d’orage quantique.
- **Pyromiels:** gardiens du feu intérieur.
- **Floradrones:** ingénieurs du vivant.
- **Nectarions:** maîtres des flux spatio‑temporels.

**Mission #1 – « L’Écho du Nœud Source »**  
Objectif: scanner des « ondes de pollen » (mini‑énigmes sociales/artistiques).  
Récompense: 10 XP + chance d’un item rare.

---

## 11) Roadmap (compact)

- **Phase A**: Génération 777 PFP + IPFS + Candy Machine (semaine 1–2)
- **Phase B**: Mint site + leaderboard XP (semaine 2–3)
- **Phase C**: Missions hebdo + premiers airdrops (dès semaine 3)
- **Phase D**: $HNYX utilitaire + marché interne (mois 2+)

---

## 12) Command Map (matches your system prompt)

- `/generate_traits` → `python scripts/01_generate_traits.py`
- `/render_batch` → `python scripts/02_render_batch_example.py` (plug your generator)
- `/generate_metadata` → `python scripts/03_generate_metadata.py`
- `/upload_ipfs` → `ts-node scripts/04_upload_ipfs_pinata.ts`
- `/mint_setup` → `sugar validate && sugar upload && sugar deploy`
- `/create_token` → `bash scripts/07_create_spl_token.sh`
- `/airdrop_rewards` → `ts-node scripts/06_airdrop_rewards.ts`
- `/story_drop` → update `docs/lore.md` + insert mission rows in DB
- `/generate_marketing_pack` → use docs/marketing_copy.md + assets/

---

## 13) Quickstart

```bash
pyenv local 3.10.14
python -m venv .venv && source .venv/bin/activate
pip install pillow requests python-dotenv
npm i -D ts-node typescript @solana/web3.js @solana/spl-token pinata-web3 @pinata/sdk dotenv

python scripts/01_generate_traits.py
# integrate your image generator in scripts/02_render_batch_example.py then run:
python scripts/02_render_batch_example.py

# after real images exist
node -v  # ensure >=18
npx ts-node scripts/04_upload_ipfs_pinata.ts
export IPFS_IMG_CID=<CID_RETURNED>
python scripts/03_generate_metadata.py

# Metaplex sugar (installed separately)
sugar validate && sugar upload && sugar deploy
```

---

## 14) Checklist (MVP)

- [ ] Generate 777 trait combos
- [ ] Render all PFPs (consistent style)
- [ ] Upload images to IPFS → grab CID
- [ ] Generate metadata with final CID
- [ ] Sugar deploy Candy Machine v3
- [ ] Spin up Supabase, run schema
- [ ] Publish Mission #1 and leaderboard
- [ ] Create $HNYX and seed liquidity
- [ ] Run early supporter legendary raffle
- [ ] Launch mint site & announce

---

**Notes:**
- Keep *one* source of truth for trait weights (01 script). Any later tweaks re‑generate everything.
- Lock the visual pipeline early (seed, sampler, LoRA) to keep the PFP grid consistent.
- Use a multisig or hardware wallet for treasury and mint authority.

