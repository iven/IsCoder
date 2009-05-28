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
import vte

from IsCoder.Constants import *
from IsCoder.Widgets import *

import locale
import gettext
locale.setlocale(locale.LC_ALL, "")
gettext.bindtextdomain("iscoder", DataDir + "/locale")
gettext.textdomain("iscoder")
_ = gettext.gettext

class MainWin(gtk.Window):
    "Main Window"

    def __init__(self):
        gtk.Window.__init__(self)

        # Enable RGBA colormap support
        colormap = self.get_screen().get_rgba_colormap()
        if colormap:
            gtk.widget_set_default_colormap(colormap)

        # Basic settings
        self.set_default_size(840, 640)
        self.set_title(_("IsCoder - I'm a Simple Encoder"))
        self.connect("destroy", self.quit_cb)
        gtk.window_set_default_icon_name("iscoder")

        # Start packing widgets
        main_vbox = gtk.VBox()
        self.add(main_vbox)

        # MenuBar and ToolBar
        uimanager = self.get_uimanager()

        menubar = uimanager.get_widget('/MenuBar')
        main_vbox.pack_start(menubar, False)

        # Main Panes
        main_hpaned = gtk.HPaned()
        main_vbox.pack_start(main_hpaned)

        # Left Pane
        left_pane = gtk.VBox()
        left_pane.set_border_width(5)
        main_hpaned.pack1(left_pane, False, False)

        label = HeaderLabel("Categories")
        left_pane.pack_start(label, False)

        cate_box = CategoriesBox()
        cate_box.connect("category-changed", self.on_category_changed)
        left_pane.pack_start(cate_box, False, False)

        label = HeaderLabel("Profile")
        left_pane.pack_start(label, False)

        profile_box = ProfileBox()
        left_pane.pack_start(profile_box, True, True)

        # Right Pane
        right_pane = gtk.VBox()
        main_hpaned.pack2(right_pane)

        notebook = PluginsBook()
        right_pane.pack_start(notebook)

        #terminal = vte.Terminal()
        #right_pane.pack_start(terminal)
        #terminal.fork_command()

    def get_uimanager(self):
        ui = """<ui>
                    <menubar name="MenuBar">
                        <menu action="File">
                            <menuitem action="Quit"/>
                        </menu>
                        <menu action="Help">
                            <menuitem action="About"/>
                        </menu>
                    </menubar>
                </ui>"""

        uimanager = gtk.UIManager()

        accel_group = uimanager.get_accel_group()
        self.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('MainWin')
        action_group.add_actions([
            ('File', None, '_File'),
            ('Quit', gtk.STOCK_QUIT, '_Quit', '<Control>Q', 'Quit the Program', self.quit_cb),
            ('Help', None, '_Help'),
            ('About', gtk.STOCK_ABOUT, '_About', None, 'About IsCoder', self.show_about_cb),
            ])
        uimanager.insert_action_group(action_group, 0)

        uimanager.add_ui_from_string(ui)

        return uimanager

    def on_category_changed(self, widget, category):
        print category

    def show_about_cb(self, *args):
        about_dialog = AboutDialog(self)
        about_dialog.run()
        about_dialog.destroy()

    def quit_cb(self, *args):
        gtk.widget_pop_colormap()
        gtk.main_quit()

if __name__ == "__main__":
    MainWin().show_all()
    gtk.main()
