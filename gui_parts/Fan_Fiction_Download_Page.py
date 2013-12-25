# -*- coding: utf-8 -*-

import wx
import wx.html
import os
import os.path
import time
import ConfigParser
import shutil
from classes.download import FFDownload

down = FFDownload()


class DownloadFanfiction(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

# Defaults here

        self.location = ''

# Sizers here

        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        widget_sizer = wx.BoxSizer(wx.VERTICAL)
        selection_sizer = wx.BoxSizer(wx.HORIZONTAL)
        location_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)
        output_sizer = wx.BoxSizer(wx.VERTICAL)
        secondary_widget_sizer = wx.BoxSizer(wx.VERTICAL)
        add_file_sizer = wx.BoxSizer(wx.HORIZONTAL)

# Objects here

        self.url_box = wx.TextCtrl(self, -1, size=(200, 30))
        self.url_button = wx.Button(self, -1, 'Download')

        self.output_box = wx.TextCtrl(self, -1, size=(600, 300),
             style=wx.TE_MULTILINE | wx.TE_RICH2 | wx.TE_READONLY)

        self.location_button = wx.Button(self, -1, 'Browse')
        self.library = wx.ListBox(self, -1, size=(300, 300))
        self.lib_size = self.library.GetSize()
        self.add_story = wx.Button(self, -1, 'Add Story')
        self.add_size = self.add_story.GetSize()
        self.remove_story = wx.Button(self, -1, 'Remove Story')
        self.remove_size = self.remove_story.GetSize()

# Add objects to sizers here

        input_sizer.Add(self.url_box, 0)
        input_sizer.Add(self.url_button, 0)
        output_sizer.Add(self.output_box, 0)
        location_sizer.Add(self.location_button, 0)
        add_file_sizer.Add(self.add_story, 0)
        spacer_size = self.lib_size[0] - self.remove_size[0] - self.add_size[0]
        add_file_sizer.AddSpacer((spacer_size, 0))
        add_file_sizer.Add(self.remove_story, 0)

