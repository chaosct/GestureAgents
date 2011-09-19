#!/usr/bin/env python
# -*- coding: utf-8 -*-

all_tasks = []

def run_after(f):
    global all_tasks
    all_tasks.append(f)
    
def run_all_now():
    global all_tasks
    l = all_tasks
    all_tasks = []
    for t in l:
        t()
    
