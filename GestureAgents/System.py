from GestureAgents.Events import Event
import GestureAgents.Reactor as Reactor

class System(object):
    """
    Reference implementation of a system holding a recognizer tree
    """
    def __init__(self, sources=None):
        self.new_agents = {}
        self.recognizers = []
        self.sources = sources or []
        self.running = False

    def newAgent(self, recognizer):
        if recognizer not in self.new_agents:
            if recognizer in self.sources:
                self.new_agents[recognizer] = recognizer.newAgent
            else:
                self.new_agents[recognizer] = Event()
                self.recognizers.append(recognizer(self))
        return self.new_agents[recognizer]

    def run_apps(self):
        "Minimal reactor loop for the event system to work"
        
        self.running = True

        while self.running:
            self.update()
            Reactor.run_all_now()

    def stop(self):
        self.running=False

    def update(self):
        'just override this method'
        pass

