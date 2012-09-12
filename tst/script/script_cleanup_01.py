

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


        
def setup():
    pass

def cleanup():
    pass


def case_01():
    test.assert_true(1==1, "1==1")


if __name__ == "__main__":
    

    test.set_setup(setup)
    test.add_test_case(case_01)
    test.set_cleanup(cleanup)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


