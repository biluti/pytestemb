




import pytestemb as test


import time


def defaultValue():
    test.assert_true(1==1, "1==1")

def boundValue():
    test.trace_script("No wait")
    test.assert_true(1==1, "")
    test.assert_true(1==1, "1==1")
    test.assert_true(1==1, "1==1")
    test.trace_script("Easy trace")




def loop():
    
    for i in range(0,10):
        test.assert_true(1==1, "1==1 loop:%d" % i)
        time.sleep(0.01)





if __name__ == "__main__":
    
    
    test.add_test_case(defaultValue)
    test.add_test_case(boundValue)
    test.add_test_case(loop)
    test.run()

    
    
    
    
    
    
    
    
    
    


