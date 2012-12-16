# -*- coding: UTF-8 -*-




import pytestemb as test





def test_load():
    for i in range(50000):
        test.assert_equal(1, 2, u"long data" * 64)
        test.assert_equal(1, 1, u"long data" * 64)
        test.trace_script( u"long data" * 64)
        test.tag_value("test","value")
        





if __name__ == "__main__":


    test.add_test_case(test_load)
    test.run_script()













