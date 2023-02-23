"""
Static Functionfile

MODULE UNDER UNIT TEST

Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# IMPORTS
from datetime import datetime, timedelta


# ENUMS
class ENUM_Input_Type:  # see help print string for information on arg input types
    REGULAR = "REGULAR"
    OPTIONAL = "OPTIONAL"
    END = "END"
    OPTIONAL_END = "OPTIONAL_END"

class ENUM_Demanded_Value_Type:
    STR = "STR"
    UNSIGNED_INT = "UNSIGNED_INT"
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"


# PARAM CLASSES
class PARAM_Arg_Form:

    def __init__(self, input_type: ENUM_Input_Type, demanded_value_type: ENUM_Demanded_Value_Type):
        """
        :param input_type: an "ENUM_Input_Type" value defining a generic form for the input
        :param demanded_value_type: an "ENUM_Demanded_Value_Type" value identifying what data form the given string
                must be casted to in order to be legitimate
        """
        self.input_type = input_type
        self.demanded_value_type = demanded_value_type


# FUNCTIONS
def parse(raw_inputs: list, demanded_input_form: list) -> list or str:
    """
    Take distinct inputs from the user and attempt to parse them into a given form
    :param raw_inputs: [arg_1_input, ...].
        A list of what are determined as distinct inputs, with the exception that the final inputs may be part of an
            "end" input. All strings.
    :param demanded_input_form: [arg_1_form, ...]
        A list of specifications for the necessary form of each input, of type PARAM_arg_form.
        Consider that no mandatory (regular) args should come after the first optional one, and that only the final arg
            can be an 'end' arg.
        THIS FUNCTION WILL NOT CHECK THAT THE INPUTS ARE REASONABLE, AND WILL HAVE AN EXCEPTION OR UNUSABLE RETURN IF
            ENUM VALUES ARE NOT USED FOR THIS ARGUMENT
    :return:
        If parse is successful:
            list: A new list of parsed inputs, ready for operation
                form of parsed inputs:
                    in general:
                        a value of a form in accordance with the demanded_value_type
                    for an optional or optional_end arg with no input:
                        None
                    for an end or optional_end arg with an input requested as a string:
                        a string
                    for an end or optional_end arg with an input requested as a non-string:
                        a list of parsed values
        If parse is not successful:
            str: A message for the user
    """
    parsed_inputs = []
    index_iterator = -1  # iterator following the index in the 'demanded_input_form' list that the below loop is on
    for arg_form in demanded_input_form:
        index_iterator += 1

        input_type = arg_form.input_type
        demanded_value_type = arg_form.demanded_value_type

        # get the raw value
        try:
            raw_value = raw_inputs[index_iterator]
        except IndexError:
            raw_value = None

        # consider user entering no value or dot for no value
        if input_type == ENUM_Input_Type.REGULAR or input_type == ENUM_Input_Type.END:
            if raw_value is None:
                return "Command Failure: arg number " + str(index_iterator + 1) + " not found in command"
        elif input_type == ENUM_Input_Type.OPTIONAL or input_type == ENUM_Input_Type.OPTIONAL_END:
            if raw_value == '.':
                raw_value = None

        # try to parse the raw value
        if input_type == ENUM_Input_Type.REGULAR or input_type == ENUM_Input_Type.OPTIONAL:
            if raw_value is None:  # this means that this is an optional input
                parsed_value = None
            else:  # 'raw_value' is a real string
                if demanded_value_type == ENUM_Demanded_Value_Type.STR:
                    parsed_value = raw_value
                elif demanded_value_type == ENUM_Demanded_Value_Type.UNSIGNED_INT:
                    parsed_value = _parse_unsigned_int(raw_value)
                    if parsed_value is None:
                        return "Command Failure: arg number " + str(index_iterator + 1) + " could not be parsed to a" \
                                " non-negative int. Raw value was:\n" + raw_value
                elif demanded_value_type == ENUM_Demanded_Value_Type.DATE:
                    parsed_value = _parse_date(raw_value)
                    if parsed_value is None:
                        return "Command Failure: arg number " + str(index_iterator + 1) + " could not be parsed to a" \
                                  " date. Raw value was:\n" + raw_value
                elif demanded_value_type == ENUM_Demanded_Value_Type.TIME:
                    parsed_value = _parse_time(raw_value)
                    if parsed_value is None:
                        return "Command Failure: arg number " + str(index_iterator + 1) + " could not be parsed to a" \
                                  " time. Raw value was:\n" + raw_value
                elif demanded_value_type == ENUM_Demanded_Value_Type.DURATION:
                    parsed_value = _parse_duration(raw_value)
                    if parsed_value is None:
                        return "Command Failure: arg number " + str(index_iterator + 1) + " could not be parsed to a" \
                                  " duration. Raw value was:\n" + raw_value
            # noinspection PyUnboundLocalVariable
            parsed_inputs.append(parsed_value)
        elif input_type == ENUM_Input_Type.END or input_type == ENUM_Input_Type.OPTIONAL_END:
            if raw_value is None:  # this means that this is an optional input
                parsed_value = None
            else:  # 'raw_value' is a real string
                raw_end_values = raw_inputs[index_iterator:]  # this is an end arg so get all of the necessary raw values
                if demanded_value_type == ENUM_Demanded_Value_Type.STR:
                    parsed_value = " ".join(raw_end_values)
                elif demanded_value_type == ENUM_Demanded_Value_Type.UNSIGNED_INT:
                    parsed_value = []
                    for raw_end_value in raw_end_values:
                        new_parsed_value = _parse_unsigned_int(raw_end_value)
                        if new_parsed_value is None:
                            return "Command Failure: not all elements of end arg could be parsed to a non-negative int. " \
                                   "Offending raw value was:\n" + raw_end_value
                        parsed_value.append(new_parsed_value)
                elif demanded_value_type == ENUM_Demanded_Value_Type.DATE:
                    parsed_value = []
                    for raw_end_value in raw_end_values:
                        new_parsed_value = _parse_date(raw_end_value)
                        if new_parsed_value is None:
                            return "Command Failure: not all elements of end arg could be parsed to a date. " \
                                   "Offending raw value was:\n" + raw_end_value
                        parsed_value.append(new_parsed_value)
                elif demanded_value_type == ENUM_Demanded_Value_Type.TIME:
                    parsed_value = []
                    for raw_end_value in raw_end_values:
                        new_parsed_value = _parse_time(raw_end_value)
                        if new_parsed_value is None:
                            return "Command Failure: not all elements of end arg could be parsed to a time. " \
                                   "Offending raw value was:\n" + raw_end_value
                        parsed_value.append(new_parsed_value)
                elif demanded_value_type == ENUM_Demanded_Value_Type.DURATION:
                    parsed_value = []
                    for raw_end_value in raw_end_values:
                        new_parsed_value = _parse_duration(raw_end_value)
                        if new_parsed_value is None:
                            return "Command Failure: not all elements of end arg could be parsed to a duration. " \
                                   "Offending raw value was:\n" + raw_end_value
                        parsed_value.append(new_parsed_value)
            # noinspection PyUnboundLocalVariable
            parsed_inputs.append(parsed_value)
            # here is the effective end of this function if there is in fact an end arg
    return parsed_inputs



# PRIVATE FUNCTIONS
def _parse_unsigned_int(value: str) -> int or None:
    """
    Attempts to parse a string into an positive int and return the int
    :param value: a string that may be a positive int
    :return:
        If parse is successful:
            int: The positive int value of the input string
        If parse is not successful:
            None
    """
    return int(value) if value.isdigit() else None


_parse_date_MINIMUM_DAY_NAMES_LOWERCASE = ["m", "tu", "w", "th", "f", "sa", "su"]  # from Monday to Sunday
_parse_date_SHORT_DAY_NAMES_LOWERCASE = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]  # from Monday to Sunday
_parse_date_SHORT_DAY_NAMES_PRINT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]  # from Monday to Sunday,
        # with capital first letter
_parse_date_YEAR_MONTH_DAY_FORMAT_STR = "%Y-%m-%d"  # str for strftime for formatting the year month and day together
def _parse_date(value: str, today_datetime: datetime=None) -> str or None:
    # noinspection SpellCheckingInspection
    """
    Attempts to parse a string into a uniform string defining a date
    :param value: A string that can be parsed to a legitimate date, expecting lowercase
            Acceptable Format Examples ('_' for any non-digit char, ',' delimiting different examples):
                2000_12_25,2000_1_25,2000_12_5,2000_1_5
                12_25,1_25,12_5,1_5 (the first upcoming 12-25, not today if it is 12-25)
                25,5 (the first upcoming 25th, not today if it is the 25th)

                "today" (today)

                "nnn","n" (tomorrow's tomorrow's tomorrow) (one 'n' per tomorrow as many as you want)
                "nnn25","n5" (next next next 25th after the first upcoming 25th) (one 'n' per next as many as you want)
                "w","tu","th" (this coming Wednesday)
                "wed","tue","thu" (this coming Wednesday)
                "nnnw","ntu","nth" (one 'n' per next as many as you want)
                "nnnwed","ntue","nthu" (one 'n' per next as many as you want)
    :param today_datetime: if given, will be used as datetime instance for function to use for relative date string
            parsing in place of datetime.today() call in function
    :return:
        If parse is successful:
            str: A uniform string defining the date represented by the input string
        If parse is not successful:
            None
    """
    today_datetime = datetime.today() if today_datetime is None else today_datetime

    # try to parse the input to a datetime
    datetime_of_parsed_date = None
    if value[:1].isdigit():

        # split date str by non digits
        in_terms = []  # list of int inputs by end of this block
        this_term_chars = []
        all_terms_are_numbers = False
        for char in value:
            if char.isdigit():
                this_term_chars.append(char)
            else:
                new_term_str = ''.join(this_term_chars)
                if not new_term_str.isdigit():
                    break
                in_terms.append(int(new_term_str))
                this_term_chars = []
        else:
            new_term_str = ''.join(this_term_chars)
            if new_term_str.isdigit():
                in_terms.append(int(new_term_str))
                all_terms_are_numbers = True

        if all_terms_are_numbers and len(in_terms) < 4:  # 0 or negative value impossible

            # extract values from in_terms
            year = month = None
            if len(in_terms) == 3:  # 2000_12_25
                year, month, day = in_terms
            if len(in_terms) == 2:  # 12_25
                month, day = in_terms
            if len(in_terms) == 1:  # 25
                day = in_terms[0]

            # check given values
            # noinspection PyUnboundLocalVariable
            if not ((year is not None and (year < 1 or year > 9999)) or
                    (month is not None and (month < 1 or month > 12)) or
                    (day < 1)):
                # here day may still be higher than is legitimate, this depends in part on the month and year

                # fill in Nones
                if month is None:
                    month = today_datetime.month
                    if today_datetime.day >= day:
                        month += 1
                        if month == 13:
                            month = 1
                if year is None:
                    year = today_datetime.year
                    if today_datetime.month > month or (today_datetime.month == month and today_datetime.day >= day):
                        year += 1

                # make sure day value is not too high
                tmp = datetime(year=year, month=month, day=28) + timedelta(days=4)
                if day <= (tmp - timedelta(days=tmp.day)).day:  # if the day value we have is no greater than the
                        # highest possible day value for the given month in the given year
                    datetime_of_parsed_date = datetime(year=year, month=month, day=day)
    elif value == "today":
        datetime_of_parsed_date = today_datetime
    elif value:

        # count number of 'n' chars at beginning of value and get the part of value after the 'n's
        n_count = 0
        for char in value:
            if char != 'n':
                break
            n_count += 1
        term = value[n_count:]

        # noinspection SpellCheckingInspection
        if not term:  # in: "nnn", here: ""
            datetime_of_parsed_date = today_datetime + timedelta(days=n_count)
        elif term.isdigit():  # in: "nnn25", here: "25"
            day = int(term)
            if day > 0:

                # figure year and month
                year = today_datetime.year
                month = today_datetime.month
                if today_datetime.day >= day:
                    month += 1
                month += n_count
                year += int((month - 1) / 12)
                month = ((month - 1) % 12) + 1

                # make sure day value is not too high
                tmp = datetime(year=year, month=month, day=28) + timedelta(days=4)
                if day <= (tmp - timedelta(days=tmp.day)).day:  # if the day value we have is no greater than the
                        # highest possible day value for the given month in the given year
                    datetime_of_parsed_date = datetime(year=year, month=month, day=day)
        else:  # in: "nnnw" or "nnnwed", here: "w" or "wed"

            # get day of week
            day_of_week = None  # 0 to 6, from Monday to Sunday if gets populated, else None
            if term in _parse_date_MINIMUM_DAY_NAMES_LOWERCASE:
                day_of_week = _parse_date_MINIMUM_DAY_NAMES_LOWERCASE.index(term)
            elif term in _parse_date_SHORT_DAY_NAMES_LOWERCASE:
                day_of_week = _parse_date_SHORT_DAY_NAMES_LOWERCASE.index(term)

            if day_of_week is not None:

                # calculate the datetime
                days_to_first_correct_weekday = day_of_week - today_datetime.weekday()
                if days_to_first_correct_weekday <= 0:
                    days_to_first_correct_weekday += 7
                datetime_of_parsed_date = today_datetime + timedelta(days=days_to_first_correct_weekday + (n_count * 7))

    return None if datetime_of_parsed_date is None else \
            datetime_of_parsed_date.strftime(_parse_date_YEAR_MONTH_DAY_FORMAT_STR) + " " + \
            _parse_date_SHORT_DAY_NAMES_PRINT[datetime_of_parsed_date.weekday()]


def _parse_time(value: str) -> str or None:
    """
    Attempts to parse a string into a uniform string defining a time
    :param value: A string that may represent a legitimate time
    :return:
        If parse is successful:
            str: A 5 digit character string like 'HH:MM', could possibly be the input string itself
        If parse is not successful:
            None
    """
    input_length = len(value)
    if (input_length == 1 or input_length == 2) and value.isdigit() and int(value) < 24:
        return ("0" if input_length == 1 else "") + value + ":00"
    elif (input_length == 4 or input_length == 5) and value[:-3].isdigit() and int(value[:-3]) < 24 and \
            value[-3] == ':' and value[-2:].isdigit() and int(value[-2:]) < 60:
        return ("0" if input_length == 4 else "") + value
    return None


def _parse_duration(value: str) -> int or None:
    """
    Attempts to parse a string into a duration
    :param value:
        Acceptable Formats:
                :00, :125, :45, 3:0, 3:, 3:45, 123:1250 (a non-negative integer or blank for hours
                        followed by a ':' char, followed by a non-negative integer or blank for
                        minutes)

                0, 5, 05, 40, 60, 100, 1365 (a non-negative integer taken as a number of hours)
                0m, 45m, 75M (a non-negative integer followed by an 'm' or 'M' char)
                0h, 2H, 5h (a non-negative integer followed by an 'h' or 'H' char)

                0h00, 0123h1215, 2H30 (two non-negative integers for hours and minutes
                        respectively, with an 'h' or 'H' char delimiting)
                0h00M, 0123h1215m, 2H30m (two non-negative integers for hours and minutes
                        respectively, with an 'h' or 'H' char delimiting and an 'm' or 'M' char
                        punctuating)
    :return:
        If parse is successful:
            int: the number of minutes
        If parse is not successful:
            None
    """
    value = value.lower()
    if ':' in value:
        terms = value.split(':')
        if len(terms) == 2:  # cannot have fewer than 2 if there is minimum one ':' char in value
            hours, minutes = terms

            # replace blanks
            hours = hours if hours else "0"
            minutes = minutes if minutes else "0"

            if hours.isdigit() and minutes.isdigit():
                return int(hours) * 60 + int(minutes)
    elif value.isdigit():
        return int(value) * 60
    elif value[:-1].isdigit():
        if value[-1] == 'm':
            return int(value[:-1])
        elif value[-1] == 'h':
            return int(value[:-1]) * 60
    elif 'h' in value:
        terms = value.split('h')
        if len(terms) == 2:  # cannot have fewer than 2 if there is minimum one 'h' char in
                # lowercased value
            hours, minutes = terms

            # remove trailing 'm' if it exists
            if minutes and minutes[-1] == 'm':
                minutes = minutes[:-1]

            if hours.isdigit() and minutes.isdigit():
                return int(hours) * 60 + int(minutes)
    return None
