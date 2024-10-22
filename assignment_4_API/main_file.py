import json
import requests


def check_book(book_name):
    result = requests.get(f'http://localhost:5000/book_availability?book_name={book_name}')
    data = result.json()
    if "error" in data:
        print(f"{data['error']}")
        return False
    return data["exists"]


def book_reservation(book_name, reserved_until, user_name):
    reservation = {
        "book_name": book_name,
        "reserved_until": reserved_until,
        "user_name": user_name,
    }
    response = requests.post(f'http://localhost:5000/reserve_book',
                             headers={'content-type': 'application/json'},
                             data=json.dumps(reservation))


def cancel_reservation(book_name, user_name):
    cancel = {
        "book_name": book_name,
        "user_name": user_name,
    }
    response = requests.post(f'http://localhost:5000/book_cancellation',
                             headers={'content-type': 'application/json'},
                             data=json.dumps(cancel))


def run():
    print('///////////////////////////////////')
    print('//           Welcome             //')
    print('//             To                //')
    print('//          Book Share           //')
    print('///////////////////////////////////')
    print()
    user_name = input("Enter the first_name, with only lowercase character \n")
    user_input = input("Enter the '1' for reserving the book or '2' for cancelling the book ")
    if user_input == '1':
        book_name = input("What is the name of the book, you are looking for? ")
        book_found = check_book(book_name)
        if book_found:
            reserve = input("Do you want to reserve the book? (Eg : yes or no) ")
            if reserve == "yes" or reserve == "y":
                reservation_date = input("Enter the date until which the book has to be reserved? (eg. %Y-%m-%d) ")
                book_reservation(book_name, reservation_date, user_name)
                print()
        else:
            print("Incorrect book name")
    elif user_input == '2':
        book_name = input("What is the name of the book, you want to cancel? ")
        cancellation = cancel_reservation(book_name, user_name)


if __name__ == '__main__':
    run()
