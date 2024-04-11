# goo-getf

## Description

Goo-getf is a simple CLI tool for extracting direct-download links suitable for downloading files from public services such as Google Drive, Google Colab etc. It excepts a list of HTML files, parses all contained references and outputs the list of links. Generated links can be used to download files using wget or curl or similar tool.

Goo-getf is a simple Python script, so it works on any platform with Python.

## Dependencies

Goo-getf uses [BeautifulSoup](http://beautiful-soup-4.readthedocs.io/) package to parse HTML, so

**bs4 Python package is required**.

No other non-standard packages are used.

## Installation

Only goo-getf.py file is required. No installation procedure. On Linux don't forget to check x-attribute of the file, on Windows path to Python executable should be resolvable.

## Usage

*Unix-like system:*    **./goo-get.py      [OPTIONS] FILES**
*Windows-like system:* **python goo-get.py [OPTIONS] FILES**

For more detailes use help: **goo-get.py -h**

## Application

When parsing websites with wget (or similar tool), links to downloadable files published on services like Google Drive typically stay unresolved and files itself are not downloaded. If file sharing is stopped, local image of website becomes incomplete. With goo-getf one can download such files and enjoy permanent access.
