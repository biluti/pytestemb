


import pytestemb






class MyRun(pytestemb.Test):
    
   
    def setup(self):
        pass
    
    @pytestemb.skip
    def case_0(self):
        pytestemb.fail("")



    def cleanup(self):
        pass





if __name__ == "__main__":
    
    
    
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


