

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




def level_1():
    level_2()

def level_2():
    level_3()

def level_3():
    test.assert_true(1==2, "1==1")

   
        
def start():
    pass

def stop():
    pass





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(level_3)
    test.add_test_case(level_2)
    test.add_test_case(level_1)
    test.set_cleanup(stop)
    test.run()

    
    
    
    
    
    
    
    
    
    


