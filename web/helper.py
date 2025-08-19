import calendar

from flask import current_app

from crew_brief.calendar_data import weekdays

class Day:

    def __init__(self, date, today):
        self.date = date
        self.today = today
        self.day = date.day

    @property
    def is_same(self):
        return self.date.year == self.today.year and self.date.month == self.today.month

    @property
    def is_today(self):
        return self.date == self.today


class Month:

    def __init__(self, number, cal, today=None):
        self.number = number
        self.cal = cal
        self.today = today

        self.name = calendar.month_name[self.number]
        self.abbr = calendar.month_abbr[self.number]
        self._days = None

    @property
    def days(self):
        if self._days is None:
            self._days = []
            for date in self.cal.itermonthdates(self.today.year, self.today.month):
                self._days.append(Day(date, self.today))
        return self._days


class MonthZIPCount:

    def __init__(self, year, month, today, cal=None):
        self.year = year
        self.today = today
        if cal is None:
            cal = calendar.Calendar(firstweekday=get_firstweekday())
        self.cal = cal
        if isinstance(month, int):
            month = Month(month, self.cal, self.today)
        self.month = month


def get_firstweekday():
    """
    Get first weekday number from config or default to Sunday.
    """
    return current_app.config.get('firstweekday', calendar.SUNDAY)
