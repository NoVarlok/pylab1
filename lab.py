import time
from datetime import timedelta
import sys
phoneBook = {}
filename = None
used_phone_numbers = {}
possible_operations = {"Add": "Add a new record to the phohebook",
                        "Change": "Change a record in the phonebook",
                        "Search": "Search for an record in the phonebook",
                        "Delete": "Delete a record",
                        "Age": "Get an age of the person", "Quit": "Exit from the program",
                        "Print": "Print content of the phonebook into console",
                        "Save": "Save content of the phonebook into the source file",
                        "Show operations": "Shows list of possible operations"}


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
            filename = input("\n").strip()
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
    if not str.isalpha(name[0]):
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
    if str.isnumeric(phone_number) and len(phone_number) == 11:
        return True
    print("Incorrect_name 'phone number' format")
    return False


def correct_name(name):
    return str.upper(name[0])+name[1:]


def get_entry_date():
    print("You chose to add a new record. To do this enter 'Name;Surname;DD.MM.YYYY;Phone number (11 digits)'")
    information = input(">>> ").strip()
    add_to_the_phone_book(information)


def delete_by_name_last_name():
    print("You chose to delete a record by name + last name. To do this enter 'Name;Surname")
    information = input(">>> ").strip()
    if len(information) != 2:
        print("Wrong format")
        return
    name, last_name, date, phone_number = information
    if check_name(name) and check_name(last_name):
        name = correct_name(name)
        last_name = correct_name(last_name)
        if (name, last_name) in phoneBook:
            used_phone_numbers.pop(phoneBook[(name, last_name)][1])
            phoneBook.pop((name, last_name))
        else:
            print("There is no such person in the phone book")


def add_to_the_phone_book(information):
    information = information.split(";")
    if len(information) != 4:
        print("Wrong format")
        return
    name, last_name, date, phone_number = information
    if check_name(name) and check_name(last_name) and check_date(date) and check_phone(phone_number):
        name = correct_name(name)
        last_name = correct_name(last_name)
        if phone_number in used_phone_numbers:
            print("Phone Number %s is already used in the record\n%s;%s;%s;%s" %
                  (phone_number, name, last_name, date, phone_number))
            print("Do you want to replace it by new record?")
            while 1:
                answer = input("Enter 'Yes' if you want to rewrite the record or enter 'No' to skip\n").strip()
                if answer == "Yes":
                    break
                elif answer == "No":
                    return
        if (name, last_name) in phoneBook:
            print("Record %s;%s;%s;%s is already in the phonebook" % (name, last_name, date, phone_number))
            while 1:
                answer = input("Enter 'Yes' if you want to rewrite the record or enter 'No' to skip\n").strip()
                if answer == "Yes":
                    phoneBook[(name, last_name)] = [date, phone_number]
                    phone_number[phone_number] = (name, last_name)
                    break
                elif answer == "No":
                    break
        else:
            phoneBook[(name, last_name)] = [date, phone_number]


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


def search_by_mask(_name, _last_name, _data, _phone_number):
    result = {}
    if ((check_name(_name) or _name == '*') and (check_name(_last_name) or _last_name == '*')
            and (check_date(_data) or _data == '*') and (check_phone(_phone_number) or _phone_number == '*')):
        for (name, last_name), (data, phone_number) in phoneBook:
            if ((name == _name or _name == '*') and
                    (last_name == _last_name or _last_name == '*') and
                    (data == _data or _data == '*') and
                    (phone_number == _phone_number or _phone_number == '*')):
                result[(name, data)] = [data, phone_number]
        print_phone_book(result)


def change():
    information = input("You chose to change a record. To do this enter 'Name;Surname'\n").strip().split()
    if len(information) != 2:
        print("Wrong format")
        return
    name, last_name = information
    if check_name(name) and check_name(last_name):
        correct_name(name)
        correct_name(last_name)
        data, phone_number = phoneBook[(name, last_name)]
        _name, _last_name, _data, _phone_number = name, last_name, data, phone_number
        answer = input("Enter 'Yes' if you want to change person's 'NAME' or enter 'No' to skip\n").strip()
        while answer != 'Yes' and answer != 'No':
            answer = input("Enter 'Yes' if you want to change person's 'NAME' or enter 'No' to skip\n").strip()
        if answer == 'Yes':
            _name = input("Enter new 'NAME'\n").strip()
            while not check_name(_name):
                _name = input("Enter new 'NAME'\n").strip()
            correct_name(_name)
        answer = input("Enter 'Yes' if you want to change person's 'LAST NAME' or enter 'No' to skip\n").strip()
        while answer != 'Yes' and answer != 'No':
            answer = input("Enter 'Yes' if you want to change person's 'LAST NAME' or enter 'No' to skip\n").strip()
        if answer == 'Yes':
            _last_name = input("Enter new 'LAST NAME'\n").strip()
            while not check_name(_last_name):
                _last_name = input("Enter new 'LAST NAME'\n").strip()
            correct_name(_last_name)
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
            _data = input("Enter new 'PHONE NUMBER'\n").strip()
            while not check_phone(_data):
                _data = input("Enter new 'PHONE NUMBER'\n").strip()
        used_phone_numbers.pop(phone_number)
        phoneBook.pop((name, last_name))
        used_phone_numbers[_phone_number] = (_name, _last_name)
        phoneBook[(_name, _last_name)] = (_data, _phone_number)


def age_of_person():
    information = input("You chose to get an age of the person. To do this enter 'Name;Surname'\n").strip().split()
    if len(information) != 2:
        print("Wrong format")
        return
    name, last_name = information
    if check_name(name) and check_name(last_name):
        correct_name(name)
        correct_name(last_name)
        now = timedelta(time.localtime(0))
        used_time = phoneBook[(name, last_name)][1]
        used_time = time.strptime(used_time, '%d.%m.%Y')
        delta = used_time - now
        print(delta)


def show_list_of_operations():
    print("List of operations, which can be used")
    for operation, description in possible_operations.items():
        print(operation, '->', description)


if __name__ == '__main__':
    print("Hello, its a phone book realisation")
    start()
    show_list_of_operations()
    while True:
        operation = input("Choose an operation\n").strip()
        if operation == "Add":
            get_entry_date()
        elif operation == "Change":
            change()
        elif operation == "Search":
            search_by_mask()
        elif operation == "Delete":
            delete_by_name_last_name()
        elif operation == "Age":
            age_of_person()
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
            print("Operation %s is not found. Please, used 'Show operations' to see the list of possible operations"
                  % operation)

