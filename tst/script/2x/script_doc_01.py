


import pytestemb as test




class MyRun(test.Test):   
    """ @Type Cross
        Other """
    
    def setup(self):
        test.fail("")
    
    def func_case(self):
        """ description of fun case"""
        test.success("")
            
    def cleanup(self):
        pass





if __name__ == "__main__":
    


    test.run()

    
    
    
    
    
    
    
    
    
    


