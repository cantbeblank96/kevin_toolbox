import json


def write_json(content, file_path):
    with open(file_path, 'w') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)
