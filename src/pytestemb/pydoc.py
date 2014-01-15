# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : pydoc manages doc extraction from script
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import os        
import sys
import importlib


import pytestemb.valid as valid
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





class DocGen:
    
    CASE_DOC = "case_doc"
    SCRIPT   = "script"
    CASE     = "case"
    NAME     = "name"
    DOC      = "doc"
    
    def __init__(self, basepath):
        self.basepath = basepath
        sys.path.append(self.basepath)
    
    
    def scan_project(self, sub):
        directory = os.path.join(self.basepath, sub)
        lscript = []
        for root, _dirs, files in os.walk(directory):
            for filen in files:
                if filen.endswith(".py") and filen not in ["__init__.py"]:
                    lscript.append(os.path.relpath(os.path.join(root, filen), self.basepath))
        return [ll.replace("/", ".").strip(".py") for ll in lscript ]        
   
    
    @staticmethod
    def _parse_class_doc(doc_str):
        res = {}
        if doc_str is None:
            pass
        else:
            count = 0
            for line in doc_str.splitlines():
                try:
                    key, value = line.strip(" \t").split(":")
                    res[key.strip(" \t")] = value.strip(" \n")
                except (IndexError, ValueError) as ex:
                    res["error line=%d" % count] = "except : %s, value : '%s'" % (ex, line)
                count += 1
        return res
        
    
    
    def script_doc(self, name):
        res = {self.SCRIPT:name, self.DOC:[], self.CASE:[]}
        dm = importlib.import_module(name)
        tc = valid.Valid.retrieve_test_class_(dm)
        
        if len(tc) != 1:
            raise Exception("One class 'Test' expected")
        else:
            pass
        
        inst = tc[0]()
        
        res[self.DOC] = self._parse_class_doc(inst.__doc__)
        
        _setup, cases, _cleanup =  valid.Valid.retrieve_test_method(inst)

        for case in cases:
            func_case = getattr(inst, case)
            res[self.CASE].append({self.NAME:func_case.func_name, self.CASE_DOC:func_case.func_doc})
            
        return res

        
        
         
    
    
    
        
        
        

    
    
    
    
    
    
        
    
        
    
