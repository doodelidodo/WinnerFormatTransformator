from util import *

def main():
    try:
        import_file = get_file_from_folder()
    except:
        error_handling(9000, "", False)
        return

    try:
        prefix = get_prefix(import_file)
    except:
        error_handling(9010, import_file)
        return

    try:
        new_catalog = import_csv(import_file)
    except:
        error_handling(9020, import_file)
        return

    try:
        new_catalog = transform_dataset(new_catalog, prefix, price_per, inflation)
    except:
        error_handling(9030, import_file)
        return

    try:
        if len(new_catalog) > 100000:
            export_files(new_catalog, prefix, 4 , import_file)
        else:
            export_files(new_catalog, prefix, 1, import_file)
        delete_file(import_file)
    except:
        error_handling(9040, import_file)
        return

if __name__ == '__main__':
    main()