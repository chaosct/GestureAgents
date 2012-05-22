'''
Created on 18/05/2012

@author: carles
'''

from GestureAgents.Reactor import run_after, run_all_now, schedule_after, cancel_schedule, duplicate_instance
import time

class ChangeValue(object):
    def __init__(self):
        self.calls = 0
    def callme(self):
        self.calls += 1
        
def testRunAfter():
    cv = ChangeValue()
    run_all_now()
    assert cv.calls == 0
    run_after(cv.callme)
    assert cv.calls == 0
    run_all_now()
    assert cv.calls == 1
    run_all_now()
    assert cv.calls == 1

def testSchedule():
    cv = ChangeValue()
    run_all_now()
    assert cv.calls == 0
    schedule_after(1,cv, ChangeValue.callme)
    assert cv.calls == 0
    run_all_now()
    assert cv.calls == 0
    time.sleep(1)
    run_all_now()
    assert cv.calls == 1
    

def testCancelSchedule():
    cv = ChangeValue()
    schedule_after(1,cv, ChangeValue.callme)
    cancel_schedule(cv)
    time.sleep(1)
    run_all_now()
    assert cv.calls == 0

def testDuplicate():
    cv1 = ChangeValue()
    cv2 = ChangeValue()
    schedule_after(1,cv1, ChangeValue.callme)
    duplicate_instance(cv1, cv2)
    time.sleep(1)
    run_all_now()
    assert cv1.calls == 1
    assert cv2.calls == 1
    