from pathlib import Path
from colorama import Fore, Style, init as colorama_init
from datetime import date, timedelta
import json


def build_dict(seq, key):
    return dict((d[key], dict(d)) for (index, d) in enumerate(seq))


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
    data = read_from_json(file_name).values()
    for d in data:
        d['strength'] = 0
    write_collection_to_json(data, file_name)
    print(file_name + " reseted!")


def get_stats(file_name):
    colorama_init()
    data = read_from_json(file_name).values()
    low = len([d for d in data if d['strength'] < 1])
    mid = len([d for d in data if 1 <= d['strength'] < 3])
    high = len([d for d in data if 3 <= d['strength']])
    print(f"Total number of items: {len(data)}")
    print(f"{Fore.RED}(0): {low}")
    print(f"{Fore.YELLOW}(1-3): {mid}")
    print(f"{Fore.GREEN}(3+): {high}{Style.RESET_ALL}")


def get_bookmarks(file_name):
    data = read_from_json(file_name).values()
    bookmarked = [d for d in data if d['bookmarked']]
    print_bookmarks(bookmarked)


def print_sentence(d):
    print('\nid: ', d['id'])
    print('eng: ', d['english'])
    print('fr: ', d['french'])
    print('lvl: ', d['level'])
    print('strength: ', d['strength'])


def print_bookmarks(bookmarked):
    if not bookmarked:
        print("No bookmarks")
    for d in bookmarked:
        print_sentence(d)


def clear_bookmark_by_ids(file_name, *ids):
    data = read_from_json(file_name)
    bookmarked = [d for d in data.values() if d['bookmarked']]
    for d in bookmarked:
        if d["id"] in ids:
            d["bookmarked"] = False
    write_collection_to_json(data, file_name)


def remove_field(file_name, field):
    data = read_from_json(file_name)
    for d in data.values():
        d.pop(field, None)
    write_collection_to_json(data, file_name)
    print("Data updated!")


def add_field(file_name, new_field, default_value):
    data = read_from_json(file_name)
    for d in data:
        d[new_field] = default_value
    write_collection_to_json(data, file_name)
    print("Data updated!")


def write_progress(yes, no, later, _faults, time):
    progress = read_from_json("progress.json")
    today = str(date.today())
    total_questions = yes + no + later

    # if we have already entry for today, update it
    # otherwise create a new entry for today
    data_index = progress.get(today)
    if data_index != None:
        data_index['correct'] += yes
        data_index['wrong'] += no
        data_index['questions'] += total_questions
        data_index['spent_time'] += time
        data_index['faults'] = list(
            set(data_index['faults'] + _faults))
    else:
        data = dict(
            date=str(today),
            questions=total_questions,
            correct=yes,
            wrong=no,
            spent_time=time,
            faults=_faults
        )
        progress[str(today)] = data

    write_collection_to_json(progress, "progress.json")
    print(f"progress updated for {today}")


def get_progress():
    data = read_from_json("progress.json")
    print()
    for d in data.values():
        print_progress(d)


def get_progress_by_date(_date):
    data = read_from_json("progress.json").values()
    progress = next(d for d in data if d['date'] == _date)
    print_progress(progress)


def print_progress(d):
    result = percentage(d['correct'], d['questions'])
    secs = d['spent_time']
    if secs < 60:
        time = str(secs) + " seconds"
    else:
        time = str((secs // 60)) + " minutes, " + str((secs % 60)) + " seconds"
    print(
        f"{d['date']}: \tquestions: {d['questions']:3d} \t\tresult: {result:5s} \ttime spent: {time}")


def print_wrong_questions_by_day(date, summary):
    data = read_from_json("sentences.json")
    # data = build_dict(read_data, key="id")

    progress = read_from_json("progress.json")
    data_index = progress.get(date, None)

    # get indices of the wrong answered questions
    if not data_index:
        print("No data for today")
        return
    indices = data_index['faults']
    for ind in indices:
        print()
        sen = data.get(str(ind))
        if summary:
            print(sen.get('english'))
            print(sen.get('french'))
        else:
            print_sentence(sen)

    print()


def print_wrong_questions_this_week():
    today = date.today()
    for i in range(7, 0, -1):
        dt = str(today - timedelta(days=i))
        print(dt)
        print_wrong_questions_by_day(dt, summary=True)


def percentage(part, whole):
    return f"{ int(100 * int(part)/int(whole))}%"
