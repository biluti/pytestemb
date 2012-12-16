# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : trace manages trace coming from module and script execution
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"


import os
import sys
import time
import codecs
import hashlib
import platform


import logging.handlers



import utils
import gtime





class Trace:
    def __init__(self):
        self.gtime = gtime.Gtime.create()
        self.result = None
        self.started = False

    def set_result(self, result):
        self.result = result


    def start(self):
        pass

    def trace_script(self, msg):
        pass

    def trace_io(self, interface, data):
        pass

    def trace_result(self, name, des):
        pass
    
    def trace_warning(self, msg):
        pass


    def trace_env(self, scope, data):
        pass

    def trace_layer(self, scope, data):
        pass

    def format_result(self, name, des):
        line = []

        if    name == "assert_ko":
            
            if des.has_key("msg"):
                msg = des["msg"]
            else:
                msg = ""
            line.append("%s : '%s'" % (name, msg))

            for s in des["stack"]:
                line.append("    File \"%s\", line %d, in %s" % (s["path"], s["line"], s["function"]))
                line.append("        %s" % (s["code"]))
                    
            line.append("    File \"%s\", line %d, in %s" % (des["file"], des["line"], des["function"]))
            line.append("        + function   : \"%s\"" % des["function"])
            line.append("        + expression : \"%s\"" % des["expression"])
            line.append("        + values     : \"%s\"" % des["values"])
            line.append("        + time       : \"%s\"" % des["time"])
        
        
        elif name == "abort":
            
            if des.has_key("msg"):
                msg = des["msg"]
            else:
                msg = ""
            line.append("%s : '%s'" % (name, msg))

            for s in des["stack"]:
                line.append("    File \"%s\", line %d, in %s" % (s["path"], s["line"], s["function"]))
                line.append("        %s" % (s["code"]))
                    
            line.append("    File \"%s\", line %d, in %s" % (des["file"], des["line"], des["function"]))
            line.append("        + function   : \"%s\"" % des["function"])
            line.append("        + expression : \"%s\"" % des["expression"])
            line.append("        + time       : \"%s\"" % des["time"])
            
        
        elif    name == "assert_ok":
            if des.has_key("msg"):
                msg = des["msg"]
            else:
                msg = ""            
            line.append("%s : '%s'" % (name, msg))
        
        elif  name == "py_exception":
            line.append("%s : time:'%s'" % (name, des["time"]))
            
            for s in des["stack"]:
                line.append("    File \"%s\", line %d, in %s" % (s["path"], s["line"], s["function"]))
                line.append("        %s" % (s["code"]))
            line.append("    %s" % (des["exception_class"]))
            line.append("    %s" % (des["exception_info"]))

        elif    name in ["case_start", "case_stop", "assert_ok", "script_start", "script_stop", "tag_value", "warning"]:
            info = ", ".join(["%s:'%s'" % (k,v) for k,v in des.iteritems()])
            line.append("%s : %s" % (name, info))                 
        else:
            line.append("%s : %s" % (name, utils.str_dict(des)))
            
        return line
    
    def trace_report(self, msg):
        pass


class TraceManager(Trace):
    def __init__(self):
        Trace.__init__(self)
        self.dictra = dict()
        
    def add_trace(self, name, tra):
        if not self.dictra.has_key(name):
            self.dictra[name] = tra
        else:
            pass

    def set_result(self, result):
        for tra in self.dictra.itervalues() :
            tra.set_result(result)

    def start(self):
        for tra in self.dictra.itervalues() :
            tra.start()

    def trace_script(self, msg):
        for tra in self.dictra.itervalues() :
            tra.trace_script(msg)

    def trace_io(self, interface, data):
        for tra in self.dictra.itervalues() :
            tra.trace_io(interface, data)

    def trace_result(self, name, des):
        for tra in self.dictra.itervalues() :
            tra.trace_result(name, des)

    def trace_warning(self, msg):
        for tra in self.dictra.itervalues() :
            tra.trace_warning(msg)


    def trace_env(self, scope, data):
        for tra in self.dictra.itervalues() :
            tra.trace_env(scope, data)
            
    def trace_layer(self, scope, data):
        for tra in self.dictra.itervalues() :
            tra.trace_layer(scope, data)
    
    def trace_report(self, msg):
        for tra in self.dictra.itervalues() :
            tra.trace_report(msg)


    def add_traces(self, interfaces):
        for interface in interfaces:
            if interface == "octopylog":
                self.add_trace("octopylog", TraceOctopylog())
            elif interface == "stdout":
                self.add_trace("stdout",    TraceStdout())
            elif interface == "txt":
                self.add_trace("txt",       TraceTxt())
            elif interface == "none":
                pass
            else:
                raise Exception("Invalid interfaces")




