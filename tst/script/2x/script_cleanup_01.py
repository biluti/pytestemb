


import pytestemb as test


        
def func_setup():
    pass

def func_case():
    test.success("")
        
def func_cleanup():
    raise Exception("")





if __name__ == "__main__":
    

    test.set_setup(func_setup)
    test.add_test_case(func_case)
    test.set_cleanup(func_cleanup)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


