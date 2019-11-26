import time
import datetime
from datetime import timedelta
import sys
phoneBook = {}
filename = None
used_phone_numbers = {}
possible_operations = {"Add": "Add a new record to the phohebook",
                        "Change": "Change a record in the phonebook",
                        "Search": "Advanced Search for an record in the phonebook by mask",
                        "Delete": "Delete a record",
                        "Delete by phone number": "Delete a record with entered phone number",
                        "Age": "Get an age of the person",
                        "Nearest birthdays": "Get a list of persons with a birthday in the next 30 days",
                        "Regarding age": "Get a lists of persons younger, equal and elder than entered years old",
                        "Search by date": "Get a list of persons with a birthday birthday on the entered day",
                        "Print": "Print content of the phonebook into console",
                        "Save": "Save content of the phonebook into the source file",
                        "Show operations": "Shows list of possible operations",
                        "Quit": "Exit from the program"}


def start():
    global filename
    filename = None
    phoneBook.clear()
    used_phone_numbers.clear()
    source_file = None
    print("Do you want to load data from the file?")
    answer = input("Enter 'Yes' or 'No (if you will enter 'No', output file will be named 'output.txt')\n").strip()
    while answer != "Yes" and answer != "No":
        print("Incorrect_name format")
        answer = input("Enter 'Yes' or 'No (if you will enter 'No', output file will be named 'output.txt')\n").strip()
    if answer == "No":
        filename = "output.txt"
        file = open(filename, 'w')
        file.close()
    else:
        while filename is None:
            print("Enter name of the source data file (it will be also used as output file):")
            filename = input().strip()
            try:
                file = open(filename, 'r')
                file.close()
            except IOError:
                print("Cannot open file '%s'!" % filename)
                filename = None
    with open(filename, 'r') as file:
        for line in file:
            add_to_the_phone_book(line.strip())


def show_list_of_operations():
    for operation, description in possible_operations.items():
        print("%s: %s" % (operation, description))


def check_name(name):
    if len(name) == 0 or not str.isalpha(name[0]):
        print("Incorrect_name 'name'/'last name' format")
        return False
    for char in name:
        if not str.isalpha(char) and not str.isalnum(char) and char != ' ':
            print("Incorrect_name 'name'/'last name' format")
            return False
    return True


def check_date(date):
    try:
        valid_date = time.strptime(date, '%d.%m.%Y')
    except ValueError:
        print("Incorrect_name 'date' format")
        return False
    return True


def check_phone(phone_number):
    if phone_number[:2] == "+7":
        phone_number = phone_number.replace('+7', '8', 1)
    if str.isnumeric(phone_number) and len(phone_number) == 11 and phone_number[0] == '8':
        return True
    print("Incorrect_name 'phone number' format")
    return False


def correct_name(name):
    return str.upper(name[0])+name[1:]


def correct_phone_number(_phone_number):
    return _phone_number.replace('+7', '8', 1)


def get_entry_data():
    print("You chose to add a new record. To do this enter 'Name;Last Name;DD.MM.YYYY;Phone number (11 digits)'")
    information = input(">>> ").strip()
    add_to_the_phone_book(information)


def delete_by_name_last_name():
    print("You chose to delete a record by name + last name. To do this enter 'Name;Last Name'")
    information = input(">>> ").strip().split(';')
    if len(information) != 2:
        print("Incorrect format")
        return
    name, last_name = information
    if check_name(name) and check_name(last_name):
        name = correct_name(name)
        last_name = correct_name(last_name)
        if (name, last_name) in phoneBook:
            used_phone_numbers.pop(phoneBook[(name, last_name)][1])
            phoneBook.pop((name, last_name))
        else:
            print("There is no such person in the phone book")


def delete_by_phone_number():
    print("You chose to delete a record by phone number. To do this enter phone number (11 digits)")
    phone_number = input().strip()
    while not check_phone(phone_number):
        phone_number = input().strip()
    phone_number = correct_phone_number(phone_number)
    if phone_number in used_phone_numbers:
        deleted_user = used_phone_numbers[phone_number]
        phoneBook.pop(deleted_user)
        used_phone_numbers.pop(phone_number)
    else:
        print("There is no person with this phone number in the phone book")


