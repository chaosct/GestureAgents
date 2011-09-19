#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Event:
    "A simple event with subscription"
    def __init__(self):
        self.registered = []
        self.lookupf = {}
    def register(self,f,i):
        #print "register",f,i 
        if i not in self.lookupf:
            self.registered.append((f,i))
            self.lookupf[i]=f
            
    def unregister(self,i):
        f = self.lookupf[i]
        #print "unregister",f,i
        del self.lookupf[i]
        self.registered.remove((f,i))
        
    def call(self,*args,**kwargs):
        for f,i in list(self.registered):
            f(i,*args,**kwargs)

class EventClient:
    "A class that unregisters itself from events"
    def __init__(self):
        self.registers = dict()
    def register_event(self,event,f):
        event.register(f,self)
        self.registers[event]=f
    def unregister_event(self,event):
        del self.registers[event]
        event.unregister(self)
    def unregister_all(self):
        for event in self.registers:
            event.unregister(self)
        self.registers.clear()
    def copy_to(self,d):
        for event, f in self.registers.iteritems():
            d.register_event(event,f)
        


