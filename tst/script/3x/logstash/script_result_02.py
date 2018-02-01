# -*- coding: UTF-8 -*-




import pytestemb as test

import time
import random

import mock



def test_ok():
    test.success()
    time.sleep(ran_test_time())
    
def test_ko():
    test.fail()
    time.sleep(ran_test_time())    


def ran_test_number():
    return random.randint(5, 40)

def ran_test_time():
    return random.randint(1, 5)



if __name__ == "__main__":
    
    
    for i in range(ran_test_number()):
        test.add_test_case(test_ok)
    for i in range(ran_test_number()):
        test.add_test_case(test_ko)
        
    test.run()