def add_to_the_phone_book(information):
    information = information.split(";")
    if len(information) != 4:
        print("Incorrect format")
        return
    name, last_name, date, phone_number = information
    if check_name(name) and check_name(last_name) and check_date(date) and check_phone(phone_number):
        name = correct_name(name)
        last_name = correct_name(last_name)
        phone_number = correct_phone_number(phone_number)
        while (name, last_name) in phoneBook:
            print("Same 'name/last name'")
            print("Record %s;%s;%s;%s is already in the phonebook" % (name, last_name, *phoneBook[(name, last_name)]))
            print("Enter:")
            print("'Rename' to stay record in the phonebook")
            print("'Replace' to delete old record and add new")
            print("'Skip' to stop adding of the record")
            answer = input().strip()
            while answer != 'Rename' and answer != 'Replace' and answer != 'Skip':
                print("Incorrect format")
                answer = input().strip()
            if answer == "Rename":
                information = input("Enter new 'name;last_name'\n").strip().split(';')
                while len(information) != 2 or not check_name(information[0]) or not check_name(information[1]):
                    print("Incorrect format")
                    information = input("Enter new 'name;last_name'\n").strip().split(';')
                name = correct_name(information[0])
                last_name = correct_name(information[1])
            elif answer == "Replace":
                used_phone_numbers.pop(phoneBook[(name, last_name)][1])
                phoneBook.pop((name, last_name))
            else:
                return
        while phone_number in used_phone_numbers:
            user = used_phone_numbers[phone_number]
            print("Same 'phone number'")
            print("Record %s;%s;%s;%s is already in the phonebook" %
                  (*user, phoneBook[user][0], phone_number))
            print("Enter:")
            print("'Change number' to stay record in the phonebook")
            print("'Replace' to delete old record and add new")
            print("'Skip' to stop adding of the record")
            answer = input().strip()
            while answer != 'Change number' and answer != 'Replace' and answer != 'Skip':
                print("Incorrect format")
                answer = input().strip()
            if answer == "Change number":
                information = input("Enter new 'phone number (11 digits)'\n").strip()
                while not check_phone(information):
                    print("Incorrect format")
                    information = input("Enter new 'phone number (11 digits)'\n").strip()
                phone_number = correct_phone_number(information)
            elif answer == "Replace":
                deleted_user = used_phone_numbers[phone_number]
                used_phone_numbers.pop(phone_number)
                phoneBook.pop(deleted_user)
            else:
                return
        phoneBook[(name, last_name)] = (date, phone_number)
        used_phone_numbers[phone_number] = (name, last_name)


def print_phone_book(_phoneBook):
    empty_string = "-" * 56
    print("-" * 56)
    print("%-10s | %-15s | %-10s | %s" % ("Name", "Last Name", "Birthday", "Phone Number"))
    print(empty_string)
    for ((name, last_name), (date, phone_number)) in _phoneBook.items():
        print("%-10s | %-15s | %-10s | %s" % (name, last_name, date, phone_number))
        print(empty_string)


def save():
    with open(filename, 'w') as openfile:
        for (name, last_name), (data, phone_number) in phoneBook.items():
            print(name, last_name, data, phone_number, sep=";", file=openfile)


def search_by_mask(_name='*', _last_name='*', _data='*', _phone_number='*'):
    result = {}
    if ((_name == '*' or check_name(_name)) and (_last_name == '*' or check_name(_last_name))
            and (_data == '*' or check_date(_data)) and (_phone_number == '*' or check_phone(_phone_number))):
        if _name != '*':
            _name = correct_name(_name)
        if _last_name != '*':
            _last_name = correct_name(_last_name)
        if _phone_number != '*':
            _phone_number = correct_phone_number(_phone_number)
        for (name, last_name), (data, phone_number) in phoneBook.items():
            if ((name == _name or _name == '*') and
                    (last_name == _last_name or _last_name == '*') and
                    (data == _data or _data == '*') and
                    (phone_number == _phone_number or _phone_number == '*')):
                result[(name, last_name)] = [data, phone_number]
        print_phone_book(result)


