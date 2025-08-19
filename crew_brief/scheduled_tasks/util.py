import datetime

def midnight(date=None):
    """
    Return date at midnight, defaulting to today.
    """
    if date is None:
        date = datetime.date.today()
    return datetime.datetime.combine(date, datetime.time())
