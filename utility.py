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


def get_bookmarks(file_name):
    data = read_from_json(file_name)
    bookmarked = [d for d in data if d['bookmarked']]
    print_bookmarks(bookmarked)


def print_bookmarks(bookmarked):
    if not bookmarked:
        print("No bookmarks")
    for d in bookmarked:
        print('\nid: ', d['id'])
        print('eng: ', d['english'])
        print('fr: ', d['french'])
        print('lvl: ', d['level'])
        print('strength: ', d['strength'])


def clear_bookmark_by_ids(file_name, *ids):
    data = read_from_json(file_name)
    bookmarked = [d for d in data if d['bookmarked']]
    for d in bookmarked:
        if d["id"] in ids:
            d["bookmarked"] = False
    write_collection_to_json(data, file_name)


def add_field(file_name, new_field, default_value):
    data = read_from_json(file_name)
    for d in data:
        d[new_field] = default_value
    write_collection_to_json(data, file_name)
    print("Data updated!")
