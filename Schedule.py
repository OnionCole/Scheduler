"""
Classfile

Written by Cole Anderson
"""
__author__ = "Cole Anderson"



# IMPORTS
from sortedcontainers import SortedDict

from Event import Event


# FUNCTIONS
def get_duration_print_str(duration: int) -> str:
    """
    Get a print string that represents a duration
    :param duration: non-negative number of minutes
    :return:
    """
    hours = int(duration / 60)
    minutes = duration % 60
    return (" " if hours < 100 else "") + (" " if hours < 10 else "") + str(hours) + "H" + \
            (
                (
                    ("0" if minutes < 10 else "") + str(minutes)
                ) if minutes else "  "
            )


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
                self._add_event_from_load_in_str(event_str=load_in_event)


    def __repr__(self):
        repr_s = "SCHEDULE:\n"
        if bool(self.__events):
            for date, time_dict in self.__events.items():
                repr_s += "\n" + date + ":"
                for time, id_dict in time_dict.items():
                    for id_, event in id_dict.items():
                        repr_s += "\n\t\t" + time + ": " + str(id_) + ": " + event.event_type + ": (" + \
                                get_duration_print_str(event.duration) + "), " + event.tag + ": " + event.description
        else:
            repr_s += "\nSchedule is empty."
        return repr_s


    def add_event(self, date: str, time: str, event_type: str, duration: int, tag: str, description: str) -> (int, str):
        """
        Add an event from args
        :param date:
        :param time:
        :param event_type:
        :param duration:
        :param tag:
        :param description:
        :return: First Return Element: the id of the new event
        Second Return Element: the string representation of the new event
        """
        new_event = Event(date=date, time=time, event_type=event_type, duration=duration, tag=tag,
                description=description)
        return self._add_event_instance(new_event), str(new_event)


    def _add_event_from_load_in_str(self, event_str: str) -> int:
        """
        Add an event from an event load in string that Event can parse into an Event instance
        :param event_str:
        :return: the id of the new event
        """
        return self._add_event_instance(Event.from_load_in_string(event_str))


    def _add_event_instance(self, event: Event) -> int:
        """
        Add an Event instance to the Schedule
        :param event:
        :return: the id of the new event
        """

        # add entries for the date and time of the new event if they do not yet exist
        if event.date not in self.__events:
            self.__events[event.date] = SortedDict()
        if event.time not in self.__events[event.date]:
            self.__events[event.date][event.time] = SortedDict()

        # get the new id for the new event
        event_id = self.__highest_event_id + 1

        # add the new event
        self.__events[event.date][event.time][event_id] = event

        # adjust the highest event id
        self.__highest_event_id = event_id

        return event_id


    def delete_event(self, event_id: int) -> (Event or None):
        """
        Delete an event
        :param event_id:
        :return: "deleted" Event instance if event was deleted, None otherwise
        """
        for date, time_dict in self.__events.items():
            for time, id_dict in time_dict.items():
                for id_ in id_dict.keys():
                    if event_id == id_:  # if we found the id of the event that we are looking to delete
                        rtn = id_dict[event_id]
                        del id_dict[event_id]

                        # remove now empty dicts
                        if not id_dict:
                            del time_dict[time]
                            if not time_dict:
                                del self.__events[date]

                        return rtn
        return None


    def replace_event(self, replaced_event_id: int, date: str=None, time: str=None, event_type: str=None,
            duration: int=None, tag: str=None, description: str=None) -> (int, str):
        """
        Replace an event, does not create the new event if the old fails to delete, pass in None for an Event arg to retain current value for that arg
        :param replaced_event_id:
        :param date:
        :param time:
        :param event_type:
        :param duration:
        :param tag:
        :param description:
        :return: First Return Element: -1 if failure, id of new event otherwise
        Second Return Element: None if deletion failed, otherwise the string representation of the modified event
        """

        # try delete event
        deleted_event_instance = self.delete_event(event_id=replaced_event_id)
        if deleted_event_instance is None:  # the deletion failed
            return -1, None

        # add new event
        return self.add_event(date=deleted_event_instance.date if date is None else date,
                time=deleted_event_instance.time if time is None else time,
                event_type=deleted_event_instance.event_type if event_type is None else event_type,
                duration=deleted_event_instance.duration if duration is None else duration,
                tag=deleted_event_instance.tag if tag is None else tag,
                description=deleted_event_instance.description if description is None else description)


    def list_of_load_in_strings_for_events(self) -> list:
        """
        Get list of load in strings for all events held in the Schedule object
        :return:
        """
        return [event.to_load_in_string() + '\n' for time_dict in self.__events.values() for id_dict in time_dict.values() for event in id_dict.values()]
