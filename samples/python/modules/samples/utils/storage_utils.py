import os
import json
from samples.utils.custom_json_encoder import CustomJsonEncoder


def create_directory(dir: str, clear_if_not_empty: bool = False) -> str:
    os.makedirs(dir, exist_ok=True)

    if clear_if_not_empty:
        for file in os.listdir(dir):
            file_path = os.path.join(dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return dir


def create_json_file(fpath: str, data: any, indent: int = 4) -> None:
    if not os.path.exists(os.path.dirname(fpath)):
        create_directory(os.path.dirname(fpath))

    with open(fpath, 'w') as f:
        json.dump(data, f, indent=indent, cls=CustomJsonEncoder)


def create_text_file(fpath: str, text: str) -> None:
    if not os.path.exists(os.path.dirname(fpath)):
        create_directory(os.path.dirname(fpath))

    with open(fpath, 'w') as f:
        f.write(text)


def create_data_file(fpath: str, data: any) -> None:
    if not os.path.exists(os.path.dirname(fpath)):
        create_directory(os.path.dirname(fpath))

    with open(fpath, 'wb') as f:
        f.write(data)
