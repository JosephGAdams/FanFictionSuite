# -*- coding: utf-8 -*-
import zipfile
import os
import os.path


class create_zipfile:

    def zipdir(self,location, path, title):
        file_loc = os.path.join(location, '{title}.epub'.format(title=title))
        book_zip = zipfile.ZipFile(file_loc, 'w')
        rootlen = len(path)
        for root, dirs, files in os.walk(path):
            for file in files:
                fn = os.path.join(root, file)
                book_zip.write(fn, fn[rootlen:])
        book_zip.close()
