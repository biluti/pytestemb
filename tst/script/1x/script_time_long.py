

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



def t4():
    """
    @goal : -
    @coverage : -
    """    
    time.sleep(10)


def t5():
    """
    @goal : -
    @coverage : -
    """
    time.sleep(70)



        
        
def start():
    time.sleep(0.1)

def stop():
    time.sleep(0.1)





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(t4)
    test.add_test_case(t5)
    test.set_cleanup(stop)
    test.run()

    
    
    
    
    
    
    
    
    
    


