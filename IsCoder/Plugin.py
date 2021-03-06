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

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("iscoder", DataDir + "/locale")
gettext.textdomain("iscoder")
_ = gettext.gettext

class Plugin(gtk.ScrolledWindow):
    """Plugin class, all plugins should be inherited from this."""

    def __init__(self, pname = "", cname = "", widgets = ()):
        gtk.ScrolledWindow.__init__(self)

        self.pname = pname
        self.cname = cname
        self.widgets = widgets

        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)

        viewport = gtk.Viewport()
        viewport.set_shadow_type(gtk.SHADOW_NONE)
        self.add(viewport)

        vbox = gtk.VBox()
        vbox.set_border_width(5)
        viewport.add(vbox)

        for widget in widgets:
            vbox.pack_start(widget, False, False)
