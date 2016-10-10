# -*- coding: UTF-8 -*-


import pytestemb




import mock



class MyRun(pytestemb.Test):
    
   
    def setup(self):
        pass
    

    def test_ver_y(self):
        import os
        os.environ["PACKAGE_VERSION"]   = "y.y.y"
        os.environ["HARDWARE_VERSION"]  = "y.y.y"
        pytestemb.trace_json({"ver":"y"})
    
    def test_ver_x(self):
        import os
        os.environ["PACKAGE_VERSION"]   = "x.x.x"
        os.environ["HARDWARE_VERSION"]  = "x.x.x"
        pytestemb.trace_json({"ver":"x"})
        
    def test_ver_z(self):
        import os
        
        os.environ["SIMULATOR"]   = "true"
        os.environ["NIGHTLY"]  = "true"
        
        pytestemb.trace_json({"ver":"x"})
        

if __name__ == "__main__":
    
    
        
    pytestemb.run()













