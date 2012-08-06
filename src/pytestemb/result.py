# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : result manages result of script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



import sys
import copy
import time
import inspect


import utils
import gtime


class TestErrorFatal(Exception):
    "Fatal Error"
    pass





class Result:

    def __init__(self, trace):
        self.trace = trace

        self.start_date = time.localtime()
        self.start_clock = time.clock()
        self.gtime = gtime.Gtime.create()
        self.delay_trace_ctrl = []

    def trace_result(self, name, des):
        self.trace.trace_result(name, des)

    def trace_warning(self, msg):
        self.trace.trace_warning(msg)

    def get_time(self):
        return self.gtime.get_time()

    def get_assert_caller(self):
        CALL_DEPTH = 4
        default = dict.fromkeys(["path","line","function","code"], "no info")
        traceback = inspect.stack()
        dic = {}
        stack = []
        try :
            dic["file"]         = copy.copy(traceback[CALL_DEPTH][1])
            dic["line"]         = copy.copy(traceback[CALL_DEPTH][2])
            dic["function"]     = copy.copy(traceback[CALL_DEPTH][3])
            dic["expression"]   = copy.copy(traceback[CALL_DEPTH][4][0].strip(" \t\n"))
            for index in range(CALL_DEPTH+1, len(traceback)):
                if          traceback[index][1].endswith("valid.py") \
                    and     traceback[index][3] == ("run_case"):
                    break
                stack.append(copy.copy(default))
                stack[-1]["path"]      = copy.copy(traceback[index][1])
                stack[-1]["line"]      = copy.copy(traceback[index][2])
                stack[-1]["function"]  = copy.copy(traceback[index][3])
                stack[-1]["code"]      = copy.copy(traceback[index][4][0].strip("\n"))           
            stack.reverse()
        finally:
            del traceback
            return dic, stack


    def _assert_(self, exp, fatal, des, values=""):
        if exp :
            self.assert_ok(des)
        else :
            # info = self.get_assert_caller()
            info, stack = self.get_assert_caller()
            
            des["stack"] = stack
            des["values"] = values
            des.update(info)
            self.assert_ko(des)
            if fatal :
                raise TestErrorFatal

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

    def error_config(self, des):
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

    def tag_value(self, des):
        pass    

    def doc(self, des):
        pass

    def trace_ctrl(self, des):
        # delay sending
        self.delay_trace_ctrl.append(des)


def trace(func):
    """ call trace_result
     decorator function """
    def decorated(*args, **kwargs):

        if func.func_name == "warning":
            trace_func = args[0].trace_warning
            trace_func(args[1])
        else:
            try:
                trace_func = args[0].trace_result
                trace_func(func.func_name, args[1])
            except Exception, ex:
                raise

        result = func(*args, **kwargs)
        return result
    return decorated


def stamp(func):
    """ add time stamp """
    def decorated(*args, **kwargs):
        # args[0] = self
        stamp = args[0].get_time()
        try:
            args[1]["time"] = stamp
        except Exception, ex:
            pass
        result = func(*args, **kwargs)
        return result
    return decorated



class ResultStdout(Result):
    SEPARATOR = "="
    SCRIPT_START = "SCRIPT_START"
    SCRIPT_STOP = "SCRIPT_STOP"
    SETUP_START = "SETUP_START"
    SETUP_STOP = "SETUP_STOP"
    CLEANUP_START = "CLEANUP_START"
    CLEANUP_STOP = "CLEANUP_STOP"
    CASE_START = "CASE_START"
    CASE_STOP = "CASE_STOP"
    CASE_NOTEXECUTED = "CASE_NOTEXECUTED"
    ERROR_CONFIG = "ERROR_CONFIG"
    ERROR_IO = "ERROR_IO"
    ERROR_TEST = "ERROR_TEST"
    WARNING = "WARNING"
    ASSERT_OK = "ASSERT_OK"
    ASSERT_KO = "ASSERT_KO"
    PY_EXCEPTION = "PY_EXCEPTION"
    TRACE = "TRACE"
    DOC = "DOC"
    TAGVALUE = "TAGVALUE"


    def __init__(self, trace):
        Result.__init__(self, trace)


    def write_no_arg(self, key):
        sys.stdout.write("%s%s\n" % (key, ResultStdout.SEPARATOR))

    def write_one_arg(self, key, value):
        sys.stdout.write("%s%s%s\n" % (key, ResultStdout.SEPARATOR ,value))


    def write(self, opcode, arg):
        arg = arg.__str__().encode("utf-8")
        sys.stdout.write("%s%s%s\n" % (opcode, ResultStdout.SEPARATOR, arg))


    @trace
    def script_start(self, des):
        self.write(ResultStdout.SCRIPT_START, des)
        for item in self.delay_trace_ctrl:
            self.write(ResultStdout.TRACE, item)

    @trace
    def script_stop(self, des):
        self.write(ResultStdout.SCRIPT_STOP, des)

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
    def error_config(self, des):
        self.write(ResultStdout.ERROR_CONFIG, des)

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

    @stamp
    @trace
    def assert_ko(self, des):
        self.write(ResultStdout.ASSERT_KO, des)

    @stamp
    @trace
    def py_exception(self, des):
        self.write(ResultStdout.PY_EXCEPTION, des)

    @trace
    def tag_value(self, des):
        self.write(ResultStdout.TAGVALUE, "%s=%s" % (des.keys()[0], des.values()[0]))

    @trace
    def doc(self, des):
        self.write(ResultStdout.DOC, des)

    def trace_ctrl(self, des):
        # delay sending
        self.delay_trace_ctrl.append(des)





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






