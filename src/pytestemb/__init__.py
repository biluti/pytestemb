# -*- coding: UTF-8 -*-



__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



VERSION_STRING = "4.0.0"




import sys
import types
import platform



import pytestemb.trace as trace
import pytestemb.valid as valid
import pytestemb.result as result
import pytestemb.pexception as pexeception
import pytestemb.utils as utils



import argparse
from pytestemb.valid import Test
from pytestemb.valid import skip
from pytestemb.valid import skipif


INTERFACE = {}


INTERFACE_DEFAULT = 0
INTERFACE_LIST = 1


INTERFACE["result"] = (("standalone"),
                       ("none", "standalone", "stdout"))
INTERFACE["trace"] =  ([],
                       ("none", "octopylog", "txt", "logstash", "logtxt"))



def checker(parser, name, value):
    for line in INTERFACE[name][INTERFACE_LIST] :
        if line == value:
            break
    else :
        parser.error("Interface %s is not valid, see --help" % value)


def parse():
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-r", "--result", action="store", type=str,  default="standalone",  help="set the interface for result")
    parser.add_argument("-t", "--trace",
                        action="append", type=str, dest="trace", default=[],
                        help="set the interface for trace")
    parser.add_argument("-p", "--path",
                        action="store", type=str, dest="path", default=None,
                        help="add path to Python path")
    parser.add_argument("-c", "--config",
                        action="store", type=str, dest="config", default=None,
                        help="add config general purpose string (flag, filename ...)")
    parser.add_argument("-m", "--mode",
                        action="store", type=str, dest="mode", default=None,
                        help="add mode general purpose string (debug, ...)")
    
    parser.add_argument("--json",
                        action="store", type=str, default=None,
                        help="json report")
    parser.add_argument("--junit",
                        action="store", type=str, default=None,
                        help="junit report")
    
    parser.add_argument("-v", "--version", action="version", version=VERSION_STRING,  help="version of software")    
    
    
    args = parser.parse_args()

    

    return args



# detect if pytestemb in lib_mode
if sys.argv[1:].count("--pytestemb_lib_mode") == 1:
    pass
else:
    ARGS = parse()
    if ARGS.path is not None:
        sys.path.append(ARGS.path)

    trace.TraceManager.create(ARGS.trace)
    result.Result.create(ARGS.result, trace.TraceManager.get(), ARGS.json, ARGS.junit)
    valid.Valid.create(result.Result.get())
    
    trace.TraceManager.get().set_result(result.Result.get())
    trace.TraceManager.get().start()
    
    # Configuration management
    SCOPE_CF = "CF"
    trace.TraceManager.get().trace_env(SCOPE_CF, "Library version : pytestemb %s" % VERSION_STRING)
    trace.TraceManager.get().trace_env(SCOPE_CF, "Python-version : %s" % platform.python_version())
    trace.TraceManager.get().trace_env(SCOPE_CF, "Plateform : %s" % platform.platform(terse=True))
    trace.TraceManager.get().trace_env(SCOPE_CF, "Default encoding : %s" % sys.getdefaultencoding())
    trace.TraceManager.get().trace_env(SCOPE_CF, "Report json : %s" % ARGS.json)
    trace.TraceManager.get().trace_env(SCOPE_CF, "Report junit : %s" % ARGS.junit)




def add_trace(interfaces):
    trace.TraceManager.get().add_traces(interfaces)
    trace.TraceManager.get().set_result(result.Result.get())
    trace.TraceManager.get().start()


def set_setup(func_setup):
    """
    @function           : set_setup(func_setup)
    @param func_setup   : (function) a test case function
    @return             : None
    @summary            : add a setup function to the script
    """

    valid.Valid.get().set_setup(func_setup)

def set_cleanup(func_cleanup):
    """
    @function           : set_cleanup(func_cleanup)
    @param func_cleanup : (function) a test case function
    @return             : None
    @summary            : add a cleanup function to the script
    """

    valid.Valid.get().set_cleanup(func_cleanup)




def set_create(func_create):
    """
    @function           : set_create(func_create)
    @param func_create  : (function) a create function
    @return             : None
    @summary            : add a create function to the script
    """

    valid.Valid.get().set_create(func_create)
        

def set_destroy(func_destroy):
    """
    @function           : set_destroy(func_destroy)
    @param func_destroy : (function) a destroy function
    @return             : None
    @summary            : add a destroy function to the script
    """

    valid.Valid.get().set_destroy(func_destroy)



def set_tracecase(func_tracecase):
    """
    @function           : set_tracecase(func_tracecase)
    @param func_destroy : (function) a trace function with two string parameter (script_name, case_name)
    @return             : None
    @summary            : add a tracecase name function to the script
    """
    valid.Valid.get().set_tracecase(func_tracecase)



def set_fatal_mode(stop_case_run=False):
    """
    @function           : set_fatal_mode(stop_case_run)
    @param func_destroy : (boolean) a destroy function
    @return             : None
    @summary            : set mode for behavior when fatal : True abort all cases 
    """
    valid.Valid.get().set_fatal_mode(stop_case_run)
        
        


def add_test_case(func_case):
    """
    @function       : add_test_case(func_case)
    @param func_case: (function) a test case function
    @return         : None
    @summary        : add a test case to the script
    """
    valid.Valid.get().add_test_case(func_case)


def run():
    """
    @function       : run_script()
    @return         : None
    @summary        : start the run of script
    @warning        : -
    """
    
    valid.Valid.get().scan()
    valid.Valid.get().run_script()
    trace.TraceManager.get().stop()



def _create_des_(msg):
    if msg is None :
        return {}
    else:
        return dict({u"msg":utils.to_unicode(msg)})


