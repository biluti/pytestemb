


import pytestemb as test
import pytestemb.result as result



class MyRun(test.Test):        
    def setup(self):
        pass
    
    def func_case(self):
        
        try:
            test.fail_fatal("")
        except result.TestErrorFatal:
            print 'z'*3
            test.success("")
            
    def cleanup(self):
        pass





if __name__ == "__main__":
    

    test.set_fatal_mode(True)
    test.run()

    
    
    
    
    
    
    
    
    
    


