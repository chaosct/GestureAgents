#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
A policy function must accept the arguments involving the context and the action.
It must return True, False, or None:
* True if the situation _must_ be changed
* False if the situation _must_not_ be changed
* None if the situattion doesn't apply to the policy rule

For instance, when receiving confirm on an Agent, it has to decide to substitute
the current confirmed winner Recognizer by the new one.

a correct policy could be:

def never(CurrentRecognizer, NewRecognizer):
    return False

Policies should have order that can be define by its priority (-100,100).

for convenience -100 is the first rule and 100 the last one.

"""


class PolicyRuleset(object):
    def __init__(self, debugname="Policy", debug=False):
        self._policies = dict()
        self.debugname = debugname
        self.debug = debug

    def result(self, *args, **kwargs):
        for priority in sorted(self._policies):
            for policy in self._policies[priority]:
                result = policy(*args, **kwargs)
                if result is not None:
                    if self.debug:
                        print "%s(%s,%s):" % (self.debugname, args[0], args[1]),
                        print policy.__doc__ or policy, " = ", result
                    return result
        if self.debug:
            print "%s(%s,%s):" % (self.debugname, args[0], args[1]),
            print "default to None"
        return None

    def add_rule(self, rule, priority=0):
        self._policies.setdefault(priority, []).append(rule)
        return rule

    def __repr__(self):
        from StringIO import StringIO
        description = StringIO()
        print >>description, "PolicyRuleset:"
        for priority in sorted(self._policies):
            for policy in self._policies[priority]:
                desc = policy.__doc__ or policy
                print >>description, "\t(%d)" % priority, desc
        return description.getvalue()

    def rule(self, priority=0):
        """Decorator to add a rule to this ruleset:
        @MyRuleset.rule(10)
        def myrule(..):
        """
        return lambda f: self.add_rule(f, priority)


def set_gesture_priority(over,under):
    from GestureAgents.AppRecognizer import SensorProxy
    from GestureAgents.Agent import Agent
    def explicit_priority(r1, r2):
        if type(r1) == SensorProxy and type(r2) == SensorProxy:
            if r1.host.original_recognizer == under and \
               r2.host.original_recognizer == over:
                return True
    explicit_priority.__doc__ = "explicit priority ({} > {})".format(over,under)
    Agent.compatibility_policy.rule(0)(explicit_priority)