# -*- coding: utf-8 -*-
import shutil
import os
import os.path


class move_content:

    def move_files(self, files, location, content_loc):
        for each in files['file_location']:
            file_loc = os.path.join(os.path.abspath(each))
            name = os.path.basename(file_loc)
            src = file_loc
            dst = os.path.join(content_loc, name)
            shutil.copyfile(src, dst)