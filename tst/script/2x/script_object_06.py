


import pytestemb




class MyRun(pytestemb.Test):
    
    
    a = 0
    
        
    def setup(self):
        pass
        
    def case_0(self):
        pytestemb.success("")

    def case_1(self):
        pytestemb.success("")

    def case_2(self):
        pytestemb.success("")

    @staticmethod
    def case_3():
        pytestemb.success("")



    def cleanup(self):
        pass



if __name__ == "__main__":
    
    pytestemb.run()

    
    

    
    


