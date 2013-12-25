# -*- coding: utf-8 -*-


class create_content_opf:

    def create_content(self, items, book_id, title, creator):

        manifest_items = []
        for each in items['file_id']:
            index = items['file_id'].index(each)
            item = ('\n<item id="item{item_identifier}" href="{item_href}"'
            '\nmedia-type="application/xhtml+xml"/>').format(item_identifier=each,
                  item_href=items['file_href'][index])

            manifest_items.append(item)
        manifest_items = ''.join(manifest_items)

        spine_items = []
        for each in items['file_id']:
            id_item = '<itemref idref="item{id}"/>'.format(id=each)
            spine_items.append(id_item)
        spine_items = ''.join(spine_items)

        content = ('<?xml version="1.0" encoding="utf-8"?>'
'\n<package xmlns="http://www.idpf.org/2007/opf"'
'\nxmlns:dc="http://purl.org/dc/elements/1.1/"'
'\nunique-identifier="bookid" version="2.0">'
'\n<metadata>'
'\n<dc:title>{title}</dc:title>'
'\n<dc:creator>{author}</dc:creator>'
'\n<dc:identifier'
'\nid="bookid">urn:uuid:{book_id}</dc:identifier>'
'\n<dc:language>en-US</dc:language>'
'\n</metadata>'
'\n<manifest>'
'\n<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
'\n<item id="item00" href="table_of_contents.html" media-type="application/xhtml+xml"/>'

'\n{manifest_items}'
'\n</manifest>'
'\n<spine toc="ncx">'
'\n<itemref idref="item00"/>'
'\n{spine_items}'
'\n</spine>'
'\n</package>').format(title=title, book_id=book_id,
             manifest_items=manifest_items, spine_items=spine_items, author=creator)
        return content