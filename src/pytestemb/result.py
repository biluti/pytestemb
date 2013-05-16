# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : result manages result of script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



import sys
import time
import inspect


import pytestemb.utils as utils
import pytestemb.gtime as gtime


class TestErrorFatal(Exception):
    pass

class TestAbort(Exception):
    pass



class Result:
    
    __single = None
    
    CASE_NOTEXECUTED    = "CASE_NOTEXECUTED"
    ERROR_IO            = "ERROR_IO"
    ERROR_TEST          = "ERROR_TEST"
    WARNING             = "WARNING"
    ASSERT_OK           = "ASSERT_OK"
    ASSERT_KO           = "ASSERT_KO"
    PY_EXCEPTION        = "PY_EXCEPTION"
    ABORT               = "ABORT"
    ABORTED             = "ABORTED"
    TRACE               = "TRACE"
    DOC                 = "DOC"
    TAGVALUE            = "TAGVALUE"

    def __init__(self, inst_trace):
        self.trace = inst_trace
        self.start_date = time.localtime()
        self.start_clock = time.clock()
        self.gtime = gtime.Gtime.create()
        self.delay_trace_ctrl = []
        
        # report
        self.case = False
        self.result = []
        self.time_exec = None
        
        
        self._report_callback = None
        
        


    @classmethod
    def create(cls, interface, mtrace):
    
        if   interface == "none" :
            res = Result(mtrace)
        elif interface == "stdout" :
            res = ResultStdout(mtrace)
        elif interface == "standalone" :
            res = ResultStandalone(mtrace)
        else:
            assert False
        cls.__single = res
        
        
    @classmethod
    def get(cls):
        return cls.__single 
        
    def trace_trace(self, des):
        pass          

    def trace_result(self, name, des):
        self.trace.trace_result(name, des)

    def trace_warning(self, msg):
        self.trace.trace_warning(msg)

    def get_time(self):
        return self.gtime.get_time()


    @staticmethod
    def get_assert_caller(call_depth):

        DEFAULT = dict.fromkeys(["path", "line", "function", "code"], "no info")
        traceback = inspect.stack()
        dic = {}
        stack = []

        dic["file"]         = traceback[call_depth][1]
        dic["line"]         = traceback[call_depth][2]
        dic["function"]     = traceback[call_depth][3]
        dic["expression"]   = traceback[call_depth][4][0].strip(" \t\n")
        
        try:
            for index in range(call_depth+1, len(traceback)):
                if          traceback[index][1].endswith("valid.py") \
                    and     (traceback[index][3] == "run_case" or traceback[index][3] == "run_try") :
                    break
                stack.append(dict(DEFAULT))
                stack[-1]["path"]      = traceback[index][1]
                stack[-1]["line"]      = traceback[index][2]
                stack[-1]["function"]  = traceback[index][3]
                stack[-1]["code"]      = traceback[index][4][0].strip("\n")
        except Exception:
            pass 
            
        stack.reverse()

        return dic, stack



    def _assert_(self, exp, fatal, des, values=""):
        if exp :
            self.assert_ok(des)
        else :
            info, stack = self.get_assert_caller(4)
            des["stack"]    = stack
            des["values"]   = values
            des.update(info)
            self.assert_ko(des)
            if fatal :
                raise TestErrorFatal

    def abort_test(self, des):
        info, stack = self.get_assert_caller(3)
        des["stack"] = stack
        des.update(info)
        self.abort(des)
        raise TestAbort
        

    def success(self, des):
        self.assert_ok(des)
    
    def fail(self, des):
        self._assert_(False, False, des)

    def fail_fatal(self, des):
        self._assert_(False, True, des)

    def assert_true(self, exp, des):
        values = "%s" % exp
        self._assert_(exp, False, des, values)

    def assert_false(self, exp, des):
        values = "%s" % exp
        self._assert_(not(exp), False, des, values)

    def assert_true_fatal(self, exp, des):
        values = "%s" % exp
        self._assert_(exp, True, des, values)

    def assert_false_fatal(self, exp, des):
        values = "%s" % exp
        self._assert_(not(exp), True, des, values)

    def assert_equal(self, exp1, exp2, des):
        values = "%s != %s" % (utils.to_unicode(exp1), utils.to_unicode(exp2))
        self._assert_((exp1 == exp2), False, des, values)

    def assert_equal_fatal(self, exp1, exp2, des):
        values = "%s != %s" % (utils.to_unicode(exp1), utils.to_unicode(exp2))
        self._assert_((exp1 == exp2), True, des, values)

    def assert_notequal(self, exp1, exp2, des):
        values = "%s == %s" % (utils.to_unicode(exp1), utils.to_unicode(exp2))
        self._assert_((exp1 != exp2), False, des, values)

    def assert_notequal_fatal(self, exp1, exp2, des):
        values = "%s == %s" % (utils.to_unicode(exp1), utils.to_unicode(exp2))
        self._assert_((exp1 != exp2), True, des, values)

    def create_start(self, des):
        pass
        
    def create_stop(self, des):
        pass

    def destroy_start(self, des):
        pass
        
    def destroy_stop(self, des):
        pass
        
    def script_start(self, des):
        pass

    def script_stop(self, des):
        pass

    def setup_start(self, des):
        pass

    def setup_stop(self, des):
        pass

    def cleanup_start(self, des):
        pass

    def cleanup_stop(self, des):
        pass

    def case_start(self, des):
        pass

    def case_stop(self, des):
        pass

    def case_not_executed(self, des):
        pass

    def error_io(self, des):
        pass

    def error_test(self, des):
        pass

    def warning(self, des):
        pass

    def assert_ok(self, des):
        pass

    def assert_ko(self, des):
        pass

    def py_exception(self, des):
        pass
    
    def abort(self, des):
        pass

    def aborted(self, des):
        pass
    
    def tag_value(self, des):
        pass    

    def doc(self, des):
        pass

    def trace_ctrl(self, des):
        # delay sending
        self.delay_trace_ctrl.append(des)
            



    def report_script_start(self, des):
        self.time_exec = des["time"]
        

    def report_add_callback(self, callback):
        self._report_callback = callback

    def report_trace(self, info):
        if self._report_callback is not None:
            self._report_callback(info)
        self.trace.trace_report(info)
        
        
    def report_add_line(self, col1, col2):
        col1 = col1.ljust(60)
        col2 = col2.ljust(32)
        self.report_trace("| %s| %s|\n"  % (col1, col2))


    def report_script_stop(self, des):
        
        SIZE = 95
    
        self.time_exec = des["time"] - self.time_exec     
        
        # | aborted |   ok    |   ko    | result
        # +---------+---------+---------+--------
        # |    0    |   0     |   0     |   ?  
        # |    0    |   0     |   1     |   ko
        # |    0    |   1     |   0     |   ok
        # |    0    |   1     |   1     |   ko       
        # |    1    |   0     |   0     |   aborted
        # |    1    |   0     |   1     |   aborted
        # |    1    |   1     |   0     |   aborted
        # |    1    |   1     |   1     |   aborted
        #
        # result_aborted = aborted
        # result_unknown = not(aborted or ok or ko)
        # result_ok = ok and not(aborted) and not(ko)
        # result_ko = ko and not(aborted)
        ok      = False
        ko      = False
        aborted = False
        
        self.report_trace("\n+%s+\n" % ("-"*SIZE))
        self.report_add_line("Script time execution" , "%.3f (sec)" % self.time_exec)
        
        self.report_trace("+%s+\n" % ("-"*SIZE))   
        for case in self.result :
            
            if case[self.ABORTED] > 0 or aborted:
                self.report_add_line("Case \"%s\"" % case["case"], "aborted")
                aborted = True
            elif    case[self.PY_EXCEPTION] != None :    
                self.report_add_line("Case \"%s\"" % case["case"], case[self.PY_EXCEPTION])
                ko = True
            elif    case[self.ASSERT_KO] == 0 \
                and case[self.ASSERT_OK] > 0:
                self.report_add_line("Case \"%s\"" % case["case"], "ok")
                ok = True
            elif    case[self.ASSERT_KO] == 0 \
                and case[self.ASSERT_OK] == 0:
                self.report_add_line("Case \"%s\"" % case["case"], "??")       
            else:
                self.report_add_line("Case \"%s\"" % case["case"], "ko")
                ko = True
    
        self.report_trace("+%s+\n" % ("-"*SIZE))    
        if aborted :
            self.report_add_line("Script \"%s\"" % des["name"] , "ABORTED")    
        elif not(aborted or ok or ko):
            self.report_add_line("Script \"%s\"" % des["name"] , "??")
        elif ok and not(aborted) and not(ko) :
            self.report_add_line("Script \"%s\"" % des["name"] , "OK")
        elif ko and not(aborted):
            self.report_add_line("Script \"%s\"" % des["name"] , "KO")
        else:
            raise Exception("assert")
        
        self.report_trace("+%s+\n" % ("-"*SIZE))


    def report_case_start(self, des):
        self.result.append({"case":des["name"]})
        self.result[-1][self.ASSERT_OK] = 0
        self.result[-1][self.ASSERT_KO] = 0
        self.result[-1][self.PY_EXCEPTION] = None
        self.result[-1][self.ABORTED]   = 0        
        self.case = True

    def report_case_stop(self):
        self.case = False

    def report_assert_ok(self):
        self.result[-1][self.ASSERT_OK] += 1

    def report_assert_ko(self):
        if self.case :
            self.result[-1][self.ASSERT_KO] += 1
            
    def report_py_exception(self, des):
        if self.case:
            self.result[-1][self.PY_EXCEPTION] = des["exception_class"]
          
    def report_abort(self):
        if self.case:
            self.result[-1][self.ABORTED] += 1
        
    def report_aborted(self):
        if self.case:
            self.result[-1][self.ABORTED] += 1
        


















