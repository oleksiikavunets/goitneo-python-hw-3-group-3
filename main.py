from address_book import address_book
from commands import (
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    show_upcoming_birthdays, bot_help
)


def main():
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args, input_error = parse_input(user_input)

        if input_error:
            print(input_error)
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            address_book.cache_data()
            break

        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args))
        elif command == "change":
            print(change_contact(args))
        elif command == "phone":
            print(show_phone(args))
        elif command == "all":
            print(show_all())
        elif command == "add-birthday":
            print(add_birthday(args))
        elif command == "show-birthday":
            print(show_birthday(args))
        elif command == "birthdays":
            print(show_upcoming_birthdays())
        elif command == 'help':
            print(bot_help())
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
