




import pytestemb as test





def defaultValue():
    test.assert_true_fatal(1==2, "1==2")
    test.assert_true(1==1, "1==1")

def boundValue():
    test.trace_script("No wait")
    test.assert_true(1==1, "1==1")
    test.assert_true(1==2, "1==2")
    test.assert_true(1==1, "1==1")
    test.trace_script("Easy trace")
    pass






if __name__ == "__main__":
    
    
    test.add_test_case(defaultValue)
    test.add_test_case(boundValue)
    test.run()

    
    
    
    
    
    
    
    
    
    


