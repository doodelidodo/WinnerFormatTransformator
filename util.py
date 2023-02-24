import codecs
import pandas as pd
import json
from datetime import datetime
import os
import configparser
import re
import sys
import numpy as np

price_per = str(sys.argv[1])
inflation = str(sys.argv[2])

CONFIG = "D:/Abacus/WinnerImport/WinnerTransformator.cfg"
parser = configparser.ConfigParser()
parser.read(CONFIG)

SEPARATOR = ';'
ENCODING = 'latin1'
IMPORT_FOLDER = parser.get('Default', 'importFolder')
EXPORT_FOLDER = parser.get('Default', 'exportFolder')
ERROR_FOLDER = parser.get('Default', 'errorFolder')
PREFIX_FOLDER = parser.get('Default', 'prefixFolder')
PREFIXES = json.loads(parser.get('Default', 'prefixes'))


def transform_dataset(df, prefix, price_per, inflation):
    the_prefix = set_prefix(prefix)

    df = (
        df.astype({'!Artikel-Nr.': str})
            .pipe(drop_unnamed_columns)
            .iloc[1:]
            .rename(columns={"!Artikel-Nr.": "ArtikelNr"})
            .pipe(set_serie)
            .assign(ArtikelNr=lambda df: df['ArtikelNr'].str.replace(r'@@[0-9]{1,2}', '', regex=True))
            .assign(ArtikelNr=lambda df: df['ArtikelNr'].str.replace('#', ''))
            .assign(ArtikelNr=lambda df: prefix['prefix'] + "-" + df['ArtikelNr'])
            .assign(PreisPer=price_per, Teuerung=inflation)
            .assign(Beschreibung=lambda df: df['Beschreibung'].str.replace("\n", " ").str.replace(";", " "))
            .assign(prefix = the_prefix)
            .assign(suffix=str(prefix.get('suffix', '')))
            .pipe(pricegroup_separator)
            .assign(Preisgruppe=lambda df: df['Preisgruppe'].str.split('.').str[0])
    )

    return df


def pricegroup_separator(df):
    preisgruppen = [prod for prod in df.columns if 'Preisgruppe' in prod]
    not_preisgruppen = [prod for prod in df.columns if 'Preisgruppe' not in prod]
    df = df.melt(id_vars=not_preisgruppen, value_vars=preisgruppen, var_name='Preisgruppe', value_name='Preis')
    return df.dropna(subset=['Preis']).sort_values(['ArtikelNr', 'Preisgruppe'])


def get_file_from_folder():
    folder_path = IMPORT_FOLDER
    all_files = os.listdir(folder_path)
    files_with_timestamps = [(filename, os.path.getmtime(os.path.join(folder_path, filename))) for filename in all_files]
    sorted_files = sorted(files_with_timestamps, key=lambda x: x[1], reverse=True)
    return sorted_files[0][0]


def import_csv(file):
    csv_data = pd.read_csv(IMPORT_FOLDER + file, sep=SEPARATOR, encoding=ENCODING, low_memory=False)
    return pd.DataFrame(csv_data)


def drop_unnamed_columns(df):
    return df.filter(regex='^(?!Unnamed)', axis=1)


def set_serie(df):
    return df.assign(
        serie=lambda dataframe: dataframe['ArtikelNr'].map(lambda anr: anr.split("@@", 1)[1] if '@@' in anr else ''))


def get_prefix(file_name):
    for pref in PREFIXES:
        if get_label(file_name) == pref['FileName']:
            return pref
    raise Exception("Kein passender Prefix gefunden")

def set_prefix(prefix):
    if 'prefixOrigin' in prefix:
        return prefix['prefixOrigin']
    else:
        return prefix['prefix']

def export_files(data_frame, prefix, num_parts):
    if data_frame.empty:
        raise ValueError("The input DataFrame is empty")
    if num_parts <= 0:
        raise ValueError("The number of parts must be greater than 0")
    
    prefix_file = prefix['prefix']
    prefix_testfile = set_prefix(prefix)


    all_products = mark_variants(data_frame)
    part_data_frames = np.array_split(all_products, num_parts)

    for i, part_df in enumerate(part_data_frames, start=1):
        dt = datetime.now().strftime("%Y%m%d-%H%M%S")
        if num_parts > 1: 
            file_name = f"{prefix_file}-all-{dt}-{i}.csv"
        else:
            file_name = f"{prefix_file}-all-{dt}.csv"

        write_test_files(prefix_testfile, PREFIX_FOLDER, file_name)

        file_path = os.path.join(EXPORT_FOLDER, file_name)
        part_df.to_csv(file_path, index=False, sep=SEPARATOR, encoding='utf-8-sig')


def mark_variants(df):
    counts = df.ArtikelNr.value_counts()

    df.loc[df.ArtikelNr.isin(counts.index[counts.gt(1)]), 'variante'] = 1
    df.loc[df.ArtikelNr.isin(counts.index[counts.eq(1)]), 'variante'] = 0

    return df

def write_test_files(prefix, path, name):
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = f"{path}{prefix}.txt"
    with codecs.open(file_name, "a", "utf-8") as f:
        f.write(f"{name}\n")


def error_handling(error, file, delete=True):
    if not os.path.exists(ERROR_FOLDER):
        os.makedirs(ERROR_FOLDER)
    file_name = ERROR_FOLDER + "error.txt"
    with codecs.open(file_name, "a", "utf-8") as f:
        f.write(error + "\n")
    if delete:
        delete_file(file)


def delete_file(file):
    os.remove(IMPORT_FOLDER + file)


def get_label(file_name):
    file_name = file_name.split('_')[0]
    file_name = re.sub('[^a-zA-Z.]+', '', file_name)
    return file_name.split('.')[0]
