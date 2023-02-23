"""
Classfile

Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# ENUMS
class ENUM_Event_Type:
    ATTN = "ATTN"  # attendance
    DEAD = "DEAD"  # deadline


# CLASS
class Event:

    def __init__(self, date: str, time: str, event_type: str, duration: int, tag: str, description: str):
        """
        NOTE: ALL ARGUMENTS FOR THIS FUNCTION MUST BE SAME AS THE NAMES OF FIELDS (THAT ASSUMPTION IS CARRIED)
        :param date: date of event
        :param time: time of event
        :param event_type: MUST BE A VALUE OF ENUM_Event_Type
        :param duration: a non-negative number in minutes, expected value depends on event_type
        :param tag: a string making any general classification among different Event instances to group them
        :param description: string identifying event
        """
        self.date = date
        self.time = time
        self.event_type = event_type
        self.duration = duration
        self.tag = tag
        self.description = description


    @classmethod
    def from_load_in_string(cls, load_in_string: str):
        """
        Secondary constructor
        :param load_in_string: of the type returned from to_load_in_string
        :return: (Event) new Event object
        """
        params = load_in_string.split("|")
        return cls(date=params[0], time=params[1], event_type=params[2], duration=int(params[3]), tag=params[4],
                description=params[5])


    def to_load_in_string(self):
        return self.date + "|" + self.time + "|" + self.event_type + "|" + str(self.duration) + "|" + self.tag + "|" + \
                self.description


    def __repr__(self):
        return str(self.__dict__)
