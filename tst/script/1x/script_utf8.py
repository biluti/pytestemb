# -*- coding: UTF-8 -*-




import pytestemb as test

vector = [  "предыстория",
            "الإنكليزية",
            "предыстория",
            "الإنكليزية",
            "ascii",
            "ascii",
            "\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629"
            "\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629"
            "\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            "\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            "",
            "",
            "\xC3",
            "\xC3",
            ]



def test_assert():
    for itm in vector:
        test.assert_true(True,  itm)
        test.assert_true(False, itm)


def test_assert_equal():
    for val1 in vector:
        for val2 in vector:
            test.assert_equal(val1, val2, "equal")



def test_trace():
    # msg
    for itm in vector:
        test.trace_script(          itm)
        test.trace_env("env",       itm)
        test.trace_io("io",         itm)
        test.trace_layer("layer",   itm)
    # scope
    for itm in vector:
        test.trace_env(itm, "env")
        test.trace_io(itm, "io")
        test.trace_layer(itm, "layer")



if __name__ == "__main__":

    test.add_trace(["txt"])
    test.add_test_case(test_assert)
    test.add_test_case(test_trace)
    test.add_test_case(test_assert_equal)

    test.run_script()













