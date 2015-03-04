


import pytestemb




class MyRun(pytestemb.Test):
    
    
    @pytestemb.skip("skip case0")
    def setup(self):
        pass
     
    
    @pytestemb.skip("skip case0")
    def case_0(self):
        pytestemb.fail("")

#     def cleanup(self):
#         pass





if __name__ == "__main__":
    
    
    
    pytestemb.run()

    
    
    
    
    
    
    
    
    
    


