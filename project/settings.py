# -*- coding: utf-8 -*-

import os

REPO_NAME = "autodd"  # Used for FREEZER_BASE_URL
DEBUG = True

# Assumes the app is located in the same directory
# where this file resides
APP_DIR = os.path.dirname(os.path.abspath(__file__))

def parent_dir(path):
    '''Return the parent of a directory.'''
    return os.path.abspath(os.path.join(path, os.pardir))

PROJECT_ROOT = os.path.join(parent_dir(APP_DIR), "generated_site")
# In order to deploy to Github pages, you must build the static files to
# the project root
FREEZER_DESTINATION = PROJECT_ROOT
# Since this is a repo page (not a Github user page),
# we need to set the BASE_URL to the correct url as per GH Pages' standards
# FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)
# For local testing, this will do
FREEZER_BASE_URL = "http://localhost"
FREEZER_REMOVE_EXTRA_FILES = False  # IMPORTANT: If this is True, all app files
                                    # will be deleted when you run the freezer
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']
FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')
FLATPAGES_EXTENSION = '.md'

# I had to add this - might need to be removed for gh-pages deployment
FREEZER_RELATIVE_URLS = True