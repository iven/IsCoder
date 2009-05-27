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
import os

from IsCoder.Constants import *

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("iscoder", DataDir + "/locale")
gettext.textdomain("iscoder")
_ = gettext.gettext

class LargeButton(gtk.Button):
    "Large buttons in the left pane"

    def __init__(self, label_text = "", image_path = None):
        gtk.Button.__init__(self)
        self.set_size_request(180, 45)

        hbox = gtk.HBox()
        self.add(hbox)

        align = gtk.Alignment(0, .5, 1, 1)
        align.set_padding(0, 0, 0, 10)
        hbox.pack_start(align, False, False)

        if image_path and os.path.exists(image_path):
            image = gtk.Image()
            image.set_from_file(image_path)
            align.add(image)

        label = gtk.Label()
        label.set_markup("<span size='medium'>%s</span>" % label_text)
        hbox.pack_start(label, True, True)

    def highlight(self):
        pass

    def unhighlight(self):
        pass


class LargeLabel(gtk.Label):
    "Large label in the left pane"

    def __init__(self, value = ""):
        gtk.Label.__init__(self)
        self.set_markup("<span size=\"x-large\">%s</span>" % value)
        self.props.xalign = 0

