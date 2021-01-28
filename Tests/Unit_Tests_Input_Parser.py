"""
Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# IMPORTS
import unittest

from datetime import datetime
from string import ascii_lowercase

import Input_Parser as Module
ENUM_Input_Type = Module.ENUM_Input_Type
ENUM_Demanded_Value_Type = Module.ENUM_Demanded_Value_Type
PARAM_Arg_Form = Module.PARAM_Arg_Form



# TEST CASES
class Test_Parse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._incorrect_test_case_assumptions_message = None  # set to a string if any of the below test case values are
                # not legitimate

        cls.example_raw_inputs = {ENUM_Demanded_Value_Type.STR          : "foobar",
                                  ENUM_Demanded_Value_Type.UNSIGNED_INT : "12",
                                  ENUM_Demanded_Value_Type.DATE         : "2020-09-30",
                                  ENUM_Demanded_Value_Type.TIME         : "13:59"}
        if (Module._parse_unsigned_int(cls.example_raw_inputs[ENUM_Demanded_Value_Type.UNSIGNED_INT]) is None) or \
                (Module._parse_date(cls.example_raw_inputs[ENUM_Demanded_Value_Type.DATE]) is None) or \
                (Module._parse_time(cls.example_raw_inputs[ENUM_Demanded_Value_Type.TIME]) is None):
            cls._incorrect_test_case_assumptions_message = \
                    "TEST CASE ASSUMPTIONS FAILURE: cls.example_raw_inputs does not pass parsing"

        cls.example_input_legitimate_only_as_a_string = "This string cannot be parsed except to a string"
        if (Module._parse_unsigned_int(cls.example_input_legitimate_only_as_a_string) is not None) or \
                (Module._parse_date(cls.example_input_legitimate_only_as_a_string) is not None) or \
                (Module._parse_time(cls.example_input_legitimate_only_as_a_string) is not None):
            cls._incorrect_test_case_assumptions_message = \
                    "TEST CASE ASSUMPTIONS FAILURE: cls.example_input_legitimate_only_as_a_string passes some parsing"


    def setUp(self):
        self.failIf(self._incorrect_test_case_assumptions_message is not None,
                self._incorrect_test_case_assumptions_message)  # make sure that the test assumptions are correct
                # before running any tests, should not need to be run before every test but this is to ensure that it
                # is checked before any test is run so that all tests can be failed


    def test_success_regular_args_all_demanded_value_types(self):
        """
        All args are regular and legitimate
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               self.example_raw_inputs[ENUM_Demanded_Value_Type.UNSIGNED_INT],
                               self.example_raw_inputs[ENUM_Demanded_Value_Type.DATE],
                               self.example_raw_inputs[ENUM_Demanded_Value_Type.TIME]]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.DATE),
                               PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.TIME)]
        expected_output     = [raw_inputs[0],
                               Module._parse_unsigned_int(raw_inputs[1]),
                               Module._parse_date(raw_inputs[2]),
                               Module._parse_time(raw_inputs[3])]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_regular_args_unsigned_int(self):
        """
        Single arg is not a legitimate unsigned int
        """
        raw_inputs          = [self.example_input_legitimate_only_as_a_string]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.UNSIGNED_INT)]
        self.assertIsNone(Module._parse_unsigned_int(raw_inputs[0]), "\nParse function " +
                Module._parse_unsigned_int.__name__ + " passed an input unexpectedly.\nInput: " + raw_inputs[0])

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_regular_args_date(self):
        """
        Single arg is not a legitimate date
        """
        raw_inputs          = [self.example_input_legitimate_only_as_a_string]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.DATE)]
        self.assertIsNone(Module._parse_date(raw_inputs[0]), "\nParse function " +
                Module._parse_date.__name__ + " passed an input unexpectedly.\nInput: " + raw_inputs[0])

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_regular_args_time(self):
        """
        Single arg is not a legitimate time
        """
        raw_inputs          = [self.example_input_legitimate_only_as_a_string]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.TIME)]
        self.assertIsNone(Module._parse_time(raw_inputs[0]), "\nParse function " +
                Module._parse_time.__name__ + " passed an input unexpectedly.\nInput: " + raw_inputs[0])

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))

    def test_success_optional_args_all_demanded_value_types(self):
        """
        All args are optional and legitimate
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               self.example_raw_inputs[ENUM_Demanded_Value_Type.UNSIGNED_INT],
                               self.example_raw_inputs[ENUM_Demanded_Value_Type.DATE],
                               self.example_raw_inputs[ENUM_Demanded_Value_Type.TIME]]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.DATE),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.TIME)]
        expected_output     = [raw_inputs[0],
                               Module._parse_unsigned_int(raw_inputs[1]),
                               Module._parse_date(raw_inputs[2]),
                               Module._parse_time(raw_inputs[3])]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_optional_args_unsigned_int(self):
        """
        Single arg is not a legitimate unsigned int
        """
        raw_inputs          = [self.example_input_legitimate_only_as_a_string]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.UNSIGNED_INT)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_optional_args_date(self):
        """
        Single arg is not a legitimate date
        """
        raw_inputs          = [self.example_input_legitimate_only_as_a_string]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.DATE)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_optional_args_time(self):
        """
        Single arg is not a legitimate time
        """
        raw_inputs          = [self.example_input_legitimate_only_as_a_string]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.TIME)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_args_dots(self):
        """
        All args are optional and given as dots
        """
        raw_inputs          = [".", "."]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR)]
        expected_output     = [None, None]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_args_dot_and_nothing(self):
        """
        All args are optional, one is given as dot and other as nothing
        """
        raw_inputs          = ["."]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR)]
        expected_output     = [None, None]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_args_nothing(self):
        """
        All args are optional and given as nothing
        """
        raw_inputs          = []
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL, ENUM_Demanded_Value_Type.STR)]
        expected_output     = [None, None]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_end_arg_with_string_demanded(self):
        """
        First arg is regular and second is end with a string demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "foo", "bar", "ham"]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.STR)]
        expected_output     = [raw_inputs[0],
                               " ".join(raw_inputs[1:])]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_end_arg_with_int_demanded(self):
        """
        First arg is regular and second is end with an int demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "1", "3", "49"]
        _msg_generic = "\nParse function " + Module._parse_unsigned_int.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.UNSIGNED_INT)]
        expected_output     = [raw_inputs[0],
                               [Module._parse_unsigned_int(el) for el in raw_inputs[1:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_end_arg_with_date_demanded(self):
        """
        First arg is regular and second is end with a date demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "2020-09-30", "2020-09-28", "2020-09-29"]
        _msg_generic = "\nParse function " + Module._parse_date.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_date(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_date(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_date(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.DATE)]
        expected_output     = [raw_inputs[0],
                               [Module._parse_date(el) for el in raw_inputs[1:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_end_arg_with_time_demanded(self):
        """
        First arg is regular and second is end with a time demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "13:00", "13:01", "13:02"]
        _msg_generic = "\nParse function " + Module._parse_time.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_time(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_time(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_time(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.TIME)]
        expected_output     = [raw_inputs[0],
                               [Module._parse_time(el) for el in raw_inputs[1:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_end_arg_with_int_demanded(self):
        """
        First arg is regular and second is end with an int demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "1", self.example_input_legitimate_only_as_a_string, "49"]
        _msg_generic = "\nParse function " + Module._parse_unsigned_int.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.UNSIGNED_INT)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_end_arg_with_date_demanded(self):
        """
        First arg is regular and second is end with a date demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "2020-09-30", self.example_input_legitimate_only_as_a_string, "2020-09-29"]
        _msg_generic = "\nParse function " + Module._parse_date.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_date(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_date(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.DATE)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_end_arg_with_time_demanded(self):
        """
        First arg is regular and second is end with a time demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "13:00", self.example_input_legitimate_only_as_a_string, "13:02"]
        _msg_generic = "\nParse function " + Module._parse_time.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_time(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_time(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR, ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.END,     ENUM_Demanded_Value_Type.TIME)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_end_arg_with_string_demanded(self):
        """
        First arg is regular and second is optional end with a string demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "foo", "bar", "ham"]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.STR)]
        expected_output     = [raw_inputs[0],
                               " ".join(raw_inputs[1:])]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_end_arg_with_int_demanded(self):
        """
        First arg is regular and second is optional end with an int demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "1", "3", "49"]
        _msg_generic = "\nParse function " + Module._parse_unsigned_int.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.UNSIGNED_INT)]
        expected_output     = [raw_inputs[0],
                               [Module._parse_unsigned_int(el) for el in raw_inputs[1:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_end_arg_with_date_demanded(self):
        """
        First arg is regular and second is optional end with a date demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "2020-09-30", "2020-09-28", "2020-09-29"]
        _msg_generic = "\nParse function " + Module._parse_date.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_date(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_date(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_date(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.DATE)]
        expected_output     = [raw_inputs[0],
                               [Module._parse_date(el) for el in raw_inputs[1:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_end_arg_with_time_demanded(self):
        """
        First arg is regular and second is optional end with a time demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "13:00", "13:01", "13:02"]
        _msg_generic = "\nParse function " + Module._parse_time.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_time(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_time(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_time(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.TIME)]
        expected_output     = [raw_inputs[0],
                               [Module._parse_time(el) for el in raw_inputs[1:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_optional_end_arg_with_int_demanded(self):
        """
        First arg is regular and second is optional end with an int demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "1", self.example_input_legitimate_only_as_a_string, "49"]
        _msg_generic = "\nParse function " + Module._parse_unsigned_int.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.UNSIGNED_INT)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_optional_end_arg_with_date_demanded(self):
        """
        First arg is regular and second is optional end with a date demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "2020-09-30", self.example_input_legitimate_only_as_a_string, "2020-09-29"]
        _msg_generic = "\nParse function " + Module._parse_date.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_date(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_date(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.DATE)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_failure_optional_end_arg_with_time_demanded(self):
        """
        First arg is regular and second is optional end with a time demanded
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               "13:00", self.example_input_legitimate_only_as_a_string, "13:02"]
        _msg_generic = "\nParse function " + Module._parse_time.__name__ + \
                " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_time(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_time(raw_inputs[3]), _msg_generic + raw_inputs[3])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.TIME)]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertIsInstance(output, str, "\nParse should have returned a string error message.\nraw_inputs: " +
                str(raw_inputs) + "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_end_arg_dot(self):
        """
        First arg is regular and second is optional end given as dot
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR],
                               ".", "foo", "bar"]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.STR)]
        expected_output     = [raw_inputs[0],
                               None]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                         "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_optional_end_arg_nothing(self):
        """
        First arg is regular and second is optional end given as nothing
        """
        raw_inputs          = [self.example_raw_inputs[ENUM_Demanded_Value_Type.STR]]
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.STR),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END, ENUM_Demanded_Value_Type.STR)]
        expected_output     = [raw_inputs[0],
                               None]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                         "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_all_together_except_optional_end(self):
        """
        All input types (except optional_end) and all demanded value types
        """
        raw_inputs          = ["11",
                               "12",
                               "13",
                               "14",
                               "110", "111", "112"]
        _msg_generic = "\nParse function " + Module._parse_unsigned_int.__name__ + \
                       " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[0]), _msg_generic + raw_inputs[0])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[3]), _msg_generic + raw_inputs[3])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[4]), _msg_generic + raw_inputs[4])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[5]), _msg_generic + raw_inputs[5])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[6]), _msg_generic + raw_inputs[6])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.END,      ENUM_Demanded_Value_Type.UNSIGNED_INT)]
        expected_output     = [Module._parse_unsigned_int(raw_inputs[0]),
                               Module._parse_unsigned_int(raw_inputs[1]),
                               Module._parse_unsigned_int(raw_inputs[2]),
                               Module._parse_unsigned_int(raw_inputs[3]),
                               [Module._parse_unsigned_int(el) for el in raw_inputs[4:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                         "\ndemanded_input_form: " + str(demanded_input_form))


    def test_success_all_together_except_end(self):
        """
        All input types (except end) and all demanded value types
        """
        raw_inputs          = ["11",
                               "12",
                               "13",
                               "14",
                               "110", "111", "112"]
        _msg_generic = "\nParse function " + Module._parse_unsigned_int.__name__ + \
                       " failed to parse an input unexpectedly.\nInput: "
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[0]), _msg_generic + raw_inputs[0])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[1]), _msg_generic + raw_inputs[1])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[2]), _msg_generic + raw_inputs[2])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[3]), _msg_generic + raw_inputs[3])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[4]), _msg_generic + raw_inputs[4])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[5]), _msg_generic + raw_inputs[5])
        self.assertIsNotNone(Module._parse_unsigned_int(raw_inputs[6]), _msg_generic + raw_inputs[6])
        demanded_input_form = [PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.REGULAR,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL,      ENUM_Demanded_Value_Type.UNSIGNED_INT),
                               PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL_END,      ENUM_Demanded_Value_Type.UNSIGNED_INT)]
        expected_output     = [Module._parse_unsigned_int(raw_inputs[0]),
                               Module._parse_unsigned_int(raw_inputs[1]),
                               Module._parse_unsigned_int(raw_inputs[2]),
                               Module._parse_unsigned_int(raw_inputs[3]),
                               [Module._parse_unsigned_int(el) for el in raw_inputs[4:]]]

        output = Module.parse(raw_inputs, demanded_input_form)
        self.assertEqual(expected_output, output, "\nParse output incorrect.\nraw_inputs: " + str(raw_inputs) +
                         "\ndemanded_input_form: " + str(demanded_input_form))


