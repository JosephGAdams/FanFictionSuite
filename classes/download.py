# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urlparse
import requests
import os
import os.path
import shutil
import ConfigParser
import time


class FFDownload:

#Dicts and lists used to store information used when accessing different sites.

    supported_sites = [
        'fanfiction',
        'adult-fanfiction',
        'archiveofourown',
        'asianfanfiction',
        'asianfanfics',
        'patronuscharm',
        'sugarquill',
        'siye'
        ]

    name_to_use = {
        'fanfiction': 'fanfiction',
        'adult-fanfiction': 'adult-fanfiction',
        'archiveofourown': 'archiveofourown',
        'asianfanfiction': 'asianfanfiction',
        'asianfanfics': 'asianfanfics',
        'patronuscharm': 'patronuscharm',
        'sugarquill': 'sugarquill',
        'siye': 'siye',
        }

# If you want to ignore the first link result then 0 would be changed to 1
    download_from_link_result = {
        'fanfiction': 0,
        'adult-fanfiction': 0,
        'archiveofourown': 0,
        'asianfanfiction': 0,
        'asianfanfics': 0,
        'patronuscharm': 0,
        'sugarquill': 0,
        'siye': 0,
        }

# Set requests option for redirects for true for these sites.
    redirects_allowed_for_sites = ['fanfiction', 'archiveofourown']

# Append to url to get past warnings about age restricted content etc.
    bypass_url_warning = {
        'fanfiction': None,
        'adult-fanfiction': None,
        'archiveofourown': '?view_adult=true',
        'asianfanfiction': None,
        'asianfanfics': None,
        'patronuscharm': None,
        'sugarquill': None,
        'siye': None,
        }

# for sites that do not lend themselves for Title capture, these are default
# titles that will not be used in titles if they are found by the title search.
    disallowed_titles = ['The Sugar Quill']

    title_search_format = {
        'fanfiction': 'multi',
        'adult-fanfiction': 'single',
        'archiveofourown': 'multi',
        'asianfanfiction': 'single',
        'asianfanfics': 'single',
        'patronuscharm': 'single',
        'sugarquill': 'multi-part',
        'siye': 'single',
        }

    title_search = {
        'fanfiction': ['b', 'class', 'xcontrast_txt'],
        'adult-fanfiction': ['title'],
        'archiveofourown': ['h2', 'class', 'title heading'],
        'asianfanfiction': ['title'],
        'asianfanfics': ['title'],
        'patronuscharm': ['title'],
        'sugarquill': ['td', 'class', 'info2_pane', 'b'],
        'siye': ['title'],
        }

# If the titles are not stored in a conventional way i.e:
# unbound string refers to titles that are stored outside of a specific tag
# and have to be accessed using known_tag.nextSibling
    title_type = {
        'fanfiction': None,
        'adult-fanfiction': None,
        'archiveofourown': None,
        'asianfanfiction': None,
        'asianfanfics': None,
        'patronuscharm': None,
        'sugarquill': 'unbound_string',
        'siye': None,
        }

#Remove characters from title that are either disallowed or not wanted.
    format_title = {
        'fanfiction': None,
        'adult-fanfiction': 'Story:',
        'archiveofourown': None,
        'asianfanfiction': None,
        'asianfanfics': None,
        'patronuscharm': None,
        'sugarquill': ':',
        'siye': None,
        }

    link_search = {
        'fanfiction': ['select', 'id', 'chap_select'],
        'adult-fanfiction': ['select', 'name', 'chapnav'],
        'archiveofourown': ['select', 'name', 'selected_id'],
        'asianfanfiction': ['select', 'name', 'chapter'],
        'asianfanfics': ['select', 'name', 'chapterNav'],
        'patronuscharm': ['select', 'name', 'select'],
        'sugarquill': ['select', 'name', 'chapno'],
        'siye': ['select', 'name', 'chapter'],
        }

    link_attribute = {
        'fanfiction': ['option'],
        'adult-fanfiction': ['option'],
        'archiveofourown': ['option'],
        'asianfanfiction': ['option'],
        'asianfanfics': ['option'],
        'patronuscharm': ['option'],
        'sugarquill': ['option'],
        'siye': ['option'],
        }

    link_value = {
        'fanfiction': ['value'],
        'adult-fanfiction': ['value'],
        'archiveofourown': ['value'],
        'asianfanfiction': ['value'],
        'asianfanfics': ['value'],
        'patronuscharm': ['value'],
        'sugarquill': ['value'],
        'siye': ['value'],
        }

    chapter_search = {
        'fanfiction': ['div', 'id', 'storytext'],
        'adult-fanfiction': ['td', 'colspan', '3'],
        'archiveofourown': ['div', 'class', 'userstuff module'],
        'asianfanfiction': ['div', 'id', 'story'],
        'asianfanfics': ['div', 'id', 'bodyText'],
        'patronuscharm': ['div', 'id', 'storytext'],
        'sugarquill': ['td', 'class', 'content_pane'],
        'siye': ['span', 'style', 'font-size: 100%;'],
        }

