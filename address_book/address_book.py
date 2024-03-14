import os
import pathlib
import pickle
from collections import UserDict
from collections import defaultdict
from datetime import datetime, timedelta

_CACHE_DIR = pathlib.Path(__file__).parent.joinpath('.cache')

os.makedirs(_CACHE_DIR, exist_ok=True)


class AddressBook(UserDict):

    def __init__(self):
        super().__init__()
        self._load_cache_data()

    def cache_data(self):
        with open(_CACHE_DIR.joinpath("book.bin"), "wb") as file:
            pickle.dump(self, file)

    def _load_cache_data(self):
        cache_file = _CACHE_DIR.joinpath("book.bin")

        if cache_file.exists():
            with open(_CACHE_DIR.joinpath("book.bin"), "rb") as file:
                cache = pickle.load(file)
                self.data.update(cache)

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name not in self.data:
            raise LookupError(f'Record with name "{name}" was not found.')
        return self.data[name]

    def delete(self, name):
        if name not in self.data:
            raise LookupError(f'Record with name "{name}" was not found.')
        del self.data[name]

    def get_birthdays_per_week(self):
        results = defaultdict(list)
        today = datetime.today().date() + timedelta(days=1)
        records = self.data.values()

        for record in records:
            name = record.name.value
            birthday = record.birthday
            if not birthday:
                continue
            birthday = datetime.strptime(birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                if (dow := birthday_this_year.weekday()) >= 5:
                    birthday_this_year = birthday_this_year + timedelta(days=(0 - dow + 7) % 7)

                results[birthday_this_year.strftime('%A')].append(name)

        return '\n'.join(
            f'{dow}: ' + ', '.join(names) for dow, names in results.items()
        ) if results else 'No upcoming birthdays withing next 7 days.'


address_book = AddressBook()
