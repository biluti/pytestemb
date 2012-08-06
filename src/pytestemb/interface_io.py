# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : interface_io is base module for io interface management
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"


 
import pytestemb


  

class InterfaceError(Exception):
    "Exception raised by InterfaceIO"
    def __init__(self, info):
        Exception.__init__(self)
        self.info = info
    def __str__(self):
        return self.info.__str__()   

 

class Interface_io:
    """ base class for interfaceIO """

    def __init__(self, name=""):
        self.name = name

    def trace_io(self, interface, data):
        pytestemb.trace_io(interface, data)

    def start(self):
        pass
    
    def stop(self):
        pass

 

 
""" Patern 

__interface__ = {}

 
def create(name):
    __interface__[name] = Interface_io()   


def start(name):
    __interface__[name].start()

   

def stop(name):   
    __interface__[name].stop()

"""  

 