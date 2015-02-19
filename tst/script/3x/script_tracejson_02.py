# -*- coding: UTF-8 -*-




import pytestemb as test

import time
import random

import mock


class JsonError(test.Test):  
    
    def json_error_dict(self):
        vector = [["test",],
                   "test",
                   10,
                   self.json_error_dict]
        for obj in vector:
            try:
                test.trace_json(obj)
                test.fail()
            except TypeError, ex:
                test.success(ex)    

    def json_error_key(self):
        vector = [{10:10}, 
                  {10.0:10},
                  {self.json_error_key:10}]
        for obj in vector:
            try:
                test.trace_json(obj)
                test.fail()
            except TypeError, ex:
                test.success(ex)
                
    def json_error_reservedkey(self):
        pass

    def json_valid(self):
        vector = [{"key_a":"test"},
                  {"key_b":10},
                  {u"ééé":u"ééé"},
                  ]
        for obj in vector:        
            test.trace_json(obj)
      
    

if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

        
    test.run_script()













