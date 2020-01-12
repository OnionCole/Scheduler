"""
Classfile

Written by Cole Anderson
"""



# IMPORTS
from sortedcontainers import SortedDict

from Event import Event


# CLASS
class Schedule:

    def __init__(self, load_in_events=None):
        """
        :param load_in_events: (list) optional input, used to load in events where each event is represented by a string parseable by the Event class
        """
        self.__events = SortedDict()  # {date:{time:{id:event}}}, where the id is a unique number across the dict always > 0
        self.__highest_event_id = 1

        if load_in_events is not None:
            for load_in_event in load_in_events:
                self.add_event(event_load_in_string=load_in_event)


    def __repr__(self):
        repr_s = "SCHEDULE:\n"
        for date, time_dict in self.__events.items():
            repr_s += "\n" + date + ":"
            for time, id_dict in time_dict.items():
                for id, event in id_dict.items():
                    repr_s += "\n\t\t" + time + ": " + str(id) + ": " + event.event_type + ", " + event.description
        return repr_s


    def add_event(self, event_load_in_string=None, **event_kwargs) -> (int, str):
        """
        Add new event
        :param event_load_in_string: (string) optional load in string that Event can parse into an event, if present will be used instead of kwargs
        :param event_kwargs: kwargs for the new event
        :return: First Return Element: the id of the new event
        Second Return Element: the string representation of the new event
        """

        # create the new event
        new_event = Event(**event_kwargs) if event_load_in_string is None else Event.from_load_in_string(event_load_in_string)

        # add entries for the date and time of the new event if they do not yet exist
        if new_event.date not in self.__events:
            self.__events[new_event.date] = SortedDict()
        if new_event.time not in self.__events[new_event.date]:
            self.__events[new_event.date][new_event.time] = SortedDict()

        # get the new id for the new event
        new_event_id = self.__highest_event_id + 1

        # add the new event
        self.__events[new_event.date][new_event.time][new_event_id] = new_event

        # adjust the highest event id
        self.__highest_event_id = new_event_id

        return new_event_id, str(new_event)


    def delete_event(self, event_id) -> (dict or None):
        """
        Delete an event
        :param event_id:
        :return: __dict__ of deleted event if event was deleted, None otherwise
        """
        for date, time_dict in self.__events.items():
            for time, id_dict in time_dict.items():
                for id in id_dict.keys():
                    if event_id == id:  # if we found the id of the event that we are looking to delete
                        rtn = id_dict[event_id].__dict__
                        del id_dict[event_id]

                        # remove now empty dicts
                        if not id_dict:
                            del time_dict[time]
                            if not time_dict:
                                del self.__events[date]

                        return rtn
        return None


    def replace_event(self, replaced_event_id: int, decline_value: str, **replacement_event_kwargs) -> (int, str):
        """
        Replace an event, does not create the new event if the old fails to delete
        :param replaced_event_id:
        :param decline_value: if a value in replacement_event_kwargs matches this value, use the value from the event being replaced
        :param replacement_event_kwargs:
        :return: First Return Element: -1 if failure, id of new event otherwise
        Second Return Element: None if deletion failed, otherwise the string representation of the modified event
        """
        dict_of_deleted_event = self.delete_event(event_id=replaced_event_id)
        if dict_of_deleted_event is None:  # the deletion failed
            return -1, None

        # replace intended empty values with the values of the deleted event
        for key, value in replacement_event_kwargs.items():
            if value == decline_value:
                replacement_event_kwargs[key] = dict_of_deleted_event[key]

        return self.add_event(**replacement_event_kwargs)


    def list_of_load_in_strings_for_events(self) -> list:
        """
        Get list of load in strings for all events held in the Schedule object
        :return:
        """
        return [event.to_load_in_string() + '\n' for time_dict in self.__events.values() for id_dict in time_dict.values() for event in id_dict.values()]
