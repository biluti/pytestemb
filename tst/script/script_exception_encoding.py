# -*- coding: UTF-8 -*-






import pytestemb as test


def test_exception():
    raise Exception(u"abcééé".encode("latin_1"))


if __name__ == "__main__":
    
    
    test.add_test_case(test_exception)
    test.run_script()

    

    


