# -*- coding: UTF-8 -*-


import pytestemb as test

import time

import mock



class MyTestException(Exception):
    pass



class TestLog(test.Test):
        
    def setup(self):
        pass
        
    def case_trace(self):
        test.trace_env("env_scope",     "trace_env")
        test.trace_io("interface",      "trace_io")
        test.trace_layer("layer_scope", "trace_layer")
        test.trace_script("trace_script")
 

    def case_exception(self):
        raise MyTestException("case_exception")

    def case_ok(self):
        test.success("ok")

    def case_ko(self):
        test.fail("ko")


 


if __name__ == "__main__":
    

        
    test.run_script()




    
    
    
    
    


