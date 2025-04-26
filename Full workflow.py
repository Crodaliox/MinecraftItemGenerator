


import json
import time

from mistralai import Mistral
import xml.etree.ElementTree as ET
import json

model = "mistral-large-latest"

client = Mistral("emTQYTygOhVbQAeNLVeZu7u8MeKhskYp")

# Définir les items
items = ["bow", "egg"]


# Créer un prompt pour le modèle
prompt = f"You are a video game developer to develop the minecraft video game. Your goal is to generates a new minecraft item name that combines these two items: {items[0]} and {items[1]}. I just want the name and no quote.  "

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

#Etablissement de la catégorie de l'item
categories = ["Axe", "Pickaxe", "Fishing rod", "Flint and Steel", "Hoe", "Shears", "Shovel", "Bow", "Crossbow", "Shield", "Sword", "Trident", "Arrow", "Helmet", "Chestplate", "Leggings", "Boots", "Food", "Seeds", "Materials", "Dyes", "Music disc", "Book", "bowl", "Buckets", "Bootles", "other"]
promptCategory=""
for category in categories:
    promptCategory = promptCategory + ", " + category

prompt = f"In minecraft, I want to incorporate this item : {resultItem}. Give me for you the probability in % this item could be for each category. Categories is : {promptCategory}. No sentences. I want the same order. I want this format for each : 'category : percentage probability'."
time.sleep(2)
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

import re
# Extract all probabilities as float
probabilities = [float(match.group()) for match in re.finditer(r"\d+\.?\d*", chat_response.choices[0].message.content)]
# Création du dictionnaire en combinant les deux listes
probabilities = dict(zip(categories, probabilities))
# Trouver l'indice de la valeur maximale
maxCategory = max(probabilities, key=probabilities.get)
print(maxCategory)

# Chemin du fichier JSON


file_path = 'generatedItems.json'
isItemHere = False
# Charger les données existantes ou créer une nouvelle liste
import requests

url_json = "https://etiennejulien.com/minecraft/infitems/generatedItems.json"

try:
    response = requests.get(url_json)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Erreur lors du chargement : {response.status_code}")
        data = []
except:
    print("Impossible de charger le fichier distant.")
    data = []

idItem = 0
for i, do in enumerate(data):
    if((do['items0'] == items[0] or do['items0'] == items[1]) and (do['items1'] == items[0] or do['items1'] == items[1])):
        isItemHere = True
    if(do["resultItem"] == resultItem):
        isItemHere = True

    idItem+=1

if isItemHere == False:
    # Ajouter la nouvelle entrée
    new_entry = {
        "id" : idItem,
        "items0": items[0],
        "items1": items[1],
        "category": maxCategory,
        "resultItem": resultItem
    }

    print(f"Les nouvelles données ont été ajoutées à {file_path}")
    data.append(new_entry)

    # Écrire les données mises à jour dans le fichier JSON
    requests.post("https://etiennejulien.com/minecraft/infitems/updateItems.php", json=data)
else:
    print("Item already exists")

"""2. Generation du sprite de l'item"""


from diffusers import DiffusionPipeline
from diffusers import EulerAncestralDiscreteScheduler
import torch
import os
import json
import numpy as np
from PIL import Image,ImageEnhance
from rembg import remove

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16).to("cuda")
pipe.load_lora_weights("artificialguybr/PixelArtRedmond")


IsImageGenerated = False

for i in range(len(data)):
# Accéder aux valeurs dans le dictionnaire
  print(data[i]["resultItem"])

  prompt = data[i]["resultItem"] + ",no background, one item, PixArFK"
  filename=data[i]["resultItem"].lower().replace(" ", "")

  base_url = "https://etiennejulien.com/minecraft/infitems/imagesGenerated/"

  num_images = 1

  for j in range(num_images):

      image_name = f"{filename}.png"
      image_url = base_url + image_name

      check_response = requests.head(image_url)

      if check_response.status_code == 200:
          print(f"L'image {image_name} existe déjà sur le serveur, génération sautée.")
          continue  # On saute à l’itération suivante
      else:
          print(f"L'image {image_name} n'existe pas, génération en cours...")

      image = pipe(prompt , num_inference_steps=50, batch=10).images[0]
      image = remove(image,alpha_matting=True)
      image.save(f"{filename}HR.png")
      img_16x16 = image.resize((16, 16), Image.Resampling.NEAREST)  # NEAREST pour un effet pixel-art
      img_16x16.save(f"{filename}.png")

      # Chargement de l'image pour l'envoyer au serveur
      with open(f"{filename}.png", 'rb') as f:
          image_data = f.read()

      # URL de l'API PHP pour recevoir l'image
      upload_url = "https://etiennejulien.com/minecraft/infitems/get_image.php"


      params = {
          'filename': filename + '.png',  # Nom de l'image à enregistrer
      }


      response = requests.post(upload_url, params=params, files={'image': image_data})

      # Vérification de la réponse du serveur
      if response.status_code == 200:
          print(f"Image {filename}.png envoyée avec succès!")
      else:
          print(f"Erreur lors de l'envoi de l'image {filename}{j}.png : {response.status_code}")
