# -*- coding: utf-8 -*-
from GestureAgents.AppRecognizer import AppRecognizer
from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgents.Events import Event


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
        self.systemsystem = system
        self.original_recognizer = original_recognizer
        if not fksys:
            self.fksystem = fksystem(self)
        else:
            self.fksystem = fksys
        AppRecognizer.__init__(self, self.fksystem, original_recognizer)

    def AR2_newAgent(self, recognizer):
        if recognizer not in self.new_agents:
            if recognizer is TuioCursorEvents:
                self.new_agents[recognizer] = self.systemsystem.newAgent(recognizer)
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
        return c
