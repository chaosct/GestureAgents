# -*- coding: utf-8 -*-
from GestureAgents.AppRecognizer import FakeAgent
from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgents.Events import Event
from GestureAgents.Recognizer import Recognizer, newHypothesis
import copy
from GestureAgents.Agent import Agent
from GestureAgents.Events import Event


class SensorProxyAgent(Agent):
    def __init__(self, original, creator):
        self.original_agent = original
        self.to_discard = True
        self.acquired_dict = {}
        self.sensorproxy = creator
        Agent.__init__(self, creator, list(original.events))
        self.recycled = self.original_agent.recycled

    def __getattr__(self, attrname):
        return getattr(self.original_agent, attrname)

    def acquire(self, r):
        if not self.acquired_dict and not self.sensorproxy.to_complete:
            self.sensorproxy.acquire(self.original_agent)
        self.acquired_dict[r] = self.get_AR(r)
        return Agent.acquire(self, r)

    def complete(self, r):
        # We find all AppRecognizer2 possibliy requiring this completion
        # and add to the SensorProxy list in order to finally complete in
        # case of completion of gesture
        del self.acquired_dict[r]
        ARlist = self.get_AR(r)
        self.sensorproxy.to_complete |= ARlist
        Agent.complete(self, r)

    def discard(self, r):
        if r == self._recognizer_complete:
            if not self.sensorproxy.failed:
                # finishing
                if not self.sensorproxy.executed:
                    self.to_discard = True
                else:
                    self.sensorproxy.finish()
            else:
                #Agent fail
                pass
        else:
            # fail
            if r in self.acquired_dict:
                del self.acquired_dict[r]
                if not self.acquired_dict and not self._recognizer_complete:# and self.owners:
                    self.sensorproxy.discard(self.original_agent)
        Agent.discard(self, r)

    def get_AR(self, r):
        rlist = set([r])
        ARlist = set()
        while rlist:
            R = rlist.pop()
            if isinstance(R, AppRecognizer2):
                ARlist.add(R)
            else:
                if R.agent:
                    for e in R.agent.events.itervalues():
                        for i in e.lookupf:
                            rlist.add(i)
        return ARlist


class SensorProxy(Recognizer):
    ninstances = 0

    def __init__(self, system, recognizer, host):
        Recognizer.__init__(self, system)

        self.recognizer = recognizer
        self.newAgent = Event()
        self.register_event(self.system.newAgent(recognizer), SensorProxy._eventNewAgent)
        self.name = "SensorProxy(%s) %d" % (str(recognizer.__name__), SensorProxy.ninstances)
        SensorProxy.ninstances += 1
        self.to_complete = set()
        self.host = host
        host.proxies.append(self)
        self.alreadycompleted = False

    @newHypothesis
    def _eventNewAgent(self, agent):
        self.unregister_event(self.system.newAgent(self.recognizer))
        self.agent = self._makeAgentAgent(agent)
        self.newAgent(self.agent)
        self.otheragent = agent
        if not self.agent.is_someone_subscribed():
            self.fail("Noone interested")
        else:
            for ename, event in agent.events.iteritems():
                ffff = lambda self, a, eventname=ename: self.enqueueEvent(
                    a, eventname)
                self.register_event(event, ffff)

    def enqueueEvent(self, a, e):
        if self.failed:
            return
        self.agent.original_agent = a
        if e == "finishAgent":
            self.agent.finish()
        else:
            self.agent.events[e](self.agent)

    def execute(self):
        self.executed = True
        if self.agent.to_discard:
            pass
        to_complete = self.to_complete
        self.to_complete = set()
        for r in to_complete:
            r.proxyexecuted(self)

    def _makeAgentAgent(self, agent):
        a = SensorProxyAgent(agent, self)
        return a

    def duplicate(self):
        d = self.get_copy(self.system, self.recognizer, self.host)
        d.newAgent = self.newAgent

    def __repr__(self):
        return self.name

    def complete(self):
        if self.alreadycompleted:
            return
        self.alreadycompleted = True
        Recognizer.complete(self)


class fksystem(object):

    def __init__(self, instance):
        self.instance = instance

    def newAgent(self, recognizer):
        return self.instance.AR2_newAgent(recognizer)

    def __getattr__(self, attr):
        return getattr(self.instance, attr)


