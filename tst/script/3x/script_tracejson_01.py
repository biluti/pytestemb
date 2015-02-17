# -*- coding: UTF-8 -*-




import pytestemb as test

import time

import mock



def test_json():
    
    
    for i in range(100):
        time.sleep(0.2)
        obj = {"time_perf":i}
        test.trace_json(obj)
    



if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

    test.add_test_case(test_json)
        
    test.run_script()













