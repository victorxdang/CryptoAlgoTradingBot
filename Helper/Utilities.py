import time


"""
Description:
    This class will contain many useful helper/utility functions that can be used
    for a variety of tasks.
"""

dict_time_table = {
    'm' : {'m' : 1,     'h' : 1/60, 'd' : 1/1440, 'w' : 1/10080},
    'h' : {'m' : 60,    'h' : 1,    'd' : 1/24,   'w' : 1/168},
    'd' : {'m' : 1440,  'h' : 24,   'd' : 1,      'w' : 1/7},
    'w' : {'m' : 10080, 'h' : 168,  'd' : 7,      'w' : 1}
}


def convert_time_from_str(time: str, convert_to: str = 'm') -> float:
    """
    Description:
        Converts the time passed to this function to the time unit specified by
        convert_to

    Parameters:
        time : (required) the time as a string format (ex. '1h')
        convert_to : (optional) the time unit to convert it to (defaults to minutes, 'm')

        The following units are supported for both parameters (not case-sensitive):
        'm', 'h', 'd', 'w'

    Return:
        Returns the converted time as an integer or -1 if the conversion could not be
        done.
    """

    unit = time[-1].lower()
    convert_to = convert_to.lower()
    raw_time = float(time[:-1])

    value = dict_time_table.get(unit).get(convert_to)
    return raw_time * value if value is not None else -1

    
def generate_nonce():
    """
    Description:
        Generates a nonce to be used within the payload for POST requests. Or for other uses, doesn't
        necessarily have to be for POST requests.

    Return:
        Returns the generated nonce.
    """

    return int(1000 * time.time())


def list_to_string(list_from, delimiter: str = ','):
    """
    Description:
        Creates a string from a list of values seperated by the string specified in
        'delimiter'.

    Parameters:
        list_from : (required) a list of values, if an object passed to this parameter
        is not a list, then the object itself will be returned.
        delimiter : (optional) the character/string to use to seperate each element in the list
        (defaults to ',').

    Return:
        Returns the string of comma seperated values formed from the provided list, or
        the object itself if it wasn't a list.
    """

    if type(list_from) is list:
        return delimiter.join(map(str, list_from))
    else:
        return list_from