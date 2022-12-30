from util import *

import_file = get_file_from_folder()

# Katalog auswählen und in ein pandas DataFrame umwandeln
prefix = get_prefix(import_file)
new_catalog = import_csv()

# Die importierten Daten ins Abacus Format transformieren
new_catalog = transform_dataset(new_catalog, prefix)

export_import_files(new_catalog, prefix)