class ResultStandalone(Result):

    def __init__(self, trace):
        Result.__init__(self, trace)

        self.case = None
        self.result = []

    @trace
    def script_start(self, des):
        sys.stdout.write("Start running %s ...\n" % des["name"])
        for item in self.delay_trace_ctrl:
            sys.stdout.write("Trace : %s\n" % item)

    def magical(self, data, size):
        return (len(data)-size)

    def add_line(self, col1, col2):
        col1 = col1.ljust(60)
        col2 = col2.ljust(32)
        sys.stdout.write("| %s| %s|\n"  % (col1, col2))

    @trace
    def script_stop(self, des):
        sys.stdout.write("End running %s\n" % des["name"])

        test_ok = True

        sys.stdout.write("\n+%s+\n" % ("-"*95))
        for case in self.result :
            if case["assert_ko"] == 0 :
                self.add_line("Case \"%s\"" % case["case"], "ok")
            else :
                self.add_line("Case \"%s\"" % case["case"], "ko")
                test_ok = False
        sys.stdout.write("+%s+\n" % ("-"*95))
        if test_ok :
            self.add_line("Script \"%s\"" % des["name"] , "OK")
        else:
            self.add_line("Script \"%s\"" % des["name"] , "KO")
        sys.stdout.write("+%s+\n" % ("-"*95))

    @trace
    def setup_start(self, des):
        pass

    @trace
    def setup_stop(self, des):
        pass

    @trace
    def cleanup_start(self, des):
        pass

    @trace
    def cleanup_stop(self, des):
        pass

    @stamp
    @trace
    def case_start(self, des):
        self.result.append({"case":des["name"]})
        self.result[-1]["assert_ok"] = 0
        self.result[-1]["assert_ko"] = 0
        sys.stdout.write("Case \"%s\" :\n" % des["name"])

    @stamp
    @trace
    def case_stop(self, des):
        pass

    @stamp
    @trace
    def case_not_executed(self, des):
        pass

    @stamp
    @trace
    def error_config(self, des):
        self.result[-1]["error_config"] += 1

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
        sys.stdout.write("Warning : %s\n" % des["msg"])

    @stamp
    @trace
    def assert_ok(self, des):
        self.result[-1]["assert_ok"] += 1

    @stamp
    @trace
    def assert_ko(self, des):
        
        
        if des.has_key("msg"):   
            msg = des["msg"]
        else:
            msg = ""     
        
        sys.stdout.write("Assert KO : '%s'\n" % msg)
        
        for s in des["stack"]:
            loc = "    File \"%s\", line %d, in %s\n" % (s["path"], s["line"], s["function"])
            loc += "        %s\n" % (s["code"])
            sys.stdout.write("%s" % loc)       
        sys.stdout.write("    File \"%s\", line %d, in %s\n" % (des["file"], des["line"], des["function"]))       
        sys.stdout.write("        + function   : \"%s\"\n" % des["function"])
        sys.stdout.write("        + expression : \"%s\"\n" % des["expression"])
        sys.stdout.write("        + values     : \"%s\"\n" % des["values"])

        self.result[-1]["assert_ko"] += 1
        

                       

    @stamp
    @trace
    def py_exception(self, des):
        dis = "Exception \n"
        for sline in des["stack"] :
            dis += "    File \"%s\", line %d, in %s\n" % (sline["path"], sline["line"], sline["function"])
            dis += "        %s\n" % (sline["code"])
        dis += "    %s\n" % (des["exception_class"])
        dis += "    %s\n" % (des["exception_info"])
        

        
        sys.stdout.write(dis.encode("utf-8"))

        try :
            self.result[-1]["assert_ko"] += 1
        except Exception, ex:
            pass




    @trace
    def tag_value(self, des):
        pass
        
    @trace
    def doc(self, des):
        import pydoc
        sys.stdout.write("\n")

        sys.stdout.write("Name : %s\n" % des[pydoc.KEY_NAME])
        sys.stdout.write("Type : %s\n" % des[pydoc.KEY_TYPE])
        sys.stdout.write("Doc :\n%s\n" % des[pydoc.KEY_DOC])



#    def trace_ctrl(self, des):
#        sys.stdout.write("Trace info : %s\n" % des.__str__())


def create(interface, mtrace):

    if   interface == "none" :
        return Result(mtrace)
    elif interface == "stdout" :
        return ResultStdout(mtrace)
    elif interface == "standalone" :
        return ResultStandalone(mtrace)
    else:
        assert False


