

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
    print((test.get_uedi()))




        
        
def start():
    print((test.get_uedi()))

def stop():
    print((test.get_uedi()))





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(t4)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


