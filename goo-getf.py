#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google files parser

Created on Fri Mar 22 11:59:29 2024
@author: IGOR POLEV
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

from contextlib import closing
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
        if self.files:
            self.pipe_mod = False
        else:
            self.pipe_mod = True

        # Parsable links
        self.parsable_links = {
            'colab.research.google.com/github/' : {
                'flag'    : 'def',
                'dl_link' : ''
            },
            'drive.google.com/drive/folders/' : {
                'flag'    : 'fol',
                'dl_link' : ''
            },
            'drive.google.com/file/d/' : {
                'flag'    : 'def',
                'dl_link' : 'https://drive.usercontent.google.com/download?id={}'
            },
            'docs.google.com/document/d/' : {
                'flag'    : 'doc',
                'dl_link' : 'https://docs.google.com/document/export?format=docx&id={}'
            },
            'docs.google.com/presentation/d/' : {
                'flag'    : 'doc',
                'dl_link' : 'https://docs.google.com/presentation/export?format=pptx&id={}'
            },
            'docs.google.com/spreadsheets/d/' : {
                'flag'    : 'doc',
                'dl_link' : 'https://docs.google.com/spreadsheets/d/{}/export?format=xlsx'
            },
            'colab.research.google.com/drive/' : {
                'flag'    : 'def',
                'dl_link' : 'https://drive.usercontent.google.com/download?id={}'
            }
        }
        self.parsable_keys = self.parsable_links.keys()
        for key in self.parsable_keys:
            self.parsable_links[key]['key_len'] = len(key)

    def run(self):
        if self.pipe_mod:
            for file in sys.stdin:
                self.parse_file(file.rstrip('\n'))
        else:
            for file in self.files:
                self.parse_file(file)

    def parse_file(self, file):

        try:
            with closing(open(file, 'r')) as fl:
                hrefs = BeautifulSoup(fl.read(), 'html.parser').find_all('a')
        except IOError as err:
            sys.stderr.write("IO error: {} while processing file {}\n".format(err, file))
            return
        except OSError as err:
            sys.stderr.write("OS error: {} while processing file {}\n".format(err, file))
            return
        if not hrefs:
            return

        hrefs = list(map(lambda h: h.get('href'), hrefs))
        for key in self.parsable_keys:
            if not self.parsable_links[key]['flag'] in self.flags:
                continue
            dl_link = self.parsable_links[key]['dl_link']
            key_len = self.parsable_links[key]['key_len']
            for href in hrefs:
                if not href:
                    continue
                id_start = href.find(key)
                if id_start == -1:
                    continue
                if not dl_link:
                    print(href)
                    continue
                id_start += key_len
                id_stop = len(href) - 1
                for term_sym in '/?#':
                    sym_idx = href.find(term_sym, id_start)
                    if sym_idx != -1 and sym_idx < id_stop:
                        id_stop = sym_idx
                print(dl_link.format(href[id_start : id_stop]))

if __name__ == "__main__":
    try:
        script = GooGetFiles(sys.argv[1:])
        script.run()
    except getopt.GetoptError as err:
        sys.stderr.write(
            "Bad command-line arguments: {}.\nUse 'goo-getf -h' for help.\n".format(err)
        )
        sys.exit(2)
    except Exception as err:
        sys.stderr.write("Unexpected error: {}\n".format(err))
        sys.exit(3)
    sys.exit(0)