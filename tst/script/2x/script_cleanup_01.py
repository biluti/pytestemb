


import pytestemb as test





class MyRun(test.Test):        
    def setup(self):
        pass
    
    def func_case(self):
        test.success("")
            
    def cleanup(self):
        raise Exception("")





if __name__ == "__main__":
    

    test.run()

    
    
    
    
    
    
    
    
    
    


