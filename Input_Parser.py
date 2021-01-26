"""
Static Functionfile

MODULE UNDER UNIT TEST

Written by Cole Anderson
"""
__author__ = "Cole Anderson"



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


def _parse_date(value: str) -> str or None:
    """
    Attempts to parse a string into a uniform string defining a date
    :param value: A string that may represent a legitimate date
    :return:
        If parse is successful:
            str: A uniform string defining the date represented by the input string, could possibly be the input string
                itself
        If parse is not successful:
            None
    """
    return value if len(value) == 10 else None


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
    if (input_length == 4 or input_length == 5) and value[:-3].isdigit() and int(value[:-3]) < 24 and \
            value[-3] == ':' and value[-2:].isdigit() and int(value[-2:]) < 60:
        return ("0" if input_length == 4 else "") + value
    return None



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
