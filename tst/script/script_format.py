




import pytestemb as test





def case_msg_txt():
    test.assert_true(1==1, "1==1")

def case_msg_int():
    test.assert_true(1==1, 1)






if __name__ == "__main__":
    
    
    test.add_test_case(case_msg_txt)
    test.add_test_case(case_msg_int)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


