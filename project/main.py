# -*- coding: utf-8 -*-

'''Entry point to all things to avoid circular imports.'''
from project.app import app, freezer, pages
from project.views import *