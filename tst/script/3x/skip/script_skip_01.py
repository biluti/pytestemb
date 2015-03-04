


import pytestemb






class MyRun(pytestemb.Test):
    
   
    def setup(self):
        pass
    
    
    @pytestemb.skip("skip case0")
    def case_0(self):
        pytestemb.fail("")

    @pytestemb.skipif(False, "skip case1")
    def case_1(self):
        pytestemb.fail("")

    @pytestemb.skipif(True, "skip case2")
    def case_2(self):
        pytestemb.fail("")

    def cleanup(self):
        pass





if __name__ == "__main__":
    
    
    
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


