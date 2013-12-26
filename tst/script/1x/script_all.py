

"""
@goal: -
@todo: -
@warning: -
@requires: -
@precondition: -
@postcondition: -
"""


import pytestemb as test




def case_assert_true():
    """
    @goal : -
    @coverage : -
    """
    test.assert_true(1==1)
    test.assert_true(1==2)
    test.assert_true(1==1, "1==1")
    test.assert_true(1==2, "1==2")
    
    test.assert_true_fatal(1==1)
    test.assert_true_fatal(1==1, "1==1")
    test.assert_true_fatal(1==2, "1==2")
    
def case_assert_false():
    """
    @goal : -
    @coverage : -
    """
    test.assert_false(1==2)
    test.assert_false(1==1)
    test.assert_false(1==2, "1==2")
    test.assert_false(1==1, "1==1")
    
    test.assert_false_fatal(1==2)
    test.assert_false_fatal(1==2, "1==2")
    test.assert_false_fatal(1==1, "1==1")
    



def case_assert_equal():
    """
    @goal : -
    @coverage : -
    """
    test.assert_equal(1,1)
    test.assert_equal(1,2)
    test.assert_equal(1,1, "1==1")
    test.assert_equal(1,2, "1==2")
    
    test.assert_equal_fatal(1,1)
    test.assert_equal_fatal(1,1, "1==1")
    test.assert_equal_fatal(1,2, "1==2")




def case_assert_notequal():
    """
    @goal : -
    @coverage : -
    """
    test.assert_notequal(1,2)
    test.assert_notequal(1,1)
    test.assert_notequal(1,2, "1==2")
    test.assert_notequal(1,1, "1==1")
    
    test.assert_notequal_fatal(1,2)
    test.assert_notequal_fatal(1,2, "1==2")
    test.assert_notequal_fatal(1,1, "1==1")
    
    

def warning_01():
    """
    @goal : -
    @coverage : -
    """    
    test.warning("")

def warning_02():
    """
    @goal : -
    @coverage : -
    """    
    test.warning("")
    test.assert_true(True, "")

def warning_03():
    """
    @goal : -
    @coverage : -
    """    
    test.warning("")
    test.assert_true(False, "")



def fail_01():
    test.fail()
    test.fail_fatal()
    
def fail_02():
    test.fail("fail")
    test.fail_fatal("fail_fatal")


def tagvalue():
    test.tag_value("tag", "value")




if __name__ == "__main__":
    
    test.set_doc(__doc__)
    test.add_test_case(case_assert_true)
    test.add_test_case(case_assert_false)
    test.add_test_case(case_assert_equal)
    test.add_test_case(case_assert_notequal)
    
    test.add_test_case(warning_01)
    test.add_test_case(warning_02)
    test.add_test_case(warning_03)
    test.add_test_case(fail_01)
    test.add_test_case(fail_02)
    
    test.add_test_case(tagvalue)
    
    
    test.run_script()

    
    
    
    
    
    
    
    
    
    



