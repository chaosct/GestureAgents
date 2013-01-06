'''
Created on 18/05/2012

@author: carles
'''
from GestureAgents.Agent import Agent
from GestureAgents.Events import Event
import GestureAgents.Reactor as Reactor
from nose.tools import ok_, raises


class Creator(object):
        newAgent = Event()

eventlist = ('testevent1', 'test2')


def testInit():
    agent = Agent(eventlist, Creator)
    yield is_empty, agent


def is_empty(agent):
    assert agent._recognizers_acquired == []
    assert agent._recognizer_complete is None
    assert sorted(
            agent.events.keys()) == sorted(list(eventlist) + ["finishAgent"])
    assert agent.owners == [Creator]
    assert agent.name == str(Creator) + " Agent"
    assert agent.newAgent == Creator.newAgent
    assert agent.completed == False
    assert agent.finished == False
    assert agent.recycled == False


class FakeRec:
    pass


def testAcquire():
    agent = Agent(eventlist, Creator)
    recog = FakeRec()
    yield agent.acquire, recog
    yield raises(AssertionError)(is_empty), agent


def testSimpleDiscard():
    agent = Agent(eventlist, Creator)
    recog = FakeRec()
    agent.acquire(recog)
    agent.discard(recog)
    yield is_empty, agent


def testSimpleComplete():
    agent = Agent(eventlist, Creator)
    recog = FakeRec()
    agent.acquire(recog)
