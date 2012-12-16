




import pytestemb as test


class MyError(Exception):
    pass

def ex_01():
    raise IndexError()


def ex_02():
    raise KeyError()

def ex_03():
    raise MyError("test")    

if __name__ == "__main__":
    
    
    test.add_test_case(ex_01)
    test.add_test_case(ex_02)
    test.add_test_case(ex_03)
    test.run_script()

    

    


