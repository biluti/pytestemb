
"""
@goal           :: Template of script structure :
                    - define pydoc structure 
                    - define case definition
@status         :: [WORKING, RELEASED, DEPRECATED]
@environment    :: [device_01, device_02, ...]
@precondition   :: [device_01] is in state ...
                   [device_02] is in state ...
@postcondition  :: System under test is in state ...
@version        :: 1.1
@author         :: jmbeguinet
@date           :: 2009-02-17 17:13:33
"""


import pytestemb as test





def case_01():
    """
    @goal        :: Perform some basic request :
                     - bound value
                     - error value
    @coverage    :: <id551516>
                    <id551544>
                    <id559118>
    @warning     :: 
    """
    test.assert_true(1==1, "1==1")



def case_02():
    """
    @goal        :: Perform some basic request :
                     - bound value
                     - error value
    @coverage    :: 
    @warning     :: 
    """
    test.assert_true(1==1, "1==1")
    test.assert_true(1==1, "1==1")







if __name__ == "__main__":
    
    
    test.add_test_case(case_01)
    test.add_test_case(case_02)
    test.run_script()

    
    
    import cProfile 
    cProfile.run('test.run_script()')
    
    
    
    
    
    
    
    


