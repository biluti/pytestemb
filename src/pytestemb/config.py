# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : config manages configuration runtime of other modules
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"


import sys
import time



class ConfigError(Exception):
    """ Exception raised by config"""
    def __init__(self, info):
        Exception.__init__(self)
        self.info = info
    def __str__(self):
        return self.info.__str__() 
    
    




class Config:
    def __init__(self, trace):
        self.conf = {}
        self.trace = trace
        
    def trace_config(self, msg):
        self.trace.trace_config(msg)
        
    def start(self):
        pass

    def get_config(self, key):
        if self.conf.has_key(key):
            return self.conf[key]
        else:
            raise ConfigError("Key \"%s\" not in configuration" % key.__str__())
    
    def to_string(self):
        ret = ""
        for k,v in self.conf.items():
            ret = "%s = %s\n" % (k,v)
        return ret 
         




class ConfigStdin(Config):
    
    def __init__(self, trace):
        Config.__init__(self, trace)
        
        
    def add_line(self, line):
        try:
            k, v = line.split(":")
            self.conf[k] = v
        except :
            self.trace_config("Error line invalid : %s" % line)
        
    def start(self):
        
        self.trace_config("CONFIG = STDIN")
        time.sleep(0.5)
        try:
            line = sys.stdin.readline()
            while line:
                line = line[:-1]
                if line == "END" : 
                    break
                else :
                    self.add_line(line)
                line = sys.stdin.readline()
        except Exception , ex:
            self.trace_config("CONFIG = Exception %s" % ex.__str__())
            
        self.trace_config(self.conf.__str__())
        
    
    
def create(interface, trace):    
    if   interface == "none" :
        return Config(trace)
    elif interface == "stdin" :
        return ConfigStdin(trace)
    else:
        assert False
    
    
    