# tags separated by a comma are to be grabbed separately but in order
    to_grab = {
        'fanfiction': ['p'],
        'adult-fanfiction': ['font', 'p'],
        'archiveofourown': ['p'],
        'asianfanfiction': ['span'],
        'asianfanfics': ['p'],
        'patronuscharm': ['p'],
        'sugarquill': [None],
        'siye': [None],
         }

    # Get the site name of a url
    def get_fandom(self, user_input):
        '''Find the site name from url

           user_input -- the url given by the user

        '''
        raw_name = urlparse.urlparse(user_input)
        full_site_name = raw_name.netloc.split('.')
        for each in full_site_name:
            if each in self.supported_sites:
                site_name = self.name_to_use[each]
                break
            else:
                site_name = 'Not found'
        return site_name

    # Create folder to store story
    def create_folder(self, title, location):
        folder_path_and_name = os.path.join(location, title)
        try:
            os.mkdir(folder_path_and_name, 0777)
        except:
            pass
        return folder_path_and_name

    # Create the soup to be searched
    def get_soup(self, url, site_name):
        '''Get soup from url

           url       -- the website location you are downloading from
           site_name -- the name of the site, gained from the url

        '''

        headers = {'User-Agent': '''Mozilla/5.0 (X11; Ubuntu;Linux
        x86_64;rv:25.0) Gecko/20100101 Firefox/25.0'''}

        if site_name is 'archiveofourown' and \
            url.endswith('view_adult=True') is not True:
            url = '{0}{1}'.format(url, self.bypass_url_warning[site_name])

        if site_name in self.redirects_allowed_for_sites:
            grab_page = requests.get(url, headers=headers,
            allow_redirects=True)
        else:
            grab_page = requests.get(url, headers=headers,
            allow_redirects=False)
        page_source = grab_page.text
        soup = BeautifulSoup(page_source)
        # Writes the page being grabbed to current working directory, let's you'
        # see what page you are getting when using the given url.
        #For testing purposes only.
        f = open('test.html', 'w')
        f.write(str(soup))
        f.close()
        return soup

    # Find the title of the story
    def get_title(self, soup, site_name):
        '''Download title

           site_name -- the site you are downloading from
           soup      -- the raw page you are scraping
        '''

        title = 'Unknown Title'
        if self.title_search_format[site_name] == 'multi':
            title_block = soup.find(self.title_search[site_name][0],
                attrs={self.title_search[site_name][1]:
                 self.title_search[site_name][2]})

        elif self.title_search_format[site_name] == 'single':
            title_block = soup.find(self.title_search[site_name])

        elif self.title_search_format[site_name] == 'multi-part':
            title_block = soup.findAll(self.title_search[site_name][0],
                    attrs={self.title_search[site_name][1]:
                    self.title_search[site_name][2]})
            block_part = soup.findAll(self.title_search[site_name][3])
            if self.title_type[site_name] == 'unbound_string':
                title_block = BeautifulSoup(block_part[1].nextSibling)

        try:
            title = title_block.text.replace(self.format_title[site_name], '')
        except:
            title = title_block.text
        title = title.strip()

        if site_name == 'patronuscharm':
            split_title = title.split(':')
            title = split_title[-1].replace('.', '').strip()

        if title in self.disallowed_titles:
            title = '{0} - {1}'.format(site_name,
            ''.join([str(each) for each in time.localtime()]))
        return title

    def get_links(self, site_name, soup):
        link_block = soup.find(self.link_search[site_name][0],
            attrs={self.link_search[site_name][1]:
            self.link_search[site_name][2]})
        raw_content = [x for x in link_block.findAll('option')]
        content = []
        for each in raw_content:
            try:
                content.append(each['value'])
            except:
                pass
        return content

    def grab_content(self, site_name, soup):
        body_part = soup.findAll(self.chapter_search[site_name][0],
            attrs={self.chapter_search[site_name][1]:
            self.chapter_search[site_name][2]})
        # Create soup using joined str of body_part result set.
        new_soup = BeautifulSoup(''.join([str(each) for each in body_part]))
        new_soup_search = new_soup.findAll(self.to_grab[site_name])
        # Join result of new_soup_search.
        chapter = ''.join([str(each) for each in new_soup_search])
        if chapter == '':
            chapter = ''.join([str(each) for each in body_part])
        page_setup = ('<?xml version="1.0" encoding="utf-8"?>'
            '\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" '
            '"http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
            '\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
            '\n<head>'
            '\n<title></title>'
            '\n<meta content="HTML"></meta>'
            '\n</head>'
            '\n<body>'
            '\n{0}'
            '\n</body>'
            '\n</html>').format(chapter)
        return page_setup

    # Save content to folder
    def store_content(self, content, name, folder_path_and_name):
        '''Download content gained from page

           content              -- story text
           name                 -- story name
           folder_path_and_name -- location to download to
        '''
        output_location = '{0}/{1}'.format(folder_path_and_name, name)
        f = open(output_location, 'w')
        f.write(content)
        f.close()

    # Create the url for each page
    def build_url(self, url, site_name, chapter_number):
        '''Modify url for downloading

           url            -- base url to work from
           site_name      -- name of site you are downloading from
           chapter_number -- which chapter is to be downloaded
        '''

        parse_url = urlparse.urlparse(url)
        split_url = parse_url.path.split('/')

        if site_name == 'fanfiction':
            split_url[3] = chapter_number
            url = 'http://{0}{1}'.format(parse_url.netloc, '/'.join(split_url))

        elif site_name == 'adult-fanfiction':
            url = 'http://{0}/{1}'.format(parse_url.netloc, chapter_number)

        elif site_name == 'harrypotterfanfiction':
            split_url = parse_url.path.split('?')
            split_url[-1] = chapter_number
            url = 'http://{0}/viewstory.php{1}'.format(parse_url.netloc,
                ''.join(split_url))

        elif site_name == 'archiveofourown':
            split_url = parse_url.path.split('/')
            split_url[-1] = chapter_number
            url = 'http://{0}{1}{2}'.format(parse_url.netloc,
            '/'.join(split_url), self.bypass_url_warning[site_name])

        elif site_name == 'asianfanfiction':
            split_url = parse_url.query.split('=')
            split_url[-1] = chapter_number
            url = 'http://{0}{1}?{2}'.format(parse_url.netloc, parse_url.path,
            '='.join(split_url))

        elif site_name == 'asianfanfics':
            url = chapter_number

        elif site_name == 'patronuscharm':
            split_url[3] = chapter_number
            url = 'http://{0}{1}'.format(parse_url.netloc, '/'.join(split_url))

        elif site_name == 'sugarquill':
            url_end = parse_url.query.split('=')
            url_end[-1] = chapter_number
            url_ender = '='.join(url_end)
            url = 'http://{0}{1}?{2}'.format(parse_url.netloc, parse_url.path, url_ender)

        elif site_name == 'siye':
            url_end = parse_url.query.split('=')
            url_end[-1] = chapter_number
            url_ender = '='.join(url_end)
            url = 'http://{0}{1}?{2}'.format(parse_url.netloc, parse_url.path, url_ender)

        print url
        return url

    def include_settings_file(self, location, url, title):
        settings_location = os.path.join(os.getcwd(), 'classes', 'settings.ini')
        shutil.copy(settings_location, location)

    def modify_settings_file(self, location, url, title):
        parser = ConfigParser.ConfigParser()
        file_location = os.path.join(location, 'settings.ini')
        parser.read(file_location)
        parser.set('basic_details', 'story_url', str(url))
        parser.set('basic_details', 'story_title', str(title))
        with open(file_location, 'w') as configfile:
            parser.write(configfile)