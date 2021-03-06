# -*- coding: UTF-8 -*-

""" 
PyTestEmb Project : parser manages parsing of stdout result
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"





import pytestemb.result as result


from collections import UserDict

class StdoutReaderError(Exception):
    pass

    


class StdoutReader(object):
    
    def __init__(self):
        self.script_started = False 
        self.case_started = False
        
    def new_script(self):
        self.script_started = False 
        self.case_started = False
    
    
    @staticmethod
    def check_started(state):
        if state :
            return
        else :
            raise StdoutReaderError("Not started")   
        
    
    def add_line(self, line):
        
        line = line.strip("\r\n")
        if line == "":
            return
        
        pos = line.find(result.ResultStdout.SEPARATOR)
        if pos == line[-1] :
            self.process(line, None)
        else :
            try:
                self.process(line[0:pos], line[pos+1:])
            except StdoutReaderError as ex:
                raise StdoutReaderError(ex.__str__() + ",line : %s" % line)

    @staticmethod
    def conv_dict(data):
        try:
            return UserDict(eval(data))
        except SyntaxError as ex:
            raise StdoutReaderError("Problem during parsing : exception '%s', data '%s'" % (ex.__str__(), data))   
    
    def process(self, key, value):
        pass



class ResultStdoutReader(StdoutReader):
    
    def __init__(self):
        StdoutReader.__init__(self)
        self.script = []

    def __str__(self):
        dis = ""
        for scr in self.script:
            dis += "%s\n" % scr.__str__()
        return dis
    
    @staticmethod
    def create_resultcounter():
        obj = result.ResultCounter()
        obj.add_kind(result.ResultStdout.ERROR_IO)
        obj.add_kind(result.ResultStdout.ERROR_TEST)
        obj.add_kind(result.ResultStdout.WARNING)
        obj.add_kind(result.ResultStdout.ASSERT_OK)
        obj.add_kind(result.ResultStdout.ASSERT_KO)
        obj.add_kind(result.ResultStdout.PY_EXCEPTION)
        obj.add_kind(result.ResultStdout.ABORT)
        obj.add_kind(result.ResultStdout.ABORTED)            
        obj.add_kind(result.ResultStdout.TAGVALUE)
        obj.add_kind(result.ResultStdout.SKIP)
        return obj
    
    
    
    def process(self, key, value):
        # SCRIPT_START
        if      key == result.ResultStdout.SCRIPT_START :
            dic = self.conv_dict(value)
            self.check_started(not(self.script_started))
            self.script.append(result.ResultScript(dic["name"]))
            self.script[-1].time_exec = dic["time"]
            self.script_started = True
        # SCRIPT_STOP
        elif    key == result.ResultStdout.SCRIPT_STOP :
            dic = self.conv_dict(value)
            self.check_started(self.script_started)
            self.script_started = False
            self.script[-1].time_exec = dic["time"] - self.script[-1].time_exec 
        # SETUP_START, CLEANUP_START, CASE_START
        elif        key == result.ResultStdout.SETUP_START or  key == result.ResultStdout.CLEANUP_START\
                or  key == result.ResultStdout.CREATE_START or  key == result.ResultStdout.DESTROY_START or  key == result.ResultStdout.CASE_START :
            self.check_started(not(self.case_started))
            timeex = None
            if      key == result.ResultStdout.SETUP_START :
                value = "setup"
            elif    key == result.ResultStdout.CLEANUP_START:   
                value = "cleanup"
            elif    key == result.ResultStdout.CREATE_START:    
                value = "create"
            elif    key == result.ResultStdout.DESTROY_START:   
                value = "destroy"                          
            else :
                dic = self.conv_dict(value)
                value = dic["name"]
                timeex = dic["time"]
                
            obj = self.create_resultcounter()
            obj.name = value
            obj.timeex = timeex
            self.script[-1].case.append(obj)
            self.case_started = True
        # SETUP_STOP, CLEANUP_STOP, CASE_STOP
        elif        key == result.ResultStdout.SETUP_STOP or  key == result.ResultStdout.CLEANUP_STOP\
                or  key == result.ResultStdout.CREATE_STOP or  key == result.ResultStdout.DESTROY_STOP or  key == result.ResultStdout.CASE_STOP :
            self.check_started(self.case_started)
            self.case_started = False
            
            if key == result.ResultStdout.CASE_STOP:
                dic = self.conv_dict(value)
                self.script[-1].case[-1].timeex = dic["time"] - self.script[-1].case[-1].timeex    
 
        # CASE_NOTEXECUTED
        elif    key == result.ResultStdout.CASE_NOTEXECUTED :
            self.check_started(not(self.case_started))
            obj = self.create_resultcounter()
            obj.set_not_executed()
            obj.name = value
            self.script[-1].case.append(obj)
        # TRACE
        elif    key == result.ResultStdout.TRACE :
            self.check_started(self.script_started)
            self.script[-1].trace.append(self.conv_dict(value))
        # CASE_XX
        elif        key == result.ResultStdout.ERROR_IO or  key == result.ResultStdout.ERROR_TEST\
                or  key == result.ResultStdout.WARNING or  key == result.ResultStdout.ASSERT_OK or  key == result.ResultStdout.ASSERT_KO\
                or  key == result.ResultStdout.PY_EXCEPTION or  key == result.ResultStdout.ABORT or  key == result.ResultStdout.ABORTED:
            self.check_started(self.case_started)
            self.script[-1].case[-1].add_result(key, self.conv_dict(value))
        # TAGVALUE
        elif        key == result.ResultStdout.TAGVALUE:
            self.check_started(self.script_started)
            tv = value.partition("=")
            self.script[-1].case[-1].add_result(key, {tv[0]:tv[2]})       
        # SKIP
        elif        key == result.ResultStdout.SKIP:
            self.check_started(self.script_started)
            self.script[-1].case[-1].add_result(key, self.conv_dict(value))                                   
        else :
            pass


class DocStdoutReader(StdoutReader):
    
    def __init__(self):
        StdoutReader.__init__(self)
        self.data = []
        
    def __str__(self):
        return ""
    
    def process(self, key, value):
        # DOC
        if  key == result.ResultStdout.DOC :
            self.data.append(self.conv_dict(value))
        else:
            pass
            #print "key=%s value=%s" % (key, value)
            
            
            