"""
Classfile

Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# IMPORTS
from abc import ABC, abstractmethod


# ENUMS
class ENUM_Event_Type:
    ATND = "ATND"  # attendance
    DDLN = "DDLN"  # deadline


# ABSTRACT CLASS
class Base_Event(ABC):

    @classmethod
    @abstractmethod
    def from_load_in_string(cls, load_in_string: str):
        event = Attendance_Event.from_load_in_string(load_in_string)
        if event is None:  # load in string was not identified to represent an Attendance event
            event = Deadline_Event.from_load_in_string(load_in_string)
        return event  # could, in an error case where the load_in_string could not be parsed, be
                # None

    @abstractmethod
    def to_load_in_string(self):
        pass

    def __repr__(self):
        return str(self.__dict__)


# DERIVED CLASSES

class Attendance_Event(Base_Event):
    event_type = ENUM_Event_Type.ATND

    def __init__(self, date: str, time: str, end_time: str, tag: str, description: str):
        """
        NOTE: ALL ARGUMENTS FOR THIS FUNCTION MUST BE SAME AS THE NAMES OF FIELDS (THAT ASSUMPTION
                IS CARRIED)
        :param date: date of event
        :param time: time of event
        :param end_time: end time of event
        :param tag: a string making any general classification among different Event instances to
                group them
        :param description: string identifying event
        """
        self.date = date
        self.time = time
        self.end_time = end_time
        self.tag = tag
        self.description = description


    @classmethod
    def from_load_in_string(cls, load_in_string: str):
        """
        Secondary constructor
        :param load_in_string: of the type returned from to_load_in_string
        :return:
            if the event type in the load in string matches this subclass of Event:
                new Attendance_Event object
            else:
                None
        """
        params = load_in_string.split("|")
        return cls(date=params[1], time=params[2], end_time=params[3], tag=params[4],
                description=params[5]) if params[0] == cls.event_type else None


    def to_load_in_string(self):
        return self.event_type + "|" + self.date + "|" + self.time + "|" + self.end_time + "|" + \
                self.tag + "|" + self.description


class Deadline_Event(Base_Event):
    event_type = ENUM_Event_Type.DDLN

    def __init__(self, date: str, time: str, duration: int, tag: str, description: str):
        """
        NOTE: ALL ARGUMENTS FOR THIS FUNCTION MUST BE SAME AS THE NAMES OF FIELDS (THAT ASSUMPTION
                IS CARRIED)
        :param date: date of event
        :param time: time of event
        :param duration: a non-negative number in minutes, expected value depends on event_type
        :param tag: a string making any general classification among different Event instances to
                group them
        :param description: string identifying event
        """
        self.date = date
        self.time = time
        self.duration = duration
        self.tag = tag
        self.description = description


    @classmethod
    def from_load_in_string(cls, load_in_string: str):
        """
        Secondary constructor
        :param load_in_string: of the type returned from to_load_in_string
        :return:
            if the event type in the load in string matches this subclass of Event:
                new Deadline_Event object
            else:
                None
        """
        params = load_in_string.split("|")
        return cls(date=params[1], time=params[2], duration=int(params[3]), tag=params[4],
                description=params[5]) if params[0] == cls.event_type else None


    def to_load_in_string(self):
        return self.event_type + "|" + self.date + "|" + self.time + "|" + str(self.duration) + \
               "|" + self.tag + "|" + self.description

