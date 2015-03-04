# -*- coding: UTF-8 -*-




import pytestemb as test

import time
import random

import mock


class JsonError(test.Test):  
    
 

    def json_valid(self):
        vector = [{"crash":{"sha1":"445454", "exp":"assert"}},]
        for obj in vector:        
            test.trace_json(obj)
        test.success()
      
    

if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

        
    test.run_script()













