import utility
from pathlib import Path
from datetime import date
from timeit import default_timer as timer
import json
import random


def take_quiz(file_name, number_of_questions):

    # read data
    data = utility.read_from_json(file_name)

    # copy data to a new list to shuffle and prevent messing order of the original list
    shuffled = list(data.values()).copy()
    random.shuffle(shuffled)

    # sort based on the strength
    sorted_data = sorted(shuffled, key=lambda k: k["strength"])

    # select the first x from the sorted list
    questions_indices = [ind['id']
                         for ind in sorted_data[:number_of_questions]]

    yes = no = later = 0

    print(f"Quiz for {number_of_questions} questions started...")
    print("For each question, first the sentence will be shown in english\n"
          + "Try to come up with its french equivalent\n" + "Press any key to continue")

    faults = []
    start = timer()
    for index in questions_indices:
        question = data.get(str(index))
        # can randomly ask french or english
        input("\n" + question["english"])
        print(question["french"] + "\n")

        ans = False
        while not ans:
            user_input = input(
                "Did you know the answer? (y)es - (n)o - (a)sk later\n")
            ans = True
            if user_input == "y":
                yes += 1
                question["strength"] = question["strength"] + 1
            elif user_input == "n":
                no += 1
                faults.append(index)
                question["strength"] = 0 if question["strength"] < 1 else question["strength"] - 1
            elif user_input == "a":
                later += 1
                pass
            else:
                ans = False

        ans = False
        while not ans:
            user_input = input(
                "Do you want to bookmark the question? (y)es - (n)o\n")
            ans = True
            if user_input == "y":
                question["bookmarked"] = True
            elif user_input == "n" or user_input == "":
                question["bookmarked"] = False
            else:
                ans = False

    end = timer()
    delta_time = int(end - start)  # Time in seconds, e.g. 5.38091952400282
    print(
        f"out of {number_of_questions}:\n correct answers: {yes}\n wrong answers: {no}\n ask later: {later}")

    # write back data to json file
    utility.write_collection_to_json(data, file_name)

    # write the progress
    print()
    utility.write_progress(yes=yes, no=no, later=later,
                           _faults=faults, time=delta_time)
    utility.get_progress_by_date(str(date.today()))
