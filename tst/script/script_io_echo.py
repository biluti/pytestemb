




import pytestemb as test


import interface_echo as echo




def setup():
    echo.create()
    
    


def check_io():
    
    for i in range(0,32):
        test.trace_script("Loop %d" % i)
        echo.send("AABB%d" % i)
        rx = echo.receive()
        test.assert_true(rx=="AABB%d" % i)






if __name__ == "__main__":
    
    test.set_setup(setup)
    test.add_test_case(check_io)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


