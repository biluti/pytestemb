



import sys



import pytestemb as test





def test_path():
    for line in sys.path :
        print line

#    test.assert_true_fatal(1==2, "1==2")
#    test.assert_true(1==1, "1==1")









if __name__ == "__main__":
    
    
    test.add_test_case(test_path)
    test.run()

    
    
    
    
    
    
    
    
    
    


