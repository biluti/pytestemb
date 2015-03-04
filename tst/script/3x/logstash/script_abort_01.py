# -*- coding: UTF-8 -*-




import pytestemb as test



import mock



def test_abort():
    test.abort("")

        

if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

    test.add_test_case(test_abort)
        
    test.run_script()


