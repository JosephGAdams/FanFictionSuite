# -*- coding: utf-8 -*-


class create_content_toc:

    def create_toc(self, items, book_id, title):

        nav_points = []
        i = 1
        for each in items['file_id']:
            index = items['file_id'].index(each)
            item = ('<navPoint id="navpoint-{item_number}" playOrder="{item_number}">'
'\n<navLabel>'
'\n<text>Chapter {item_number}</text>'
'\n</navLabel>'
'\n<content src="{item_href}"/>'
'\n</navPoint>').format(item_number=i,
                 item_href=items['file_href'][index])
            nav_points.append(item)
            i = i + 1
        nav_points = ''.join(nav_points)

        content = ('<?xml version="1.0" encoding="utf-8"?>'
'\n<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"'
'\n"http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">'
'\n<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
'\n<head>'
'\n<meta name="dtb:uid"'
'\ncontent="urn:uuid:{identifier}"/>'
'\n<meta name="dtb:depth" content="1"/>'
'\n<meta name="dtb:totalPageCount" content="{page_count}"/>'
'\n<meta name="dtb:maxPageNumber" content="0"/>'
'\n</head>'
'\n<docTitle>'
'\n<text>{book_title}</text>'
'\n</docTitle>'
'\n<navMap>'
'<navPoint id="navpoint-0" playOrder="0">'
'\n<navLabel>'
'\n<text>Chapter 0</text>'
'\n</navLabel>'
'\n<content src="table_of_contents.html"/>'
'\n</navPoint>'
'\n{nav}'
'\n</navMap>'
'\n</ncx>').format(book_title=title, identifier=book_id,
            page_count=len(items['file_id']), nav=nav_points)

        return content