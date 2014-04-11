=============
GestureAgents
=============


Author: Carles F. Julià <carles.fernandez@upf.edu>

Description/Abstract:
GestureAgents is a framework for building multi-user systems with support for concurrent multi-tasking. Shareable interfaces, those that can be used by more than one person at a time, can play an important role in the collaboration; but for that to happen, systems must support participants to develop different tasks simultaneously. GestureAgents provides a solution to implement such systems and to recognize the gestures of different applications running simultaneously.


Testing:
    There are some example Apps in the Apps directory, to test them you just have to execute the python program from inside its folder.
    TIP: you should add this main folder to your PYHONPATH:
    $ cd Apps/DemoApp
    $ PYTHONPATH=../.. python DemoApp.py

    Use TUIO events to interact with the demos (reacTIVision, TUIOSimulator, etc)
