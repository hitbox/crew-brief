import calendar

def weekday_data(weekday):
    return {
        'number': weekday,
        'name': calendar.day_name[weekday],
        'abbr': calendar.day_abbr[weekday],
    }

def weekdays(cal=None):
    if cal is None:
        cal = Calendar(firstweekday=calendar.SUNDAY)
    return [weekday_data(weekday) for weekday in cal.iterweekdays()]

def date_data(year, month, date, today=None):
    data = {
        'date': date,
        'day': date.day,
        'is_same': date.year == year and date.month == month,
    }
    if today is not None:
        data['is_today'] = today == date
    return data

def expand_month(month, year=None, cal=None, today=None):
    """
    Return dict from month number.
    """
    data = {
        'number': month,
        'name': calendar.month_name[month],
        'abbr': calendar.month_abbr[month],
    }
    if today is not None:
        data['is_same'] = month == today.month
    if year is not None and cal is not None:
        data['days'] = [date_data(year, month, date, today=today) for date in cal.itermonthdates(year, month)]
    return data
