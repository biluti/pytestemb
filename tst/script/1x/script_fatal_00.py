

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
    test.assert_true(True)
    test.fail_fatal("")
    test.assert_true(True)

def case_02():
    test.assert_true(True)

def case_03():
    test.assert_true(True)




if __name__ == "__main__":
    


    test.set_fatal_mode(True)
    test.set_setup(setup)
    test.add_test_case(case_01)
    test.add_test_case(case_02)
    test.add_test_case(case_03)
    test.set_cleanup(cleanup)
    test.run()

    
    
    
    
    
    
    
    
    
    