class Test__Parse_Unsigned_Int(unittest.TestCase):

    def test_failure_empty_input(self):
        self.assertIsNone(Module._parse_unsigned_int(""))


    def test_success(self):
        self.assertEqual(42, Module._parse_unsigned_int("42"))


    def test_success_zero(self):
        self.assertEqual(0, Module._parse_unsigned_int("0"))


    def test_failure_bad_number(self):
        self.assertIsNone(Module._parse_unsigned_int("-42"))
        self.assertIsNone(Module._parse_unsigned_int("42.5"))


    def test_failure_non_number(self):
        self.assertIsNone(Module._parse_unsigned_int("foobar"))


class Test__Parse_Date(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.datetime_2020_11_09 = datetime(year=2020, month=11, day=9)  # a Monday
        cls.datetime_2020_12_28 = datetime(year=2020, month=12, day=28)  # a Monday
        cls.datetime_2021_01_04 = datetime(year=2021, month=1, day=4)  # a Monday
        cls.datetime_2021_01_06 = datetime(year=2021, month=1, day=6)  # a Wednesday
        cls.datetime_2021_02_08 = datetime(year=2021, month=2, day=8)  # a Monday

        cls.acceptable_weekday_inputs = {"m", "tu", "w", "th", "f", "sa", "su", "mon", "tue", "wed", "thu", "fri",
                "sat", "sun"}


    def test_failure_empty_input(self):
        self.assertIsNone(Module._parse_date("", today_datetime=None))


    """
    
    DELIMITED NUMBERS INPUT
    
    """

    """
    General:
    """

    def test_failure_extra_term(self):
        self.assertIsNone(Module._parse_date("1_2_3_", today_datetime=None))
        self.assertIsNone(Module._parse_date("1_2_3_4", today_datetime=None))


    """
    2000_12_25,2000_1_25,2000_12_5,2000_1_5
    """

    def test_success_full_date_input_two_digit_month_day_delimiters(self):
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020-12-29", today_datetime=None))

        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020(12-29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020-12(29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020(12(29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020(12;29", today_datetime=None))

        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020r12-29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020-12d29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020r12r29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020r12d29", today_datetime=None))

        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020r12{29", today_datetime=None))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("2020}12d29", today_datetime=None))


    def test_success_full_date_input_zero_pads(self):
        self.assertEqual("2021-01-05 Tue", Module._parse_date("2021(01;05", today_datetime=None))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("2021(1;05", today_datetime=None))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("2021(01;5", today_datetime=None))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("2021(1;5", today_datetime=None))
        self.assertEqual("0005-01-01 Sat", Module._parse_date("5(1;1", today_datetime=None))
        self.assertEqual("0005-01-01 Sat", Module._parse_date("05(1;1", today_datetime=None))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("0002021(001;00000005", today_datetime=None))


    def test_failure_full_date_input_blanks(self):
        self.assertIsNone(Module._parse_date("_2_3", today_datetime=None))
        self.assertIsNone(Module._parse_date("1__3", today_datetime=None))
        self.assertIsNone(Module._parse_date("1_2_", today_datetime=None))
        self.assertIsNone(Module._parse_date("__3", today_datetime=None))
        self.assertIsNone(Module._parse_date("1__", today_datetime=None))
        self.assertIsNone(Module._parse_date("_2_", today_datetime=None))
        self.assertIsNone(Module._parse_date("__", today_datetime=None))


    def test_failure_full_date_input_term_out_of_range(self):
        self.assertIsNone(Module._parse_date("0_2_3", today_datetime=None))
        self.assertIsNone(Module._parse_date("10000_2_3", today_datetime=None))

        self.assertIsNone(Module._parse_date("1_0_3", today_datetime=None))
        self.assertIsNone(Module._parse_date("1_13_3", today_datetime=None))

        self.assertIsNone(Module._parse_date("1_2_0", today_datetime=None))
        self.assertIsNone(Module._parse_date("1_2_32", today_datetime=None))
        self.assertIsNone(Module._parse_date("2021_2_29", today_datetime=None))


    """
    12_25,1_25,12_5,1_5 (the first upcoming 12-25, not today if it is 12-25)
    """

    def test_success_month_day_input_day_relative_to_today(self):
        self.assertEqual("2020-12-29 Tue", Module._parse_date("12-29", today_datetime=self.datetime_2020_12_28))  #
                # day later in month than today
        self.assertEqual("2022-01-04 Tue", Module._parse_date("01-04", today_datetime=self.datetime_2021_01_04))  #
                # day same day in month as today
        self.assertEqual("2022-01-03 Mon", Module._parse_date("01-03", today_datetime=self.datetime_2021_01_04))  #
                # day earlier in month than today


    def test_success_month_day_input_two_digit_month_day_delimiters(self):
        self.assertEqual("2020-12-29 Tue", Module._parse_date("12-29", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("12;29", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2020-12-29 Tue", Module._parse_date("12r29", today_datetime=self.datetime_2020_12_28))


    def test_success_month_day_input_zero_pads(self):
        self.assertEqual("2021-01-05 Tue", Module._parse_date("01;05", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("1;05", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("01;5", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("1;5", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("001;000005", today_datetime=self.datetime_2020_12_28))


    def test_failure_month_day_input_blanks(self):
        self.assertIsNone(Module._parse_date("_3", today_datetime=None))
        self.assertIsNone(Module._parse_date("2_", today_datetime=None))
        self.assertIsNone(Module._parse_date("_", today_datetime=None))


    def test_failure_month_day_input_term_out_of_range(self):
        self.assertIsNone(Module._parse_date("0_3", today_datetime=None))
        self.assertIsNone(Module._parse_date("13_3", today_datetime=None))

        self.assertIsNone(Module._parse_date("2_0", today_datetime=None))
        self.assertIsNone(Module._parse_date("2_32", today_datetime=None))
        self.assertIsNone(Module._parse_date("2_29", today_datetime=self.datetime_2021_01_04))


    """
    25,5 (the first upcoming 25th, not today if it is the 25th)
    """

    def test_success_day_input_day_relative_to_today(self):
        self.assertEqual("2020-12-29 Tue", Module._parse_date("29", today_datetime=self.datetime_2020_12_28))  #
                # day later in month than today
        self.assertEqual("2021-02-04 Thu", Module._parse_date("04", today_datetime=self.datetime_2021_01_04))  #
                # day same day in month as today
        self.assertEqual("2021-02-03 Wed", Module._parse_date("03", today_datetime=self.datetime_2021_01_04))  #
                # day earlier in month than today


    def test_success_day_input_day_relative_to_today_cross_year(self):
        self.assertEqual("2021-01-28 Thu", Module._parse_date("28", today_datetime=self.datetime_2020_12_28))  #
                # day same day in month as today in December
        self.assertEqual("2021-01-27 Wed", Module._parse_date("27", today_datetime=self.datetime_2020_12_28))  #
                # day earlier in month than today in December


    def test_success_day_input_zero_pads(self):
        self.assertEqual("2020-12-29 Tue", Module._parse_date("29", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("05", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("5", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("000005", today_datetime=self.datetime_2020_12_28))


    def test_failure_day_input_blank(self):
        self.assertIsNone(Module._parse_date("", today_datetime=None))


    def test_failure_day_input_term_out_of_range(self):
        self.assertIsNone(Module._parse_date("0", today_datetime=None))
        self.assertIsNone(Module._parse_date("32", today_datetime=None))
        self.assertIsNone(Module._parse_date("29", today_datetime=self.datetime_2021_02_08))


    """
    
    SPECIAL WORD:
    
    """

    """
    All:
    """

    def test_success_special_word_input_today(self):
        self.assertEqual("2020-12-28 Mon", Module._parse_date("today", today_datetime=self.datetime_2020_12_28))


    """
    
    'n' PREFIXED EXPRESSIONS:
    
    """

    """
    Unacceptable Forms
    """

    # noinspection SpellCheckingInspection
    def test_failure_unnacceptable_forms_ns_and_no_ns(self):
        self.assertIsNone(Module._parse_date("\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("n\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("\\n", today_datetime=None))
        self.assertIsNone(Module._parse_date("n\\n", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn\\n", today_datetime=None))

        self.assertIsNone(Module._parse_date("25\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("n25\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn25\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("\\25", today_datetime=None))
        self.assertIsNone(Module._parse_date("n\\25", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn\\25", today_datetime=None))
        self.assertIsNone(Module._parse_date("25n", today_datetime=None))
        self.assertIsNone(Module._parse_date("n25n", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn25n", today_datetime=None))

        self.assertIsNone(Module._parse_date("fn", today_datetime=None))
        self.assertIsNone(Module._parse_date("nfn", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnnfn", today_datetime=None))
        self.assertIsNone(Module._parse_date("f\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("nf\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnnf\\", today_datetime=None))
        self.assertIsNone(Module._parse_date("f25", today_datetime=None))
        self.assertIsNone(Module._parse_date("nf25", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnnf25", today_datetime=None))
        self.assertIsNone(Module._parse_date("\\f", today_datetime=None))
        self.assertIsNone(Module._parse_date("n\\f", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn\\f", today_datetime=None))
        self.assertIsNone(Module._parse_date("25f", today_datetime=None))
        self.assertIsNone(Module._parse_date("n25f", today_datetime=None))
        self.assertIsNone(Module._parse_date("nnn25f", today_datetime=None))


    """
    "nnn","n" (tomorrow's tomorrow's tomorrow) (one 'n' per tomorrow as many as you want)
    """

    # noinspection SpellCheckingInspection
    def test_success_tomorrow_input(self):
        self.assertEqual("2021-01-05 Tue", Module._parse_date("n", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-06 Wed", Module._parse_date("nn", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-07 Thu", Module._parse_date("nnn", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-12 Tue", Module._parse_date("nnnnnnnn", today_datetime=self.datetime_2021_01_04))


    # noinspection SpellCheckingInspection
    def test_success_tomorrow_input_cross(self):

        self.assertEqual("2021-01-04 Mon", Module._parse_date("nnnnnnn", today_datetime=self.datetime_2020_12_28))  #
                # year
        self.assertEqual("2021-02-01 Mon", Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn",
                today_datetime=self.datetime_2020_12_28))  # two months including a year


    """
    "nnn25","n5" (next next next 25th after the first upcoming 25th) (one 'n' per next as many as you want)
    """

    # noinspection SpellCheckingInspection
    def test_success_next_day_input_day_relative_to_today_variable_n_count(self):

        # day later in month than today
        self.assertEqual("2021-01-29 Fri", Module._parse_date("n29", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-03-29 Mon", Module._parse_date("nnn29", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2023-03-29 Wed", Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnn29",
                today_datetime=self.datetime_2020_12_28))

        # day same day in month as today
        self.assertEqual("2021-03-04 Thu", Module._parse_date("n04", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-05-04 Tue", Module._parse_date("nnn04", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2023-05-04 Thu", Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnn04",
                today_datetime=self.datetime_2021_01_04))

        # day earlier in month than today
        self.assertEqual("2021-03-03 Wed", Module._parse_date("n03", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-05-03 Mon", Module._parse_date("nnn03", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2023-05-03 Wed", Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnn03",
                today_datetime=self.datetime_2021_01_04))


    def test_success_next_day_input_zero_pads(self):
        self.assertEqual("2020-12-29 Tue", Module._parse_date("n29", today_datetime=self.datetime_2020_11_09))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("n05", today_datetime=self.datetime_2020_11_09))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("n5", today_datetime=self.datetime_2020_11_09))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("n000005", today_datetime=self.datetime_2020_11_09))


    def test_failure_next_day_input_day_out_of_range(self):
        self.assertIsNone(Module._parse_date("n0", today_datetime=None))
        self.assertIsNone(Module._parse_date("n32", today_datetime=None))
        self.assertIsNone(Module._parse_date("n29", today_datetime=self.datetime_2021_01_04))


    # noinspection SpellCheckingInspection
    """
    "w","tu","th" (this coming Wednesday)
    "wed","tue","thu" (this coming Wednesday)
    "nnnw","ntu","nth" (one 'n' per next as many as you want)
    "nnnwed","ntue","nthu" (one 'n' per next as many as you want)
    """
    
    def test_success_weekday_input_0_ns(self):
        self.assertEqual("2021-01-05 Tue", Module._parse_date("tue", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-05 Tue", Module._parse_date("tu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-06 Wed", Module._parse_date("wed", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-06 Wed", Module._parse_date("w", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-07 Thu", Module._parse_date("thu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-07 Thu", Module._parse_date("th", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-08 Fri", Module._parse_date("fri", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-08 Fri", Module._parse_date("f", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-09 Sat", Module._parse_date("sat", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-09 Sat", Module._parse_date("sa", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-10 Sun", Module._parse_date("sun", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-10 Sun", Module._parse_date("su", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-11 Mon", Module._parse_date("mon", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-11 Mon", Module._parse_date("m", today_datetime=self.datetime_2021_01_04))


    # noinspection SpellCheckingInspection
    def test_success_weekday_input_1_n(self):
        self.assertEqual("2021-01-12 Tue", Module._parse_date("ntue", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-12 Tue", Module._parse_date("ntu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-13 Wed", Module._parse_date("nwed", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-13 Wed", Module._parse_date("nw", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-14 Thu", Module._parse_date("nthu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-14 Thu", Module._parse_date("nth", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-15 Fri", Module._parse_date("nfri", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-15 Fri", Module._parse_date("nf", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-16 Sat", Module._parse_date("nsat", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-16 Sat", Module._parse_date("nsa", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-17 Sun", Module._parse_date("nsun", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-17 Sun", Module._parse_date("nsu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-18 Mon", Module._parse_date("nmon", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-01-18 Mon", Module._parse_date("nm", today_datetime=self.datetime_2021_01_04))


    # noinspection SpellCheckingInspection
    def test_success_weekday_input_4_ns_cross_1_month(self):
        self.assertEqual("2021-02-02 Tue", Module._parse_date("nnnntue", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-02 Tue", Module._parse_date("nnnntu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-03 Wed", Module._parse_date("nnnnwed", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-03 Wed", Module._parse_date("nnnnw", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-04 Thu", Module._parse_date("nnnnthu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-04 Thu", Module._parse_date("nnnnth", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-05 Fri", Module._parse_date("nnnnfri", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-05 Fri", Module._parse_date("nnnnf", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-06 Sat", Module._parse_date("nnnnsat", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-06 Sat", Module._parse_date("nnnnsa", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-07 Sun", Module._parse_date("nnnnsun", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-07 Sun", Module._parse_date("nnnnsu", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-08 Mon", Module._parse_date("nnnnmon", today_datetime=self.datetime_2021_01_04))
        self.assertEqual("2021-02-08 Mon", Module._parse_date("nnnnm", today_datetime=self.datetime_2021_01_04))


    # noinspection SpellCheckingInspection
    def test_success_weekday_input_8_ns_cross_1_year(self):
        self.assertEqual("2021-02-23 Tue", Module._parse_date("nnnnnnnntue", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-23 Tue", Module._parse_date("nnnnnnnntu", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-24 Wed", Module._parse_date("nnnnnnnnwed", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-24 Wed", Module._parse_date("nnnnnnnnw", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-25 Thu", Module._parse_date("nnnnnnnnthu", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-25 Thu", Module._parse_date("nnnnnnnnth", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-26 Fri", Module._parse_date("nnnnnnnnfri", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-26 Fri", Module._parse_date("nnnnnnnnf", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-27 Sat", Module._parse_date("nnnnnnnnsat", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-27 Sat", Module._parse_date("nnnnnnnnsa", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-28 Sun", Module._parse_date("nnnnnnnnsun", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-02-28 Sun", Module._parse_date("nnnnnnnnsu", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-03-01 Mon", Module._parse_date("nnnnnnnnmon", today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2021-03-01 Mon", Module._parse_date("nnnnnnnnm", today_datetime=self.datetime_2020_12_28))


    # noinspection SpellCheckingInspection
    def test_success_weekday_input_58_ns_cross_2_years(self):
        self.assertEqual("2022-02-08 Tue",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntue",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-08 Tue",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnntu",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-09 Wed",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnwed",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-09 Wed",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnw",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-10 Thu",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnthu",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-10 Thu",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnth",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-11 Fri",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnfri",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-11 Fri",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnf",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-12 Sat",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnsat",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-12 Sat",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnsa",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-13 Sun",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnsun",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-13 Sun",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnsu",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-14 Mon",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnmon",
                today_datetime=self.datetime_2020_12_28))
        self.assertEqual("2022-02-14 Mon",
                Module._parse_date("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnm",
                today_datetime=self.datetime_2020_12_28))


    def test_success_weekday_input_day_of_week_offset_from_other_tests_0_ns(self):
        self.assertEqual("2021-01-12 Tue", Module._parse_date("tue", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-12 Tue", Module._parse_date("tu", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-13 Wed", Module._parse_date("wed", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-13 Wed", Module._parse_date("w", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-07 Thu", Module._parse_date("thu", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-07 Thu", Module._parse_date("th", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-08 Fri", Module._parse_date("fri", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-08 Fri", Module._parse_date("f", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-09 Sat", Module._parse_date("sat", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-09 Sat", Module._parse_date("sa", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-10 Sun", Module._parse_date("sun", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-10 Sun", Module._parse_date("su", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-11 Mon", Module._parse_date("mon", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-11 Mon", Module._parse_date("m", today_datetime=self.datetime_2021_01_06))


    # noinspection SpellCheckingInspection
    def test_success_weekday_input_day_of_week_offset_from_other_tests_2_ns(self):
        self.assertEqual("2021-01-26 Tue", Module._parse_date("nntue", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-26 Tue", Module._parse_date("nntu", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-27 Wed", Module._parse_date("nnwed", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-27 Wed", Module._parse_date("nnw", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-21 Thu", Module._parse_date("nnthu", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-21 Thu", Module._parse_date("nnth", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-22 Fri", Module._parse_date("nnfri", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-22 Fri", Module._parse_date("nnf", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-23 Sat", Module._parse_date("nnsat", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-23 Sat", Module._parse_date("nnsa", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-24 Sun", Module._parse_date("nnsun", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-24 Sun", Module._parse_date("nnsu", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-25 Mon", Module._parse_date("nnmon", today_datetime=self.datetime_2021_01_06))
        self.assertEqual("2021-01-25 Mon", Module._parse_date("nnm", today_datetime=self.datetime_2021_01_06))


    def test_failure_weekday_input_illegitimate_lowercase_letter_inputs_up_to_4_chars_0_ns(self):
        for a in ascii_lowercase.replace('n', ''):
            if a not in self.acceptable_weekday_inputs:
                self.assertIsNone(Module._parse_date(a, today_datetime=None))
            for b in ascii_lowercase:
                ab = a + b
                if ab not in self.acceptable_weekday_inputs:
                    self.assertIsNone(Module._parse_date(ab, today_datetime=None))
                for c in ascii_lowercase:
                    abc = ab + c
                    if abc not in self.acceptable_weekday_inputs:
                        self.assertIsNone(Module._parse_date(abc, today_datetime=None))
                    for d in ascii_lowercase:
                        self.assertIsNone(Module._parse_date(abc+d, today_datetime=None))


    def test_failure_weekday_input_illegitimate_lowercase_letter_inputs_up_to_4_chars_1_n(self):
        n_prefix = "n"
        for a in ascii_lowercase.replace('n', ''):
            if a not in self.acceptable_weekday_inputs:
                self.assertIsNone(Module._parse_date(n_prefix+a, today_datetime=None))
            for b in ascii_lowercase:
                ab = a + b
                if ab not in self.acceptable_weekday_inputs:
                    self.assertIsNone(Module._parse_date(n_prefix+ab, today_datetime=None))
                for c in ascii_lowercase:
                    abc = ab + c
                    if abc not in self.acceptable_weekday_inputs:
                        self.assertIsNone(Module._parse_date(n_prefix+abc, today_datetime=None))
                    for d in ascii_lowercase:
                        self.assertIsNone(Module._parse_date(n_prefix+abc+d, today_datetime=None))


class Test__Parse_Time(unittest.TestCase):

    def test_failure_empty_input(self):
        self.assertIsNone(Module._parse_time(""))


    """
    
    1 and 2 chars
    
    """

    def test_success_1_2_chars(self):

        # 1 char
        self.assertEqual("05:00", Module._parse_time("5"))

        # 2 chars
        self.assertEqual("15:00", Module._parse_time("15"))


    def test_success_1_2_chars_minimum(self):

        # 1 char
        self.assertEqual("00:00", Module._parse_time("0"))

        # 2 char
        self.assertEqual("00:00", Module._parse_time("00"))


    def test_success_1_2_chars_maximum(self):

        # 2 char
        self.assertEqual("23:00", Module._parse_time("23"))


    def test_failure_1_2_chars_out_of_range(self):

        # 2 char
        self.assertIsNone(Module._parse_time("24"))


    def test_failure_1_2_chars_str_not_a_natural_number(self):

        # 1 char
        self.assertIsNone(Module._parse_time("."))
        self.assertIsNone(Module._parse_time("-"))
        self.assertIsNone(Module._parse_time("f"))

        # 2 chars
        self.assertIsNone(Module._parse_time("2."))
        self.assertIsNone(Module._parse_time("-1"))
        self.assertIsNone(Module._parse_time("fo"))


    """
    
    4 and 5 chars
    
    """

    def test_success_4_5_chars(self):

        # 4 chars
        self.assertEqual("05:00", Module._parse_time("5:00"))

        # 5 chars
        self.assertEqual("15:00", Module._parse_time("15:00"))


    def test_success_4_5_chars_minimum(self):

        # 4 chars
        self.assertEqual("00:00", Module._parse_time("0:00"))

        # 5 chars
        self.assertEqual("00:00", Module._parse_time("00:00"))


    def test_success_4_5_chars_maximum(self):

        # 5 chars
        self.assertEqual("23:59", Module._parse_time("23:59"))


    def test_failure_4_5_chars_bad_delimiter(self):

        # 4 chars
        self.assertIsNone(Module._parse_time("5-00"))
        self.assertIsNone(Module._parse_time("5;00"))
        self.assertIsNone(Module._parse_time("5a00"))
        self.assertIsNone(Module._parse_time("5A00"))
        self.assertIsNone(Module._parse_time("5000"))
        self.assertIsNone(Module._parse_time("5100"))

        # 5 chars
        self.assertIsNone(Module._parse_time("15-00"))
        self.assertIsNone(Module._parse_time("15;00"))
        self.assertIsNone(Module._parse_time("15a00"))
        self.assertIsNone(Module._parse_time("15A00"))
        self.assertIsNone(Module._parse_time("15000"))
        self.assertIsNone(Module._parse_time("15100"))


    def test_failure_4_5_chars_out_of_range(self):

        # 5 chars
        self.assertIsNone(Module._parse_time("24:00"))
        self.assertIsNone(Module._parse_time("00:60"))


    def test_failure_4_5_chars_term_not_a_natural_number(self):

        # 4 chars

        self.assertIsNone(Module._parse_time(".:00"))
        self.assertIsNone(Module._parse_time("0:2."))

        self.assertIsNone(Module._parse_time("-:00"))
        self.assertIsNone(Module._parse_time("0:-1"))

        self.assertIsNone(Module._parse_time("f:00"))
        self.assertIsNone(Module._parse_time("0:fo"))

        # 5 chars

        self.assertIsNone(Module._parse_time("2.:00"))
        self.assertIsNone(Module._parse_time("00:2."))

        self.assertIsNone(Module._parse_time("-1:00"))
        self.assertIsNone(Module._parse_time("00:-1"))

        self.assertIsNone(Module._parse_time("fo:00"))
        self.assertIsNone(Module._parse_time("00:fo"))



# MAIN
if __name__ == '__main__':
    unittest.main()
