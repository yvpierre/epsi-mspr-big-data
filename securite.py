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

grouped_data['Code Département'] = grouped_data['Code Département'].apply(lambda x: str(x).zfill(2))

# Chemin du nouveau fichier CSV à enregistrer
output_csv_path = 'output/clean_infos-securite-par-departement-2016-2023.csv'

# Enregistrer le DataFrame dans un fichier CSV
grouped_data.to_csv(output_csv_path, index=False)
