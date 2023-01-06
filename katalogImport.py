from util import *

try: 
    import_file = get_file_from_folder()
except:
    error_handling("Der Katalog konnte nicht auf den Server geladen werden", False)


try:
    prefix = get_prefix(import_file)
except:
    error_handling("Für den Katalog " + import_file + " wurde kein Prefix in der Config definiert")


try: 
    new_catalog = import_csv()
except:
    error_handling("Der Katalog konnte nicht korrekt importiert werden")


# Die importierten Daten ins Abacus Format transformieren
try:
    new_catalog = transform_dataset(new_catalog, prefix)
except:
    error_handling("Der Katalog konnte nicht korrekt mutiert werden für den Import")


try:
    export_import_files(new_catalog, prefix)
    success()
except: 
    error_handling("Der Katalog konnte nicht exportiert werden")
