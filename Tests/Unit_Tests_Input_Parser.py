"""
Written by Cole Anderson
"""



# IMPORTS
import unittest

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

    def test_success(self):
        self.assertEqual(42, Module._parse_unsigned_int("42"))


    def test_success_zero(self):
        self.assertEqual(0, Module._parse_unsigned_int("0"))


    def test_failure_non_number(self):
        self.assertIsNone(Module._parse_unsigned_int("foobar"))


    def test_failure_negative(self):
        self.assertIsNone(Module._parse_unsigned_int("-42"))


    def test_failure_decimal(self):
        self.assertIsNone(Module._parse_unsigned_int("42.5"))



class Test__Parse_Date(unittest.TestCase):

    def test_success(self):
        self.assertEqual("2020-09-30", Module._parse_date("2020-09-30"))



class Test__Parse_Time(unittest.TestCase):

    def test_success_one_char(self):
        self.assertEqual("05:00", Module._parse_time("5"))


    def test_success_two_chars(self):
        self.assertEqual("15:00", Module._parse_time("15"))


    def test_success_one_char_minimum(self):
        self.assertEqual("00:00", Module._parse_time("0"))


    def test_success_two_char_minimum(self):
        self.assertEqual("00:00", Module._parse_time("00"))


    def test_success_two_char_maximum(self):
        self.assertEqual("23:00", Module._parse_time("23"))


    def test_failure_two_char_out_of_range_high(self):
        self.assertIsNone(Module._parse_time("24"))


    def test_failure_two_char_decimal(self):
        self.assertIsNone(Module._parse_time("2."))


    def test_failure_two_char_negative(self):
        self.assertIsNone(Module._parse_time("-1"))


    def test_failure_one_char_string(self):
        self.assertIsNone(Module._parse_time("f"))


    def test_failure_two_char_string(self):
        self.assertIsNone(Module._parse_time("fo"))


    def test_success_four_chars(self):
        self.assertEqual("05:00", Module._parse_time("5:00"))


    def test_success_five_chars(self):
        self.assertEqual("15:00", Module._parse_time("15:00"))


    def test_success_four_char_minimum(self):
        self.assertEqual("00:00", Module._parse_time("0:00"))


    def test_success_five_char_minimum(self):
        self.assertEqual("00:00", Module._parse_time("00:00"))


    def test_success_five_char_maximum(self):
        self.assertEqual("23:59", Module._parse_time("23:59"))


    def test_failure_five_char_out_of_range_high_hours(self):
        self.assertIsNone(Module._parse_time("24:00"))


    def test_failure_five_char_out_of_range_high_minutes(self):
        self.assertIsNone(Module._parse_time("00:60"))


    def test_failure_five_char_decimal_hours(self):
        self.assertIsNone(Module._parse_time("2.:00"))


    def test_failure_five_char_decimal_minutes(self):
        self.assertIsNone(Module._parse_time("00:2."))


    def test_failure_five_char_negative_hours(self):
        self.assertIsNone(Module._parse_time("-1:00"))


    def test_failure_five_char_negative_minutes(self):
        self.assertIsNone(Module._parse_time("00:-1"))


    def test_failure_four_char_string_hours(self):
        self.assertIsNone(Module._parse_time("f:00"))


    def test_failure_four_char_string_minutes(self):
        self.assertIsNone(Module._parse_time("0:fo"))


    def test_failure_five_char_string_hours(self):
        self.assertIsNone(Module._parse_time("fo:00"))


    def test_failure_five_char_string_minutes(self):
        self.assertIsNone(Module._parse_time("00:fo"))



# MAIN
if __name__ == '__main__':
    unittest.main()
