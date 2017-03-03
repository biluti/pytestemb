


import pytestemb as test




class MyRun(test.Test):        
    def setup(self):
        print((test.is_assert()))
    
    def func_case_0(self):
        test.success("")
        print((test.is_assert()))
        test.fail("")
        print((test.is_assert()))
        test.success("")
        print((test.is_assert()))
        
        
    def cleanup(self):
        print((test.is_assert()))






if __name__ == "__main__":
    


    test.run()

    
    
    
    
    
    
    
    
    
    


