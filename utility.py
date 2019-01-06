from pathlib import Path
from colorama import Fore, Style, init as colorama_init
import json


def read_from_json(file_name):
    json_data = Path(file_name).read_text(encoding="utf-8")
    try:
        data = json.loads(json_data)
    except ValueError:
        data = []

    return data


def write_collection_to_json(data, file_name):
    # write added json to file
    Path(file_name).write_text(json.dumps(
        data, ensure_ascii=False, indent=4), encoding="utf-8")


def reset_data_strength(file_name):
    data = read_from_json(file_name)
    for d in data:
        d['strength'] = 0
    write_collection_to_json(data, file_name)
    print(file_name + " reseted!")


def get_stats(file_name):
    colorama_init()
    data = read_from_json(file_name)
    low = len([d for d in data if d['strength'] < 4])
    mid = len([d for d in data if 3 < d['strength'] < 8])
    high = len([d for d in data if 7 < d['strength']])
    print(f"Total number of items: {len(data)}")
    print(f"{Fore.RED}(0-3): {low}")
    print(f"{Fore.YELLOW}(4-7): {mid}")
    print(f"{Fore.GREEN}(8+): {high}{Style.RESET_ALL}")
