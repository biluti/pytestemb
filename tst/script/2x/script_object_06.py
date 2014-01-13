


import pytestemb




class MyRun0(pytestemb.Test):
    
    
    a = 0
    _A = 1
    __A__ = 2
    
    def setup(self):
        pass
    
    def __private_0(self):
        pass

    def _private_1(self):
        pass

    @staticmethod
    def case_staticmethod():
        pass

    def case_0(self):
        pytestemb.success("")

    def case_1(self):
        pytestemb.success("")

    def case_2(self):
        pytestemb.success("")

    def cleanup(self):
        pass





if __name__ == "__main__":
    
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


