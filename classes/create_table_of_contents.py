# -*- coding: utf-8 -*-


class table_of_contents:

    def create_table_of_contents(self, files):
        links = []
        print files['file_href']
        for each in files['file_href']:
            item = '<li><a href="{href}">{href}</a></li>'.format(href=each)
            links.append(item)
        links = ''.join(links)

        content = ('<?xml version="1.0" encoding="utf-8"?>'
                '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
                '\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
                    '\n<head>'
                    '\n<title></title>'
                        '\n<meta content="HTML"></meta>'
                    '\n</head>'
                    '\n<body>'
                    '\n<ul>'
                        '\n{links}'
                    '\n</ul>'
                    '\n</body>'
                '\n</html>').format(links=links)
        return content