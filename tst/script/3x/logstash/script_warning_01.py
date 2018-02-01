# -*- coding: UTF-8 -*-




import pytestemb as test



import mock



def test_warning():
    test.warning("warm")

        

if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

    test.add_test_case(test_warning)
        
    test.run()


