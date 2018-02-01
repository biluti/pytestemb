# -*- coding: UTF-8 -*-




import pytestemb as test



import mock



def test_exception():
    raise Exception("test")

        

if __name__ == "__main__":
    
    
    test.add_trace(["txt", "logstash", "octopylog"])

    test.add_test_case(test_exception)
        
    test.run()


