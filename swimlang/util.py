##################################################################################
# Utility functions
##################################################################################

def alpha(val):
    if val is None or val == '':
        return False
    for c in val:
        ordc = ord(c.lower())
        if ordc not in range(ord('a'), ord('z') + 1):
            return False
    return True


def numeric(val):
    if val is None or val == '':
        return False
    for c in val:
        ordc = ord(c)
        if ordc not in range(ord('0'), ord('9') + 1):
            return False
    return True


def alphanumeric(val):
    if val is None or val == '':
        return False
    for c in val:
        if not (alpha(c) or numeric(c)):
            return False
    return True


def valid_var(val):
    if val is None or val == '':
        return False
    if not alpha(val[0]) and val[0] != '_':
        return False
    for c in val:
        if not (alphanumeric(c) or c == '_'):
            return False
    return True


def isspace(val):
    if val is None:
        return False
    return val.isspace()
