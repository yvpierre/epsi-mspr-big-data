import pandas as pd

# Chemin du fichier Excel
file_path = 'sources/presidentiel_departement_2022.xlsx'

# Charger les données
data = pd.read_excel(file_path)

# Identifier initialement toutes les colonnes à supprimer
colonnes_a_supprimer = [col for col in data.columns if 'Unnamed' in col]  # Suppression des colonnes non nommées

# Ne supprimez les colonnes avec les points qu'après avoir réorganisé le dataframe
colonnes_a_supprimer.extend([
    'Etat saisie', 'Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins',
    'Blancs', '% Blancs/Ins', '% Blancs/Vot', 'Nuls', '% Nuls/Ins', '% Nuls/Vot',
    'Exprimés', '% Exp/Ins', '% Exp/Vot', 'Sexe', 'Voix', '% Voix/Exp'
])

# Utilisez les données avant de les supprimer
columns = []
for i in range(12):  # Assurez-vous que cela correspond au nombre réel de candidats
    suffix = f".{i}" if i > 0 else ""
    columns.append((f'Nom{suffix}', f'Prénom{suffix}', f'% Voix/Ins{suffix}'))

# Melting the dataframe to long format
df_long = pd.DataFrame()
for col in columns:
    if all(item in data.columns for item in [col[0], col[1], col[2]]):
        temp_df = data[['Code du département', 'Libellé du département', col[0], col[1], col[2]]]
        temp_df.columns = ['Code du département', 'Libellé du département', 'Nom', 'Prénom', '% Voix/Ins']
        df_long = pd.concat([df_long, temp_df], ignore_index=True)

# Supprimer les colonnes sélectionnées après toutes les manipulations
data.drop(columns=colonnes_a_supprimer, inplace=True)

# Resetting index and sorting the data
df_long.reset_index(drop=True, inplace=True)
df_long.sort_values(by=['Code du département', 'Libellé du département', 'Nom', 'Prénom'], inplace=True)

df_long.insert(0, 'Année', 2022)

# Export the transformed data to a new Excel file
output_csv_path = 'output/2022_presidentiel_departement.csv'
df_long.to_csv(output_csv_path, index=False)
