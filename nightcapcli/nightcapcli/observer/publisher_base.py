#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
# region Imports
from uuid import uuid4

# endregion


class NightcapCLIPublisherBase(object):
    """

    This class is used as the base publisher

    ...

    Attributes
    ----------
        channles: -> list
            A list of all the current channels attached to the observer

    Methods
    -------
        Accessible
        -------
            get_channel(self, channel): -> dict
                returns the channel information

            new_channel(self): -> uid
                creates a new channel

            register(self, channel, who, callback=None, attr=None):
                register an object to the observer

            unregister(self, channel, who):
                unregister from the observer

            del_channel(self, channel):
                delete a channel

            dispatch(self, channel, message):
                send message to channel
    """

    def __init__(self, channels) -> None:
        self.channels = {channel: dict() for channel in channels}

    def get_channel(self, channel) -> dict:
        return self.channels[channel]

    def new_channel(self) -> str:
        _uid = uuid4().hex
        if _uid not in dict(self.channels).keys():
            self.channels[_uid] = dict()
            return _uid
        else:
            self.new_channel()

    def register(self, channel, who, callback=None, attr=None) -> dict:
        if callback is None:
            if attr is None:
                callback = getattr(who, "cli_update")
            else:
                callback = getattr(who, attr)
        self.get_channel(channel)[who] = callback

    def unregister(self, channel, who) -> None:
        del self.get_channel(channel)[who]

    def del_channel(self, channel) -> None:
        del self.channels[channel]

    def dispatch(self, channel, message) -> None:
        for subscriber, callback in dict(self.get_channel(channel)).items():
            callback(message)