def trace(func):
    """ call trace_result
     decorator function """
    def decorated(*args, **kwargs):
        trace_func = args[0].trace_result
        trace_func(func.func_name, args[1])
        return func(*args, **kwargs)
    return decorated


def stamp(func):
    """ add time stamp """
    def decorated(*args, **kwargs):
        args[1]["time"] = args[0].get_time()
        result = func(*args, **kwargs)
        return result
    return decorated



class ResultStdout(Result):
    SEPARATOR = "="
    
    
    CREATE_START        = "CREATE_START"
    CREATE_STOP         = "CREATE_STOP"
    
    DESTROY_START       = "DESTROY_START"
    DESTROY_STOP        = "DESTROY_STOP"  
      
    SCRIPT_START        = "SCRIPT_START"
    SCRIPT_STOP         = "SCRIPT_STOP"
    
    SETUP_START         = "SETUP_START"
    SETUP_STOP          = "SETUP_STOP"
    
    CLEANUP_START       = "CLEANUP_START"
    CLEANUP_STOP        = "CLEANUP_STOP"
    
    CASE_START          = "CASE_START"
    CASE_STOP           = "CASE_STOP"
    



    def __init__(self, inst_trace):
        Result.__init__(self, inst_trace)

    @staticmethod
    def write_no_arg( key):
        sys.stdout.write("%s%s\n" % (key, ResultStdout.SEPARATOR))

    @staticmethod
    def write_one_arg( key, value):
        sys.stdout.write("%s%s%s\n" % (key, ResultStdout.SEPARATOR, value))

    @staticmethod
    def write(opcode, arg):
        arg = arg.__str__().encode("utf-8")
        sys.stdout.write("%s%s%s\n" % (opcode, ResultStdout.SEPARATOR, arg))

    @stamp
    @trace
    def script_start(self, des):
        self.write(ResultStdout.SCRIPT_START, des)
        for item in self.delay_trace_ctrl:
            #self.write(ResultStdout.TRACE, item)
            self.trace_trace(item)
        self.report_script_start(des)
        

    def trace_trace(self, des):
        self.write(ResultStdout.TRACE, des)

    @trace
    def create_start(self, des):
        self.write(ResultStdout.CREATE_START, des)

         
    @trace
    def create_stop(self, des):
        self.write(ResultStdout.CREATE_STOP, des)

    @trace
    def destroy_start(self, des):
        self.write(ResultStdout.DESTROY_START, des)

          
    @trace
    def destroy_stop(self, des):
        self.write(ResultStdout.DESTROY_STOP, des)
                
    @stamp     
    @trace
    def script_stop(self, des):
        self.write(ResultStdout.SCRIPT_STOP, des)
        self.report_script_stop(des)

    @trace
    def setup_start(self, des):
        self.write(ResultStdout.SETUP_START, des)

    @trace
    def setup_stop(self, des):
        self.write(ResultStdout.SETUP_STOP, des)

    @trace
    def cleanup_start(self, des):
        self.write(ResultStdout.CLEANUP_START, des)

    @trace
    def cleanup_stop(self, des):
        self.write(ResultStdout.CLEANUP_STOP, des)

    @stamp
    @trace
    def case_start(self, des):
        self.write(ResultStdout.CASE_START, des)
        self.report_case_start(des)

    @stamp
    @trace
    def case_stop(self, des):
        self.write(ResultStdout.CASE_STOP, des)

    @stamp
    @trace
    def case_not_executed(self, des):
        self.write(ResultStdout.CASE_NOTEXECUTED, des)


    @stamp
    @trace
    def error_io(self, des):
        self.write(ResultStdout.ERROR_IO, des)

    @stamp
    @trace
    def error_test(self, des):
        self.write(ResultStdout.ERROR_TEST, des)

    @stamp
    @trace
    def warning(self, des):
        self.write(ResultStdout.WARNING, des)

    @stamp
    @trace
    def assert_ok(self, des):
        self.write(ResultStdout.ASSERT_OK, des)
        self.report_assert_ok()

    @stamp
    @trace
    def assert_ko(self, des):
        self.write(ResultStdout.ASSERT_KO, des)
        self.report_assert_ko()

    @stamp
    @trace
    def py_exception(self, des):
        self.write(ResultStdout.PY_EXCEPTION, des)
        self.report_py_exception(des)

    @stamp
    @trace        
    def abort(self, des):
        self.write(ResultStdout.ABORT, des)        
        self.report_abort()

    @stamp
    @trace        
    def aborted(self, des):
        self.write(ResultStdout.ABORTED, des)
        self.report_aborted()    
    
    @trace
    def tag_value(self, des):
        self.write(ResultStdout.TAGVALUE, "%s=%s" % (des.keys()[0], des.values()[0]))

    @trace
    def doc(self, des):
        self.write(ResultStdout.DOC, des)

    def trace_ctrl(self, des):
        # delay sending
        self.delay_trace_ctrl.append(des)












