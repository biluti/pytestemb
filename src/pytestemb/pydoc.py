# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : pydoc manages doc extraction from script
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"







import pytestemb.utils as utils


TYPE_SCRIPT     = "script"
TYPE_SETUP      = "setup"
TYPE_CLEANUP    = "cleanup"
TYPE_CASE       = "case"

KEY_TYPE = "type"
KEY_NAME = "name"
KEY_DOC  = "doc"



class Pydoc:
    
    __single = None
    
    def __init__(self, result):
        self.result = result

    @classmethod
    def create(cls, result):
        cls.__single = cls(result)
        return cls.__single
    
    @classmethod
    def get(cls):
        return cls.__single 
        
                
    
    def set_doc(self, doc):
        des = dict()
        des[KEY_TYPE] = TYPE_SCRIPT
        des[KEY_NAME] = utils.get_script_name()
        if doc is None :
            des[KEY_DOC] = ""
        else:
            des[KEY_DOC] = Pydoc.clean(doc)
        self.result.doc(des)
        
        
    def set_setup(self, funcsetup):
        self._function(TYPE_SETUP, funcsetup)
    
    def set_cleanup(self, funccleanup):
        self._function(TYPE_CLEANUP, funccleanup)
    
    def add_test_case(self, funccase):
        self._function(TYPE_CASE, funccase)
        
    
    def _function(self, ftype, func):
        des = dict()
        des[KEY_TYPE] = ftype
        des[KEY_NAME] = func.func_name
        if func.__doc__ is None :
            des[KEY_DOC] = ""
        else:
            des[KEY_DOC] = Pydoc.clean(func.__doc__)
        self.result.doc(des)
    
    @staticmethod
    def clean(doc):
        doc = doc.expandtabs(4)
        doc = doc.strip("\n")
        return doc

        
import sys
import importlib
import pytestemb.valid as valid


class DocGen:
    
    def __init__(self, basepath):
        self.basepath = basepath
        sys.path.append(self.basepath)
    
    
    
    def project(self, sub):
        
        import os
        
        directory = os.path.join(self.basepath, sub)
        
        lscript = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".py") and file not in ["__init__.py"]:
                    
                    #print root
                    #print os.path.relpath(os.path.join(root, file), self.basepath)
                    lscript.append(os.path.relpath(os.path.join(root, file), self.basepath))
                    #print os.path.join(root, file)
        
        for l in lscript:
            l = l.replace("/", ".")
            l = l.strip(".py")
            self.script_doc(l)
    
    
    
    def script_doc(self, name):
        
        dm = importlib.import_module(name)
        
        
        tc = valid.Valid.retrieve_test_class_(dm)
        if len(tc) != 1:
            raise Exception("One class Test expected")
        else:
            pass
        
        setup, cases, cleanup =  valid.Valid.retrieve_test_method(tc[0]())
        
        print ""
        print name 
        print "\n".join(cases)
        
        
        
         
    
    
    
        
        
        

    
    
    
    
    
    
        
    
        
    
