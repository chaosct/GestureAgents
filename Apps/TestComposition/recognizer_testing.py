# -*- coding: utf-8 -*-
from GestureAgentsTUIO.Tuio import TuioAgentGenerator
import GestureAgents.Reactor as Reactor
import GestureAgents.Gestures as Gestures
from GestureAgents.Agent import Agent


def test_events(evlist):
    """Program a series of input events for testing:
    [(type, arg1, arg2, [(timestamp1, event1 ),
                         (timestamp2, event2 ), ...] ),...]
    returns the total duration of the events + 1 seconds
    """
    maxtime = 0
    for entry in evlist:
        t = entry[0]
        if t == 'f':
            sid, pos, events = entry[1:]
            a = TuioAgentGenerator.makeCursorAgent()
            a.pos = pos
            a.posx = pos[0]
            a.posy = pos[1]
            a.sessionid = sid
            a.xmot = 0
            a.ymot = 0
            a.mot_accel = 0
            for e in events:
                time, ev_type = e[:2]
                maxtime = max(maxtime, time)
                if ev_type == 'in':
                    f = lambda s, a=a: (a.newAgent(a), a.newCursor(a))
                elif ev_type == 'out':
                    f = lambda s, a=a: (a.removeCursor(a), a.finish())
                else:
                    raise NotImplementedError
                Reactor.schedule_after(time, None, f)
    return maxtime+1


def run_apps(maxtime, debug=False):
    "Minimal reactor loop for the event system to work"
    if debug:
        if Gestures.recognizers_loaded:
            print "Loaded %d gesture recognizers:" % len(Gestures.recognizers)
            for r in Gestures.recognizers:
                print "\t%s" % str(r)

        print "=" * 5 + "Agent.completion_policy Policy rules:" + "=" * 5
        print Agent.completion_policy
    running = [True]

    def stop(a):
        running[0] = False
    Reactor.schedule_after(maxtime, None, stop)
    while running[0]:
        Reactor.run_all_now()
