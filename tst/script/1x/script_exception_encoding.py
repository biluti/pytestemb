# -*- coding: UTF-8 -*-






import pytestemb as test


def test_exception1():
    raise Exception(u"abcééé".encode("latin_1"))

def test_exception2():
    raise Exception("\xC3")

def test_exception3():
    s = u""
    s += "\xC3"


if __name__ == "__main__":
    
    
    test.add_trace(["txt"])
    test.add_test_case(test_exception1)
    test.add_test_case(test_exception2)
    test.add_test_case(test_exception3)
    test.run()

    

    


