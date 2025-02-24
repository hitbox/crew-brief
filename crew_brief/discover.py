"""
Look for interesting data from the JSON files.
"""

from . import nodes

def has_interesting(data):
    """
    Has eventDetails in any userEvents and one of userEvents has a list.
    """
    if member_data := data['member_data']:
        for user_event in member_data['userEvents']:
            # Has truthy eventDetails
            if event_details := user_event.get('eventDetails'):
                # A list exists in the eventDetails.
                if has_list(event_details):
                    return True
    return None

def has_list(data):
    """
    Recursively find a list in nested data.
    """
    for value in data.values():
        if isinstance(value, (list, tuple)):
            return True
        if isinstance(value, dict):
            if has_list(value):
                return True
    return None

def max_parents(data):
    """
    Return the maximum number of parents in data, recursively.
    """
    return max(len(parents) for parents, data in nodes.visit(data['member_data']))

def get_interesting_files(database):
    """
    Filter and sort database for interesting data.
    """
    database = filter(has_interesting, database)
    database = sorted(database, reverse=True, key=max_parents)
    return database
