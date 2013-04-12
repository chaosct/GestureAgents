# -*- coding: utf-8 -*-
from GestureAgents.AppRecognizer import AppRecognizer
from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgents.Events import Event


class AppRecognizer2(AppRecognizer):
    def __init__(self, system, original_recognizer):
        self.new_agents = {}
        self.recognizers = []
        self.systemsystem = system
        AppRecognizer.__init__(self, self, original_recognizer)

    def newAgent(self, recognizer):
        if recognizer not in self.new_agents:
            if recognizer is TuioCursorEvents:
                self.new_agents[recognizer] = self.systemsystem.newAgent(recognizer)
            else:
                self.new_agents[recognizer] = Event()
                self.recognizers.append(recognizer(self))
        return self.new_agents[recognizer]

