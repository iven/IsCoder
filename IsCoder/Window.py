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
from IsCoder.Widgets import *
from IsCoder.Pages import *
from IsCoder.Profile import *

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

        self.profile = Profile()

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
        uimanager = self.__get_uimanager()

        menubar = uimanager.get_widget('/MenuBar')
        main_vbox.pack_start(menubar, False)

        toolbar = uimanager.get_widget('/ToolBar')
        toolbar.set_icon_size(gtk.ICON_SIZE_LARGE_TOOLBAR)
        toolbar.set_style(gtk.TOOLBAR_BOTH)
        main_vbox.pack_start(toolbar, False)

        # Main Panes
        main_hpaned = gtk.HPaned()
        main_vbox.pack_start(main_hpaned)

        # Right Pane
        self.right_pane = gtk.Frame()
        self.right_pane.set_shadow_type(gtk.SHADOW_NONE)
        self.right_pane.set_border_width(5)
        main_hpaned.pack2(self.right_pane)

        self.categories= {}
        for name, label in Categories:
            self.categories[name] = CategoryPage(name)

        # Left Pane
        left_pane = gtk.VBox()
        left_pane.set_border_width(5)
        main_hpaned.pack1(left_pane, False, False)

        label = HeaderLabel("Categories")
        left_pane.pack_start(label, False)

        self.cate_box = CategoriesBox(self)
        left_pane.pack_start(self.cate_box, False, False)

        label = HeaderLabel("Profile")
        left_pane.pack_start(label, False)

        profile_box = ProfileBox(self)
        left_pane.pack_start(profile_box, True, True)

    def __get_uimanager(self):
        ui = """<ui>
                    <menubar name="MenuBar">
                        <menu action="File">
                            <menuitem action="Add" />
                            <menuitem action="Remove" />
                            <menuitem action="Clear" />
                            <separator name="sep1" />
                            <menuitem action="Command" />
                            <separator name="sep2" />
                            <menuitem action="Quit" />
                        </menu>
                        <menu action="Process">
                            <menuitem action="Start" />
                            <menuitem action="Pause" />
                            <menuitem action="Stop" />
                        </menu>
                        <menu action="Help">
                            <menuitem action="About"/>
                        </menu>
                    </menubar>
                    <toolbar name="ToolBar">
                        <toolitem action="Add" />
                        <toolitem action="Remove" />
                        <toolitem action="Clear" />
                        <separator name="sep1" />
                        <toolitem action="Command" />
                        <separator name="sep2" />
                        <toolitem action="Start" />
                        <toolitem action="Pause" />
                        <toolitem action="Stop" />
                    </toolbar>
                </ui>"""

        uimanager = gtk.UIManager()

        accel_group = uimanager.get_accel_group()
        self.add_accel_group(accel_group)

        action_group = gtk.ActionGroup('MainWin')
        action_group.add_actions([
            ('File', None, '_File'),
            ('Process', None, '_Process'),
            ('Help', None, '_Help'),
            ('Quit', gtk.STOCK_QUIT, '_Quit', '<Control>Q', 'Quit the Program', self.quit_cb),
            ('About', gtk.STOCK_ABOUT, '_About', None, 'About IsCoder', self.show_about_cb),
            ('Add', gtk.STOCK_ADD, 'Add', '<Control>A', 'Add files to the file list', None),
            ('Remove', gtk.STOCK_REMOVE, 'Remove', '<Control>R', 'Remove files from the file list', None),
            ('Clear', gtk.STOCK_CLEAR, 'Clear', '<Control>C', 'Clear all files in the file list', None),
            ('Command', gtk.STOCK_EXECUTE, 'Command', '<Control>T', 'Show Command Line', None),
            ('Start', gtk.STOCK_MEDIA_PLAY, 'Start', '<Control>Return', 'Start Encoding', None),
            ('Pause', gtk.STOCK_MEDIA_PAUSE, 'Pause', '<Control>P', 'Pause Encoding', None),
            ('Stop', gtk.STOCK_MEDIA_STOP, 'Stop', '<Control>S', 'Stop Encoding', None),
            ])
        uimanager.insert_action_group(action_group, 0)

        uimanager.add_ui_from_string(ui)

        return uimanager

    def set_page(self, category):
        "Being called when the category buttons is clicked."
        child = self.right_pane.get_child()
        if child is not None:
            self.right_pane.remove(child)
        self.right_pane.add(self.categories[category])
        self.right_pane.show_all()

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
