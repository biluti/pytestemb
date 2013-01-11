# -*- coding: UTF-8 -*-

""" 

"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"






class PytestembError(Exception):
    """Exception raised by Pytestemb"""
    def __init__(self, info):
        Exception.__init__(self)
        self.info = info
    def __str__(self):
        return self.info.__str__()  
    
    
