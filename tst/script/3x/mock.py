# -*- coding: UTF-8 -*-



import os
import pytestemb as test





def mock_jenkins():
    
    os.environ["BUILD_TAG"]         = "NA"
    os.environ["NODE_NAME"]         = "nodetest"
    os.environ["BUILD_URL"]         = "NA"
    os.environ["JOB_NAME"]          = "jenkins-testjob"
    os.environ["PACKAGE_VERSION"]   = test.VERSION_STRING
    


def mock_trace():
    test.add_trace(["txt", "logstash", "octopylog"])
    

def mock():
    mock_jenkins()
    mock_trace()
    


mock()





