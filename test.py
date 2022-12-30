import configparser
import json
parser = configparser.ConfigParser()
parser.read('WinnerTransformator.cfg')

print(parser.get('Default', 'importFolder'))
prefixes = json.loads(parser.get('Default', 'prefixes'))

for prefix in prefixes:
    print(prefix['FileName'])