from update import update_json
import utility
import quiz
import sys

file_name = "sentences.json"


def switch_command(command):
    if command == "update":
        ans = input("Are you sure to update data? (y/n)")
        if ans == "y":
            update_json(file_name)
        else:
            quit()
    elif command == "reset":
        ans = input("Are you sure to reset progress? (y/n)")
        if ans == "y":
            utility.reset_data_strength(file_name)
        else:
            quit()
    elif command == "quiz":
        number_of_questions = int(input("How many questions?\n"))
        quiz.take_quiz(file_name, number_of_questions)
    elif command == "stats":
        utility.get_stats(file_name)
    elif command == "get-bookmarks":
        utility.get_bookmarks(file_name)
    elif command == "clear-bookmarks":
        id = int(input("Enter id of the bookmark to remove?\n"))
        utility.clear_bookmark_by_ids(file_name, id)
    else:
        print("unknown command")
        quit()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("USAGE: python app.py <command>")
        print("commands: update, reset, quiz, stats, get-bookmarks, clear-bookmarks")
        quit()
    else:
        command = sys.argv[1]

    switch_command(command)
