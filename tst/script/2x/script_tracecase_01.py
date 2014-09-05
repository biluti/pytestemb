


import pytestemb




class MyRun(pytestemb.Test):
        
    def setup(self):
        pass
        
    def case_0(self):
        pytestemb.success("")

    def case_1(self):
        pytestemb.success("")

    def case_2(self):
        pytestemb.success("")

    def cleanup(self):
        pass


def tracecase(name):
    pass



if __name__ == "__main__":
    
    pytestemb.set_tracecase(tracecase)
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


