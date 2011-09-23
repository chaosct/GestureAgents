#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from heapq import heappush, heappop

all_tasks = []
scheduled_tasks = []

def run_after(f):
    global all_tasks
    all_tasks.append(f)

def schedule_after(time,instance,f):
    heappush(scheduled_tasks,(datetime.datetime.now()+datetime.timedelta(seconds=time),(instance,f)))

def duplicate_instance(original,new):
    to_insert = [(t,(new,f)) for t,(i,f) in scheduled_tasks if i == original]
    for item in to_insert:
        heappush(scheduled_tasks,item)
        
def cancel_schedule(instance):
    global scheduled_tasks
    l, scheduled_tasks = scheduled_tasks, []
    for t,(i,f) in l:
        if i != instance:
            heappush(scheduled_tasks,(t,(i,f)))
    
def run_all_now():
    global all_tasks
    while all_tasks:
        l = all_tasks
        all_tasks = []
        for t in l:
            t()
    if scheduled_tasks:
        now = datetime.datetime.now()
        while scheduled_tasks and scheduled_tasks[0][0]<now:
            t,(i,f) = heappop(scheduled_tasks)
            f(i)
    while all_tasks:
        l = all_tasks
        all_tasks = []
        for t in l:
            t()
    
