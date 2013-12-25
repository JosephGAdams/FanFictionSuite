# -*- coding: utf-8 -*-
import wx
import os
import os.path
import shutil
from classes.folder_structure import folder_structure
from classes.collect_files import find_files
from classes.create_book_id import create_book_id
from classes.create_mimetype import mimetype
from classes.create_container import container
from classes.move_book_content import move_content
from classes.create_table_of_contents import table_of_contents
from classes.create_content import create_content_opf
from classes.create_toc import create_content_toc
from classes.populate_folders import pop_folders
from classes.create_zip_archive import create_zipfile

folder_struct = folder_structure()
finder = find_files()
create_id = create_book_id()
create_mime = mimetype()
create_cont = container()
mover = move_content()
table = table_of_contents()
create_cont_opf = create_content_opf()
create_cont_toc = create_content_toc()
folder_pop = pop_folders()
zipper = create_zipfile()


class ConvertFanfiction(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

# Sizers here

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        widget_sizer = wx.BoxSizer(wx.HORIZONTAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)

# Objects here

        self.choose_location_button = wx.Button(self, -1, 'location')

# Add objects to sizers here

        widget_sizer.Add(self.choose_location_button, 0)

# Add sizers to sizers here

        main_sizer.Add(widget_sizer, 0)
        widget_sizer.Add(input_sizer, 0)

        self.SetSizer(main_sizer)
        self.Fit()

# Bindings here

    def choose_location(self, event):
            dialog = wx.DirDialog(self, 'choose')
            if dialog.ShowModal() == wx.ID_OK:
                location = dialog.GetPath()
            elif dialog.ShowModal() == wx.ID_CANCEL:
                location = os.path.abspath('./')
                dialog.Destroy()
                return 'fail'
            dialog.Destroy()
            name = os.path.basename(location)
            folder_locations = folder_struct.make_structure(location)
            print folder_locations
            file_list = finder.search_location(location)
            unique_identifier = create_id.create_random_id()
            mime = create_mime.create_content()
            #if error - re-name
            cont = create_cont.create_content()
            table_of_cont = table.create_table_of_contents(file_list)
            mover.move_files(file_list, location, folder_locations['oebps_folder_location'])
            create_opf_file = create_cont_opf.create_content(file_list, unique_identifier, name, 'unknown')
            create_toc_file = create_cont_toc.create_toc(file_list, unique_identifier, name)
            folder_pop.create_files(folder_locations['epub_folder_location'], mime, 'mimetype')
            folder_pop.create_files(folder_locations['meta-inf_folder_location'], cont, 'container.xml')
            folder_pop.create_files(folder_locations['oebps_folder_location'], table_of_cont, 'table_of_contents.html')
            folder_pop.create_files(folder_locations['oebps_folder_location'], create_opf_file, 'content.opf')
            folder_pop.create_files(folder_locations['oebps_folder_location'], create_toc_file, 'toc.ncx')
            zipper.zipdir(location, folder_locations['epub_folder_location'], name)
            shutil.rmtree(folder_locations['epub_folder_location'])