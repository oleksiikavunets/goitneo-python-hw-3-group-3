import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

        if not re.match(r'^\d{10}$', value):
            raise ValueError('Improper phone format. Must be 10 digits ')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

        if not re.match(r'^\d{2}.\d{2}.\d{4}$', value):
            raise ValueError('Improper Birthday format. Must be `DD.MM.YYYY`.')
