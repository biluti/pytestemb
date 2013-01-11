# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : valid manages script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import sys
import inspect


import utils
import pytestemb.result as result
import pytestemb.pexception as pexception


# redirect sys.stderr => sys.stdout
sys.stderr = sys.stdout






class Valid:
    def __init__(self, result):
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
        
        self.case_name = None
        

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


    def get_case_name(self):
        return self.case_name


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
            self.case_name = "setup"
            self.run_try(self.setup)
            self.result.setup_stop({})
            self.case_name = None
        # Case
        for acase in self.case :
            name = acase.func_name
            self.result.case_start({"name":name})
            self.case_name = name
            self.run_case(acase)
            self.result.case_stop({"name":name})
            self.case_name = None
        # Cleanup
        if self.cleanup == self._nothing_:
            pass
        else:
            self.result.cleanup_start({})
            self.case_name = "cleanup"
            self.run_try(self.cleanup)
            self.result.cleanup_stop({})
            self.case_name = None
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
        DEFAULT = dict.fromkeys(["path","line","function","code"], "no info")
        traceback = inspect.trace()
        stack = []
        
        try:
            for index in range(CALL_DEPTH, len(traceback)):
                stack.append(dict(DEFAULT))
                stack[-1]["path"]      = traceback[index][1]
                stack[-1]["line"]      = traceback[index][2]
                stack[-1]["function"]  = traceback[index][3]
                stack[-1]["code"]      = utils.to_unicode(traceback[index][4][0].strip("\n"))
        except Exception:
            pass

        des = {}
        des["stack"]            = stack
        des["exception_info"]   = utils.to_unicode(exception)
        des["exception_class"]  = exception.__class__.__name__

        self.result.py_exception(des)






