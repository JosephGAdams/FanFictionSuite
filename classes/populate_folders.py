# -*- coding: utf-8 -*-
import os
import os.path


class pop_folders:

    def create_files(self, location, content, file_name):
        file_loc = os.path.join(location, file_name)
        print 'file - makesurenotfolder = {}'.format(file_loc)
        f = open(file_loc, 'w')
        f.write(content)
        f.close()
