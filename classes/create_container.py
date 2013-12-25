# -*- coding: utf-8 -*-


class container:

    def create_content(self):
        content = ('<?xml version="1.0"?>'
'<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
'<rootfiles>'
'<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />'
'</rootfiles>'
'</container>')
        return content