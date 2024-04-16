import pandas as pd

# Chemin du fichier Excel
file_path = 'sources/infos-securite-par-departement-2016-2023.xlsx'

# Charger les données
data = pd.read_excel(file_path)

# Grouper les données par 'annee' et 'Code.département' et calculer la moyenne de 'tauxpourmille'
grouped_data = data.groupby(['annee', 'Code.département'])['tauxpourmille'].mean().reset_index()

# Renommer les colonnes pour plus de clarté
grouped_data.columns = ['Année', 'Code Département', 'Taux pour Mille Moyen']

# Ajuster le format de l'année
grouped_data['Année'] = grouped_data['Année'].apply(lambda x: 2000 + x)

# Chemin du nouveau fichier Excel à enregistrer
output_file_path = 'output/clean_infos-securite-par-departement-2016-2023.xlsx'

# Enregistrer le DataFrame dans un fichier Excel
grouped_data.to_excel(output_file_path, index=False)
