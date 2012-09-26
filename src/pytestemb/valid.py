# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : valid manages script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import sys
import copy
import inspect




import result
import utils
import pexception


# redirect sys.stderr => sys.stdout
sys.stderr = sys.stdout






class Valid:
    def __init__(self, config, result):
        self.config = config
        self.result = result
        self.setup      = self._nothing_
        self.cleanup    = self._nothing_
        self.create     = self._nothing_
        self.destroy    = self._nothing_
        self.case = []
        self.name = utils.get_script_name()
        
        self.aborted = False
        
        self.abort_fatal_mode = False
        self.abort_fatal = False
        

    def _nothing_(self):
        pass

    def set_setup(self, funcSetup):
        if self.setup == self._nothing_ :
            self.setup = funcSetup
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("Setup function already set")


    def set_cleanup(self, funcCleanup):
        if self.cleanup == self._nothing_ :
            self.cleanup = funcCleanup
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("CleanUp function already set")


    def set_create(self, funcCreate):
        if self.create == self._nothing_ :
            self.create = funcCreate
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("funcCreate function already set")
        

    def set_destroy(self, funcDestroy):
        if self.destroy == self._nothing_ :
            self.destroy = funcDestroy
        else:
            # Avoid user mistake with two time function set
            raise pexception.PytestembError("funcDestroy function already set")
    
    def set_fatal_mode(self, stop_case_run):
        self.abort_fatal_mode = stop_case_run
        
        

    def add_test_case(self, funcCase):
        self.case.append(funcCase)



    def run_script(self):
        self.result.script_start({"name":self.name})
        # Create 
        if self.create == self._nothing_:
            pass
        else:
            self.result.create_start({})
            self.run_try(self.create)
            self.result.create_stop({})
        # Setup
        if self.setup == self._nothing_:
            pass
        else:
            self.result.setup_start({})
            self.run_try(self.setup)
            self.result.setup_stop({})
        # Case
        for acase in self.case :
            name = acase.func_name
            self.result.case_start({"name":name})
            self.run_case(acase)
            self.result.case_stop({"name":name})
        # Cleanup
        if self.cleanup == self._nothing_:
            pass
        else:
            self.result.cleanup_start({})
            self.run_try(self.cleanup)
            self.result.cleanup_stop({})
        # Destroy    
        if self.destroy == self._nothing_:
            pass
        else:
            self.result.destroy_start({})
            self.run_try(self.destroy, force=True)
            self.result.destroy_stop({})
    
        self.result.script_stop({"name":self.name})


    def run_try(self, func, force=False):
        
        if self.aborted and not force:
            self.result.aborted({})
            return

        try:
            func()
        except result.TestErrorFatal:
            pass
        except result.TestAbort:
            self.aborted = True                  
        except (Exception), (error):
            self.inspect_traceback(error)


    def run_case(self, case):
        
        if self.aborted or self.abort_fatal:
            self.result.aborted({})
            return
        try:
            case()
        except result.TestErrorFatal:
            if self.abort_fatal_mode:
                self.abort_fatal = True          
        except result.TestAbort:
            self.aborted = True        
        except (Exception), (error):
            self.inspect_traceback(error)
 
 

    def inspect_traceback(self, exception):
        CALL_DEPTH = 1
        traceback = inspect.trace()
        stack = []
        default = dict.fromkeys(["path","line","function","code"], "no info")
        try:
            for index in range(CALL_DEPTH, len(traceback)):
                stack.append(copy.copy(default))
                stack[-1]["path"]      = copy.copy(traceback[index][1])
                stack[-1]["line"]      = copy.copy(traceback[index][2])
                stack[-1]["function"]  = copy.copy(traceback[index][3])
                stack[-1]["code"]      = copy.copy(traceback[index][4][0].strip("\n"))
        except Exception:
            pass
        finally:
            del traceback
        des = {}
        des["stack"]            = stack
        des["exception_info"]   = utils.to_unicode(exception.__str__())
        des["exception_class"]  = exception.__class__.__name__

        self.result.py_exception(des)






