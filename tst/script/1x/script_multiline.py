# -*- coding: UTF-8 -*-



import pytestemb as test


vector = [  "предыстория",
            "الإنكليزية",
            "предыстория",
            "الإنكليزية",
            "ascii",
            "ascii",
            "\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629"
            "\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629"
            "\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            "\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9",
            "",
            "",

            ]


def multi_100():

    msg = "\n".join(["aaaaaa %d" % i for i in range(100)])
    
    test.trace_script(msg)
    test.trace_io("io", msg)
    test.trace_env("env", msg)
    test.trace_layer("layer", msg)



def multi_utf8():     
       
    msg = "\n".join("%s" % vector)
    test.trace_script(msg)
    test.trace_io("io", msg)
    test.trace_env("env", msg)
    test.trace_layer("layer", msg)        
        
        
def start():
    pass

def stop():
    pass





if __name__ == "__main__":
    
    test.add_trace(["txt"])
    test.set_setup(start)
    test.add_test_case(multi_100)
    test.add_test_case(multi_utf8)
    test.set_cleanup(stop)
    test.run_script()

    
    
    
    
    
    
    
    
    
    


