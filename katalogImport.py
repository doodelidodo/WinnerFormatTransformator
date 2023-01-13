from util import *

try: 
    import_file = get_file_from_folder()

    try:
        prefix = get_prefix(import_file)

        try:
            new_catalog = import_csv()

            try:
                new_catalog = transform_dataset(new_catalog, prefix)
                try:
                    export_import_files(new_catalog, prefix['prefix'])
                    success()
                    print(datetime.now().strftime("%Y%m%d-%H%M%S"))

                except:
                    error_handling("Der Katalog konnte nicht exportiert werden")
            except:
                error_handling("Der Katalog konnte nicht korrekt mutiert werden für den Import")

        except:
            error_handling("Der Katalog konnte nicht korrekt importiert werden")

    except:
        error_handling("Für den Katalog " + import_file + " wurde kein Prefix in der Config definiert")

except:
    error_handling("Der Katalog konnte nicht auf den Server geladen werden", False)