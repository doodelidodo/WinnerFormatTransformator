# WinnerFormatTransformator
Dieses Programm wandelt ein Katalog-Export vom Winner in ein besser lesbares csv um, dass dann im Abacus weiterverarbeitet wird.
Die Config ist hardcodiert und zeigt immer auf folgenden Pfad: "D:/Abacus/WinnerImport/WinnerTransformator.cfg". Dies wurde daher so umgesetzt,
da Abacus im Prozess das File auf dem Server ausführt, wo genau weiss man nicht und darum wurde der Pfad zur Config Datei fix definiert.

### Config File: WinnerTransformator.cfg
Im Config File können folgende Werte gesetzt werden:
- importFolder -> wo muss die Datei liegen, die dann vom Programm importier und verarbeitet wird
- exportFolder -> wohin wird / werden das File / die Files exportiert
- errorFolder -> in diesem Folder wird ein error.txt File erstellt, wenn ein Problem auftritt. Der Fehler wird als neue Zeile eingefügt, welcher dann via Report im Abacus ausgegebn werden kann
- prefixFolder -> in diesem Folder wird ein Text-File generiert, mit dem Prefix vom Lieferanten. Zudem werden alle Files in diesem txt aufgeführt, die generiert wurden. 
- prefixes -> in diesem json können die verschiedenen Kataloge hinterlegt werden. Mögliche Attribute sind
    - FileName -> eindeutige Bezeichnung vom File. So fängt der Name an vom Katalog-File
    - prefix -> mit welchem Prefix die Artikel von diesem Katalog importiert werden sollen
    - suffix -> dieser Wert ist wichtig für die Kondition für die Lieferanten


### Beispiel:

```
[Default]
importFolder = D:/Abacus/abac/out/Prozesse/1001-Katalogimport/INPUT/
exportFolder = D:/Abacus/abac/out/Prozesse/1001-Katalogimport/TEMP/
errorFolder = D:/Abacus/abac/out/Prozesse/1001-Katalogimport/ERROR/
prefixFolder = D:/Abacus/abac/out/Prozesse/1001-Katalogimport/PREFIX/


prefixes = [{
                "FileName": "AEG",
                "prefix": "AI",
                "suffix": "02"
            },
            {
                "FileName": "AMEU",
                "prefix": "AI"
            },
            {
                "FileName": "BAUKD",
                "prefix": "BA"
            },
            {
                "FileName": "BLAND",
                "prefix": "BL"
            }]
```
