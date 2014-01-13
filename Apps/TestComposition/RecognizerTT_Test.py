#!/usr/bin/env python
# -*- coding: utf-8 -*-

from GestureAgents.Recognizer import Recognizer, newHypothesis
from GestureAgents.Agent import Agent
import math
from GestureAgentsTUIO.Gestures2D.RecognizerTap import RecognizerTap


def build_and_register_TT(RTKlass=RecognizerTap):

    class RecognizerTT_Test(Recognizer):
        rtotal = 0

        def __init__(self, system):
            Recognizer.__init__(self, system)
            self.RTKlass = RTKlass
            self.agent = None
            self.firstap = None
            self.secondtap = None
            self.thirdtap = None
            self.register_event(
                self.system.newAgent(RTKlass), RecognizerTT_Test.EventNewAgent)
            self.time = 0.3
            self.maxd = 10
            self.newAgent = self.system.newAgent(RecognizerTT_Test)

        @newHypothesis
        def EventNewAgent(self, Tap):
            self.agent = self.make_DoubleTapAgent()
            self.agent.pos = Tap.pos
            self.newAgent.call(self.agent)
            if not self.agent.is_someone_subscribed():
                self.fail(cause="Noone Interested")
            else:
                self.unregister_event(self.system.newAgent(RTKlass))
                self.register_event(Tap.newTap, RecognizerTT_Test.FirstTap)

        def FirstTap(self, Tap):
            self.firstap = Tap
            self.unregister_event(Tap.newTap)
            self.register_event(
                self.system.newAgent(RTKlass), RecognizerTT_Test.EventNewAgent2)
            self.expire_in(self.time)
            self.acquire(Tap)

        @newHypothesis
        def EventNewAgent2(self, Tap):
            if self.dist(Tap.pos, self.firstap.pos) > self.maxd:
                self.fail(cause="Max distance")
            else:
                self.unregister_event(self.system.newAgent(RTKlass))
                self.register_event(Tap.newTap, RecognizerTT_Test.SecondTap)

        def SecondTap(self, Tap):
            if self.dist(Tap.pos, self.firstap.pos) > self.maxd:
                self.fail(cause="Max distance")
            else:
                self.secondtap = Tap
                self.unregister_event(Tap.newTap)
                self.cancel_expire()
                self.register_event(
                    self.system.newAgent(RTKlass), RecognizerTT_Test.EventNewAgent3)
                self.expire_in(self.time)
                self.acquire(Tap)

        @newHypothesis
        def EventNewAgent3(self, Tap):
            if self.dist(Tap.pos, self.secondtap.pos) > self.maxd:
                self.fail(cause="Max distance")
            else:
                self.unregister_event(self.system.newAgent(RTKlass))
                self.register_event(Tap.newTap, RecognizerTT_Test.ThirdTap)

        def ThirdTap(self, Tap):
            if self.dist(Tap.pos, self.firstap.pos) > self.maxd:
                self.fail(cause="Max distance")
            else:
                self.thirdtap = Tap
                self.unregister_event(Tap.newTap)
                self.cancel_expire()
                self.acquire(Tap)
                self.complete()
                #print "I win",self
                #print self.agent.newDoubleTap.registered
                #import pdb; pdb.set_trace()
                self.fail_all_others()

        def execute(self):
            #print "I execute",self
            self.agent.pos = self.thirdtap.pos
            #print self.agent.newDoubleTap.registered
            self.agent.newTripleTap(self.agent)
            self.finish()

        def duplicate(self):
            d = self.get_copy(self.system)
            d.firstap = self.firstap
            d.secondtap = self.secondtap
            d.thirdtap = self.thirdtap
            return d

        @staticmethod
        def dist(a, b):
            dx, dy = (a[0] - b[0], a[1] - b[1])
            return math.sqrt(dx ** 2 + dy ** 2)

        def make_DoubleTapAgent(self):
            a = Agent(self,("newTripleTap",))
            return a

        # def fail(self, cause="Unknown"):
        #     print self, "fail, cause=" + cause
        #     #raise Exception("RecognizerTT_Test fail")
        #     Recognizer.fail(self)

    return RecognizerTT_Test
