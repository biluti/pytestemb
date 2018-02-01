




import pytestemb as test


def deep_02():
    0/0

def deep_01():
    deep_02()



def deep_00():
    deep_01()

    

if __name__ == "__main__":
    
    
    test.add_test_case(deep_00)
    test.run()

    

    


