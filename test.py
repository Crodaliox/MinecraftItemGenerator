import json
from mistralai import Mistral
import xml.etree.ElementTree as ET
import json as json

model = "mistral-large-latest"

client = Mistral("emTQYTygOhVbQAeNLVeZu7u8MeKhskYp")

# Définir les items
items = ["bois", "perroquet"]

# Créer un prompt pour le modèle
prompt = f"Tu es développeur de jeux vidéo pour développer le jeu vidéo minecraft. Ton but est de créer un nouvel item du jeu à partir de deux item défini. Génère seulement un nouveau nom d'item de minecraft qui combine ces deux items : {items[0]} et {items[1]}. C'est comme si tu fabriquais un nouvel objet à partir de deux objets. Pas besoin de faire des phrases pour expliquer comment tu vas faire. Je veux juste le nom. Le nombre de mot max est de 8 mots et je veux un nom qui ressemble au nom d'item de minecraft"

chat_response = client.chat.complete(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt,
        },
    ]
)
print(chat_response.choices[0].message.content)
resultItem = chat_response.choices[0].message.content 
# Chemin du fichier JSON
file_path = 'generatedItems.json'

# Charger les données existantes ou créer une nouvelle liste
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

# Ajouter la nouvelle entrée
new_entry = {
    "items0": items[0],
    "items1": items[1],
    "resultItem": resultItem
}

# Vérifier si l'item existe déjà
existing_items = {entry["resultItem"] for entry in data}
if resultItem not in existing_items:
    print(f"Les nouvelles données ont été ajoutées à {file_path}")
    data.append(new_entry)


# Écrire les données mises à jour dans le fichier JSON
with open(file_path, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

