import json
from pathlib import Path
from typing import Any, Dict

DIR_META_FILE_NAME = ".dir_meta.json"


def get_dir_meta_file_path(dir: Path):
    return dir / DIR_META_FILE_NAME


def get_file_meta(file: Path) -> Dict[str, Any]:
    file_name = file.name
    meta_file = get_dir_meta_file_path(file.parent)
    meta_dict = get_json_dict(meta_file)
    file_meta = meta_dict.get(file_name)
    return file_meta if file_meta else {}


def save_file_meta(file: Path, data):
    file_name = file.name
    dir_meta_path = get_dir_meta_file_path(file.parent)

    dir_meta = get_json_dict(file=dir_meta_path)
    dir_meta[file_name] = data
    write_dict_to_json(dict=dir_meta, filename=dir_meta_path)


def get_json_dict(file: Path) -> Dict:
    try:
        with open(file) as f:
            return json.load(f)
    except FileNotFoundError:
        data = {}

    return data


def write_dict_to_json(dict: Dict, filename: Path):
    # Open the file in write mode, overwriting any existing file
    with open(filename, "w") as file:
        # Write the dictionary to the file in JSON format
        json.dump(dict, file)

    print(f"Dictionary successfully written to '{filename}' in JSON format.")
