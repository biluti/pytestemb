# -*- coding: UTF-8 -*-




import pytestemb




import mock


import time


class TimeStamp(pytestemb.Test):
    
   
    def setup(self):
        pass
    
    def test_0(self):
        time.sleep(60)
        obj = {"test":0}
        pytestemb.trace_json(obj)
        
    def test_1(self):
        time.sleep(60)
        obj = {"test":1}
        pytestemb.trace_json(obj)

    def test_2(self):
        time.sleep(60)
        obj = {"test":2}
        pytestemb.trace_json(obj)


if __name__ == "__main__":
    
    
        
    pytestemb.run()













