"""
Contains helper functions for the gas_app app
"""
def cap_firsts(given_string):
    """
    Helper function. Puts strings in proper case, while
    preserving given uppercase letters.
    """
    new_str = ""
    for i in range(len(given_string)):
        if given_string[i].isspace():
            new_str += given_string[i]
        elif i == 0 or given_string[i-1].isspace():
            new_str += given_string[i].upper()
        else:
            new_str += given_string[i]
    return new_str
