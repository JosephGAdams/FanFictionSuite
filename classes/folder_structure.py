# -*- coding: utf-8 -*-
import os
import os.path


class folder_structure:

    def make_directory(self, location, dir_name):
        folder_location = os.path.join(location, dir_name)
        try:
            os.mkdir(folder_location, 0777)
        except Exception as e:
            print e
        return folder_location

    def make_structure(self, location):
        epub_folder = self.make_directory(location, 'epub_folder')
        meta_inf_folder = self.make_directory(epub_folder, 'META-INF')
        oebps_folder = self.make_directory(epub_folder, 'OEBPS')
        paths = {
            'epub_folder_location': epub_folder,
            'meta-inf_folder_location': meta_inf_folder,
            'oebps_folder_location': oebps_folder,
            }
        return paths