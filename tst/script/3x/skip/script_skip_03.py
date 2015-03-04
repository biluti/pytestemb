


import pytestemb





def condition():
    return True





class MyRun(pytestemb.Test):
    
    
    
    @pytestemb.skipif(condition, "exception")
    def case_0(self):
        pytestemb.fail("")

    @pytestemb.skipif(condition, "exception")
    def case_1(self):
        pytestemb.fail("")






if __name__ == "__main__":
    
    
    
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


