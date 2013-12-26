

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


def a():
    test.assert_equal(test.get_case_name(), "a")

def b():
    test.assert_equal(test.get_case_name(), "b")

def c():
    test.assert_equal(test.get_script_name(), "script_get_name")


def start():
    if test.get_case_name() == "setup":
        pass
    else:
        raise Exception("")

def stop():
    if test.get_case_name() == "cleanup":
        pass
    else:
        raise Exception("")





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(a)
    test.add_test_case(b)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


