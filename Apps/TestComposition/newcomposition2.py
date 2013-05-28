# -*- coding: utf-8 -*-
from GestureAgents.AppRecognizer import FakeAgent
from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgents.Events import Event
from GestureAgents.Recognizer import Recognizer, newHypothesis
import copy
from GestureAgents.Agent import Agent
from GestureAgents.Events import Event


def log(f):
    # return f
    def logme(self, *args, **kwargs):
        sargs = ", ".join([repr(a) for a in args])
        skwargs = ", ".join(["{}={}".format(k, v) for (k, v) in kwargs.iteritems()])
        print "{}.{}({})".format(self, f.__name__, ", ".join([sargs, skwargs]))
        return f(self, *args, **kwargs)
    return logme


class SensorProxyAgent(Agent):
    def __init__(self, original, creator):
        self.original_agent = original
        self.to_discard = True
        self.acquired_dict = {}
        self.sensorproxy = creator
        Agent.__init__(self, list(original.events), creator)

    def __getattr__(self, attrname):
        return getattr(self.original_agent, attrname)

    # @log
    def acquire(self, r):
        # if not self.owners:
        #     #if not owners, not acquiring is possible
        #     return False

        if not self.acquired_dict and not self.sensorproxy.to_complete:
            self.sensorproxy.acquire(self.original_agent)
        self.acquired_dict[r] = self.get_AR(r)
        return Agent.acquire(self, r)

    # @log
    def complete(self, r):
        # We find all AppRecognizer2 possibliy requiring this completion
        # and add to the SensorProxy list in order to finally complete in
        # case of completion of gesture
        del self.acquired_dict[r]
        ARlist = self.get_AR(r)
        self.sensorproxy.to_complete |= ARlist
        Agent.complete(self, r)

    # @log
    def discard(self, r):
        # if self.owners:
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
        # self.eventqueue = []
        self.register_event(self.system.newAgent(recognizer), SensorProxy._eventNewAgent)
        self.name = "SensorProxy(%s) %d" % (str(recognizer.__name__), SensorProxy.ninstances)
        SensorProxy.ninstances += 1
        self.to_complete = set()
        self.host = host
        print "Creat",self,"per",host
        host.proxies.append(self)
        self.alreadycompleted = False

    @newHypothesis
    def _eventNewAgent(self, agent):
        self.unregister_event(self.system.newAgent(self.recognizer))
        print "CREO AGENT"
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

    @log
    def complete(self):
        if self.alreadycompleted:
            return
        self.alreadycompleted = True
        for r in self.otheragent._recognizers_acquired:
            print "C ", r, r.host
        Recognizer.complete(self)

    @log
    def fail(self, cause="???"):
        Recognizer.fail(self, cause)

    @log
    def acquire(self, agent):
        Recognizer.acquire(self,agent)




class fksystem(object):

    def __init__(self, instance):
        self.instance = instance

    def newAgent(self, recognizer):
        return self.instance.AR2_newAgent(recognizer)

    def __getattr__(self, attr):
        return getattr(self.instance, attr)


class AppRecognizer2(Recognizer):
    ninstances = 0

    def __init__(self, system, original_recognizer, fksys=None):
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
        Recognizer.__init__(self, self.fksystem)
        self.name = "AppRecognizer2(%s) %d" % (str(self.original_recognizer.__name__), AppRecognizer2.ninstances)
        AppRecognizer2.ninstances += 1
        self.newAgent = Event()
        self.eventqueue = []
        self.register_event(self.fksystem.newAgent(original_recognizer), AppRecognizer2._eventNewAgent)
        self.willenqueue = True
        print self, "init"

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
            if recognizer in [TuioCursorEvents]:
                proxy = SensorProxy(self.systemsystem, recognizer, self)
                # self.proxies.append(proxy)
                self.new_agents[recognizer] = proxy.newAgent
            else:
                self.new_agents[recognizer] = Event()
                self.recognizers.append(recognizer(self.fksystem))
        return self.new_agents[recognizer]

    def execute(self):
        self.willenqueue = False
        for event_name, agent in self.eventqueue:
            self.agent.original_agent = agent
            if event_name == "finishAgent":
                self.finish()
            else:
                self.agent.events[event_name](self.agent)
        if self.to_finish:
            self.finish()

    @log
    def enqueueEvent(self, a, e):
        # if e == "finishAgent":
        #     import pdb
        #     pdb.set_trace()
        if not self.eventqueue:
            self.acquire(a)
            print "will try to complete all proxies:", [pr for pr in self.proxies if self in pr.to_complete]
            for p in self.proxies:                
                if self in p.to_complete:
                    # p.host = self #innecessari!
                    p.complete()
        if self.willenqueue:
            #copyagent = copy.copy(self.agent)
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

    @log
    def proxyexecuted(self, proxy):
        if not self.eventqueue:
            # ignore unsolicited completions
            return
        waiting = [p for p in self.proxies if self in p.to_complete]
        if not waiting:
            self.complete()

    @log
    def fail(self, cause="Unknown"):
        for p in list(self.proxies):
            print "fail {}?".format(p)
            if self in p.to_complete:
                print "yes?"
                p.to_complete.remove(self)
                print self, ">", p.to_complete
                if not p.to_complete:
                    p.fail()
                    self.proxies.remove(p)
            else:
                print "no?"
                if p.agent:
                    print p.agent.acquired_dict

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
