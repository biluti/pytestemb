# -*- coding: UTF-8 -*-



__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



VERSION_STRING = "3.1.0"


#    Historic :

#    * 3.1.0
#       - add trace_json for logstash 
#       - remove jenkins BUILD_URL and add remove prefix for NODE_NAME
#
#    * 3.0.3
#       - improve multiline for txt and logstash trace (remove useless information)
#
#    * 3.0.2
#       - logstash fix regression on jenkins_job_name 
#
#    * 3.0.1
#       - logstash add jenkins BUILD_NUMBER 
#
#    * 3.0.0
#       - add logstash json trace
#       - remove doc option 
#
#    * 2.3.0
#        - close trace ressources at end of script execution
#
#    * 2.2.2
#        - add system time in txt trace
#
#    * 2.2.1
#        - improve abortion during 'setup'
#
#    * 2.2.0
#        - improve abortion info reporting : msg and case
#
#    * 2.1.0
#        - pytestemb lib mode enable in arg '--pytestemb_lib_mode'
#
#    * 2.0.7
#        - add set_tracecase callback for case name tracing in SUT trace
#
#    * 2.0.6
#        - trace txt fix timestamp alignement
#
#    * 2.0.5
#        - add multilines for trace io/env/script/layer
#        - add parameter check on trace_trace function
#
#    * 2.0.4
#        - object model : skip method that starts with '_' (private & disable)
#
#    * 2.0.3
#        - object model : skip method that starts with '_' (private & disable)
#
#    * 2.0.2
#        - fix Unicode issue on trace function (scope, tag and interface parameter)
#
#    * 2.0.1
#        - fix issues with model object       
#
#    * 2.0.0
#        - full compatibility with Pytestemb 1.x      
#        - object model with automatic setup/case/cleanup discover
#        - setup/cleanup status is displayed in report     
#        - setup strategy : if exception occurs in setup, script is aborted              
#        - new dynamic parser for object model          
#        - get if assert has been generated during setup/case/cleanup execution               
#
# 
#   
#    class Test():
#
#        def setup(self):
#            pass
#    
#        def cleanup(self):
#            pass
#    
#        def case(self):
#            pass
#    
#        def case(self):
#            pass
#
#
#    if __name__ == "__main__":
#    
#        pytestemb.run()
#




import sys
import types
import platform



import pytestemb.trace as trace
import pytestemb.valid as valid
import pytestemb.result as result
import pytestemb.pydoc as pydoc
import pytestemb.pexception as pexeception
import pytestemb.utils as utils



from optparse import OptionParser
from pytestemb.valid import Test


INTERFACE = {}


INTERFACE_DEFAULT = 0
INTERFACE_LIST = 1


INTERFACE["result"] = (("standalone"),
                       ("none", "standalone", "stdout"))
INTERFACE["trace"] =  ([],
                       ("none", "octopylog", "txt", "logstash"))



def checker(parser, name, value):
    for line in INTERFACE[name][INTERFACE_LIST] :
        if line == value:
            break
    else :
        parser.error("Interface %s is not valid, see --help" % value)


def parse():
    
    parser = OptionParser()
    
    parser.add_option("-r", "--result",
                        action="store", type="string", dest="result", default=INTERFACE["result"][INTERFACE_DEFAULT],
                        help="set the interface for result, value can be : %s" % INTERFACE["result"][INTERFACE_LIST].__str__())
    parser.add_option("-t", "--trace",
                        action="append", type="string", dest="trace", default=INTERFACE["trace"][INTERFACE_DEFAULT],
                        help="set the interface for trace, value can be : %s" % INTERFACE["trace"][INTERFACE_LIST].__str__())
    parser.add_option("-p", "--path",
                        action="store", type="string", dest="path", default=None,
                        help="add path to Python path")
    parser.add_option("-c", "--config",
                        action="store", type="string", dest="config", default=None,
                        help="add config general purpose string (flag, filename ...)")
    parser.add_option("-m", "--mode",
                        action="store", type="string", dest="mode", default=None,
                        help="add mode general purpose string (debug, ...)")
    parser.add_option("-v", "--version",
                        action="store_true", dest="ver", default=False,
                        help="version of software")    
    
    (options, args) = parser.parse_args()
    
    if args != []:
        parser.error("Argument invalid %s " % args.__str__())
    checker(parser, "result", options.result)
    for item in options.trace:
        checker(parser, "trace", item)
    return options



# detect if pytestemb in lib_mode
if sys.argv[1:].count("--pytestemb_lib_mode") == 1:
    pass
else:
    OPTIONS = parse()
    if OPTIONS.path is not None:
        sys.path.append(OPTIONS.path)
    if OPTIONS.ver :
        sys.stdout.write("pytestemb\n")
        sys.stdout.write("Version   : %s\n" % VERSION_STRING)
        sys.stdout.write("Copyright : %s\n" % __copyright__)
        sys.stdout.write("Copyright : %s\n" % __license__)
        sys.stdout.write("Contact   : %s\n" % __email__)
        sys.exit(0)

    trace.TraceManager.create(OPTIONS.trace)
    result.Result.create(OPTIONS.result, trace.TraceManager.get())
    valid.Valid.create(result.Result.get())
    
    trace.TraceManager.get().set_result(result.Result.get())
    trace.TraceManager.get().start()
    
    # Configuration management
    SCOPE_CF = "CF"
    trace.TraceManager.get().trace_env(SCOPE_CF, "Library version : pytestemb %s" % VERSION_STRING)
    trace.TraceManager.get().trace_env(SCOPE_CF, "Python-version : %s" % platform.python_version())
    trace.TraceManager.get().trace_env(SCOPE_CF, "Plateform : %s" % platform.platform(terse=True))
    trace.TraceManager.get().trace_env(SCOPE_CF, "Default encoding : %s" % sys.getdefaultencoding())





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
    return OPTIONS.config


def get_mode():
    return OPTIONS.mode


def get_path():
    return OPTIONS.path


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







###########################################
# Compatibility with Pytestemb 1.x
###########################################

# alias
run_script = run







