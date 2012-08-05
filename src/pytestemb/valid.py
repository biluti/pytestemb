# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : valid manages script execution
"""

__author__      = "$Author: jmbeguinet $"
__version__     = "$Revision: 1.3 $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"




import sys
import copy
import inspect




import result
#import trace
import utils
import pexception


# redirect sys.stderr => sys.stdout
sys.stderr = sys.stdout






class Valid:
    def __init__(self, config, result):
        self.config = config
        self.result = result
        self.setup = self._nothing_
        self.cleanup = self._nothing_
        self.case = []
        self.name = utils.get_script_name()

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

    def add_test_case(self, funcCase):
        self.case.append(funcCase)

#    def script_need_run(self, name):
#        return True


    def run_script(self):

        self.result.script_start({"name":self.name})
        try:
            # Setup
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
            self.result.cleanup_start({})
            self.run_try(self.cleanup)
            self.result.cleanup_stop({})
        except:
            raise
        self.result.script_stop({"name":self.name})


    def run_try(self, func):
        try:
            func()
        except result.TestErrorFatal:
            pass
        except (Exception), (error):
            self.inspect_traceback(error)

    def run_case(self, case):
        try:
            case()
            return True
        except result.TestErrorFatal:
            return True
        except (Exception), (error):
            self.inspect_traceback(error)
            return False




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
        except Exception, ex:
            pass
        finally:
            del traceback
        des = {}
        des["stack"]            = stack
        des["exception_info"]   = utils.to_unicode(exception.__str__())
        des["exception_class"]  = exception.__class__.__name__

        self.result.py_exception(des)