def change():
    information = input("You choose to change a record. To do this enter 'Name;Last name'\n").strip().split(';')
    if len(information) != 2:
        print("Incorrect format")
        return
    name, last_name = information
    if check_name(name) and check_name(last_name):
        name = correct_name(name)
        last_name = correct_name(last_name)
        if (name, last_name) not in phoneBook:
            print("There is no person '%s;%s' in the phone book" % (name, last_name))
            return
        data, phone_number = phoneBook[(name, last_name)]
        _name, _last_name, _data, _phone_number = name, last_name, data, phone_number
        answer = input("Enter 'Yes' if you want to change person's 'NAME' or enter 'No' to skip\n").strip()
        while answer != 'Yes' and answer != 'No':
            answer = input("Enter 'Yes' if you want to change person's 'NAME' or enter 'No' to skip\n").strip()
        if answer == 'Yes':
            _name = input("Enter new 'NAME'\n").strip()
            while not check_name(_name):
                _name = input("Enter new 'NAME'\n").strip()
            _name = correct_name(_name)
        answer = input("Enter 'Yes' if you want to change person's 'LAST NAME' or enter 'No' to skip\n").strip()
        while answer != 'Yes' and answer != 'No':
            answer = input("Enter 'Yes' if you want to change person's 'LAST NAME' or enter 'No' to skip\n").strip()
        if answer == 'Yes':
            _last_name = input("Enter new 'LAST NAME'\n").strip()
            while not check_name(_last_name):
                _last_name = input("Enter new 'LAST NAME'\n").strip()
            _last_name = correct_name(_last_name)
        answer = input("Enter 'Yes' if you want to change person's 'BIRTHDAY' or enter 'No' to skip\n").strip()
        while answer != 'Yes' and answer != 'No':
            answer = input("Enter 'Yes' if you want to change person's 'BIRTHDAY' or enter 'No' to skip\n").strip()
        if answer == 'Yes':
            _data = input("Enter new 'BIRTHDAY'\n").strip()
            while not check_date(_data):
                _data = input("Enter new 'BIRTHDAY'\n").strip()
        answer = input("Enter 'Yes' if you want to change person's 'PHONE NUMBER' or enter 'No' to skip\n").strip()
        while answer != 'Yes' and answer != 'No':
            answer = input("Enter 'Yes' if you want to change person's 'PHONE NUMBER' or enter 'No' to skip\n").strip()
        if answer == 'Yes':
            _phone_number = input("Enter new 'PHONE NUMBER'\n").strip()
            while not check_phone(_phone_number):
                _phone_number = input("Enter new 'PHONE NUMBER'\n").strip()
            _phone_number = correct_phone_number(_phone_number)
        conflicts = {}
        if (name, last_name) != (_name, _last_name):
            if (_name, _last_name) in phoneBook:
                conflicts[(_name, _last_name)] = phoneBook[(_name, _last_name)]
        if phone_number != _phone_number:
            if _phone_number in used_phone_numbers:
                user = used_phone_numbers[_phone_number]
                conflicts[user] = phoneBook[user]
        if len(conflicts) != 0:
            print("Change '%s;%s;%s;%s' --> '%s;%s;%s;%s' \nwas canceled because of the conflicts with these records:"
                  % (name, last_name, data, phone_number, _name, _last_name, _data, _phone_number))
            print_phone_book(conflicts)
            print("Resolve the conflicts and try again")
        else:
            used_phone_numbers.pop(phone_number)
            phoneBook.pop((name, last_name))
            used_phone_numbers[_phone_number] = (_name, _last_name)
            phoneBook[(_name, _last_name)] = (_data, _phone_number)