# Add sizers to sizers here

        main_sizer.Add(widget_sizer, 0, wx.ALL, 10)
        secondary_widget_sizer.Add(add_file_sizer, 0)
        secondary_widget_sizer.Add(self.library, 0)
        main_sizer.Add(secondary_widget_sizer, 0, wx.ALL, 10)
        selection_sizer.Add(location_sizer)
        selection_sizer.Add(input_sizer)
        widget_sizer.Add(selection_sizer)
        widget_sizer.Add(output_sizer)

        self.SetSizer(main_sizer)
        self.Fit()

        try:
            story_list = self.read_library()
            for each in story_list:
                self.library.Append(each)
        except:
            pass
    #Bind
        self.add_story.Bind(wx.EVT_BUTTON, self.choose_file)
        self.remove_story.Bind(wx.EVT_BUTTON, self.story_remove)

    def lib_click(self, event):
        story_item = self.library.GetStringSelection()
        notebook = self.GetParent()
        story_item_location = self.lib_search(story_item)
        self.GetParent().GetParent().GetParent().read_page.get_file(story_item_location)
        notebook.SetSelection(1)

    def lib_search(self, story_item):
        Config = ConfigParser.ConfigParser()
        Config.read('library.ini')
        for each in Config.sections():
            if each == story_item:
                link_value = Config.items(each)[1][1]
                return link_value

    def choose_file(self, event):
        dialog = wx.DirDialog(self, 'choose')
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
        elif dialog.ShowModal() == wx.ID_CANCEL:
            self.path = os.path.abspath('./')
        self.location = self.path
        dialog.Destroy()
        title = os.path.basename(self.location)
        split_path = self.location.split('/')
        del split_path[-1]
        loc = '/'.join(split_path)

        self.add_to_library(title, loc)

    def choose_location(self, event):
        dialog = wx.DirDialog(self, 'choose')
        if dialog.ShowModal() == wx.ID_OK:
            self.path = dialog.GetPath()
        elif dialog.ShowModal() == wx.ID_CANCEL:
            self.path = os.path.abspath('./')
        self.location = self.path
        dialog.Destroy()
        self.location

    def on_click(self, event):
        self.output_box.Clear()
        url = self.url_box.GetValue()
        #download = down.down_all(url, self.location)
        site_name = down.get_fandom(url)
        if site_name == 'not found':
            self.output_box.AppendText('Download failed,\
                 site not found or not supported')
            return
        soup = down.get_soup(url, site_name)
        title = down.get_title(soup, site_name)
        folder = down.create_folder(title, self.location)
        folder_location = os.path.join(self.location, title)
        down.include_settings_file(folder_location, url, title)
        down.modify_settings_file(folder_location, url, title)
        i = 1
        # Deal with single chapter stories
        try:
            #links = down.grab_content('links', site_name, soup)
            #link_form = 'multi'
            links = down.get_links(site_name, soup)
            print links
        except:
            #content = down.grab_content('chapter', site_name, soup)
            content = down.grab_content(site_name, soup)
            name = '{1} chapter {0}.html'.format(i, title)
            down.store_content(content, name, folder)

        if len(links) > 0:
            down_from = down.download_from_link_result[site_name]

            for each in links[down_from:]:
                new_url = down.build_url(url, site_name, each)
                soup = down.get_soup(new_url, site_name)
                content = down.grab_content(site_name, soup)
                name = '{0}{1}.html'.format(0, i)
                down.store_content(content, name, folder)
                for t in range(1):
                    time.sleep(1)
                    wx.Yield()
                    self.output_box.AppendText(
                        'Downloading: {0} Chapter {1}\n'.format(title, i))

                i = i + 1
        self.output_box.AppendText('Download complete.')
        self.add_to_library(title, self.location)
        self.library.Clear()
        story_list = self.read_library()
        for each in story_list:
            self.library.Append(each)
        self.library.Update()

    # Get content of library file
    def read_library(self):
        if self.library_exists():
            lib = []
            Config = ConfigParser.ConfigParser()
            Config.read('library.ini')
            for each in Config.sections():
                #title = Config.items(each)[0][0]
                title_value = Config.items(each)[0][1]
                lib.append(title_value)
            return lib

    # Add file to library
    def add_to_library(self, title, location):
        if self.library_exists():
            self.add_file(title, location)
        else:
            self.create_lib(title, location)

    # check if library file exists
    def library_exists(self):
        return os.path.isfile('library.ini')

    # If library file does not exist create it.
    def create_lib(self, title, location):
        full_location = os.path.join(location, title)
        Config = ConfigParser.ConfigParser()
        confFile = open('library.ini', 'w')
        Config.add_section('{title}'.format(title=title))
        Config.set('{title}'.format(title=title),
                    'title',
                    '{title}'.format(title=title))
        Config.set('{title}'.format(title=title),
                   'location',
                   '{location}'.format(location=full_location))

        Config.write(confFile)
        confFile.close()

    # Add file to library.
    def add_file(self, title, location):
        full_location = os.path.join(location, title)
        Config = ConfigParser.ConfigParser()
        confFile = open('library.ini', 'a')
        Config.add_section('{title}'.format(title=title))
        Config.set('{title}'.format(title=title),
                    'title',
                    '{title}'.format(title=title))
        Config.set('{title}'.format(title=title),
                   'location',
                   '{location}'.format(location=full_location))
        Config.write(confFile)
        confFile.close()
        self.library.Append(title)

    def story_remove(self, event):
        title = self.library.GetStringSelection()
        index = self.library.GetSelection()
        remove_files = self.remove_file_completely(title)
        if remove_files is True:
            self.library.Delete(index)
            self.remove_file_from_settings(title, index)
        else:
            pass

    # Remove file listing from library file and delete all files.
    def remove_file_from_settings(self, title, file_index):
        # Add alert that file will be removed from list on reload
        parser = ConfigParser.ConfigParser()
        parser.read('library.ini')
        for each in parser.sections():
            title_value = parser.items(each)[0][1]
            file_location = parser.items(each)[1][1]
            if title == title_value:
                parser.remove_section(title)
                self.delete_files(file_location)
            else:
                pass
        confFile = open('library.ini', 'w')
        parser.write(confFile)

    # Check if user wants to continue in deleting files
    def remove_file_completely(self, title):
        dialog = wx.MessageDialog(None,
            'Remove {0}?\nThis will delete all files associated with this story.'.format(title),
            'Removal Warning',
             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialog.ShowModal() == wx.ID_YES:
            return True
        else:
            return False
        dialog.Destroy()

    # use shutil to remove folder and all files therin
    def delete_files(self, location):
        path = os.path.abspath(location)
        shutil.rmtree(path)
