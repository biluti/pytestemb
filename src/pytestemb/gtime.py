# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : gtime manages time for time stamping for other modules
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



import time


class Gtime():

    __single = None
    
    def __init__(self):
        Gtime.__single = self       
        
        self.start_date     = time.localtime()
        self.start_clock    = time.time()
        
    def get_time(self):
 
        return (time.time() - self.start_clock)
    
    @staticmethod
    def create():
        if Gtime.__single is None :
            return Gtime()
        else:
            return Gtime.__single
        
        
        




        