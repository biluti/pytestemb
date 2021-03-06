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


from collections import UserDict 


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
        compare[result.ResultStdout.SKIP] = []
         
        self.assertEqual(resultcounter.counter, compare)
    
    
    def test_case_01(self):

        reader = parser.ResultStdoutReader()
        
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
                
                
        #reader.add_line("%s%sscript_01\n" % (result.ResultStdout.SCRIPT_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))


        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR, {}))

        #reader.add_line("%s%sscript_01\n" % (result.ResultStdout.SCRIPT_STOP, result.ResultStdout.SEPARATOR, {}))
        
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
                
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))

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
        

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"case_03", "time":1.0}))
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SKIP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"msg":"skip", "time":1.0}))        
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.CASE_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"case_03", "time":2.0}))       
                   
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR, {}))

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
        compare[result.ResultStdout.SKIP] = []

         
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
        compare[result.ResultStdout.SKIP] = []     
        
        self.assertEqual(reader.script[0].case[0].counter, compare)
        self.assertEqual(reader.script[0].case[2].counter, compare)
        self.assertEqual(reader.script[0].case[3].counter, compare)
        
        compare[result.ResultStdout.SKIP] = [{'msg': 'skip', 'time': 1.0}] 
        self.assertEqual(reader.script[0].case[4].counter, compare)  
        
        
        self.assertEqual(reader.script[0].case[0].timeex, None)
        self.assertEqual("%.4f" % reader.script[0].case[2].timeex, "%.4f" %  0.0)
        self.assertEqual("%.4f" % reader.script[0].case[3].timeex, "%.4f" %  1.0)
        
        

    def test_case_03(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))

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
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))
        
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        
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
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR, {}))

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
        compare[result.ResultStdout.SKIP] = []   
         
        self.assertEqual(reader.script[0].case[0].counter, compare)
        self.assertEqual(reader.script[0].case[-1].counter, compare)
 
        
    def test_case_error_not_start(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        try :
            reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))
        except :
            return
        self.fail()
        
        
        
    def test_case_error_not_stop(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))

        try :
            reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        except :
            return
        self.fail()


    def test_case_04(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
                
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))


        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR, {}))

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
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))




        error_data = "{'info':'assert_ok_01'"
        s = "%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            error_data)
        

        
        self.assertRaises(parser.StdoutReaderError, reader.add_line, s)
                
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))



        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR, {}))

        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))

                
        

    def test_case_06(self):

        reader = parser.ResultStdoutReader()
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_START,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CREATE_START, result.ResultStdout.SEPARATOR, {}))
        
        
        exp= PY_EXCEPTION="""{'exception_info': u'', 'exception_class': 'Exception', 'stack': [{'function': 'destroy', 'path': '/home/jmb/workspace/pytestemb_git/tst/script/script_destroy_02.py', 'line': 37, 'code': '    raise Exception()'}], 'time': 0.21273398399353027}"""
        reader.add_line("%s%s%s\n" % (result.ResultStdout.PY_EXCEPTION, result.ResultStdout.SEPARATOR, exp))
        


        reader.add_line("%s%s%s\n" % (result.ResultStdout.CREATE_STOP, result.ResultStdout.SEPARATOR, {}))
        
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_START, result.ResultStdout.SEPARATOR, {}))


        error_data = "{'info':'assert_ok_01'"
        s = "%s%s%s\n" %    (   result.ResultStdout.ASSERT_OK,\
                                            result.ResultStdout.SEPARATOR,\
                                            error_data)
        

        
        self.assertRaises(parser.StdoutReaderError, reader.add_line, s)
                
        reader.add_line("%s%s%s\n" % (result.ResultStdout.SETUP_STOP, result.ResultStdout.SEPARATOR, {}))


        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.CLEANUP_STOP, result.ResultStdout.SEPARATOR, {}))

        reader.add_line("%s%s%s\n" % (result.ResultStdout.DESTROY_START, result.ResultStdout.SEPARATOR, {}))
        reader.add_line("%s%s%s\n" % (result.ResultStdout.DESTROY_STOP, result.ResultStdout.SEPARATOR, {}))
        
        reader.add_line("%s%s%s\n" %    (   result.ResultStdout.SCRIPT_STOP,\
                                            result.ResultStdout.SEPARATOR,\
                                            {"name":"script_01", "time":1}))


    def test_case_07(self):

        vector = """SCRIPT_START={'name': 'script_2trace', 'time': 0.24220800399780273}
        TRACE={u'type': u'octopylog'}
        TRACE={u'type': u'pyt', u'file': u'/tmp/pytestemb/script_2trace_0740B8B009ED6FD5.pyt'}
        CASE_START={'name': 'test_trace', 'time': 0.24247503280639648}
        TRACE={u'\\u043f\\u0440\\u0435\\u0434\\u044b\\u0441\\u0442\\u043e\\u0440\\u0438\\u044f': u'\\u043f\\u0440\\u0435\\u0434\\u044b\\u0441\\u0442\\u043e\\u0440\\u0438\\u044f'}
        TRACE={u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629': u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629'}
        TRACE={u'\\u043f\\u0440\\u0435\\u0434\\u044b\\u0441\\u0442\\u043e\\u0440\\u0438\\u044f': u'\\u043f\\u0440\\u0435\\u0434\\u044b\\u0441\\u0442\\u043e\\u0440\\u0438\\u044f'}
        TRACE={u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629': u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629'}
        TRACE={u'ascii': u'ascii'}
        TRACE={u'ascii': u'ascii'}
        TRACE={u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9': u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629\xd8\xa7\xd9\x84\xd8\xa5\xd9\x86\xd9\x83\xd9\x84\xd9\x8a\xd8\xb2\xd9\x8a\xd8\xa9'}
        TRACE={u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629': u'\\u0627\\u0644\\u0625\\u0646\\u0643\\u0644\\u064a\\u0632\\u064a\\u0629'}
        TRACE={u'': u''}
        TRACE={u'': u''}
        TRACE={u'\\xc3': u'\\xc3'}
        TRACE={u'\xc3': u'\xc3'}
        TRACE={u"'353530392d31354133093065450100ea/fs/1/84o3q@ms4hoW`Xn0PaNDo5Hc8n@`FF4noAu4nnRd4`al54haon', u'ParentId': u'353530392d31354133093065450100ea/fs/1/88A@nIAo2Gh4`o@o8n@`RDa44cl8`@`nFooiutn`e', u'Type': u'Item', u'URI': u'http://192.168.4.1:57135/PulsarServerPlugin/i/MzUzNTMwMzkyZDMxMzU0MTMzMDkzMDY1NDUwMTAwZWEvZnMvMS84NG8zcUBtczRob1dgWG4wUGFORG81SGM4bkBgRkY0bm9BdTRublJkNGBhbDU0aGFvbg%3D%3D.mp3', [^] u'Title': u'01 - Assassin'": u"'353530392d31354133093065450100ea/fs/1/84o3q@ms4hoW`Xn0PaNDo5Hc8n@`FF4noAu4nnRd4`al54haon', u'ParentId': u'353530392d31354133093065450100ea/fs/1/88A@nIAo2Gh4`o@o8n@`RDa44cl8`@`nFooiutn`e', u'Type': u'Item', u'URI': u'http://192.168.4.1:57135/PulsarServerPlugin/i/MzUzNTMwMzkyZDMxMzU0MTMzMDkzMDY1NDUwMTAwZWEvZnMvMS84NG8zcUBtczRob1dgWG4wUGFORG81SGM4bkBgRkY0bm9BdTRublJkNGBhbDU0aGFvbg%3D%3D.mp3', [^] u'Title': u'01 - Assassin'"}
        CASE_STOP={'name': 'test_trace', 'time': 0.2430438995361328}
        SCRIPT_STOP={'name': 'script_2trace', 'time': 0.24316787719726562}"""

        reader = parser.ResultStdoutReader()
        for l in vector.splitlines():
            reader.add_line(l)
    


        
                
                
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
        #self.assertEqual(stub.buffer, "%s%s%s\n" % (result.ResultStdout.SCRIPT_START, result.ResultStdout.SEPARATOR, {}))
        res.script_start({"info":"test"})
        #self.assertEqual(stub.buffer, "%s%stest\n" % (result.ResultStdout.SCRIPT_START, result.ResultStdout.SEPARATOR, {}))

        # script_stop
        res.script_stop({"name":""})
        #self.assertEqual(stub.buffer, "%s%s%s\n" % (result.ResultStdout.SCRIPT_STOP, result.ResultStdout.SEPARATOR, {}))
        res.script_stop({"info":"test", "name":""})
        #self.assertEqual(stub.buffer, "%s%stest\n" % (result.ResultStdout.SCRIPT_STOP, result.ResultStdout.SEPARATOR, {}))
        
        # case_start
        res.case_start({"name":""})
        #self.assertEqual(stub.buffer, "%s%s%s\n" % (result.ResultStdout.CASE_START, result.ResultStdout.SEPARATOR, {}))
        res.case_start({"info":"test", "name":""})
        #self.assertEqual(stub.buffer, "%s%scase\n" % (result.ResultStdout.CASE_START, result.ResultStdout.SEPARATOR, {}))

        # case_stop
        res.case_stop({})
        #self.assertEqual(stub.buffer, "%s%s%s\n" % (result.ResultStdout.CASE_STOP, result.ResultStdout.SEPARATOR, {}))
        res.case_stop({"info":"test"})
        #self.assertEqual(stub.buffer, "%s%stest\n" % (result.ResultStdout.CASE_STOP, result.ResultStdout.SEPARATOR, {}))        

        
        
if __name__ == '__main__':
    unittest.main()







