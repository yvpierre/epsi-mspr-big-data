import pandas as pd

# Chemin du fichier Excel
file_path = 'sources/presidentiel_departement_2017.xlsx'

# Charger les données
data = pd.read_excel(file_path)

colonnes_a_supprimer = [col for col in data.columns if col.startswith(('% Voix/Exp', 'Sexe', 'Voix')) and '.' in col]

# Ajoutez à cette liste les autres colonnes que vous voulez supprimer qui n'ont pas de point
colonnes_a_supprimer.extend(['Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', 'Blancs', '% Blancs/Ins', '% Blancs/Vot', 'Nuls', '% Nuls/Ins', '% Nuls/Vot', 'Exprimés', '% Exp/Ins', '% Exp/Vot', '% Vot/Ins', '% Voix/Exp', 'Sexe', 'Voix'])

# Supprimer les colonnes sélectionnées
data = data.drop(columns=colonnes_a_supprimer)

columns = []
for i in range(11):  # Adjust the range based on the number of candidates
    suffix = f".{i}" if i > 0 else ""
    columns.append((f'Nom{suffix}', f'Prénom{suffix}', f'% Voix/Ins{suffix}'))

# Melting the dataframe to long format
df_long = pd.DataFrame()
for col in columns:
    temp_df = data[['Code du département', 'Libellé du département', col[0], col[1], col[2]]]
    temp_df.columns = ['Code du département', 'Libellé du département', 'Nom', 'Prénom', '% Voix/Ins']
    df_long = pd.concat([df_long, temp_df], axis=0)

# Resetting index and sorting the data
df_long.reset_index(drop=True, inplace=True)
df_long.sort_values(by=['Code du département', 'Libellé du département', 'Nom', 'Prénom'], inplace=True)

df_long.insert(0, 'Année', 2017)

# Export the transformed data to a new Excel file
output_csv_path = 'output/2017_presidentiel_departement.csv'
df_long.to_csv(output_csv_path, index=False)