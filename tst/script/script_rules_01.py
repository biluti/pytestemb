


import pytestemb as test



def defaultValue():
    test.assert_equal(1, 1)
    test.assert_true(1==1, "1==1")



def start():
    pass

def stop():
    pass


if __name__ == "__main__":
    
    
    test.set_setup(start)
    test.set_setup(start)
    test.add_test_case(defaultValue)
    test.run_script()

    
    
    
    
    
    
    
    
    


