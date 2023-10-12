from app import app
from app.models import Power

import csv


def printFile():
    with open("data-work.txt", "r") as filedesc:
        reader = csv.reader(filedesc)
        for i in reader:
            print(i)