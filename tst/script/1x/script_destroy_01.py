

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

        
def start():
    pass

def stop():
    pass


def destroy():
    pass




if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(defaultValue)
    test.set_cleanup(stop)
    test.set_destroy(destroy)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


