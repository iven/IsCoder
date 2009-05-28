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
from IsCoder.Utils import *

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
                                         [str])}
    def __init__(self):
        gtk.VBox.__init__(self)

        self.current_button = None
        self.buttons = {}
        self.toggle_block = 0
        self.set_border_width(5)

        for name, label in Categories:
            image = Image(name, type = ImageCategory)
            button = CategoryButton(image, label)
            button.connect('clicked', self.on_button_clicked_cb)
            self.pack_start(button, False)

            self.buttons[button] = name
            if name == "General":
                button.clicked()

    def on_button_clicked_cb(self, widget):
        if self.toggle_block > 0:
            return False
        self.toggle_block += 1
        if widget is not self.current_button:
            if self.current_button:
                self.current_button.set_active(False)
            self.current_button = widget
            self.emit("category-changed", self.buttons[widget])
        widget.set_active(True)
        self.toggle_block -= 1

class ProfileBox(gtk.VBox):
    "Profile Box in the left pane"

    def __init__(self):
        gtk.VBox.__init__(self)

        self.set_border_width(5)

        tree_view = gtk.TreeView()
        self.pack_start(tree_view, True, True, 2)

        image = Image(name = gtk.STOCK_OPEN, type = ImageStock,
                size = gtk.ICON_SIZE_LARGE_TOOLBAR)
        button = LargeButton(image, _("Load Profile..."))
        self.pack_start(button, False)

        image = Image(name = gtk.STOCK_SAVE, type = ImageStock,
                size = gtk.ICON_SIZE_LARGE_TOOLBAR)
        button = LargeButton(image, _("Save Profile..."))
        self.pack_start(button, False)

class PluginsBook(gtk.Notebook):
    "Plugins notebook in the right pane"

    def __init__(self):
        gtk.Notebook.__init__(self)

        # TODO
        self.set_show_tabs(True)
