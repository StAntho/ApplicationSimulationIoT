import pandas as pd
import numpy as np
import random
import string
from datetime import datetime
import os
from time import sleep

# Définir les paramètres pour les données aléatoires
num_rows = 100  # Nombre de lignes

while True:
    df = []
    for i in range(5):
        df.append({
            # 'id': np.arange(1, num_rows + 1),
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "device": "device-"+str(i+1),
            "distance": random.uniform(0.02, 0.25),
            "value": random.randint(1, 10),
            "heart_rate": random.randint(70, 225)
        })
    df = pd.DataFrame(df)
    print(df.head())

     # Vérifier si le fichier existe déjà
    file_exists = os.path.exists('./datas/random_data.csv')
    
    # Sauvegarder le DataFrame dans un fichier CSV en mode append
    df.to_csv('./datas/random_data.csv', mode='a', index=False, header=not file_exists)

    print("Les données aléatoires ont été générées et enregistrées dans 'random_data.csv'.")

    sleep(15)  