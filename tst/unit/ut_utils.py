# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : unit test for result utils
"""

__author__      = "$Author: jmbeguinet $"
__version__     = "$Revision: 1.1 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import unittest

import pytestemb.utils as utils




    

class Test_get_script_name(unittest.TestCase):
    def setUp(self):
        pass
    
    
    
    def test_case(self):
        name = utils.get_script_name()
        self.assertEqual(name, "ut_utils")


        
        
        





        
                        
if __name__ == '__main__':
    unittest.main()







