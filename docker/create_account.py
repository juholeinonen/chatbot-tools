#Before use install these
#pip install html5lib
#pip install mechanize

import mechanize
from time import sleep
from random import randrange
import csv
import argparse

parser = argparse.ArgumentParser(description='Creating accounts for chat experiment')
parser.add_argument('start', type=int, help='What is the first account number')
parser.add_argument('end', type=int, help='what is the last account number')
args = parser.parse_args()

def createAccount(numeral):
    firstname = chr(65 + randrange(25))
    lastname = chr(65 + randrange(25))
    password = str(randrange(99999999))

    if numeral < 10:
        number = "0" + str(numeral)
    else:
        number = str(numeral)
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://asr.aalto.fi/lets-chat/login")

    br.select_form(nr=1)
    br["username"] = "temp" + number
    br["email"] = "temp" + number + "@temp.com"
    br["display-name"] = "temp" + number
    br["first-name"] = firstname
    br["last-name"] = lastname
    br["password"] = password
    br["password-confirm"] = password
    response = br.submit()

    return "temp" + number, password

usersPasswords = {}
try:
    for number in range(args.start, args.end):
        user, password = createAccount(number)
        usersPasswords[user] = password
        print("Account ", number, " created")
        sleep(12)
except:
    print("did not create all, ended at: ", number)

with open("users_passwords.csv", "a", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerows(usersPasswords.items())


