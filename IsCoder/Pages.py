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

import pygtk
import gtk

from IsCoder.Constants import *
from IsCoder import Plugins

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("iscoder", DataDir + "/locale")
gettext.textdomain("iscoder")
_ = gettext.gettext

class CategoryPage(gtk.Notebook):
    "Plugin page in the right pane"

    def __init__(self, category):
        gtk.Notebook.__init__(self)

        self.set_scrollable(True)

        self.plugins = []

        for name in dir(Plugins):
            if not name.startswith('_'):
                plugin = getattr(getattr(Plugins, name),
                        'plugin', Plugins.Empty)
                if plugin.category is category:
                    self.append_page(plugin, gtk.Label(plugin.plugin_name))
                    self.plugins.append(plugin)
