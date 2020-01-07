"""
Written by Cole Anderson
"""



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

# custom handler imports
from No_Print_FileHandler import No_Print_FileHandler

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
    from Utility import *
    from Schedule import Schedule


    # HARDCODED VARIABLES
    LOAD_IN_EVENTS_FILE_NAME = "events.txt"
    LOAD_IN_EVENTS_BACKUPS_FOLDER = "backups"


    # FUNCTIONS
    def load_in_schedule():
        """
        Load in the schedule from the file
        :return: void
        """
        global schedule
        schedule = Schedule(load_in_events=read_in_txt_as_list(LOAD_IN_EVENTS_FILE_NAME))


    def backup_schedule(file_name_start=""):
        """
        Backup the schedule
        :return: void
        """
        output_list_to_txt(output=schedule.list_of_load_in_strings_for_events(), output_file_absolute_path=LOAD_IN_EVENTS_BACKUPS_FOLDER + "/" +
                file_name_start + (" " if file_name_start else "") + str(datetime.datetime.now()).replace(':', '.'), overwrite=True)  # save backup


    def save_schedule():
        """
        Save the schedule
        :return: void
        """
        output_list_to_txt(output=schedule.list_of_load_in_strings_for_events(), output_file_absolute_path=LOAD_IN_EVENTS_FILE_NAME, overwrite=True)
        backup_schedule()


    def parse_user_inputted_time(user_inputted_time: str) -> str or None:
        """
        Parse a user inputted time value into a uniform 5 digit character string like 'HH:MM'
        :param user_inputted_time:
        :return: 5 character time string if user inputted time value could be parsed, None otherwise
        """
        input_length = len(user_inputted_time)
        if (input_length == 1 or input_length == 2) and user_inputted_time.isdigit() and int(user_inputted_time) < 24:
            return ("0" if input_length == 1 else "") + user_inputted_time + ":00"
        if (input_length == 4 or input_length == 5) and user_inputted_time[:-3].isdigit() and int(user_inputted_time[:-3]) < 24 and \
                user_inputted_time[-3] == ':' and user_inputted_time[-2:].isdigit() and int(user_inputted_time[-2:]) < 60:
            return ("0" if input_length == 4 else "") + user_inputted_time
        return None


    # SETUP
    print("""
-----------------------------------------------------------------------------------------
Scheduling Application written by Cole Anderson

Type 'help' for help
-----------------------------------------------------------------------------------------
        """)
    load_in_schedule()
    print("Schedule Loaded\n")


    # SCRIPT ARGUMENTS
    if len(sys.argv) >= 2 and sys.argv[1].strip().lower() == "print":  # just print and exit, this is for the Windows Task Scheduler to use so that it can show the schedule
            # from the command line when desired
        print(schedule)


    # MAIN
    while True:
        user_input = input(">>> ").strip().replace('|', '').lower().split(" ")
        # logging.info("INFO: user_input: " + str(user_input))

        if user_input[0] == 'help':
            print("""
    Help Page:
    
    -----
    Scheduling Application written by Cole Anderson
    
    All commands are case and beginning-space and end-space insensitive
    '|' will be removed from any user input
    Separate command args with ' '
    No arg values can include ' ' except for 'end' args which are always the last arg given for a command and can include ' '
    Enter '.' for optional ('opt') args to enter no value
    Type 'help' for help
    -----
    
    Commands:
    help                            :   print this help page
    print, p                        :   print schedule
    add, a                          :   add a new event (command args: date, time, event type, end:description)
    delete, d                       :   delete an event (command args: event id)
    modify, m                       :   modify an event (command args: event id, opt:date, opt:time, opt:event type, opt&end:description)
    save, s                         :   save changes
    save_and_print, sp              :   save changes and print new schedule
    reload                          :   reload schedule
    quit, q                         :   save changes and quit the application
    quit_without_saving             :   quit the application without saving changes
    wipe_schedule                   :   remove all events from the schedule and save now empty schedule
            """)
        elif user_input[0] == 'print' or user_input[0] == 'p':
            print(schedule)
        elif user_input[0] == 'add' or user_input[0] == 'a':
            if len(user_input) == 1:
                print("Command: 'add': (command args: date, time, event type, end:description)")
            elif len(user_input) < 5:
                print("Command Failure: 'add': Incorrect Number of Arguments Given: " + str(len(user_input) - 1) + ". (command args: date, time, event type, end:description)")
            else:
                M_parsed_time_entry = parse_user_inputted_time(user_input[2])
                if M_parsed_time_entry is None:
                    print("Command Failure: 2nd arg, 'time', could not be parsed to a uniform 5 character time string")
                else:
                    temp = schedule.add_event(date=user_input[1], time=M_parsed_time_entry, event_type=user_input[3], description=' '.join(user_input[4:]))  # (id, string representation of new
                            # event)
                    print("New Event Added:\nID:", str(temp[0]) + ", Event:", temp[1])
        elif user_input[0] == 'delete' or user_input[0] == 'd':
            if len(user_input) == 1:
                print("Command: 'delete': (command args: event id)")
            elif len(user_input) != 2:
                print("Command Failure: 'delete': Incorrect Number of Arguments Given: " + str(len(user_input) - 1) + ". (command args: event id)")
            elif not user_input[1].isdigit():
                print("Command Failure: 1st arg, 'event id', must be a positive integer")
            else:
                print("Event", user_input[1], "Could Not Be Deleted" if schedule.delete_event(int(user_input[1])) is None else "Successfully Deleted")
        elif user_input[0] == 'modify' or user_input[0] == 'm':
            if len(user_input) == 1:
                print("Command: 'modify': (command args: event id, opt:date, opt:time, opt&end:event type, opt:description)")
            elif len(user_input) < 6:
                print("Command Failure: 'modify': Incorrect Number of Arguments Given: " + str(len(user_input) - 1) +
                        ". (command args: event id, opt:date, opt:time, opt:event type, opt&end:description)")
            elif not user_input[1].isdigit():
                print("Command Failure: 1st arg, 'event id', must be a positive integer")
            else:
                M_parsed_time_entry = '.' if user_input[3] == '.' else parse_user_inputted_time(user_input[3])
                if M_parsed_time_entry is None:
                    print("Command Failure: 3rd arg, 'time', could not be parsed to a uniform 5 character time string")
                else:
                    M_new_event_id, M_new_event_description_string = schedule.replace_event(int(user_input[1]), decline_value='.', date=user_input[2], time=M_parsed_time_entry,
                            event_type=user_input[4], description=' '.join(user_input[5:]))
                    print(("Event " + user_input[1] + " Could Not Be Modified") if M_new_event_id == -1 else ("Event Successfully Modified\nNew Event ID: " + str(M_new_event_id) +
                            "\nNew Event: " + M_new_event_description_string))
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
            backup_schedule("RELOAD")
            load_in_schedule()
            print("Schedule Reloaded; Changes Since Last Save Discarded")
        elif user_input[0] == 'quit' or user_input[0] == 'q':
            save_schedule()
            print("Save Complete")
            quit()
        elif user_input[0] == 'quit_without_saving':
            backup_schedule("QUIT_WITHOUT_SAVING")
            quit()
        elif user_input[0] == 'wipe_schedule':
            if input("Are you sure that you want to remove all events from the schedule and save (y/n)? ").strip().lower() == 'y':
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
        print()
except SystemExit:
    pass
except:
    logging.critical("CRITICAL ERROR: Exception:\n" + traceback.format_exc())


# CHANGE DIRECTORY BACK TO CALLING DIRECTORY
os.chdir(calling_dir)  # return the directory to the calling directory


# TODO: decide if/how to segregate "due" events versus attendance events
# TODO: add duration
# TODO: add some sort of totals of durations, and totals by event type
# TODO: add day of week and 'next' day of week as acceptable date inputs, have date possess a date put also a weekday
# TODO: add command to just change the date and or time or duration of an event
# TODO: figure out the os Traceback occurring from 'python Scheduler.py' run in the project directory in the command line
# TODO: add some manner of feature regarding removing events that have passed
# TODO: consider allowing capital letters in input besides commands
# TODO: put back in info logging of commands without console output
