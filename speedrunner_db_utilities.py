import json
import csv

def is_database_empty(database):
    if not database:
        return True
    else:
        return False

def load_database(db_name):
    try:
        with open('./data/' + db_name + '.json', 'r') as json_file: 
            print('Loading ' + db_name + ' database successful') 
            return json.load(json_file)
    except FileNotFoundError:
        print('File ' + db_name + '.json' + ' not found')
        return {db_name:[]}

def save_database(database, db_name):
    try:
        with open('./data/' + db_name + '.json', 'w+') as json_file:
            json.dump(database, json_file)
            print('Saving ' + db_name + ' database successful') 
    except FileNotFoundError:
        print('File ' + db_name + '.json' + ' not found')
        
def print_database(database):
    print(json.dumps(database, indent=4))

def validate_database_uniqueness(database, db_key, unique_key):
    keys = set()
    for game in database[db_key]:
        if game[unique_key] in keys:
            return False
        else:
            keys.add(game[unique_key])
    return True
            

def get_data_from_csv(csv_name):
    try:
        with open(csv_name + '.csv', mode='r') as csv_file:
            entries = []

            reader = csv.reader(csv_file)
            
            keys = []
            for key in next(reader, None):
                keys.append(key)
            
            #print('keys', keys)

            entry = []
            for line in reader:
                entry = {}
                for idx in range(len(line)):
                    entry[keys[idx]] = line[idx]

                #print('new entry: ', entry)

                entries.append(entry)

            return entries
    except FileNotFoundError:
        print('File ' + csv_name + '.csv' + ' not found')
        return []
