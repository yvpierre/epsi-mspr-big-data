import pandas as pd


# Chemins vers les fichiers CSV
file_path_2017 = 'output/2017_presidentiel_departement.csv'
file_path_2022 = 'output/2022_presidentiel_departement.csv'
file_path_security = 'output/clean_infos-securite-par-departement-2016-2023.csv'
file_path_unemployment = 'output/chomage.csv'

# Charger les données des fichiers
data_2017 = pd.read_csv(file_path_2017)
data_2022 = pd.read_csv(file_path_2022)
data_security = pd.read_csv(file_path_security)
data_unemployment = pd.read_csv(file_path_unemployment)

# Fusionner les deux DataFrames des élections présidentielles en un seul
data_combined = pd.concat([data_2017, data_2022], ignore_index=True)

# Enlever les lignes avec des codes de département non-numériques
data_combined['Code du département'] = data_combined['Code du département'].apply(lambda x: f"{int(x):02d}" if x.isdigit() else None)
data_combined = data_combined.dropna(subset=['Code du département'])

# Filtrer les données de sécurité pour les périodes 2016-2017 et 2018-2022
data_security_2016_2017 = data_security[data_security['Année'].isin([2016, 2017])]
data_security_2018_2022 = data_security[data_security['Année'].isin([2018, 2019, 2020, 2021, 2022])]

# Calculer la moyenne du taux pour mille moyen pour chaque département pour les deux périodes
mean_rates_2016_2017 = data_security_2016_2017.groupby('Code Département')['Taux pour Mille Moyen'].mean().reset_index()
mean_rates_2018_2022 = data_security_2018_2022.groupby('Code Département')['Taux pour Mille Moyen'].mean().reset_index()
mean_rates_2016_2017.rename(columns={'Taux pour Mille Moyen': 'Taux pour Mille'}, inplace=True)
mean_rates_2018_2022.rename(columns={'Taux pour Mille Moyen': 'Taux pour Mille'}, inplace=True)

# Fusionner les moyennes avec les données de 2017 et 2022 dans le tableau combiné
data_2017_with_rates = pd.merge(data_combined[data_combined['Année'] == 2017], mean_rates_2016_2017, how='left', left_on='Code du département', right_on='Code Département')
data_2022_with_rates = pd.merge(data_combined[data_combined['Année'] == 2022], mean_rates_2018_2022, how='left', left_on='Code du département', right_on='Code Département')

# Recombiner les données de 2017 et 2022 avec les taux respectifs
data_final_adjusted = pd.concat([data_2017_with_rates, data_2022_with_rates], ignore_index=True)
data_final_adjusted.drop(columns=['Code Département'], inplace=True)

# Filtrer les données de chômage pour les périodes 2016-2017 et 2018-2022
data_unemployment_2016_2017 = data_unemployment[data_unemployment['Année'].isin([2016, 2017])]
data_unemployment_2018_2022 = data_unemployment[data_unemployment['Année'].isin([2018, 2019, 2020, 2021, 2022])]

# Calculer la moyenne du taux de chômage pour chaque département pour les deux périodes
mean_unemployment_2016_2017 = data_unemployment_2016_2017.groupby('Département')['Taux de chômage'].mean().reset_index()
mean_unemployment_2018_2022 = data_unemployment_2018_2022.groupby('Département')['Taux de chômage'].mean().reset_index()

# Fusionner les moyennes avec les données électorales de 2017 et 2022 dans le tableau combiné
data_2017_with_unemployment = pd.merge(data_final_adjusted[data_final_adjusted['Année'] == 2017], mean_unemployment_2016_2017, how='left', left_on='Libellé du département', right_on='Département')
data_2022_with_unemployment = pd.merge(data_final_adjusted[data_final_adjusted['Année'] == 2022], mean_unemployment_2018_2022, how='left', left_on='Libellé du département', right_on='Département')

# Recombiner les données de 2017 et 2022 avec les taux de chômage respectifs
data_final_with_unemployment = pd.concat([data_2017_with_unemployment, data_2022_with_unemployment], ignore_index=True)
data_final_with_unemployment.drop(columns=['Département'], inplace=True)

# Sauvegarder le DataFrame final ajusté dans un nouveau fichier CSV
output_path = 'output/fichier_final_ajuste_avec_chomage.xlsx'
data_final_with_unemployment.to_excel(output_path, index=False)
