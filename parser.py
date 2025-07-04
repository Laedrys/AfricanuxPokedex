import re

def read_pokemon_entries(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Gérer correctement les blocs avec entêtes [xxx]
    if not content.startswith('['):
        content = '[DUMMY]\n' + content

    entries = re.split(r'\n\[(?=\d+\])', content)

    pokemon_data = []

    for entry in entries:
        lines = entry.strip().splitlines()
        data = {}

        header = lines[0].strip()
        match = re.match(r"\[?(\d+)\]?", header)
        if match:
            data['Number'] = int(match.group(1))
        else:
            continue

        for line in lines[1:]:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # 🎯 Extraction spéciale pour Abilities
                if key == "Abilities":
                    abilities = [a.strip() for a in value.split(',')]
                    data["Ability1"] = abilities[0] if len(abilities) > 0 else ""
                    data["Ability2"] = abilities[1] if len(abilities) > 1 else ""
                else:
                    data[key] = value

        if 'Name' in data:
            pokemon_data.append(data)

    pokemon_data.sort(key=lambda x: x['Number'])
    return pokemon_data

def get_numbered_name_list(pokemon_data):
    return [(p['Number'], p['Name']) for p in pokemon_data if 'Number' in p and 'Name' in p]

def get_pokemon_by_name(pokemon_data, name):
    for p in pokemon_data:
        if p['Name'].lower() == name.lower():
            return p
    return None
