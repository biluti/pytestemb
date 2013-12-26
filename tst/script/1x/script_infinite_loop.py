

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




def wait_long_time():
    """
    @goal : -
    @coverage : -
    """
    for i in range(0,10):
        test.trace_script("%d" % i)
        time.sleep(60)





if __name__ == "__main__":
    
    test.set_doc(__doc__)
    test.add_test_case(wait_long_time)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


