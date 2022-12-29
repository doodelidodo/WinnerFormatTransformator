from numpy import NaN, empty
import pandas as pd
import json
from datetime import datetime

# ToDo
# - FileName anpassen


SEPARATOR = ';'
ENCODING = 'cp1252'

config_file = open('config.json')
config = json.load(config_file)
prefixes = config['config']['prefix']

def import_excel(file_name):
    excel_data = pd.read_excel(file_name)
    return pd.DataFrame(excel_data)

def import_csv(file_name):
    csv_data = pd.read_csv(file_name, sep = SEPARATOR, encoding = ENCODING)
    return pd.DataFrame(csv_data)

def transform_dataset(df, prefix):
    df = df.rename(columns={"Artikel-Nr.": "ArtikelNr"})
    data = pricegroup_separator(df)
    data = set_serie(data)
    data['ArtikelNr'] = data['ArtikelNr'].str.replace(r'@@[0-9]{1,2}', '', regex=True)
    data['ArtikelNr'] = prefix + "-" + data['ArtikelNr']
    data['prefix'] = prefix
    data['Preisgruppe'] = data['Preisgruppe']
    data = data.assign(Preisgruppe = lambda dataframe: dataframe['Preisgruppe']
    .map(lambda anr: anr.split(".")[0]))
    return data

def pricegroup_separator(df):
    preisgruppen = []
    not_preisgruppen = []

    for prod in df.columns:
        if 'Preisgruppe' in prod: 
            preisgruppen.append(prod)
        else: 
            not_preisgruppen.append(prod)

    data = df.melt(id_vars=not_preisgruppen, value_vars=preisgruppen, var_name='Preisgruppe', value_name='Preis')
    return data[data['Preis'].notnull()].sort_values(by=["ArtikelNr", "Preisgruppe"])

def set_serie(df):
    return df.assign(serie = lambda dataframe: dataframe['ArtikelNr']
    .map(lambda anr: anr.split("@@",1)[1] if '@@' in anr else ''))


def get_prefix(fileName):
    for pref in prefixes: 
        if fileName.startswith(pref['FileName']):
            return pref['prefix']
        
def export_import_files(df, prefix):
    singleProds = df['ArtikelNr'].unique()
    varianten = pd.DataFrame()
    non_varianten = pd.DataFrame()
    for prod in singleProds:
        filteredProds = df[df.ArtikelNr == prod]
        if len(filteredProds['ArtikelNr']) > 1:
            varianten = pd.concat([varianten, filteredProds])
        else: 
            non_varianten = pd.concat([non_varianten, filteredProds])
    dt = dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name_var = "export/" + prefix + "-var-" + dt + ".xlsx"
    file_name_non_var = "export/" + prefix + "-non_var-" + dt + ".xlsx"
    varianten.to_excel(file_name_var, index=False) 
    non_varianten.to_excel(file_name_non_var, index=False)