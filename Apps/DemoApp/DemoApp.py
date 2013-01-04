
from GestureAgentsTUIO.Tuio import TuioCursorEvents
from GestureAgents.AppRecognizer import AppRecognizer

class DemoApp(object):
	"""docstring for DemoApp"""
	def __init__(self):
		AppRecognizer(TuioCursorEvents).newAgent.register(DemoApp.newAgentPaint,self)

	def newAgentPaint(self,agent):
		print "hola"
		agent.updateCursor.register(DemoApp.event_painting,self)

	def event_painting(self,Point):
		print Point.pos

if __name__ == '__main__':
	import GestureAgentsDemo
	app = DemoApp()
	GestureAgentsDemo.run_apps()

		