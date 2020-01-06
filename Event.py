"""
Classfile

Written by Cole Anderson
"""



# CLASS
class Event:

    def __init__(self, date: str, time: str, event_type: str, description: str):
        """
        NOTE: ALL ARGUMENTS FOR THIS FUNCTION MUST BE SAME AS THE NAMES OF FIELDS
        :param date: date of event
        :param time: time of event
        :param event_type:
        :param description: string identifying event
        """
        self.date = date
        self.time = time
        self.event_type = event_type
        self.description = description


    @classmethod
    def from_load_in_string(cls, load_in_string: str):
        """
        Secondary constructor
        :param load_in_string: of the type returned from to_load_in_string
        :return: (Event) new Event object
        """
        params = load_in_string.split("|")
        return cls(params[0], params[1], params[2], params[3])


    def to_load_in_string(self):
        return self.date + "|" + self.time + "|" + self.event_type + "|" + self.description


    def __repr__(self):
        return "dtime: " + self.date + ", time: " + self.time + ", event_type: " + self.event_type + ", description: " + self.description
