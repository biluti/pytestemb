




import pytestemb as test





def defaultValue():
    test.assert_true(1==1, "1==1")

def boundValue():
    test.assert_true(1==1, "1==1")
    test.assert_true(1==1, "1==1")







if __name__ == "__main__":
    
    
    test.add_test_case(defaultValue)
    test.add_test_case(boundValue)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


