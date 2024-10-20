import json


def write_json_to_file(data, filename):
    json_str = json.dumps(data, indent=4, ensure_ascii=False)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(json_str)


def write_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
