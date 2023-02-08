import codecs
import pandas as pd
import json
from datetime import datetime
import os
import configparser
import re
import sys

price_per = str(sys.argv[1])
inflation = str(sys.argv[2])


CONFIG = "D:/Abacus/WinnerImport/WinnerTransformator.cfg"

parser = configparser.ConfigParser()
parser.read(CONFIG)

SEPARATOR = ';'
ENCODING = 'latin1'
IMPORT_FOLDER = parser.get('Default', 'importFolder')
EXPORT_FOLDER = parser.get('Default', 'exportFolder')
EXPORT_TYPE = parser.get('Default', 'exportType')
ERROR_FOLDER = parser.get('Default', 'errorFolder')
PREFIXES = json.loads(parser.get('Default', 'prefixes'))


def get_file_from_folder():
    return os.listdir(IMPORT_FOLDER)[0]


def import_csv():
    csv_data = pd.read_csv(IMPORT_FOLDER + get_file_from_folder(), sep=SEPARATOR, encoding=ENCODING, low_memory=False)
    return pd.DataFrame(csv_data)


def transform_dataset(df, prefix):
    df = df.astype({'!Artikel-Nr.': str})
    df = drop_unnamed_columns(df)
    df = df.iloc[1:]
    df = df.rename(columns={"!Artikel-Nr.": "ArtikelNr"})
    df = set_serie(df)
    df['ArtikelNr'] = df['ArtikelNr'].str.replace(r'@@[0-9]{1,2}', '', regex=True)
    df['ArtikelNr'] = df['ArtikelNr'].str.replace('#', '')
    df['ArtikelNr'] = prefix['prefix'] + "-" + df['ArtikelNr']
    df['PreisPer'] = price_per
    df['Teuerung'] = inflation
    df['Beschreibung'] = df['Beschreibung'].str.replace("\n", " ")
    df['prefix'] = prefix['prefix']
    if 'suffix' in prefix:
        df['suffix'] = prefix['suffix']
    else:
        df['suffix'] = ""   
    df = pricegroup_separator(df)
    df = df.assign(Preisgruppe=lambda dataframe: dataframe['Preisgruppe']
                   .map(lambda anr: anr.split(".")[0]))
    return df


def drop_unnamed_columns(df):
    unnamed_cols  =  df.columns.str.contains('Unnamed')
    return df.drop(df[df.columns[unnamed_cols]], axis=1)


def pricegroup_separator(df):
    preisgruppen = []
    not_preisgruppen = []
    for prod in df.columns:
        if 'Preisgruppe' in prod:
            preisgruppen.append(prod)
        else:
            not_preisgruppen.append(prod)
    df = df.melt(id_vars=not_preisgruppen, value_vars=preisgruppen, var_name='Preisgruppe', value_name='Preis')
    return df[df['Preis'].notnull()].sort_values(by=["ArtikelNr", "Preisgruppe"])


def set_serie(df):
    return df.assign(
        serie=lambda dataframe: dataframe['ArtikelNr'].map(lambda anr: anr.split("@@", 1)[1] if '@@' in anr else ''))


def get_prefix(file_name):
    the_pref = ""
    for pref in PREFIXES:
        if get_label(file_name) == pref['FileName']:
            the_pref = pref
    if the_pref == "":
        raise Exception("Kein Prefix gefunden")
    else:
        return the_pref


def export_import_files(df, prefix):
    all_products = mark_variants(df)
    dt = datetime.now().strftime("%Y%m%d-%H%M%S")
    if EXPORT_TYPE == 'xlsx':
        file_name = EXPORT_FOLDER + prefix + "-all-" + dt + ".xlsx"
        all_products.to_excel(file_name, index=False, engine="xlsxwriter")
    else:
        file_name = EXPORT_FOLDER + prefix + "-all-" + dt + ".csv"
        all_products.to_csv(file_name, index=False, sep=SEPARATOR, encoding='utf-8-sig')
    


def mark_variants(df):
    counts = df.ArtikelNr.value_counts()

    varianten = df[df.ArtikelNr.isin(counts.index[counts.gt(1)])].copy()
    non_varianten = df[df.ArtikelNr.isin(counts.index[counts.eq(1)])].copy()

    varianten['variante'] = 1
    non_varianten['variante'] = 0

    return pd.concat([varianten, non_varianten])


def error_handling(error, delete=True):
    file_name = ERROR_FOLDER + "error.txt"
    with codecs.open(file_name, "a", "utf-8") as f:
        f.write(error + "\n")
    if delete:
        delete_file()


def success():
    delete_file()


def delete_file():
    os.remove(IMPORT_FOLDER + get_file_from_folder())


def get_label(file_name):
    file_name = re.sub('[^a-zA-Z.]+', '', file_name)
    return file_name.split('.')[0]
