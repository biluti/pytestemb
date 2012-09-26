

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


def case_0():
    """
    @goal : -
    @coverage : -
    """
    test.success("success")

def case_1():
    """
    @goal : -
    @coverage : -
    """
    pass

        
        
def start():
    pass

def stop():
    pass





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(case_0)
    test.add_test_case(case_1)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