def age_of_person():
    information = input("You chose to get an age of the person. To do this enter 'Name;Last name'\n").strip().split(';')
    if len(information) != 2:
        print("Incorrect format")
        return
    name, last_name = information
    if check_name(name) and check_name(last_name):
        name = correct_name(name)
        last_name = correct_name(last_name)
        if (name, last_name) in phoneBook:
            now = datetime.datetime.now()
            now = datetime.date(*(map(int, str(now).split()[0].split('-'))))
            used_time = list(phoneBook[(name, last_name)][0].split('.'))
            birthday = datetime.date(int(used_time[2]), int(used_time[1]), int(used_time[0]))
            delta = str(now - birthday).split(',')[0].split()[0]
            print(int(delta)//365, "years old")
        else:
            print("There is no person '%s;%s' in the phone book" % (name, last_name))


def search_by_date():
    _day, _month = input("Enter DD.MM\n").strip().split('.')
    if str.isnumeric(_day) and str.isnumeric(_month):
        _day = int(_day)
        _month = int(_month)
        result = {}
        for (name, last_name), (data, phone_number) in phoneBook.items():
            birthday = data.split('.')
            day = int(birthday[0])
            month = int(birthday[1])
            if _day == day and month == _month:
                result[(name, last_name)] = (data, phone_number)
        print_phone_book(result)
    else:
        print("Incorrect format, enter phone number again")


def check_near(a: datetime.datetime, b: datetime.datetime):
    if a.month == b.month:
        if a.day <= b.day:
            return True
    elif a.month + 1 == b.month:
        if a.day >= b.day:
            return True
    elif a.month == 12 and b.month == 1:
        if a.day >= b.day:
            return True
    return False


def find_nearest_birthdays():
    result = {}
    now = datetime.datetime.now()
    add = datetime.timedelta(days=30)
    now = now + add
    for (name, last_name), (data, phone_number) in phoneBook.items():
        used_time = phoneBook[(name, last_name)][0].split('.')
        birthday = datetime.date(int(used_time[2]), int(used_time[1]), int(used_time[0]))
        if check_near(birthday, now):
            result[(name, last_name)] = (data, phone_number)
    print_phone_book(result)


def get_by_age():
    n = input("Enter age\n")
    while not str.isnumeric(n):
        print("Incorrect format")
        n = input("Enter age\n")
    n = int(n)
    less = {}
    equal = {}
    more = {}
    for (name, last_name), (data, phone_number) in phoneBook.items():
        now = datetime.datetime.now()
        now = datetime.date(*(map(int, str(now).split()[0].split('-'))))
        used_time = list(phoneBook[(name, last_name)][0].split('.'))
        birthday = datetime.date(int(used_time[2]), int(used_time[1]), int(used_time[0]))
        delta = str(now - birthday).split(',')[0].split()[0]
        delta = int(delta)//365
        if delta < n:
            less[(name, last_name)] = (data, phone_number)
        elif delta == n:
            equal[(name, last_name)] = (data, phone_number)
        else:
            more[(name, last_name)] = (data, phone_number)
    print("Persons younger than %s years old:" % n)
    print_phone_book(less)
    print("Persons %s years old:" % n)
    print_phone_book(equal)
    print("Persons elder than %s years old:" % n)
    print_phone_book(more)


def show_list_of_operations():
    print("List of operations, which can be used:")
    for operation, description in possible_operations.items():
        print(operation, '->', description)


if __name__ == '__main__':
    print("Hello, its a phone book realisation")
    start()
    show_list_of_operations()
    while True:
        print("(Note: name/last name starts from letter, phone number consists of 11 digits and starts from +7 or 8)")
        operation = input("Choose an operation\n").strip()
        if operation == "Add":
            get_entry_data()
        elif operation == "Change":
            change()
        elif operation == "Search":
            print("Its an advanced search. To find enter 'Name;Last name;DD.MM.YYYY;Phone number (11 digits)'.")
            print("If some fields are not important to you, then type '*' in their places")
            information = input().strip().split(';')
            search_by_mask(*information)
        elif operation == "Delete":
            delete_by_name_last_name()
        elif operation == "Delete by phone number":
            delete_by_phone_number()
        elif operation == "Age":
            age_of_person()
        elif operation == "Nearest birthdays":
            find_nearest_birthdays()
        elif operation == "Regarding age":
            get_by_age()
        elif operation == "Search by date":
            search_by_date()
        elif operation == "Print":
            print_phone_book(phoneBook)
        elif operation == "Save":
            save()
        elif operation == "Show operations":
            show_list_of_operations()
        elif operation == "Quit":
            save()
            break
        else:
            print("Operation '%s' is not found. Please, used 'Show operations' to see the list of possible operations"
                  % operation)
