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
import pango
import os

from IsCoder.Constants import *

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("iscoder", DataDir + "/locale")
gettext.textdomain("iscoder")
_ = gettext.gettext

IconTheme = gtk.icon_theme_get_default()
if not IconDir in IconTheme.get_search_path():
    IconTheme.prepend_search_path(IconDir)

class LargeButton(gtk.Button):
    "Large buttons in the left pane"

    def __init__(self, image, text):
        gtk.Button.__init__(self)

        self.set_size_request(180, -1)
        self.set_relief(gtk.RELIEF_NONE)

        hbox = gtk.HBox()
        self.add(hbox)

        align = gtk.Alignment(0, .5, 1, 1)
        align.set_padding(2, 0, 5, 10)
        align.add(image)
        hbox.pack_start(align, False, False)

        label = Label("<span size='medium'>%s</span>" % text)
        hbox.pack_start(label, True, True)

class CategoryButton(LargeButton, gtk.ToggleButton):

    def __init__(self, image, text):
        LargeButton.__init__(self, image, text)
        gtk.ToggleButton.__init__(self)
        self.connect("expose-event", self.expose_event_cb)

    def expose_event_cb(self, *args):
        if self.flags() & gtk.HAS_FOCUS:
            self.unset_flags(gtk.HAS_FOCUS)

class Label(gtk.Label):

    def __init__(self, markup = "", wrap = 120):
        gtk.Label.__init__(self)
        self.set_markup(markup)
        self.props.xalign = 0
        self.props.wrap_mode = pango.WRAP_WORD
        self.set_line_wrap(True)
        self.set_size_request(wrap, -1)

class HeaderLabel(Label):

    def __init__(self, value = ""):
        Label.__init__(self)
        self.style_block = 0
        self.set_markup("<span size='large' weight='800'>%s</span>" % value)
        self.connect("style-set", self.style_set_cb)

    def style_set_cb(self, *args):
        if self.style_block > 0:
            return
        self.style_block += 1
        for state in (gtk.STATE_NORMAL, gtk.STATE_PRELIGHT, gtk.STATE_ACTIVE):
            self.modify_fg(state, self.style.bg[gtk.STATE_SELECTED])
        self.style_block -= 1

class Image(gtk.Image):

    def __init__(self, name = None, type = ImageNone, size = 24):
        gtk.Image.__init__(self)

        if name is None:
            return
        try:
            if type == ImageStock:
                self.set_from_stock(name, size)
                return
            elif type == ImageCategory:
                name = "category-" + name.lower()
                pixbuf = IconTheme.load_icon(name, size, 0)
            else:
                raise gobject.GError
            self.set_from_pixbuf(pixbuf)
        except gobject.GError:
            self.set_from_stock(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_BUTTON)
