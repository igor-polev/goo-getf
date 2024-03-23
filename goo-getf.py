#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google files parser

Created on Fri Mar 22 11:59:29 2024
@author: IGOR POLEV
"""

ABOUT_TEXT = """
Google links parser. Use 'goo-getf -h' for help.
"""

HELP_TEXT = """
USAGE:
    
       Unix-like system: ./goo-get.py      [OPTIONS] FILES 
    Windows-like system: python goo-get.py [OPTIONS] FILES

Don't forget x-attribute of goo-get.py on Unix-like system or path resolution
to python.exe on Windows-like system to make it work.

Search in FILES for references to Google hosted files and output direct links
sutable for downloading via external programs (like wget or curl).

OPTIONS:
    
    -h,   --help            Display help.
    
    -f,   --folders         Include links to Google Drive folder.
    --fo, --folders-only    Parse only links to Google Drive folder.

                            IMPORTANT: Direct-download links to Google Drive
                            folders are not supported yet. Parsed links to
                            folders are only suitable for manual download via
                            browser.
"""

import sys, getopt
import os.path

from contextlib import closing
from itertools  import compress
from bs4        import BeautifulSoup

class GooGetFiles:
    
    def __init__(self, cmdl_params):

        self.flags = ['def', 'doc']
        
        # Parsing CLI arguments
        opts, self.files = getopt.getopt(cmdl_params,
            'hf',
            [
                'help',
                'folders', 'folders-only', 'fo'
            ]
        )
        for opt, val in opts:
            if opt in ['-h', '--help']:
                print(HELP_TEXT)
                sys.exit(0)
            if opt in ['-f', '--folders']:
                self.flags.append('fol')
            if opt in ['--folders-only', '--fo']:
                self.flags = ['fol']
        if not self.files:
            if not opts:
                print(ABOUT_TEXT)
                sys.exit(0)
            else:
                sys.stderr.write("No files to parse specified.\n")
                sys.exit(1)
        bad_files = list(map(lambda x: not(os.path.exists(x)), self.files))
        if any(bad_files):
            sys.stderr.write("Files not found: {}\n".format(
                list(compress(self.files, bad_files))
            ))
            sys.exit(2)
            
        # Parsable links
        self.parsable_links = {
            'colab.research.google.com/github/' : {
                'flag'     : 'def',
                'term_str' : '',
                'dl_link'  : ''
            },
            'drive.google.com/drive/folders/' : {
                'flag'     : 'fol',
                'term_str' : '',
                'dl_link'  : ''
            },
            'drive.google.com/file/d/' : {
                'flag'     : 'def',
                'term_str' : '/',
                'dl_link'  : 'https://drive.usercontent.google.com/download?id={}&export=download&authuser=0'
            },
            'docs.google.com/document/d/' : {
                'flag'     : 'doc',
                'term_str' : '/',
                'dl_link'  : 'https://docs.google.com/document/export?format=docx&id={}'
            },
            'docs.google.com/presentation/d/' : {
                'flag'     : 'doc',
                'term_str' : '/',
                'dl_link'  : 'https://docs.google.com/presentation/export?format=pptx&id={}'
            },
            'docs.google.com/spreadsheets/d/' : {
                'flag'     : 'doc',
                'term_str' : '/',
                'dl_link'  : 'https://docs.google.com/spreadsheets/d/{}/export?format=xlsx'
            },
            'colab.research.google.com/drive/' : {
                'flag'     : 'def',
                'term_str' : '?',
                'dl_link'  : 'https://drive.usercontent.google.com/download?id={}&export=download&authuser=0'
            }
        }
        self.parsable_keys = self.parsable_links.keys()

    def parse(self):
        for fl in self.files:
            with closing(open(fl, 'r')) as file:
                hrefs = BeautifulSoup(file.read(), 'html.parser').find_all('a')
            if not hrefs:
                continue
            hrefs = list(map(lambda h: h.get('href'), hrefs))
            for key in self.parsable_keys:
                if not self.parsable_links[key]['flag'] in self.flags:
                    continue
                dl_link  = self.parsable_links[key]['dl_link']
                term_str = self.parsable_links[key]['term_str']
                key_len  = len(key)
                for href in hrefs:
                    if not href:
                        continue
                    if not dl_link:
                        print(href)
                        continue
                    id_start = href.find(key)
                    if id_start == -1:
                        continue
                    id_start += key_len
                    id_end = href.find(term_str, id_start)
                    if id_end == -1:
                        id_end = len(href) - 1
                    print(dl_link.format(href[id_start : id_end]))

if __name__ == "__main__":
    try:
        script = GooGetFiles(sys.argv[1:])
        script.parse()
    except getopt.GetoptError as err:
        sys.stderr.write(
            "Bad command-line arguments: {}.\nUse 'goo-getf -h' for help.\n".format(err)
        )
        sys.exit(3)
    except Exception as err:
        sys.stderr.write("Unexpected error: {}.\n".format(err))
        sys.exit(4)
    sys.exit(0)