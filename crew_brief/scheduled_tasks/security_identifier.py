import win32security

def get_sid_for_username(username):
    sid, domain, type = win32security.LookupAccountName(None, username)
    return win32security.ConvertSidToStringSid(sid)
