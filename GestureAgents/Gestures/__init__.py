#!/usr/bin/env python
# -*- coding: utf-8 -*-

#walk this directory and import all recognizers into here

import os
import os.path
import sys
import inspect
from GestureAgents.Recognizer import Recognizer

_DIR,_FNAME = os.path.split(__file__)
_current_module = sys.modules[__name__]

_modules = [__name__+'.'+os.path.splitext(f)[0] for f in os.listdir(_DIR) if f.endswith('.py') and os.path.splitext(f)[0] != os.path.splitext(_FNAME)[0]]
recognizers = []

for mm in _modules:
    __import__(mm)
    module = sys.modules[mm]
    for name, klass in inspect.getmembers(module):
        if inspect.isclass(klass) and issubclass(klass,Recognizer) and klass is not Recognizer and klass not in recognizers:
            recognizers.append(klass)
            setattr(_current_module,name,klass)

def load_all():
    for c in recognizers:
        c()

