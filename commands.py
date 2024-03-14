from address_book import address_book, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return *func(*args, **kwargs), None
        except Exception:
            return None, None, 'Could not parse user input.\n' + bot_help()

    return inner


def bot_help(cmd=None):
    helps = {
        'add_contact': ' - `add` [name] [phone_number]    - add contact to address book, '
                       'phone number must consist of 10 digits',
        'change_contact': ' - `change` [name] [phone_number] - update phone number of existing contact, '
                          'phone number must consist of 10 digits',
        'show_phone': ' - `phone` [name]                 - show phone number of contact',
        'show_all': ' - `all`                          - show all contacts',
        'add_birthday': ' - `add-birthday` [name] [date]   - add birthday to existing contact, date format `DD.MM.YYYY`',
        'show_birthday': ' - `show-birthday` [name]         - show birthday of contact',
        'show_upcoming_birthdays': ' - `birthdays`                    - show upcoming birthdays within next 7 days',
        'help': ' - `help`                         - show available commands',
        '_': ' - `close`|`exit`                 - exit bot'
    }
    cmd_help = helps[cmd] if cmd else '\n'.join(helps.values())
    help_msg = f'\n\nCommands and Arguments:\n{cmd_help}\n'
    return help_msg


def command_exec(error_msg):
    def decorator(func):
        def inner(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                address_book.cache_data()
                return result
            except ValueError as e:
                return f'{error_msg}\nImproper arguments passed.\n{e}{bot_help(func.__name__)}'
            except Exception as e:
                return f'{error_msg}\n{e}{bot_help(func.__name__)}'

        return inner

    return decorator


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@command_exec('Could not add contact.')
def add_contact(args):
    name, phone = args
    record = Record(name, phone)
    address_book.add_record(record)
    return "Contact added."


@command_exec('Could not update contact`s phone number.')
def change_contact(args):
    name, phone = args
    record = address_book.find(name)
    record.add_phone(phone)
    return "Contact updated."


@command_exec('Could not show contact`s phone number.')
def show_phone(args):
    name, *_ = args
    return address_book.find(name).phone


@command_exec('Could not show all contacts.')
def show_all():
    contacts_msg = "\n".join(f"{name} - {record.phone}" for name, record in address_book.items())
    return contacts_msg or "Contacts empty."


@command_exec('Could not add birthday.')
def add_birthday(args):
    name, birthday = args
    record = address_book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@command_exec('Could not show contact`s birthday.')
def show_birthday(args):
    name, *_ = args
    result = address_book.find(name).birthday or f'Birthday of {name} not found.'
    return result


@command_exec('Could not show upcoming birthdays.')
def show_upcoming_birthdays():
    return address_book.get_birthdays_per_week()
