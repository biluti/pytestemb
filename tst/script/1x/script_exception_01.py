




import pytestemb as test


def gen():
    0/0



def case_01():
    gen()

def case_02():
    test.assert_true(True, "")
    gen()
    
    

if __name__ == "__main__":
    
    
    test.add_test_case(case_01)
    test.add_test_case(case_02)
    test.run()

    

    


