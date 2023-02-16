from util import *

try: 
    import_file = get_file_from_folder()

    try:
        prefix = get_prefix(import_file)

        try:
            new_catalog = import_csv()

            try:
                new_catalog = transform_dataset(new_catalog, prefix, price_per, inflation)
                try:
                    if len(new_catalog) > 100000:
                        export_files(new_catalog, prefix['prefix'], 4)
                    else:
                        export_files(new_catalog, prefix['prefix'], 1)
                    success()
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