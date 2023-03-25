"""
Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# EXTERNAL IMPORTS
import os
# os.system('mode con: cols=200 lines=48')  # change command line window dimensions as quickly as possible for user
import traceback
import logging
import sys
import datetime


# CHANGE DIRECTORY TO PROJECT DIRECTORY
calling_dir = os.getcwd()  # get the calling directory
os.chdir(os.path.dirname(__file__))  # change the directory to the script directory


# LOGGING
"""
Logging Levels Usage:
INFO     : For success reports
WARNING  : No error but an unfavorable result
ERROR    : A non fatal error
CRITICAL : A fatal error
"""

# make logger
logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger("Scheduler")
logger.setLevel(logging.NOTSET)

# make handlers
info_file_handler = logging.FileHandler("Scheduler_info_log_file.log")
warning_file_handler = logging.FileHandler("Scheduler_warning_log_file.log")

# set handler levels
info_file_handler.setLevel(logging.INFO)
warning_file_handler.setLevel(logging.WARNING)

# Create formatters and add to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

info_file_handler.setFormatter(formatter)
warning_file_handler.setFormatter(formatter)

# add handlers to the logger
logger.addHandler(info_file_handler)
logger.addHandler(warning_file_handler)


# PROGRAM
try:

    # PROJECT IMPORTS
    import Utility
    from Input_Parser import parse as input_parser_parse
    from Input_Parser import PARAM_Arg_Form, ENUM_Input_Type, ENUM_Demanded_Value_Type
    from Schedule import Schedule
    from Event import ENUM_Event_Type


    # HARDCODED VARIABLES
    LOAD_IN_EVENTS_FILE_NAME = "events.txt"
    LOAD_IN_EVENTS_BACKUPS_FOLDER = "backups"
    BLANKS_DEFAULT = 100
    BLANKS_MAX = 10000


    # FUNCTIONS USING 'schedule'
    def load_in_schedule():
        """
        Load in the schedule from the file
        :return: void
        """
        global schedule
        schedule = Schedule(load_in_events=Utility.read_in_txt_as_list(LOAD_IN_EVENTS_FILE_NAME))


    def backup_schedule(file_name_start=""):
        """
        Backup the schedule
        :return: void
        """
        Utility.output_list_to_txt(output=schedule.list_of_load_in_strings_for_events(), output_file_absolute_path=LOAD_IN_EVENTS_BACKUPS_FOLDER + "/" +
                file_name_start + (" " if file_name_start else "") + str(datetime.datetime.now()).replace(':', '.'), overwrite=True)  # save backup


    def save_schedule():
        """
        Save the schedule
        :return: void
        """
        Utility.output_list_to_txt(output=schedule.list_of_load_in_strings_for_events(), output_file_absolute_path=LOAD_IN_EVENTS_FILE_NAME, overwrite=True)
        backup_schedule()


    # INIT MESSAGE TO USER
    print("""
    -----------------------------------------------------------------------------------------
    Scheduling Application written by Cole Anderson

    Type 'help' for help
    -----------------------------------------------------------------------------------------
    """)


    # SETUP

    # deal with events
    if os.path.isfile(LOAD_IN_EVENTS_FILE_NAME):  # if the events file exists
        load_in_schedule()
        print("Schedule Loaded\n")
    else:
        print("\nEVENTS FILE: '" + LOAD_IN_EVENTS_FILE_NAME + "' DOES NOT EXIST, WILL BE CREATED UPON NEXT SAVE. \n")
        schedule = Schedule()

    # create backups folder if nonexistent
    if not os.path.isdir(LOAD_IN_EVENTS_BACKUPS_FOLDER):
        os.mkdir(LOAD_IN_EVENTS_BACKUPS_FOLDER)


    # SCRIPT ARGUMENTS
    if len(sys.argv) >= 2 and sys.argv[1].strip().lower() == "print":  # start run with a print command, this is for the Windows Task Scheduler to use so that it can show
            # the schedule from the command line when desired
        # noinspection PyUnboundLocalVariable
        print(schedule)


    # MAIN
    while True:
        user_input = [in_arg for in_arg in input(">>> ").strip().replace('|', '').lower().split(" ") if in_arg]
        # logging.info("INFO: user_input: " + str(user_input))

        parsed_args = None  # reset for debugging
        if not user_input:
            pass
        elif user_input[0] == 'help':
            print("""
    Help Page:
    
    -----
    Scheduling Application written by Cole Anderson
    
    All commands are case and beginning-space and end-space insensitive
    '|' will be removed from any user input
    Separate command args with ' '
    No arg values can include ' ' except for 'end' args which can only be the last arg given for a command and can include ' '
    Enter '.' for optional ('opt') args to enter no value, '.' is not accepted as a legitimate value for optional args,
            alternatively enter nothing to enter no value for all remaining optional args
    Type 'help' for help
    -----
    
    Commands:
    help                            :   print this help page
    blanks, b                       :   print blank lines, default: """ + str(BLANKS_DEFAULT) + ", max: " + str(BLANKS_MAX) + """ (command args: opt:number)
    print, p                        :   print schedule
    add_attendance, aa              :   add a new ATTENDANCE event (command args: date, time, opt:end time, tag, end:description)
    add_deadline, ad                :   add a new DEADLINE event (command args: date, time, opt:duration, tag, end:description)
    modify_attendance, ma           :   modify an ATTENDANCE event (command args: event id, opt:date, opt:time, opt:end time, opt:tag, opt&end:description)
    modify_deadline, md             :   modify a DEADLINE event (command args: event id, opt:date, opt:time, opt:duration, opt:tag, opt&end:description)
    delete, d                       :   delete an event (command args: end:event ids)
    save, s                         :   save changes
    save_and_print, sp              :   save changes and print new schedule
    reload                          :   reload schedule
    quit, q                         :   save changes and quit the application
    quit_without_saving             :   quit the application without saving changes
    wipe_schedule                   :   remove all events from the schedule and save now empty schedule
            """)
        elif user_input[0] == 'blanks' or user_input[0] == 'b':
            parsed_args = input_parser_parse(user_input[1:],
                    [PARAM_Arg_Form(ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.UNSIGNED_INT)])
            if type(parsed_args) == str:  # bad args
                print(parsed_args)
                print("Command: 'blanks': (command args: opt:number)")
            elif parsed_args[0] is not None and parsed_args[0] > BLANKS_MAX:  # number exceeds
                    # maximum allowable value
                print("Command Failure: Inputted number value: " + str(parsed_args[0]) +
                        ", exceeds the maximum allowable value of: " + str(BLANKS_MAX))
            else:  # execute command
                print("\n" * (BLANKS_DEFAULT if parsed_args[0] is None else parsed_args[0]),
                        end='')
        elif user_input[0] == 'print' or user_input[0] == 'p':
            print(schedule)
        elif user_input[0] == 'add_attendance' or user_input[0] == 'aa':
            parsed_args = input_parser_parse(user_input[1:],
                    [PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.DATE),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.TIME),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.TIME),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.END,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR)])
            if type(parsed_args) == str:  # bad args
                print(parsed_args)
                print("Command: 'add_attendance': (command args: date, time, opt:end time, tag, "
                        "end:description)")
            else:  # execute command
                temp = schedule.add_attendance_event(date=parsed_args[0], time=parsed_args[1],
                        end_time=parsed_args[2], tag=parsed_args[3],
                        description=parsed_args[4])  # (id, string representation of new event)
                print("New Event Added:\nID:", str(temp[0]) + ", Event:", temp[1])
        elif user_input[0] == 'add_deadline' or user_input[0] == 'ad':
            parsed_args = input_parser_parse(user_input[1:],
                    [PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.DATE),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.TIME),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.DURATION),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.END,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR)])
            if type(parsed_args) == str:  # bad args
                print(parsed_args)
                print("Command: 'add_deadline': (command args: date, time, opt:duration, tag, "
                        "end:description)")
            else:  # execute command
                temp = schedule.add_deadline_event(date=parsed_args[0], time=parsed_args[1],
                        duration=parsed_args[2], tag=parsed_args[3],
                        description=parsed_args[4])  # (id, string representation of new event)
                print("New Event Added:\nID:", str(temp[0]) + ", Event:", temp[1])
        elif user_input[0] == 'delete' or user_input[0] == 'd':
            parsed_args = input_parser_parse(user_input[1:],
                    [PARAM_Arg_Form(input_type=ENUM_Input_Type.END,
                    demanded_value_type=ENUM_Demanded_Value_Type.UNSIGNED_INT)])
            if type(parsed_args) == str:  # bad args
                print(parsed_args)
                print("Command: 'delete': (command args: end:event ids)")
            else:  # execute command
                for del_event_id in parsed_args[0]:  # for each event id given by the user
                    print("\tERROR: Event: " + str(del_event_id) + " Could Not Be Deleted" if
                            schedule.delete_event(del_event_id) is None else
                            "Event: " + str(del_event_id) + " Successfully Deleted")
        elif user_input[0] == 'modify_attendance' or user_input[0] == 'ma':
            parsed_args = input_parser_parse(user_input[1:],
                    [PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.UNSIGNED_INT),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.DATE),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.TIME),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.TIME),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL_END,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR)])
            if type(parsed_args) == str:  # bad args
                print(parsed_args)
                print("Command: 'modify_attendance': (command args: event id, opt:date, opt:time, "
                        "opt:end time, opt:tag, opt&end:description)")
            else:  # execute command
                temp = schedule.replace_attendance_event(replaced_event_id=parsed_args[0],
                        date=parsed_args[1], time=parsed_args[2], end_time=parsed_args[3],
                        tag=parsed_args[4], description=parsed_args[5])  #
                        # (id, string representation of new event OR failure message)
                if temp[0] == -1:
                    print(("Event " + str(parsed_args[0]) + " Could Not Be Modified: "
                            "Error Message: " + temp[1]))
                else:
                    print("Event Successfully Modified\nNew Event ID: " + str(temp[0]) +
                        "\nNew Event: " + temp[1])
        elif user_input[0] == 'modify_deadline' or user_input[0] == 'md':
            parsed_args = input_parser_parse(user_input[1:],
                    [PARAM_Arg_Form(input_type=ENUM_Input_Type.REGULAR,
                        demanded_value_type=ENUM_Demanded_Value_Type.UNSIGNED_INT),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.DATE),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.TIME),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.DURATION),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR),
                    PARAM_Arg_Form(input_type=ENUM_Input_Type.OPTIONAL_END,
                        demanded_value_type=ENUM_Demanded_Value_Type.STR)])
            if type(parsed_args) == str:  # bad args
                print(parsed_args)
                print("Command: 'modify_deadline': (command args: event id, opt:date, opt:time, "
                        "opt:duration, opt:tag, opt&end:description)")
            else:  # execute command
                temp = schedule.replace_deadline_event(replaced_event_id=parsed_args[0],
                        date=parsed_args[1], time=parsed_args[2], duration=parsed_args[3],
                        tag=parsed_args[4], description=parsed_args[5])  #
                        # (id, string representation of new event OR failure message)
                if temp[0] == -1:
                    print(("Event " + str(parsed_args[0]) + " Could Not Be Modified: "
                            "Error Message: " + temp[1]))
                else:
                    print("Event Successfully Modified\nNew Event ID: " + str(temp[0]) +
                        "\nNew Event: " + temp[1])
        elif user_input[0] == 'save' or user_input[0] == 's':
            save_schedule()
            print("Save Complete")
        elif user_input[0] == 'save_and_print' or user_input[0] == 'sp':
            save_schedule()
            print("Save Complete")
            print()
            print(schedule)
            print()
            print("Above Represents Print After Save")
        elif user_input[0] == 'reload':
            load_in_schedule()
            print("Schedule Reloaded; Changes Since Last Save Discarded")
        elif user_input[0] == 'quit' or user_input[0] == 'q':
            save_schedule()
            print("Save Complete")
            quit()
        elif user_input[0] == 'quit_without_saving':
            quit()
        elif user_input[0] == 'wipe_schedule':
            if input("Are you sure that you want to remove all events from the schedule and save "
                    "(y/n)? ").strip().lower() == 'y':
                backup_schedule("WIPE_SCHEDULE")
                schedule = Schedule()  # create a new, empty, schedule as the schedule
                save_schedule()
                print("Save Complete")
                print("Schedule Successfully Wiped")
            else:
                print("Schedule Wipe Not Performed")
        else:
            print("Command '" + user_input[0] + "' not recognized. Type 'help' for help")
        print()
except SystemExit:  # for quit() calls
    pass
except:
    logging.critical("CRITICAL ERROR: Exception:\n" + traceback.format_exc())


# CHANGE DIRECTORY BACK TO CALLING DIRECTORY
os.chdir(calling_dir)  # return the directory to the calling directory
