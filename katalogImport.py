from util import *

try: 
    import_file = get_file_from_folder()
    print("File wurde gefunden")

    try:
        prefix = get_prefix(import_file)
        print("Prefix wurde gefunden")

        try:
            new_catalog = import_csv()
            print("Katalog erfolgreich importiert")

            try:
                new_catalog = transform_dataset(new_catalog, prefix)
                print("Katalog erfolgreich transformiert")
                try:
                    export_import_files(new_catalog, prefix)
                    print("Katalog ist bereit für den Import ins Abacus")
                    success()
                    print("ENDE")

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








# Die importierten Daten ins Abacus Format transformieren




