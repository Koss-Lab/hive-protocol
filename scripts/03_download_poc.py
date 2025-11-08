import os
import requests

# Liste complète des images à télécharger
images = [
  {"id": 1, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-u0Z5sa5ytRyFrSPbCZ363nvl.png?st=2025-11-08T02%3A07%3A08Z&se=2025-11-08T04%3A07%3A08Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=8eb2c87c-0531-4dab-acb3-b5e2adddce6c&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T02%3A36%3A08Z&ske=2025-11-09T02%3A36%3A08Z&sks=b&skv=2024-08-04&sig=2o7OY8Y8vA%2B9k5gM9yimtPKCiPjTKmsmKBDglNa3mMI%3D"},
  {"id": 2, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-3wi0YTZJGMsJaxKqAx1CpFuO.png?st=2025-11-08T02%3A07%3A35Z&se=2025-11-08T04%3A07%3A35Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=32836cae-d25f-4fe9-827b-1c8c59c442cc&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-07T23%3A55%3A43Z&ske=2025-11-08T23%3A55%3A43Z&sks=b&skv=2024-08-04&sig=RdEMGR6CkX02UMC5TaBcB/i7ULB6F6ZY5a/tEE0a5bw%3D"},
  {"id": 3, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-CV5eOcgm3tbGcHYAxSBTUalw.png?st=2025-11-08T02%3A08%3A00Z&se=2025-11-08T04%3A08%3A00Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=31d50bd4-689f-439b-a875-f22bd677744d&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T03%3A08%3A00Z&ske=2025-11-09T03%3A08%3A00Z&sks=b&skv=2024-08-04&sig=EE1V4cW2JkyCLTfMVYsbxYVbt4rQYealJQYbsmVHaJQ%3D"},
  {"id": 4, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-YUt7Ika5LRNHOwBxyhDIHKDj.png?st=2025-11-08T02%3A08%3A28Z&se=2025-11-08T04%3A08%3A28Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=38e27a3b-6174-4d3e-90ac-d7d9ad49543f&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T00%3A15%3A58Z&ske=2025-11-09T00%3A15%3A58Z&sks=b&skv=2024-08-04&sig=W50esrURN1hj3yxyEAU2WEKuGb6qKBhQBsudBmeq%2BG0%3D"},
  {"id": 5, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-jKnhDIgNJGhLX2MzyCvAHk2m.png?st=2025-11-08T02%3A08%3A52Z&se=2025-11-08T04%3A08%3A52Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=c6569cb0-0faa-463d-9694-97df3dc1dfb1&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T03%3A08%3A52Z&ske=2025-11-09T03%3A08%3A52Z&sks=b&skv=2024-08-04&sig=VAIExkP68apU44qjRsL0SjBle5KUmL%2BEqyj344/TKr4%3D"},
  {"id": 6, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-hpCTPK8yRIrNXJMwdu1PmqdG.png?st=2025-11-08T02%3A09%3A19Z&se=2025-11-08T04%3A09%3A19Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=8eb2c87c-0531-4dab-acb3-b5e2adddce6c&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T03%3A09%3A19Z&ske=2025-11-09T03%3A09%3A19Z&sks=b&skv=2024-08-04&sig=edgktg8ZRDICF52tsewP0PG%2BAEhdYaNoQPEqVcCFBNk%3D"},
  {"id": 7, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-chJekBejrPFNMvteKbt5hMAm.png?st=2025-11-08T02%3A09%3A44Z&se=2025-11-08T04%3A09%3A44Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=38e27a3b-6174-4d3e-90ac-d7d9ad49543f&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T00%3A55%3A17Z&ske=2025-11-09T00%3A55%3A17Z&sks=b&skv=2024-08-04&sig=P7bsA1SnslkVo5RxvFYa/GjY7/b9tcEl/ZSy%2BZuBPpA%3D"},
  {"id": 8, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-NeHTKbF2Ox4tBtoGf5WCxNEh.png?st=2025-11-08T02%3A10%3A06Z&se=2025-11-08T04%3A10%3A06Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=31d50bd4-689f-439b-a875-f22bd677744d&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T03%3A10%3A06Z&ske=2025-11-09T03%3A10%3A06Z&sks=b&skv=2024-08-04&sig=QJXeRP0Kgd1i8SRjfINgOYjkXXpVDQ%2BewmJMXetU8rc%3D"},
  {"id": 9, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-BpZDdsCv8lBUOQ6iohSBnWIg.png?st=2025-11-08T02%3A10%3A28Z&se=2025-11-08T04%3A10%3A28Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=8eb2c87c-0531-4dab-acb3-b5e2adddce6c&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T03%3A10%3A28Z&ske=2025-11-09T03%3A10%3A28Z&sks=b&skv=2024-08-04&sig=AsF/Jp8WD46jZwVSDywVYsqRwE1W6hO3XxwKuE36npU%3D"},
  {"id": 10, "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-qGblSnezKhX6rMaM5Ae1naDw/user-qXiS1lkGb3De3KKJSmT8JVCM/img-W43vrKjZMB2fu3MyiQWOpSAX.png?st=2025-11-08T02%3A10%3A49Z&se=2025-11-08T04%3A10%3A49Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=32836cae-d25f-4fe9-827b-1c8c59c442cc&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T01%3A00%3A34Z&ske=2025-11-09T01%3A00%3A34Z&sks=b&skv=2024-08-04&sig=eefKfNIqxX0DGTCH%2Beec3m1H5tZZuUexQIVhCCyO7RA%3D"}
]

# Dossier de sortie
output_dir = os.path.join(os.getcwd(), "03_download_poc")
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Dossier de sortie : {output_dir}\n")

# Téléchargement
for img in images:
    img_id = img["id"]
    url = img["url"]
    try:
        print(f"⬇️  Téléchargement de l'image {img_id}...")
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        filename = os.path.join(output_dir, f"hive_guardian_{img_id}.png")
        with open(filename, "wb") as f:
            f.write(r.content)
        print(f"✅ Image {img_id} enregistrée → {filename}")
    except Exception as e:
        print(f"❌ Erreur sur l'image {img_id}: {e}")

print("\n🎉 Téléchargement terminé ! Toutes les images sont dans le dossier /03_download_poc.")