class AppRecognizer2(Recognizer):
    ninstances = 0

    def __init__(self, system, original_recognizer, fksys=None, sensors=None):
        self.new_agents = {}
        self.recognizers = []
        self.proxies = []
        self.systemsystem = system
        self.original_recognizer = original_recognizer
        if not fksys:
            self.fksystem = fksystem(self)
        else:
            self.fksystem = fksys
        self.to_finish = False

        #list of sensors that require a Proxy
        if sensors is None:
            #Default is TUIO cursor events only
            sensors = [TuioCursorEvents]
        self.sensorlist = sensors 

        Recognizer.__init__(self, self.fksystem)
        self.name = "AppRecognizer2(%s) %d" % (str(self.original_recognizer.__name__), AppRecognizer2.ninstances)
        AppRecognizer2.ninstances += 1
        self.newAgent = Event()
        self.eventqueue = []
        self.register_event(self.fksystem.newAgent(original_recognizer), AppRecognizer2._eventNewAgent)
        self.willenqueue = True
        # is original_recognizer a sensor and we have to assume that we
        # will be dealing directly with proxies
        self.directProxy = False

    @newHypothesis
    def _eventNewAgent(self, agent):
        self.unregister_event(self.fksystem.newAgent(self.original_recognizer))
        self.agent = self._makeAgentAgent(agent)
        self.newAgent(self.agent)
        self.otheragent = agent
        if not self.agent.is_someone_subscribed():
            self.fail("Noone interested")
        else:
            for ename, event in agent.events.iteritems():
                ffff = lambda self, a, eventname=ename: self.enqueueEvent(
                    a, eventname)
                self.register_event(event, ffff)

    def AR2_newAgent(self, recognizer):
        if recognizer not in self.new_agents:
            if recognizer in self.sensorlist:
                proxy = SensorProxy(self.systemsystem, recognizer, self)
                self.new_agents[recognizer] = proxy.newAgent
            else:
                self.new_agents[recognizer] = Event()
                self.recognizers.append(recognizer(self.fksystem))
        return self.new_agents[recognizer]

    def execute(self):
        if self.directProxy:
            # we wait!
            return
        self.willenqueue = False
        for event_name, agent in self.eventqueue:
            self.agent.original_agent = agent
            if event_name == "finishAgent":
                self.finish()
            else:
                self.agent.events[event_name](self.agent)
        if self.to_finish:
            self.finish()

    def enqueueEvent(self, a, e):
        if not self.eventqueue:
            self.acquire(a)
            proxies = [pr for pr in self.proxies if self in pr.to_complete]
            if not proxies:
                self.directProxy = True
                self.complete()
                proxies = [pr for pr in self.proxies if self in pr.to_complete]
            for p in proxies:                
                p.complete()
        if self.willenqueue:
            original_agent = copy.copy(a)
            self.eventqueue.append((e, original_agent))
        else:
            self.agent.original_agent = a
            if e == "finishAgent":
                if self.executed:
                    self.finish()
                else:
                    self.to_finish = True
            else:
                self.agent.events[e](self.agent)

    def proxyexecuted(self, proxy):
        if not self.eventqueue:
            # ignore unsolicited completions
            return
        waiting = [p for p in self.proxies if self in p.to_complete]
        if not waiting:
            if self.directProxy:
                self.directProxy = False
                self.execute()
            else:
                self.complete()

    def fail(self, cause="Unknown"):
        for p in list(self.proxies):
            if self in p.to_complete:
                p.to_complete.remove(self)
                if not p.to_complete:
                    p.safe_fail()
                    self.proxies.remove(p)
            # else:
            #     if p.agent:
            #         print p.agent.acquired_dict
        Recognizer.fail(self,cause)

    def _makeAgentAgent(self, agent):
        a = FakeAgent(agent, self)
        return a

    def duplicate(self):
        d = self.get_copy(self.system, self.original_recognizer, fksys=self.fksystem)
        d.new_agents = self.new_agents
        d.recognizers = self.recognizers
        d.proxies = self.proxies
        d.newAgent = self.newAgent

    def __repr__(self):
        return self.name
