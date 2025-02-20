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

def has_list(data):
    """
    Recursively find a list in nested data.
    """
    for key, value in data.items():
        if isinstance(value, (list, tuple)):
            return True
        elif isinstance(value, dict):
            if has_list(value):
                return True

def max_parents(data):
    return max(len(parents) for parents, data in nodes.visit(data['member_data']))

def interesting(data):
    count_max_parents = max_parents(data)
    return count_max_parents

def get_interesting_files(database):
    database = filter(has_interesting, database)
    database = sorted(database, reverse=True, key=interesting)
    return database
