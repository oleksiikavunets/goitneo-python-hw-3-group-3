from address_book.fields import Name, Phone, Birthday


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone) if phone else None
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phone: {self.phone}, birthday: {self.birthday}"
