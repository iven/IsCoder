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
import gobject
import os

from IsCoder.Constants import *

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("iscoder", DataDir + "/locale")
gettext.textdomain("iscoder")
_ = gettext.gettext

class AboutDialog(gtk.AboutDialog):
    "About Dialog"

    def __init__(self, parent):
        gtk.AboutDialog.__init__(self)
        self.set_transient_for(parent)

        self.set_name("IsCoder")
        self.set_version(Version)
        self.set_comments(_("This is a simple GUI frontend of mencoder."))
        self.set_copyright("Copyright \xC2\xA9 2009 Iven Day (Xu Lijian)")
        self.set_authors(["Iven Day (Xu Lijian) <ivenvd@gmail.com>",])
        self.set_website("http://www.kissuki.com/")

class CategoriesBox(gtk.VBox):
    "Category buttons group in the left pane"

    __gsignals__ = {"category-changed": (gobject.SIGNAL_RUN_FIRST,
                                         gobject.TYPE_NONE,
                                         [str]),
                                         }

    def __init__(self):
        gtk.VBox.__init__(self)

        self.set_border_width(5)

        self.buttons = {}
        for category, label in Categories:
            button = self.create_button(category, label)
            self.pack_start(button, False)
            self.buttons[category] = button

    def create_button(self, category, label):
        button = gtk.Button()
        button.set_size_request(180, 50)
        imagepath = PixmapDir + category + ".png"
        if os.path.exists(imagepath):
            image = gtk.Image()
            image.set_from_file(imagepath)
            button.set_image(image)

        button.set_label(label)

        button.connect('clicked', self.on_button_clicked_cb, category)
        button.show()

        return button

    def on_button_clicked_cb(self, widget, category):
        self.emit("category-changed", category)
