

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
    print((test.get_config()))
    print((test.get_mode()))



        
        
def start():
    pass

def stop():
    pass





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(defaultValue)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


