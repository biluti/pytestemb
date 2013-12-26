


import pytestemb as test




class MyRun(test.Test):        
    def setup(self):
        test.fail("")
    
    def func_case(self):
        test.success("")
            
    def cleanup(self):
        pass





if __name__ == "__main__":
    


    test.run()

    
    
    
    
    
    
    
    
    
    


