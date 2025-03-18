import json
import os
import pandas as pd


#Preparation du dataset de nom de fichier minecraft
# Chemin vers le dossier contenant les fichiers JSON
json_folder = 'recipes/'

# Liste pour stocker les données extraites
data = []

for filename in os.listdir(json_folder):
    if (filename.endswith('.json')):
        
        with open(os.path.join(json_folder, filename), 'r') as file:
            dataRecipe = json.load(file)
            
            if(dataRecipe['type']=="minecraft:crafting_shaped"):

                items = []
                for value in dataRecipe['key'].values():
                    if 'item' in value:
                        items.append(value['item'].replace("minecraft:", "", 1))
                    elif 'tag' in value:
                        items.append(value['tag'].replace("minecraft:", "", 1))

                pattern = dataRecipe['pattern']
                result = dataRecipe['result']['item'].replace("minecraft:", "", 1)
                data.append({'items': items, 'result': result})

            elif(dataRecipe['type']=="minecraft:crafting_shapeless"):
                for value in dataRecipe['ingredients']:
                    if 'tag' in value:
                        # Supprimer le préfixe "minecraft:"
                        items = value['tag'].replace("minecraft:", "", 1)
                    elif 'item' in value:
                        # Supprimer le préfixe "minecraft:"
                        items = value['item'].replace("minecraft:", "", 1)
               
                result = dataRecipe['result']['item'].replace("minecraft:", "", 1)
                data.append({'items': items, 'result': result})

# Convertir en DataFrame
df = pd.DataFrame(data)
# Afficher les premières lignes du DataFrame
print(df)