class ResultStandalone(Result):
    

    def __init__(self, inst_trace):
        Result.__init__(self, inst_trace)
        
        self.report_add_callback(ResultStandalone.write_stdout)

    @staticmethod
    def write_stdout(info):
        sys.stdout.write(info)

    @stamp
    @trace
    def script_start(self, des):
        
        self.report_script_start(des)
        
        dis = ""
        dis += "Start running '%s' ...\n" % des["name"]
        for item in self.delay_trace_ctrl:
            dis += "Trace : %s\n" % item
        dis += "\n"
        
        self.write_stdout(dis)

       
    @stamp
    @trace
    def script_stop(self, des):
        self.report_script_stop(des)

    @trace
    def create_start(self, des):
        self.write_stdout("Create  : \n")
        
    @trace
    def create_stop(self, des):
        pass

    @trace
    def destroy_start(self, des):
        self.write_stdout("Destroy :\n")
        
    @trace
    def destroy_stop(self, des):
        pass

    @trace
    def setup_start(self, des):
        self.write_stdout("Setup   :\n")

    @trace
    def setup_stop(self, des):
        pass

    @trace
    def cleanup_start(self, des):
        self.write_stdout("Cleanup :\n")

    @trace
    def cleanup_stop(self, des):
        pass

    @stamp
    @trace
    def case_start(self, des):
        self.report_case_start(des)
        self.write_stdout("Case    : '%s'\n" % des["name"])
        
    @stamp
    @trace
    def case_stop(self, des):
        self.case = False

    @stamp
    @trace
    def case_not_executed(self, des):
        pass


    @stamp
    @trace
    def error_io(self, des):
        pass

    @stamp
    @trace
    def error_test(self, des):
        pass

    @stamp
    @trace
    def warning(self, des):
        self.write_stdout("Warning : %s\n" % des["msg"])
        

    @stamp
    @trace
    def assert_ok(self, des):
        self.result[-1][self.ASSERT_OK] += 1

    @stamp
    @trace
    def assert_ko(self, des):
        
        self.report_assert_ko()
        
        if des.has_key("msg"):   
            msg = des["msg"]
        else:
            msg = ""     
        
        dis = ""
        dis += "Assert KO : '%s'\n" % msg
        for i in des["stack"]:
            dis += "    File \"%s\", line %d, in %s\n" % (i["path"], i["line"], i["function"])
            dis += "        %s\n" % (i["code"])

        dis += "    File \"%s\", line %d, in %s\n" % (des["file"], des["line"], des["function"])
        dis += "        + function   : \"%s\"\n" % des["function"]
        dis += "        + expression : \"%s\"\n" % des["expression"]
        dis += "        + values     : \"%s\"\n" % des["values"]
        
        self.write_stdout(dis)
        
      
    @stamp
    @trace
    def py_exception(self, des):
        
        self.report_py_exception(des)
        
        dis = "Exception \n"
        for sline in des["stack"] :
            dis += "    File \"%s\", line %d, in %s\n" % (sline["path"], sline["line"], sline["function"])
            dis += "        %s\n" % (sline["code"])
        dis += "    %s\n" % (des["exception_class"])
        dis += "    %s\n" % (des["exception_info"])
    
        self.write_stdout(dis)
        
        

    @stamp
    @trace        
    def abort(self, des):
        
        self.report_abort()
        
        if des.has_key("msg"):   
            msg = des["msg"]
        else:
            msg = ""     
            
        dis = ""
        dis += "Abort : '%s'\n" % msg
        
        for i in des["stack"]:
            loc = "    File \"%s\", line %d, in %s\n" % (i["path"], i["line"], i["function"])
            loc += "        %s\n" % (i["code"])
            dis += loc
            
        dis += "    File \"%s\", line %d, in %s\n" % (des["file"], des["line"], des["function"])       
        dis += "        + function   : \"%s\"\n" % des["function"]
        dis += "        + expression : \"%s\"\n" % des["expression"]

        self.write_stdout(dis)


    @trace
    def aborted(self, des):
        self.report_aborted()
        self.write_stdout("  Aborted\n")
        

    @trace
    def tag_value(self, des):
        pass
        
    @trace
    def doc(self, des):
        import pytestemb.pydoc as pydoc
        
        self.write_stdout("\n")

        self.write_stdout("Name : %s\n" % des[pydoc.KEY_NAME])
        self.write_stdout("Type : %s\n" % des[pydoc.KEY_TYPE])
        self.write_stdout("Doc :\n%s\n" % des[pydoc.KEY_DOC])




class ResultCounter:
    """ class to count result
    a limit is implemented (usefull for test instanciate for endurance )
    counter works as cyclic after limit is reach
    """
    def __init__(self, name="", limit=1000):
        self.name = name
        self.limit = limit
        self.timeex = None
        self.counter = {}

    def set_not_executed(self):
        self.counter = None

    def add_kind(self, kind):
        self.counter[kind] = []

    def add_result(self, kind, obj):
        """ add a result if limit is reach, the older result is remove """
        self.counter[kind].append(obj)
        if len(self.counter[kind]) > self.limit :
            self.counter[kind].pop(0)
            
    def get_counter(self):
        return self.counter

    def __str__(self):
        sstr = "%s\n" % self.name
        for k, v in self.counter.iteritems():
            sstr += "%s:%s\n" % (k, v)
        return sstr



class ResultScript:
    def __init__(self, name):
        self.name = name
        self.time_exec = None
        self.case = []
        self.trace = []
        self.tagvalue = []

    def __str__(self):
        sstr = "%s\n" % self.name
        for cas in self.case:
            sstr += "%s\n" % cas.__str__()

        for item in self.trace:
            sstr += "TRACE:%s" % item

        return sstr





