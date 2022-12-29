from util import *

import_file = 'SITAG-1354.csv'

# Katalog auswählen und in DataFrame umwandeln sowie alten aus dem Archiv laden
prefix = get_prefix(import_file)
new_catalog = import_csv(import_file)

# Die importierten Daten ins Abacus Format transformieren
new_catalog = transform_dataset(new_catalog, prefix)

export_import_files(new_catalog, prefix)



# Katalog mit alem Katalog vergleichen (wie weiss er, welcher der alte Katalog ist)
# Zudem gleich ein Excel für die alten Artikel erstellen, welche inaktiviert werden müsssen,
# Sowie ein Excel, welches die neuen Artikel drin enthält

# wenn alles geklappt hat, neuen Katalog ins Archiv verschieben



#old = import_excel('ALFiles/old.xlsx')
#new = import_excel('ALFiles/new.xlsx')

#diff_delete = compare_datasets(old, new, 'left_only')
#diff_new = compare_datasets(old, new, 'right_only')

#diff_delete.to_excel(r'delete.xlsx', index = False)
#diff_new.to_excel(r'new.xlsx', index = False)

#testImport = import_csv('data.csv')
