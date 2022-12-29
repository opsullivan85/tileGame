from dataclasses import dataclass
from typing import Callable, Any, Union, Dict


class CallbackHandler:
    """ Class to manage listening to callbacks
    """

    @dataclass
    class Callback:
        """ Data class to store a callable and whether it should be called only once
        """
        callable: Callable[..., Any]
        one_time: bool

        def __eq__(self, other: Union['CallbackHandler.Callback', Callable[..., Any]]) -> bool:
            """ If the callable is the same, then they are equal. Importantly ignores the one_time attribute.
            This is done because the value of one_time is not known except at the time of adding the callable.

            :param other: other Callback object, or a callable
            :return: True if the callbacks are the same, False otherwise
            """
            if isinstance(other, CallbackHandler.Callback):
                return self.callable == other.callable
            elif callable(other):
                return self.callable == other
            else:
                return False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listeners: Dict[Callable[..., bool], CallbackHandler.Callback] = {}

    def add_callback(self, event: Callable[..., bool], callback: Callable[..., Any], one_time: bool = False) -> bool:
        """ Adds a listener to the event.
        Having the same event / callable pair will not add a duplicate listener regaurdless of the one_time value.

        :param event: The event to listen to
        :param callback: The callable to call when the event is triggered
        :param one_time: If the callable should only be called once
        :return: If the listener was successfully added
        """
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(CallbackHandler.Callback(callback, one_time))
        return True

    # TODO: Add a handles for removing callbacks easier
    def remove_callback(self, event: Callable[..., bool], callback: Callable[..., Any]) -> bool:
        """ Removes a listener from the event.

        :param event: The event to listen to
        :param callback: The callable to call when the event is triggered
        :return: If the listener was successfully added
        """
        if event in self._listeners:
            try:
                # my understanding is that this should work even though
                # self.listeners[event] is a list of Callback objects, they should show up as equal
                self._listeners[event].remove(callback)
            except ValueError:
                # Early return here is okay because there should still be other callbacks on the event
                return False  # Callback was not in list
            if not self._listeners[event]:  # remove the listener if empty
                del self._listeners[event]
        return True

    def check_callbacks(self):
        """ Checks if any callbacks should be called, and calls them if they should be.
        """
        removals: Dict[Callable[..., bool], CallbackHandler.Callback] = {}  # List of callbacks to remove
        for event, callbacks in self._listeners.items():
            if event():
                # reversed so the removal trick works
                for callback in reversed(callbacks):
                    callback.callable()
                    if callback.one_time:
                        removals[event] = callback

        for event, callback in removals.items():
            self.remove_callback(event, callback.callable)

    def clear_callbacks(self):
        """ Clears all callbacks
        """
        self._listeners.clear()
