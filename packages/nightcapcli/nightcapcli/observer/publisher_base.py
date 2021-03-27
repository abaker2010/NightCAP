#!/usr/bin/env python3.8
# Copyright 2020 by Aaron Baker.
# All rights reserved.
# This file is part of the Nightcap Project,
# and is released under the "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.
from uuid import uuid4

class NightcapCLIPublisherBase:
    def __init__(self, channels):
        self.channels = { channel : dict()
                            for channel in channels }
    
    def get_channel(self, channel):
        return self.channels[channel]

    def new_channel(self):
        _uid = uuid4().hex
        if _uid not in dict(self.channels).keys():
            self.channels[_uid] = dict()
            return _uid
        else:
            self.new_channel()

    def register(self, channel, who, callback=None, attr=None):
        if callback is None:
            if attr is None:
                callback = getattr(who, 'cli_update')
            else:
                callback = getattr(who, attr)
        self.get_channel(channel)[who] = callback

    def unregister(self, channel, who):
        del self.get_channel(channel)[who]

    def del_channel(self, channel):
        del self.channels[channel]

    def dispatch(self, channel, message):
        for subscriber, callback in dict(self.get_channel(channel)).items():
            callback(message)