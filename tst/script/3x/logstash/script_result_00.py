# -*- coding: UTF-8 -*-




import pytestemb




import mock



class MyRun(pytestemb.Test):
    
   
    def setup(self):
        pass
    

    def test_ok(self):
        pytestemb.success()
    
        
    def test_ko(self):
        pytestemb.fail()
    
    def test_except(self):
        raise ValueError("")

    @pytestemb.skip("skip")
    def test_skip(self):
        raise Exception("")



if __name__ == "__main__":
    
    
        
    pytestemb.run()













