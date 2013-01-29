# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : unit test for result module
"""

__author__      = "$Author: jmbeguinet $"
__version__     = "$Revision: 1.5 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



import sys
import unittest

import pytestemb.trace as trace
import pytestemb.result as result
import pytestemb.parser as parser



def create_des(info):
    dic = {}
    dic["info"] = info
    return dic.__str__()
    

        

class Test_ResultReader(unittest.TestCase):
    def setUp(self):
        pass
    
    
    
    def test_case_ResultCounter(self):
        reader = parser.ResultStdoutReader()
        resultcounter = reader.create_resultcounter()
    
        compare = {}
        compare[result.ResultStdout.ERROR_IO] = []
        compare[result.ResultStdout.ERROR_TEST] = []
        compare[result.ResultStdout.WARNING] = []
        compare[result.ResultStdout.ASSERT_OK] = []
        compare[result.ResultStdout.ASSERT_KO] = []
        compare[result.ResultStdout.PY_EXCEPTION] = [] 
        compare[result.ResultStdout.TAGVALUE] = []
        compare[result.ResultStdout.ABORT] = []
        compare[result.ResultStdout.ABORTED] = []
         
        self.assertEqual(resultcounter.counter, compare)
    
    
    def test_case_01(self):

        reader = parser.ResultStdoutReader()
        
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
                
                
        #reader.add_line("%s%sscript_01\n" % (result.ResultStdout.SCRIPT_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))


        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR))

        #reader.add_line("%s%sscript_01\n" % (result.ResultStdout.SCRIPT_STOP, result.ResultStdout.SEPARATOR))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":3}))
                
        self.assertEqual(len(reader.script), 1)
        self.assertEqual(reader.script[0].name, "script_01")
        self.assertEqual(len(reader.script[0].case), 2)
        self.assertEqual(reader.script[0].case[0].name, "setup")
        self.assertEqual(reader.script[0].case[1].name, "cleanup")
        self.assertEqual(reader.script[0].time_exec, 2)

        
        
        
    
    def test_case_02(self):

        reader = parser.ResultStdoutReader()
        
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
                
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"case_01", "time":0.37946581840515137}))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ok_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_KO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ko_01")))    
        

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.TAGVALUE,\
                                            result.ResultStdout.SEPARATOR,\
                                            "TAG=VALUE"))        
     

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ok_02")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_KO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ko_02")))   
               
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.WARNING,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("warning_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.WARNING,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("warning_02")))        



        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ERROR_IO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("error_io_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ERROR_TEST,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("error_test_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"case_01", "time":1.4654846447474}))
 
 
 
         
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"tagvalue", "time":0.0}))
        
   
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"tagvalue", "time":0.0})) 
                       
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"case_02", "time":1.0}))
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"case_02", "time":2.0}))        
        
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":4}))


        compare = {}
        
        compare[result.ResultStdout.ERROR_IO] = [{"info":"error_io_01"}]
        compare[result.ResultStdout.ERROR_TEST] = [{"info":"error_test_01"}]
        compare[result.ResultStdout.WARNING] = [{"info":"warning_01"}, {"info":"warning_02"}]
        compare[result.ResultStdout.ASSERT_OK] = [{"info":"assert_ok_01"}, {"info":"assert_ok_02"}]
        compare[result.ResultStdout.ASSERT_KO] = [{"info":"assert_ko_01"}, {"info":"assert_ko_02"}]
        compare[result.ResultStdout.PY_EXCEPTION] = []
        compare[result.ResultStdout.ABORT] = []
        compare[result.ResultStdout.ABORTED] = []
        compare[result.ResultStdout.TAGVALUE] = [{"TAG":"VALUE"}]

         
        self.assertEqual(reader.script[0].case[1].counter, compare)
        
        
        self.assertEqual("%.4f" % reader.script[0].case[1].timeex, "%.4f" %  1.086019)

        
        compare = {}
        compare[result.ResultStdout.ERROR_IO] = []
        compare[result.ResultStdout.ERROR_TEST] = []
        compare[result.ResultStdout.WARNING] = []
        compare[result.ResultStdout.ASSERT_OK] = []
        compare[result.ResultStdout.ASSERT_KO] = []
        compare[result.ResultStdout.PY_EXCEPTION] = []
        compare[result.ResultStdout.TAGVALUE] = []
        compare[result.ResultStdout.ABORT] = []
        compare[result.ResultStdout.ABORTED] = []        
        
        self.assertEqual(reader.script[0].case[0].counter, compare)
        self.assertEqual(reader.script[0].case[2].counter, compare)
        self.assertEqual(reader.script[0].case[3].counter, compare) 
        
        
        self.assertEqual(reader.script[0].case[0].timeex, None)
        self.assertEqual("%.4f" % reader.script[0].case[2].timeex, "%.4f" %  0.0)
        self.assertEqual("%.4f" % reader.script[0].case[3].timeex, "%.4f" %  1.0)
        
        

    def test_case_03(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ok_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_KO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ko_01")))   
               
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.WARNING,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("warning_01")))


        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ERROR_IO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("error_io_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ERROR_TEST,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("error_test_01")))     
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.PY_EXCEPTION,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("py_exception_01")))             
        
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))
        
        
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ok_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ASSERT_KO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("assert_ko_01")))   
               
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.WARNING,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("warning_01")))


        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ERROR_IO,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("error_io_01")))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.ERROR_TEST,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("error_test_01")))           

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.PY_EXCEPTION,\
                                            result.ResultStdout.SEPARATOR,\
                                            create_des("py_exception_01")))           
        
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))


        compare = {}

        compare[result.ResultStdout.ERROR_IO] = [{"info":"error_io_01"}]
        compare[result.ResultStdout.ERROR_TEST] = [{"info":"error_test_01"}]
        compare[result.ResultStdout.WARNING] = [{"info":"warning_01"}]
        compare[result.ResultStdout.ASSERT_OK] = [{"info":"assert_ok_01"}]
        compare[result.ResultStdout.ASSERT_KO] = [{"info":"assert_ko_01"}]
        compare[result.ResultStdout.PY_EXCEPTION] = [{"info":"py_exception_01"}] 
        compare[result.ResultStdout.TAGVALUE] = []
        compare[result.ResultStdout.ABORT] = []
        compare[result.ResultStdout.ABORTED] = []        
         
        self.assertEqual(reader.script[0].case[0].counter, compare)
        self.assertEqual(reader.script[0].case[-1].counter, compare)
 
        
    def test_case_error_not_start(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        try :
            reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))
        except :
            return
        self.fail()
        
        
        
    def test_case_error_not_stop(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))

        try :
            reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        except :
            return
        self.fail()


    def test_case_04(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
                
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))


        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        self.assertEqual(len(reader.script), 1)
        self.assertEqual(reader.script[0].name, "script_01")
        self.assertEqual(len(reader.script[0].case), 2)
        self.assertEqual(reader.script[0].case[0].name, "setup")
        self.assertEqual(reader.script[0].case[1].name, "cleanup")


    def test_case_05(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))




        error_data = "{'info':'assert_ok_01'"
        s = "%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            error_data)
        

        
        self.assertRaises(parser.StdoutReaderError, reader.add_line, s)
                
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))



        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))

                
        

    def test_case_06(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        reader.add_line("%s%s{}\n" % (result.ResultStdout.CREATE_START, result.ResultStdout.SEPARATOR))
        
        
        exp= PY_EXCEPTION="""{'exception_info': u'', 'exception_class': 'Exception', 'stack': [{'function': 'destroy', 'path': '/home/jmb/workspace/pytestemb_git/tst/script/script_destroy_02.py', 'line': 37, 'code': '    raise Exception()'}], 'time': 0.21273398399353027}"""
        reader.add_line("%s%s%s\n" % (result.ResultStdout.PY_EXCEPTION, result.ResultStdout.SEPARATOR, exp))
        


        reader.add_line("%s%s{}\n" % (result.ResultStdout.CREATE_STOP, result.ResultStdout.SEPARATOR))
        
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR))


        error_data = "{'info':'assert_ok_01'"
        s = "%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            error_data)
        

        
        self.assertRaises(parser.StdoutReaderError, reader.add_line, s)
                
        reader.add_line("%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR))


        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR))

        reader.add_line("%s%s{}\n" % (result.ResultStdout.DESTROY_START, result.ResultStdout.SEPARATOR))
        reader.add_line("%s%s{}\n" % (result.ResultStdout.DESTROY_STOP, result.ResultStdout.SEPARATOR))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))


 
        
        
        
                
# stub stdout
class stub_stdout:
    def  __init__(self):
        self.buffer = None 
    def write(self, data):
        self.buffer = data

stub = stub_stdout()
sys.stdout = stub


class Test_ResultStdout(unittest.TestCase):
    
    def test_case_01(self):
        res = result.ResultStdout(trace.Trace())
        
        # script_start
        res.script_start({})
        #self.assertEqual(stub.buffer, "%s%s\n" % (result.ResultStdout.SCRIPT_START, result.ResultStdout.SEPARATOR))
        res.script_start({"info":"test"})
        #self.assertEqual(stub.buffer, "%s%stest\n" % (result.ResultStdout.SCRIPT_START, result.ResultStdout.SEPARATOR))

        # script_stop
        res.script_stop({"name":""})
        #self.assertEqual(stub.buffer, "%s%s\n" % (result.ResultStdout.SCRIPT_STOP, result.ResultStdout.SEPARATOR))
        res.script_stop({"info":"test", "name":""})
        #self.assertEqual(stub.buffer, "%s%stest\n" % (result.ResultStdout.SCRIPT_STOP, result.ResultStdout.SEPARATOR))
        
        # case_start
        res.case_start({"name":""})
        #self.assertEqual(stub.buffer, "%s%s\n" % (result.ResultStdout.CASE_START, result.ResultStdout.SEPARATOR))
        res.case_start({"info":"test", "name":""})
        #self.assertEqual(stub.buffer, "%s%scase\n" % (result.ResultStdout.CASE_START, result.ResultStdout.SEPARATOR))

        # case_stop
        res.case_stop({})
        #self.assertEqual(stub.buffer, "%s%s\n" % (result.ResultStdout.CASE_STOP, result.ResultStdout.SEPARATOR))
        res.case_stop({"info":"test"})
        #self.assertEqual(stub.buffer, "%s%stest\n" % (result.ResultStdout.CASE_STOP, result.ResultStdout.SEPARATOR))        

        
        
if __name__ == '__main__':
    unittest.main()







