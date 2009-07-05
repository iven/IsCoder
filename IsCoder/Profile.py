#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This file is part of IsCoder.

# IsCoder is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# IsCoder is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Iven Day (Xu Lijian) <ivenvd@gmail.com>
# Copyright (C) 2009 Iven Day

import os
import ConfigParser
from UserDict import UserDict
from os.path import join as path_join
from xdg.BaseDirectory import xdg_config_home

ProfileDir = path_join(xdg_config_home, "iscoder/profiles")

class Profile(ConfigParser.RawConfigParser):
    "Manage mencoder profiles"

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self, 
                {"oac": "copy=true", "ovc": "copy=true"})

        self.read("last_time")

    def read(self, name):
        profile = os.path.join(ProfileDir, name)
        try:
            ConfigParser.RawConfigParser.read(self, profile)
        except (ConfigParser.MissingSectionHeaderError,
                ConfigParser.ParsingError,
                IOError,):
            pass

        for key in self.defaults():
            value = self.defaults()[key]
            if key in ('af', 'vf'):
                self.defaults()[key] = Option(value, ',')
            else:
                self.defaults()[key] = Option(value, ':')

    def write(self, name = "last_time"):
        try:
            os.makedirs(ProfileDir)
        except OSError:
            pass
        filename = os.path.join(ProfileDir, name)
        with open(filename, 'w') as f:
            ConfigParser.RawConfigParser.write(self, f)

class Option(UserDict):
    "An option line in the profile"

    def __init__(self, str, separator):
        UserDict.__init__(self)

        self.list = []
        self.separator = separator

        for suboption in str.split(self.separator):
            k, v = suboption.split('=')
            self.list.append(k)
            self[k] = v

    def __str__(self):
        return self.separator.join(["%s=%s" % (item, self[item]) for item in self.list])

    def __setitem__(self, key, item):
        if key not in self.list:
            self.list.append(key)
        UserDict.__setitem__(self, key, item)
