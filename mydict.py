#!/usr/bin/python
# -*- coding: utf-8 -*-

# File: mydict.py
# Author: Tomás Vírseda
# License: GPL v3
# Description: Personal Dictionary module.

# Notes:
# Get translations form command line: dict -i fd-deu-eng hallo

import os
import sys
import subprocess

import log
from util import which, execmd

ERR_DEF_NOT_FOUND = b"No definitions found"

DIR_ROOT = os.path.abspath(sys.modules[__name__].__file__ + "/..")
DIR_DICT = os.path.join(DIR_ROOT, 'dict')
FILE_DICT = os.path.join(DIR_DICT, 'dict.json')


class PersonalDictionary:
    mydict = {}
    available = False

    def __init__(self, debug_level="INFO"):
        self.msg = log.get_logger("Dictionary", debug_level)
        self.checks()
        self.msg.debug("Personal Dictionary module initialized")

    def is_available(self):
        return self.available

    def checks(self):
        # Check dict directory
        if not os.path.exists('dict'):
            os.makedirs('dict')
            self.msg.debug("Directory 'dict' created")

        # Check dictionary server availability
        DICTD_AVAILABLE = which('dictd')
        self.available = self.available or DICTD_AVAILABLE
        self.msg.debug("Dictionary server available? %s", DICTD_AVAILABLE)

        # Check dictionary client availability
        DICTC_AVAILABLE = which('dict')
        self.available = self.available and DICTC_AVAILABLE
        self.msg.debug("Dictionary client available? %s", DICTC_AVAILABLE)

    def lookup(self, word, dictionary="fd-deu-eng"):
        FILE_DEF = os.path.join(DIR_DICT, dictionary, word[0].lower(), "%s.def" % word.lower())
        if not os.path.exists(FILE_DEF):
            cmd = "dict -C -d %s %s" % (dictionary, word)
            defs, error = execmd(cmd)
            if ERR_DEF_NOT_FOUND in error:
                self.msg.warning("[ - ] Word '%s': definitions not found in dictionary '%s'", word, dictionary)
                defs = error
            else:
                self.msg.info("[ + ] Word '%s': definitions found in dictionary '%s'", word, dictionary)
            os.makedirs(os.path.dirname(FILE_DEF), exist_ok=True)
            with open(FILE_DEF, 'wb') as fd:
                fd.write(defs)
        else:
            self.msg.debug("[ = ] Word '%s' from dictionary '%s' found in your Personal Dictionary", word, dictionary)
        return FILE_DEF

    def missing(self):
        defs = []
        nodefs = []
        for dictionary in os.listdir(DIR_DICT):
            DIR_PERS_DICT = os.path.join(DIR_DICT, dictionary)
            for letter in os.listdir(DIR_PERS_DICT):
                DIR_ENTRIES = os.path.join(DIR_PERS_DICT, letter)
                for entry in os.listdir(DIR_ENTRIES):
                    FILE_ENTRY = os.path.join(DIR_ENTRIES, entry)
                    with open(os.path.abspath(FILE_ENTRY), 'rb') as fe:
                        if ERR_DEF_NOT_FOUND in fe.read():
                            # ~ self.msg.warning("Definition missing in dictionary '%s' for word '%s'", dictionary, entry)
                            nodefs.append(FILE_ENTRY)
                        else:
                            defs.append(FILE_ENTRY)

        return defs, nodefs

pd = PersonalDictionary()
# ~ pd.lookup("Ichbin")
# ~ pd.lookup("Öl", "fd-deu-spa")
# ~ pd.missing()