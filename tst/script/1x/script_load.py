# -*- coding: UTF-8 -*-




import pytestemb as test


import time


def test_load():
    for i in range(500000):
        test.assert_equal(1, 2, u"long data" * 64)
        test.assert_equal(1, 1, u"long data" * 64)
        time.sleep(0.00)
        test.trace_script( u"long data" * 2)
        test.tag_value("test","value")
        





if __name__ == "__main__":


    test.add_test_case(test_load)
    test.run()













