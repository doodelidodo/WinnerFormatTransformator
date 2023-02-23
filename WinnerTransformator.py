from util import *

def main():
    try:
        import_file = get_file_from_folder()
    except:
        error_handling("Die Import-Datei konnte nicht gefunden werden.", "", False)
        return

    try:
        prefix = get_prefix(import_file)
    except:
        error_handling(f"Für {import_file} ist kein Prefix in der Config definiert. Vorgang abgebrochen", import_file)
        return

    try:
        new_catalog = import_csv(import_file)
    except:
        error_handling("Der Katalog konnte nicht importiert werden.", import_file)
        return

    try:
        new_catalog = transform_dataset(new_catalog, prefix, price_per, inflation)
    except:
        error_handling("Der Katalog konnte nicht mutiert werden.", import_file)
        return

    try:
        if len(new_catalog) > 100000:
            export_files(new_catalog, prefix['prefix'], 4)
        else:
            export_files(new_catalog, prefix['prefix'], 1)
        delete_file(import_file)
    except:
        error_handling("Der Katalog konnte nicht exportiert werden.", import_file)
        return

if __name__ == '__main__':
    main()