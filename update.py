import utility
from pathlib import Path
import json
import re


def update_json(file_name):
    eng_list = Path("en.txt").read_text(encoding="utf-8").split("\n")
    fr_list = Path("fr.txt").read_text(encoding="utf-8").split("\n")

    assert len(eng_list) == len(
        fr_list), f"Lengths are different, eng: {len(eng_list)} != fr: {len(fr_list)}"

    # read current data from json file
    data = utility.read_from_json(file_name)

    # update dict and write to json file
    (last_index, new_index) = write_to_json(data, eng_list, fr_list, file_name)

    print(f"Data updated successfully: {last_index} -> {new_index}")


def write_to_json(data, eng_list, fr_list, target_file):
    # get the last index, so can append new info
    last_index = 0 if not data else data[-1]["id"]

    # add new data to the loaded json
    index = 0

    for (eng, fr) in zip(eng_list, fr_list):
        out = re.search(r'\[([^\]]+)', eng)
        lvl = out.group(1) if out != None else 0
        eng = eng.split('[')[0]
        # add only if it is new
        if not any(sen["english"].strip().lower() == eng.lower() for sen in data):
            index += 1
            item = dict(id=last_index + index,
                        english=eng, french=fr, strength=0, level=lvl, bookmarked=False, tags=[], notes="")
            data.append(item)

    # write added json to file
    utility.write_collection_to_json(data, target_file)

    return (last_index, last_index + index)
