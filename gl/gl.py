# -*- coding: UTF-8 -*-

import sys
import time
import traceback
import json

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

class Global:

    def __init__(self):
        self.LOG = None
        self.ERR = None
        self.minStuffid = 1
        self.maxStuffid = None

    def setErr(self, err):
        self.ERR = err
        self.LOG.error(err)

    def dumpJson(self, pyObj):
        return json.dumps(pyObj, ensure_ascii=False, sort_keys=True, indent=4)

GL = Global()
