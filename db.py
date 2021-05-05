import os
import ast
import csv

D = {}
if os.path.exists('database.csv'):
    with open('database.csv', 'r') as file:
        for line in csv.reader(file):
            D[int(line[0])] = ast.literal_eval(line[1])


def _save_on_disk():
    global D
    file = open("database.csv", "w")
    for key, value in D.items():
        csv.writer(file).writerow([key, value])

    file.close()


def is_user(userID: int) -> bool:
    return userID in D.keys()


def add_user(userID: int, firstName: str, lastName: str, username: str):
    global D
    D[userID] = {'firstname': firstName, 'lastname': lastName, 'username': username, 'track': False, 'sid': ""}
    _save_on_disk()


def change_user_tracking(userID: int, track: bool) -> None:
    global D
    D[userID]['track'] = track
    _save_on_disk()


def change_user_studentid(userID: int, studentID: int) -> None:
    global D
    D[userID]['sid'] = studentID
    _save_on_disk()
