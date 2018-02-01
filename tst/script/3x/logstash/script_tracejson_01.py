# -*- coding: UTF-8 -*-




import pytestemb as test

import time
import random

import mock



def test_json():


    
    r = range(90) + [90]*60 + range(90, 0, -1)
    r = r + r

    for i in r:
        time.sleep(0.001)
        v = random.randint(0, 10)
        if random.shuffle([True, False]):
            v = v * (-1)        
        obj = {"time_perf":i+v, "product":"A"}
        test.trace_json(obj)
        v = random.randint(0, 10)
        if random.shuffle([True, False]):
            v = v * (-1)        
        obj = {"time_perf":(i/2)+v, "product":"B"}
        test.trace_json(obj)    
        v = random.randint(0, 10)
        obj = {"time_perf":(35 + v), "product":"C"}
        test.trace_json(obj)    
        
        v = random.randint(0,80)
        obj = {"time_perf":v, "product":"D"}
        test.trace_json(obj)  


if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

    test.add_test_case(test_json)
        
    test.run()













