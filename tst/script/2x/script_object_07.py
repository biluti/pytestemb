


import pytestemb




class MyRun0(pytestemb.Test):
    
    


    def case_0(self):
        pytestemb.success("")

    def case_1(self):
        pytestemb.abort("test abort")

    def case_2(self):
        pytestemb.success("")

    def cleanup(self):
        pass





if __name__ == "__main__":
    
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


