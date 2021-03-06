# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : valid manages script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import sys
import types 
import inspect
import functools


import pytestemb.utils as utils
import pytestemb.result as result
import pytestemb.pexception as pexception




# redirect sys.stderr => sys.stdout
#sys.stderr = sys.stdout


#
# create  => create, init, start env, data connection 
# setup   => set/check SUT state to be ready to execute case 
# case_a  => test case
# case_b  => test case
# cleanup => set/restore SUT state after case execution
# destroy => destroy ressource allocated in create (always executed)
#
#
# abort => stop execution
# fatal => end of case
#
# option : 
#  - all assert are fatal
#  - setup failed (exception/assert) => cleanup
#




def skip(msg):
    def decorator(test_item):
        if not isinstance(test_item, type):
            @functools.wraps(test_item)
            def skip_wrapper(*args, **kwargs):
                raise result.CaseSkip(msg)
            test_item = skip_wrapper
            test_item.skip_decorated = True

        return test_item
    return decorator

def _rf(obj):
    return obj

def skipif(condition, msg):

    if condition:
        return skip(msg)
    return _rf




class Test(object):

    def __init__(self):
        pass
    


class Valid(object):
    
    __single = None
    
    def __init__(self, inst_result):
        self._result = inst_result
        self._setup      = self._nothing_
        self._cleanup    = self._nothing_
        self._create     = self._nothing_
        self._destroy    = self._nothing_
        self._tracecase  = self._nothing_
        self._case = []
        self._name = utils.get_script_name()
        
        self._aborted = False
        self._aborted_msg = None
        
        self._abort_fatal_mode = False
        self._abort_fatal = False
        
        self._case_name = None

    @classmethod
    def create(cls, inst_result):
        cls.__single = cls(inst_result)
        return cls.__single
    
    @classmethod
    def get(cls):
        return cls.__single 
            

    def _nothing_(self):
        pass

    def set_setup(self, funcsetup):
        if self._setup == self._nothing_ :
            self._setup = funcsetup
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("Setup function already set")


    def set_cleanup(self, funccleanup):
        if self._cleanup == self._nothing_ :
            self._cleanup = funccleanup
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("CleanUp function already set")


    def set_create(self, funccreate):
        if self._create == self._nothing_ :
            self._create = funccreate
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("funcCreate function already set")
        

    def set_destroy(self, funcdestroy):
        if self._destroy == self._nothing_ :
            self._destroy = funcdestroy
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("funcDestroy function already set")



    def set_tracecase(self, functracecase):
        if self._tracecase == self._nothing_ :
            self._tracecase = functracecase
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("functracecase function already set")
        
    
    def tracecase(self, name):
        if self._tracecase != self._nothing_ :
            try:
                self._tracecase(utils.get_script_name(), name)
            except Exception as ex:
                raise pexception.PytestembError("Callback tracecase exception : '%s' => %s" % (ex.__class__.__name__, ex))
        else:
            pass
            
    
    
    def set_fatal_mode(self, stop_case_run):
        self._abort_fatal_mode = stop_case_run
        
        

    def add_test_case(self, funccase):
        self._case.append(funccase)


    def get_case_name(self):
        return self._case_name


    def _set_aborted(self, exc):
        self._aborted = True  
        self._aborted_msg = "in '%s', msg='%s'" % (self.get_case_name(), exc)

    def run_script(self):
        self._result.script_start({"name":self._name})
        # Create 
        if self._create == self._nothing_:
            pass
        else:
            self._result.create_start({})
            self._case_name = "create"
            self.run_try(self._create)
            self._result.create_stop({})
        # Setup
        if self._setup == self._nothing_:
            pass
        else:
            self._result.setup_start({})
            self._case_name = "setup"
            self.tracecase(self._case_name)
            self.run_abort(self._setup)
            self._result.setup_stop({})
            self._case_name = None
        # Case
        for acase in self._case :
            name = acase.__name__
            self._result.case_start({"name":name})
            self.tracecase(name)
            self._case_name = name
            self.run_case(acase)
            self._result.case_stop({"name":name})
            self._case_name = None
        # Cleanup
        if self._cleanup == self._nothing_:
            pass
        else:
            self._result.cleanup_start({})
            self._case_name = "cleanup"
            self.tracecase(self._case_name)
            self.run_try(self._cleanup)
            self._result.cleanup_stop({})
            self._case_name = None
        # Destroy    
        if self._destroy == self._nothing_:
            pass
        else:
            self._result.destroy_start({})
            self._case_name = "destroy"
            self.run_try(self._destroy, force=True)
            self._result.destroy_stop({})
    
        self._result.script_stop({"name":self._name})


    def run_try(self, func, force=False):
        
        if self._aborted and not force:
            self._result.aborted({"msg":self._aborted_msg})
            return

        try:
            func()
        except result.TestErrorFatal:
            pass
        except result.TestAbort as ex:
            self._set_aborted(ex)
        except result.CaseSkip as ex:
            self._result.skip({"msg":"%s" % ex})           
        except (Exception) as xxx_todo_changeme:
            (error) = xxx_todo_changeme
            self.inspect_traceback(error)


    def run_abort(self, func):
        
        if self._aborted:
            self._result.aborted({"msg":self._aborted_msg})
            return

        try:
            func()
        except result.TestErrorFatal as ex:
            self._set_aborted(ex)
            self._result.abort_in_setup("Fatal")
        except result.TestAbort as ex:
            self._set_aborted(ex)
            #self._result.abort_in_setup()
        except result.CaseSkip as ex:
            self._result.skip({"msg":"%s" % ex})         
        except (Exception) as xxx_todo_changeme1:
            (error) = xxx_todo_changeme1
            self.inspect_traceback(error)
            self._set_aborted(error) 
            self._result.abort_in_setup("Exception")
            


    def run_case(self, case):
        
        
        if self._aborted:
            self._result.aborted({"msg":self._aborted_msg})
            return
        
        if self._abort_fatal:
            self._result.aborted({})
            return        
        
        try:
            case()
        except result.TestErrorFatal:
            if self._abort_fatal_mode:
                self._abort_fatal = True          
        except result.TestAbort as ex:
            self._set_aborted(ex)
        except result.CaseSkip as ex:
            self._result.skip({"msg":"%s" % ex})            
        except (Exception) as xxx_todo_changeme2:
            (error) = xxx_todo_changeme2
            self.inspect_traceback(error)
 
 

    def inspect_traceback(self, exception):
        CALL_DEPTH = 1
        DEFAULT = dict.fromkeys(["path", "line", "function", "code"], "no info")
        traceback = inspect.trace()
        stack = []
        

        try :
            for index in range(CALL_DEPTH, len(traceback)):
                stack.append(dict(DEFAULT))
                stack[-1]["path"]      = traceback[index][1]
                stack[-1]["line"]      = traceback[index][2]
                stack[-1]["function"]  = traceback[index][3]
                stack[-1]["code"]      = utils.to_unicode(traceback[index][4][0]).strip("\n\r")
        except Exception as exception:
            pass

        des = {}
        des["stack"]            = stack
        des["exception_info"]   = utils.to_unicode(str(exception))
        des["exception_class"]  = exception.__class__.__name__

        self._result.py_exception(des)



    
    


    @classmethod
    def retrieve_test_class(cls, name="__main__"):
        module = __import__(name)
        cla = []
        for nn in dir(module):
            cc  = getattr(module, nn)
            try:
                if issubclass(cc, Test):
                    cla.append(cc)
                else:
                    continue
            except TypeError:
                continue # tested object was not a class
        return cla
    
    
    @classmethod
    def retrieve_test_class_(cls, module):
        cla = []
        for nn in dir(module):
            cc  = getattr(module, nn)
            try:
                if issubclass(cc, Test):
                    cla.append(cc)
                else:
                    continue
            except TypeError:
                continue # tested object was not a class
        return cla
    
        
    
    @classmethod
    def retrieve_test_method(cls, test_inst):
        METHOD_SKIP     = ["__init__"]
        METHOD_FORDBID  = ["create", "destroy"] 
        
        setup   = None
        cases   = []
        cleanup = None
        
        for met in dir(test_inst):
            if type(getattr(test_inst, met)) != types.MethodType:
                continue
            if met.startswith("_"):
                continue
            if met in METHOD_FORDBID:
                raise Exception("Invalid method name : '%s'" % met)
            if met in METHOD_SKIP:
                continue
            if met == "setup":
                setup = met
            elif met == "cleanup":
                cleanup = met
            else:
                cases.append(met)
        return setup, cases, cleanup


    @classmethod
    def scan(cls):
        
        
        testclasses = cls.retrieve_test_class()
        
        if len(testclasses) == 0:
            return # nothing to add
        elif len(testclasses) == 1:
            testclass = testclasses[0]
        else:
            raise pexception.PytestembError("Only one Test class supported")
        

        inst = testclass()        
        setup, cases, cleanup = cls.retrieve_test_method(inst)
        

        if setup is None:
            pass
        else:
            func_setup = getattr(inst, setup)
            Valid.get().set_setup(func_setup)
    
            
        for func_name in cases:
            func_case = getattr(inst, func_name)
            Valid.get().add_test_case(func_case)

        if cleanup is None:
            pass
        else:
            func_cleanup = getattr(inst, cleanup)
            Valid.get().set_cleanup(func_cleanup)
            







    
#class X(object):
#    A = 0
#    
#    
#    def __init__(self):
#        pass
#    
#    def a(self):
#        pass
#
#    @staticmethod
#    def b():
#        pass
#    
#        
#    
#x = X()
#
#
#n = type(x.A)
#print type(x.A)
#print type(x.a)
#print type(X.b)

    
    



