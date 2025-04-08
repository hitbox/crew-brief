import datetime

def abbr_month_int(string):
    """
    Convert abbreviated month name to integer.
    """
    return datetime.datetime.strptime(string, '%b').month
