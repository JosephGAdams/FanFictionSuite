# -*- coding: utf-8 -*-
import wx
import wx.html
import os
import os.path
import re
import ConfigParser
from classes.general_utils import utils

util = utils()


class ReadFanfiction(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

# Defaults
        self.page = ''
        self.current_chapter = 0

# Html setup
        self.html_window = wx.html.HtmlWindow(self, -1, size=(800, 600),
            style= wx.BORDER_RAISED)
        self.html_window_size = self.html_window.GetSize()
        self.html_window.SetPage(self.page)

# Sizers here

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        widget_sizer = wx.BoxSizer(wx.VERTICAL)
        self.container_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tool_sizer = wx.BoxSizer(wx.VERTICAL)
        open_folder_sizer = wx.BoxSizer(wx.HORIZONTAL)
        navigation_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sec_nav_sizer = wx.BoxSizer(wx.HORIZONTAL)
        story_display_sizer = wx.BoxSizer(wx.HORIZONTAL)
        jump_sizer = wx.BoxSizer(wx.VERTICAL)

# Objects here
        self.open_folder_button = wx.Button(self, -1, 'Open')

        self.next_page_button = wx.Button(self, -1, 'next')
        self.next_button_size = self.next_page_button.GetSize()
        self.previous_page_button = wx.Button(self, -1, 'back')
        self.back_button_size = self.previous_page_button.GetSize()

        self.jump_to_list = wx.ListBox(self, -1, size=(100, 600))
        self.to_list_size = self.jump_to_list.GetSize()

        self.sec_next_page_button = wx.Button(self, -1, 'next')
        self.sec_prev_page_button = wx.Button(self, -1, 'back')

# Add objects to sizers here
        story_display_sizer.Add(self.html_window, 0)

        jump_sizer.Add(self.jump_to_list, 0, wx.LEFT, 10)

        navigation_sizer.Add(self.previous_page_button, 0)
        navigation_sizer.AddSpacer((self.html_window_size[0] -
            self.back_button_size[0] - self.next_button_size[0], 0))
        navigation_sizer.Add(self.next_page_button)

        sec_nav_sizer.Add(self.sec_prev_page_button, 0)
        sec_nav_sizer.AddSpacer((self.html_window_size[0] - self.back_button_size[0]
            - self.next_button_size[0], 0))
        sec_nav_sizer.Add(self.sec_next_page_button, 0)

        open_folder_sizer.Add(self.open_folder_button, 0)

# Add sizers to sizers here

        main_sizer.Add(widget_sizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 10)
        tool_sizer.Add(open_folder_sizer, 0)
        tool_sizer.Add(navigation_sizer, 0)
        story_display_sizer.Add(jump_sizer, 0)
        tool_sizer.Add(story_display_sizer, 0)
        tool_sizer.Add(sec_nav_sizer, 0)
        self.container_sizer.Add(tool_sizer, 0)
        widget_sizer.Add(self.container_sizer, 0)
        self.SetSizer(main_sizer)
        self.Fit()

#Functions here

    #Shorcuts

    def page_up_down_shortcut(self, event):
        # 367 = PageDown
        if event.GetKeyCode() == 367:
            self.get_pos_down(event)
        # 366 = PageUp
        if event.GetKeyCode() == 366:
            self.get_pos_up(event)
        # 32 = Space
        if event.GetKeyCode() == 32:
            self.get_pos_down(event)

    # Get position info

    def get_pos_down(self, event):
        scroll_place = self.html_window.GetScrollPos(wx.VERTICAL)
        self.html_window.Scroll(0, scroll_place + 10)
        self.modify_settings_file_position(self.location, scroll_place + 10)

    def get_pos_up(self, event):
        scroll_place = self.html_window.GetScrollPos(wx.VERTICAL)
        self.html_window.Scroll(0, scroll_place - 10)
        self.modify_settings_file_position(self.location, scroll_place - 10)

    # Story navigation

    def jump(self, event):
        position = self.jump_to_list.GetSelection()
        if str(position) != '-1':
            raw_page = open(self.all_files[position], 'r')
            page = raw_page.read()
            self.html_window.SetPage(page)
            self.modify_settings_file(self.location, position)
            self.current_chapter = position

    def next_page(self, event):
        raw_page = open(self.all_files[self.current_chapter + 1], 'r')
        if self.current_chapter == len(self.all_files):
            return
        self.current_chapter = self.current_chapter + 1
        self.modify_settings_file(self.location, self.i)
        page = raw_page.read()
        self.jump_to_list.SetSelection(self.current_chapter)
        self.html_window.SetPage(page)

    def back_page(self, event):
        raw_page = open(self.all_files[self.current_chapter - 1], 'r')
        if self.current_chapter == 0:
            return
        self.current_chapter = self.current_chapter - 1
        self.modify_settings_file(self.location, self.i)
        page = raw_page.read()
        self.jump_to_list.SetSelection(self.current_chapter)
        self.html_window.SetPage(page)

#Modify and read last used/viewed settings

    def modify_settings_file(self, location, chapter):
        parser = ConfigParser.ConfigParser()
        file_location = os.path.join(location, 'settings.ini')
        parser.read(file_location)
        parser.set('last_viewed', 'last_chapter_opened', str(chapter))
        with open(file_location, 'w') as configfile:
            parser.write(configfile)

    def modify_settings_file_position(self, location, place):
        parser = ConfigParser.ConfigParser()
        file_location = os.path.join(location, 'settings.ini')
        parser.read(file_location)
        parser.set('last_viewed', 'last_chapter_position', str(place))
        with open(file_location, 'w') as configfile:
            parser.write(configfile)

    def remove_file_from_settings(self, title):
        # Add alert that file will be removed from list on reload
        parser = ConfigParser.ConfigParser()
        parser.read('library.ini')
        for each in parser.sections():
            title_value = parser.items(each)[0][1]
            if title == title_value:
                parser.remove_section(title)
        confFile = open('library.ini', 'w')
        parser.write(confFile)

    def get_last_page(self, location):
        parser = ConfigParser.ConfigParser()
        file_location = os.path.join(location, 'settings.ini')
        parser.read(file_location)
        chapter = parser.get('last_viewed', 'last_chapter_opened')
        return chapter

    def get_last_position(self, location):
        parser = ConfigParser.ConfigParser()
        file_location = os.path.join(location, 'settings.ini')
        parser.read(file_location)
        position = parser.get('last_viewed', 'last_chapter_position')
        return position

# Get file location and open

    def choose_location(self, event):
        dialog = wx.DirDialog(self, 'choose')
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
        elif dialog.ShowModal() == wx.ID_CANCEL:
            self.path = os.path.abspath('./')
        self.location = self.path
        dialog.Destroy()
        self.get_file(self.location)

    def get_file(self, location):
        self.jump_to_list.Clear()
        self.location = location
        self.i = 0
        path = os.path.abspath(self.location)
        try:
            list_files = os.listdir(path)
        except Exception as e:
            util.error_alert_box(str(e))
            self.remove_file_from_settings(os.path.basename(self.location))
            return
        self.all_files_unsorted = []
        for each in list_files:
            if each.endswith('.html') is not True:
                pass
            else:
                path_to_file = os.path.join(os.path.abspath(self.location),
                each)
                self.all_files_unsorted.append(path_to_file)
        self.all_files = sorted(self.all_files_unsorted, key=self.sort_it)
        self.chapters = []
        for each in self.all_files:
            self.chapters.append('Chapter ' +
            str(self.all_files.index(each) + 1))
        for each in self.chapters:
            self.jump_to_list.Append(each)
        try:
            chapter = int(self.get_last_page(self.location))
        except:
            chapter = 0
        self.current_chapter = chapter
        self.jump_to_list.SetSelection(chapter, True)
        try:
            raw_page = open(self.all_files[chapter], 'r')
        except:
            raw_page = open(self.all_files[0], 'r')
        page = raw_page.read()
        self.html_window.SetPage(page)

        pos = self.get_last_position(self.location)
        try:
            self.html_window.Scroll(0, int(pos))
        except:
            pass

# Sort files

    def sort_it(self, filename):
        return int(re.search(r'\d+', filename).group())