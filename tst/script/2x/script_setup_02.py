


import pytestemb as test


        
def func_setup():
    test.fail("")

def func_case():
    test.success("")
        
def func_cleanup():
    pass





if __name__ == "__main__":
    

    test.set_setup(func_setup)
    test.add_test_case(func_case)
    test.set_cleanup(func_cleanup)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


