

"""
@goal: -
@todo: -
@warning: -
@requires: -
@precondition: -
@postcondition: -
"""



import pytestemb as test


import time


def defaultValue():
    """
    @goal : -
    @coverage : -
    """
    test.assert_true_fatal(1==2, "1==2")
    test.assert_true(1==1, "1==1")

def boundValue():
    """
    @goal : -
    @coverage : -
    """    
    test.trace_script("No wait")
    test.assert_true(1==1, "")
    test.assert_true(1==1, "1==1")
    test.assert_true(1==2, "1==2")
    test.assert_true(1==1, "1==1")
    test.trace_script("Easy trace")




def loop():
    """
    @goal : -
    @coverage : -
    """
    test.assert_equal(1, 1, "equal")
    for i in range(0,10):
        test.assert_true(1==1, "1==1")
        time.sleep(0.01)
        
        
def start():
    pass

def stop():
    pass





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(defaultValue)
    test.add_test_case(boundValue)
    test.add_test_case(loop)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


