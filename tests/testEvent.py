'''
Created on 18/05/2012

@author: carles
'''
from nose.tools import ok_, raises
from GestureAgents.Events import Event, EventClient


class ChangeValue(object):
    def __init__(self):
        self.testvalue = 0
        self.calls = 0

    def changevalue(self, val):
        self.testvalue = val
        self.calls += 1


def testEvent():
    e = Event()
    yield ok_, (e.registered == []), "initialization"
    yield ok_, (e.lookupf == {}), "initialization"

    cv = ChangeValue()
    e.register(ChangeValue.changevalue, cv)

    values = list(range(5))

    for v in values:
        e.call(v)
        yield ok_, (cv.testvalue == v)

    cv2 = ChangeValue()
    e.register(ChangeValue.changevalue, cv2)

    for v in values:
        e(v)
        yield ok_, (cv.testvalue == v)
        yield ok_, (cv2.testvalue == v)

    yield ok_, (cv.calls == 2 * len(values)), "No duplicated calls"
    yield ok_, (cv2.calls == len(values)), "No duplicated calls"

    lastcalls = cv2.calls
    e.unregister(cv2)
    e(99)
    yield ok_, (cv2.calls == lastcalls), "unregistering"


class evtExc(object):
    def noarguments(self):
        pass

    def oneargument(self, a):
        pass

    def willraiseFailed(self):
        from GestureAgents.Recognizer import RecognizerFailedException
        raise RecognizerFailedException()

    def willraiseattrerr(self):
        raise AttributeError


def testEventExceptions():
    i = evtExc()

    e = Event()
    e.register(evtExc.noarguments, i)
    yield raises(TypeError)(e.call), 9

    e = Event()
    e.register(evtExc.oneargument, i)
    yield raises(TypeError)(e.call),

    e = Event()
    e.register(evtExc.willraiseFailed, i)
    yield e.call

    e = Event()
    e.register(evtExc.willraiseattrerr, i)
    yield raises(AttributeError)(e.call),


class Ect(EventClient):
        def __init__(self):
            EventClient.__init__(self)
            self.testvalue = 0

        def changevalue(self, val):
            self.testvalue = val


def testEventClient():

    ec = Ect()
    e = Event()
    e2 = Event()

    yield ok_, (ec.registers == {})
    ec.register_event(e, Ect.changevalue)
    ec.register_event(e2, Ect.changevalue)
    e(8)
    yield ok_, (ec.testvalue == 8)
    e2(9)
    yield ok_, (ec.testvalue == 9)
    ec.unregister_event(e2)
    e2(10)
    yield ok_, (ec.testvalue != 10)
    e(11)
    yield ok_, (ec.testvalue == 11)
    ec.unregister_all()
    e(12)
    yield ok_, (ec.testvalue != 12)


def testEventClientcopy():
    ec = Ect()
    ec2 = Ect()
    e = Event()
    e2 = Event()

    ec.register_event(e, Ect.changevalue)
    ec.copy_to(ec2)
    ec.register_event(e2, Ect.changevalue)

    e(1)
    yield ok_, (ec.testvalue == 1)
    yield ok_, (ec2.testvalue == 1)
    e2(2)
    yield ok_, (ec.testvalue == 2)
    yield ok_, (ec2.testvalue != 2)
