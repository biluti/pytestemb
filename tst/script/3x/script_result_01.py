# -*- coding: UTF-8 -*-




import pytestemb as test

import time


import mock





def test_ok():
    test.success()
    time.sleep(0.1)
    
def test_ko():
    test.fail()
    time.sleep(0.1)    


if __name__ == "__main__":
    
    
    for i in range(10):
        test.add_test_case(test_ok)
        test.add_test_case(test_ko)
        
    test.run_script()