def get_config():
    return ARGS.config


def get_mode():
    return ARGS.mode


def get_path():
    return ARGS.path


def get_script_name():
    return utils.get_script_name()


def get_trace_filename():
    
    return trace.TraceManager.get().get_trace_file()


def get_case_name():

    return valid.Valid.get().get_case_name()


def get_uedi():
    return trace.TraceManager.get().get_ueid()


def trace_trace(dic_des):
    """ reserved 
        @param des : dictionary
    """    
    result.Result.get().trace_trace(dic_des)



def assert_true(exp, msg=None):
    """
    @function       : assert_true(exp, msg=None)
    @param exp      : (boolean) expression that we expect "True" value
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert a "True" value
    """
    result.Result.get().assert_true(exp, _create_des_(msg))


def assert_false(exp, msg=None):
    """
    @function       : assert_false(exp, msg=None)
    @param exp      : (boolean) expression that we expect "False" value
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert a "False" value
    """
    result.Result.get().assert_false(exp, _create_des_(msg))


def assert_true_fatal(exp, msg=None):
    """
    @function       : assert_true_fatal(exp, msg=None)
    @param exp      : (boolean) expression that we expect "True" value
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert a "True" value, if assertion is False execution of test case is finished
    """
    result.Result.get().assert_true_fatal(exp, _create_des_(msg))


def assert_false_fatal(exp, msg=None):
    """
    @function       : assert_false_fatal(exp, msg=None)
    @param exp      : (boolean) expression that we expect "False" value
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert a "False" value, if assertion is False execution of test case is finished
    """
    result.Result.get().assert_false_fatal(exp, _create_des_(msg))


def assert_equal(exp1, exp2, msg=None):
    """
    @function       : assert_equal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert that exp1 is equal to exp2
    """
    result.Result.get().assert_equal(exp1, exp2, _create_des_(msg))


def assert_equal_fatal(exp1, exp2, msg=None):
    """
    @function       : assert_equal_fatal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert that exp1 is equal to exp2, if assertion is False execution of test case is finished
    """
    result.Result.get().assert_equal_fatal(exp1, exp2, _create_des_(msg))



def assert_notequal(exp1, exp2, msg=None):
    """
    @function       : assert_notequal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert that exp1 is not equal to exp2
    """
    result.Result.get().assert_notequal(exp1, exp2, _create_des_(msg))




def assert_notequal_fatal(exp1, exp2, msg=None):
    """
    @function       : assert_notequal(exp1, exp2, msg=None)
    @param exp1     : (object) expression1
    @param exp2     : (object) expression2
    @param msg      : (string) message string describing the goal of assertion
    @return         : None
    @summary        : assert that exp1 is not equal to exp2, if assertion is False execution of test case is finished
    """
    result.Result.get().assert_notequal_fatal(exp1, exp2, _create_des_(msg))



def warning(msg=None):
    """
    @function       : warning(msg=None)
    @param msg      : (string) message string describing the warning
    @return         : None
    @summary        : generate a warning
    """
    result.Result.get().warning(_create_des_(msg))





def success(msg=None):
    """
    @function       : success(msg=None)
    @param msg      : (string) message string describing the success
    @return         : None
    @summary        : generate a success
    """
    result.Result.get().success(_create_des_(msg))


def fail(msg=None):
    """
    @function       : fail(msg=None)
    @param msg      : (string) message string describing the warning
    @return         : None
    @summary        : generate a fail
    """
    result.Result.get().fail(_create_des_(msg))

def fail_fatal(msg=None):
    """
    @function       : fail_fatal(msg=None)
    @param msg      : (string) message string describing the warning
    @return         : None
    @summary        : generate a fail and execution of test case is finished
    """
    result.Result.get().fail_fatal(_create_des_(msg))

def abort(msg=None):
    """
    @function       : abort(msg=None)
    @param msg      : (string) message string describing the abort
    @return         : None
    @summary        : generate an abortion of script
    """
    result.Result.get().abort_test(_create_des_(msg))


def tag_value(tag, value):
    """
    @function       : tag_value(tag, value):
    @param tag      : (string) tag 
    @param value    : (string) value
    @return         : None
    @summary        : generate a tag value
    """
    result.Result.get().tag_value({utils.to_unicode(tag):utils.to_unicode(value)})



def trace_env(scope, data):
    """
    @function       : trace_env(scope, data)
    @param scope    : (string) string that refer the scope
    @param data     : (string) string to trace
    @return         : None
    @summary        : trace data towards environment trace type
    """
    trace.TraceManager.get().trace_env(utils.to_unicode(scope), utils.to_unicode(data))

def trace_io(interface, data):
    """
    @function       : trace_io(interface, data)
    @param interface: (string) string that refer the interface
    @param data     : (string) string to trace
    @return         : None
    @summary        : trace data towards io trace type
    """
    trace.TraceManager.get().trace_io(utils.to_unicode(interface), utils.to_unicode(data))


def trace_script(msg):
    """
    @function       : trace_script(msg)
    @param msg      : (string) message to trace
    @return         : None
    @summary        : trace message, for script application
    """
    trace.TraceManager.get().trace_script(utils.to_unicode(msg))


def trace_layer(scope, data):
    """
    @function       : trace_layer(scope, data)
    @param scope    : (string) string that refer the scope
    @param data     : (string) string to trace
    @return         : None
    @summary        : trace data towards layer trace type
    """
    trace.TraceManager.get().trace_layer(utils.to_unicode(scope), utils.to_unicode(data))
    

def trace_json(obj):            
    trace.TraceManager.get().trace_json(obj)


def is_assert():
    return result.Result.get().is_assert()





