# -*- coding: UTF-8 -*-




import pytestemb as test


vector = [      u"abcééé".encode("latin_1"),
                u"abcééé".encode("cp1250"),
                u"abcééé".encode("iso8859"),
                u"abcééé".encode("utf_32"),
            ]



def test_assert():
    for itm in vector:
        test.assert_true(True,  itm)
        test.assert_true(False, itm)




def test_trace():
    for itm in vector:
        test.trace_script(          itm)
        test.trace_env("env",       itm)
        test.trace_io("io",         itm)
        test.trace_layer("layer",   itm)


def test_assert_equal():
    for val1 in vector:
        for val2 in vector:
            test.assert_equal(val1, val2, "equal")




    


if __name__ == "__main__":


    test.add_test_case(test_assert)
    test.add_test_case(test_trace)
    test.add_test_case(test_assert_equal)
    test.run_script()













