# -*- coding: utf-8 -*-
import os
import os.path
import glob
import re


class find_files:

    def search_location(self, path):
        files = glob.glob(path + '/' + '*.html')
        new_files = self.format_files(files)
        return new_files

    def format_files(self, all_files):
        files = sorted(all_files, key=self.sort_files_naturally)
        file_list = {}
        file_id = [os.path.basename(x).split('.')[0] for x in files]
        file_href = [os.path.basename(x) for x in files]
        file_location = [x for x in files]
        file_list['file_id'] = file_id
        file_list['file_href'] = file_href
        file_list['file_location'] = file_location
        return file_list

    def sort_files_naturally(self, filename):
        return int(re.search(r'\d+', filename).group())