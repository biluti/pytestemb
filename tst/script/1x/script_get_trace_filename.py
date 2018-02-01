

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
    
    uedi = test.get_uedi()
    
    
    
    test.assert_equal(test.get_trace_filename(), None)
    
    test.add_trace(["txt"])
    
    filename = test.get_trace_filename()
    
    
    test.assert_true(filename.endswith("%s.pyt" % uedi))


        
        
def start():
    pass

def stop():
    pass





if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.add_test_case(t4)
    test.set_cleanup(stop)
    test.run()

    
    
    
    
    
    
    
    
    
    


