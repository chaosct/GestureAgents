# -*- coding: utf-8 -*-
from GestureAgents.AppRecognizer import AppRecognizer
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
        Agent.__init__(self, list(original.events), creator)

    def __getattr__(self, attrname):
        return getattr(self.original_agent, attrname)

    def acquire(self, r):
        self.owners[0].acquire(self.original_agent)
        return Agent.acquire(self, r)

    @log
    def complete(self, r):
        print "PASSA ALGO?"
        print self.owners
        #la pregunta és: qui està completant?
        #r és el recognizer inmediat
        #r.agent deu ser interessant per a algú
        #r.agent.events conté els r interessats
        #goto 0
        #provem de buscar-ho
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
        print "ARLIST: ", ARlist
        self.owners[0].to_complete |= ARlist
        Agent.complete(self, r)

    def discard(self, r):
        if r == self._recognizer_complete:
            # finishing
            if not self.owners[0].executed:
                # self.owners[0].host.safe_fail("Proxy was not confirmed")
                self.to_discard = True
            else:
                self.owners[0].finish()
        else:
            # fail
            pass
        Agent.discard(self, r)


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
        host.proxies.append(self)

    @log
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

    @log
    def enqueueEvent(self, a, e):
        self.agent.original_agent = a
        if e == "finishAgent":
            self.agent.finish()
        else:
            self.agent.events[e](self.agent)

    @log
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

    @log
    def duplicate(self):
        d = self.get_copy(self.system, self.recognizer, self.host)
        d.newAgent = self.newAgent

    def __repr__(self):
        return self.name




class fksystem(object):

    def __init__(self, instance):
        self.instance = instance

    def newAgent(self, recognizer):
        return self.instance.AR2_newAgent(recognizer)

    def __getattr__(self, attr):
        return getattr(self.instance, attr)


class AppRecognizer2(AppRecognizer):

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
        AppRecognizer.__init__(self, self.fksystem, original_recognizer)
        self.name = "AppRecognizer2(%s) %d" % (str(self.original_recognizer.__name__), AppRecognizer.ninstances-1)

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

    def get_copy(self, system, recognizer):
        c = super(AppRecognizer2, self).get_copy(self.system,
                                                 self.original_recognizer,
                                                 fksys=self.fksystem)
        c.new_agents = self.new_agents
        c.recognizers = self.recognizers
        c.proxies = self.proxies
        return c

    @log
    def execute(self):
        AppRecognizer.execute(self)
        if self.to_finish:
            self.finish()

    @log
    def enqueueEvent(self, a, e):
        print "OLA K ASE"
        if not self.eventqueue:
            print "ASE IN O K ASE"
            self.acquire(a)
            for p in self.proxies:
                print "p: ", p
                if self in p.to_complete:
                    print "COMPLETE please:", p
                    p.host = self
                    # if repr(p) == "SensorProxy(TuioCursorEvents) 5":
                    #     import pdb
                    #     pdb.set_trace()
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
            print "not for me"
            return
        waiting = [p for p in self.proxies if self in p.to_complete]
        if not waiting:
            self.complete()

    @log
    def fail(self, cause="Unknown"):
        for p in self.proxies:
            if self in p.to_complete:
                p.to_complete.remove(self)
                if not p.to_complete:
                    p.fail()