class TraceOctopylog(Trace):

    def __init__(self):
        Trace.__init__(self)
        self.scope = {}

    def start(self):
        if self.started:
            return
        else:
            self.started = True
            
        socketHandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        rootLogger = logging.getLogger("pytestemb")
        rootLogger.setLevel(logging.DEBUG)
        rootLogger.addHandler(socketHandler)

        des = dict({"type":"octopylog"})
        self.result.trace_ctrl(des)
        self.trace_header()
    
    
    def trace_header(self):
        self.trace_scope("trace", "#"*64)
        self.trace_scope("trace", "# %s" % time.strftime("Start %d/%m/%Y @ %H:%M:%S", self.gtime.start_date))
        self.trace_scope("trace", "#"*64)
        

    def trace_scope(self, scope, msg):
        try:
            self.scope[scope].info("%s" % msg)
        except Exception:
            self.scope[scope] = logging.getLogger("pytestemb.%s" % scope)
            self.scope[scope].info("%s" % msg)

    def trace_script(self, msg):
        self.trace_scope("script", msg)

    def trace_io(self, interface, data):
        self.trace_scope("io.%s" % interface, data)

    def trace_result(self, name, des):      
        if      name == "assert_ko":
            scope = "result_ko"
        else:
            scope = "result"
        for l in self.format_result(name, des):
            self.trace_scope(scope, l)

    def trace_warning(self, des):
        self.trace_scope("warning", des["msg"])

    def trace_env(self, scope, data):
        self.trace_scope("env.%s" % scope, data)

    def trace_layer(self, scope, data):
        self.trace_scope("layer.%s" % scope, data)

    def trace_report(self, msg):
        self.trace_scope("report", msg)
        

class TraceStdout(Trace):

    def __init__(self):
        Trace.__init__(self)

    def start(self):
        if self.started:
            return
        else:
            self.started = True        
        des = dict({"type":"stdout"})
        self.result.trace_ctrl(des)

    def _write(self, msg):
        sys.stdout.write(codecs.encode(utils.to_unicode(msg), "utf-8"))

    def trace_script(self, msg):
        self._write(msg)

    def trace_io(self, interface, data):
        self._write(data)

    def trace_result(self, name, des):
        self._write(des)
        
    def trace_warning(self, des):
        self._write(des)        

    def trace_env(self, scope, data):
        self._write(data)
        
    def trace_layer(self, scope, data):
        self._write(data)
        
    def trace_report(self, msg):
        self._write(msg)
        


class TraceTxt(Trace):

    if      platform.system() == "Linux":
        DEFAULT_DIR = "/tmp/pytestemb"
    elif    platform.system() == "Windows":
        DEFAULT_DIR = "c:\\temp\\pytestemb"
    else:
        raise Exception("Platform not supported")

    def __init__(self):
        self.file = None
        Trace.__init__(self)

    def start(self):
        if self.started:
            return
        else:
            self.started = True        
        # output path and filename for trace file

        if not(os.path.lexists(TraceTxt.DEFAULT_DIR)):
            os.mkdir(TraceTxt.DEFAULT_DIR)

        pathfile =  os.path.join(TraceTxt.DEFAULT_DIR, self.gen_file_name())
        # create file
        des = dict({"type":"pyt","file":pathfile})
        try :
            self.file = codecs.open(pathfile, encoding="utf-8", mode="w", buffering=-1)
        except (IOError) , (error):
            self.file = None
            des["error"] = error.__str__()
        self.result.trace_ctrl(des)
        # write header
        self.add_header()

    def gen_file_name(self):
        """ """
        m = hashlib.md5()
        m.update(sys.argv[0])
        m.update(time.strftime("%d_%m_%Y_%H_%M_%S", self.gtime.start_date))
        name_script = utils.get_script_name()
        name_hash = m.hexdigest()[0:16].upper()
        return"%s_%s.pyt" % (name_script, name_hash)

    def format(self, mtime, scope, msg):
        mtime = mtime.ljust(16)
        scope = scope.ljust(24)
        return "%s%s%s\n"  % (mtime, scope, msg)

    def add_header(self):
        if self.file is not None :
            dis = ""
            dis += "Script file    : %s\n" % sys.argv[0]
            dis += "Date           : %s\n" % time.strftime("%d/%m/%Y %H:%M:%S", self.gtime.start_date)
            dis += "\n%s\n" % self.format("Time(s)", "Scope", "Info")
            self.file.write(utils.to_unicode(dis))

    def add_line(self, scope, msg):
        if self.file is not None :
            mtime = "%.6f" % self.gtime.get_time()
            dis = self.format(mtime, scope, msg)
            self.file.write(utils.to_unicode(dis))

    def trace_script(self, msg):
        self.add_line("Script", msg)

    def trace_io(self, interface, data):
        self.add_line(interface, data)

    def trace_result(self, name, des):
        
        if      name == "assert_ko":
            scope = "result"
        elif    name == "assert_ok":
            scope = "result"
        elif    name == "py_exception":
            scope = "exception"
        else:
            scope = "sequence"
        for l in self.format_result(name, des):
            self.add_line(scope, l)
        
    def trace_report(self, msg):
        self.file.write(utils.to_unicode(msg))

    def trace_warning(self, des):
        self.add_line("Warning", des["msg"])
        

    def trace_env(self, scope, data):
        self.add_line(scope, data)

    def trace_layer(self, scope, data):
        self.add_line(scope, data)


def create(interfaces):
    tracemanager = TraceManager()
    tracemanager.add_traces(interfaces)
    return tracemanager






