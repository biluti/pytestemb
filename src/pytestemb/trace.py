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



import pytestemb.utils as utils
import pytestemb.gtime as gtime




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

    @staticmethod
    def format_result(name, des):
        line = []

        if    name == "assert_ko":
            
            if des.has_key("msg"):
                msg = des["msg"]
            else:
                msg = ""
            line.append("%s : '%s'" % (name, msg))

            for i in des["stack"]:
                line.append("    File \"%s\", line %d, in %s" % (i["path"], i["line"], i["function"]))
                line.append("        %s" % (i["code"]))
                    
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

            for i in des["stack"]:
                line.append("    File \"%s\", line %d, in %s" % (i["path"], i["line"], i["function"]))
                line.append("        %s" % (i["code"]))
                    
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
            
            for i in des["stack"]:
                line.append("    File \"%s\", line %d, in %s" % (i["path"], i["line"], i["function"]))
                line.append("        %s" % (i["code"]))
            line.append("    %s" % (des["exception_class"]))
            line.append("    %s" % (des["exception_info"]))

        elif    name in ["case_start", "case_stop", "assert_ok", "script_start", "script_stop", "tag_value", "warning"]:
            info = ", ".join(["%s:'%s'" % (key, value) for key, value in des.iteritems()])
            line.append("%s : %s" % (name, info))                 
        else:
            line.append("%s : %s" % (name, utils.str_dict(des)))
            
        return line
    
    def trace_report(self, msg):
        pass


class TraceManager(Trace):
    
    __single = None
    
    def __init__(self):
        Trace.__init__(self)
        self.dictra = dict()
        self.l = list()
        
    @classmethod
    def create(cls, interfaces):
        cls.__single = cls()
        cls.__single.add_traces(interfaces)
        return cls.__single
    
    @classmethod
    def get(cls):
        return cls.__single 
        
    def add_trace(self, name, tra):
        if not self.dictra.has_key(name):
            self.dictra[name] = tra
            self.l.append(tra)
        else:
            pass

    def set_result(self, result):            
        for i in self.l:
            i.set_result(result)

    def start(self):
        for i in self.l:
            i.start()            

    def trace_script(self, msg):
        for i in self.l:
            i.trace_script(msg)
            
    def trace_io(self, interface, data):
        for i in self.l:
            i.trace_io(interface, data)     
            
    def trace_result(self, name, des):
        for i in self.l:
            i.trace_result(name, des)

    def trace_warning(self, msg):
        for i in self.l:
            i.trace_warning(msg)

    def trace_env(self, scope, data):
        for i in self.l:
            i.trace_env(scope, data)
            
    def trace_layer(self, scope, data):
        for i in self.l:
            i.trace_layer(scope, data)
    
    def trace_report(self, msg):
        for i in self.l:
            i.trace_report(msg)     

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
        self._scope = {}

    def start(self):
        if self.started:
            return
        else:
            self.started = True
            
        sockethandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        rootlogger = logging.getLogger("pytestemb")
        rootlogger.setLevel(logging.INFO)
        rootlogger.addHandler(sockethandler)

        des = dict({"type":"octopylog"})
        self.result.trace_ctrl(des)
        self.trace_header()
    
    
    def trace_header(self):
        self.trace_scope("trace", "#"*64)
        self.trace_scope("trace", "# %s" % time.strftime("Start %d/%m/%Y @ %H:%M:%S", self.gtime.start_date))
        self.trace_scope("trace", "#"*64)
        

    def trace_scope(self, scope, msg):
        
        try:
            self._scope[scope]
        except KeyError:
            self._scope[scope] = logging.getLogger("pytestemb.%s" % scope)
        finally:
            self._scope[scope].info(msg)

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
        self.trace_scope("report", msg.replace("\n", ""))
        

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


    @staticmethod
    def _write(msg):
        sys.stdout.write(msg)

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
    
    SCOPE_MAPPING = {"assert_ko":"result",
                         "assert_ok":"result",
                         "py_exception":"exception",
                         }

    if      platform.system() == "Linux":
        DEFAULT_DIR = "/tmp/pytestemb"
    elif    platform.system() == "Windows":
        DEFAULT_DIR = "c:\\temp\\pytestemb"
    else:
        raise Exception("Platform not supported")

    def __init__(self):
        Trace.__init__(self)
        self.file = None


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
        des = dict({"type":"pyt", "file":pathfile})
        try :
            self.file = codecs.open(pathfile, encoding="utf-8", mode="w", buffering=-1)
        except (IOError) , (error):
            self.file = None
            des["error"] = error.__str__()
        self.result.trace_ctrl(des)
        self.add_header()

    def gen_file_name(self):
        md = hashlib.md5()
        md.update(sys.argv[0])
        md.update(time.strftime("%d_%m_%Y_%H_%M_%S", self.gtime.start_date))
        name_script = utils.get_script_name()
        name_hash = md.hexdigest()[0:16].upper()
        return "%s_%s.pyt" % (name_script, name_hash)

    @staticmethod
    def format(mtime, scope, msg):
        mtime = mtime.ljust(16)
        scope = scope.ljust(24)
        return "%s%s%s\n"  % (mtime, scope, msg)

    def add_header(self):
        dis = ""
        dis += "Script file    : %s\n" % sys.argv[0]
        dis += "Date           : %s\n" % time.strftime("%d/%m/%Y %H:%M:%S", self.gtime.start_date)
        dis += "\n%s\n" % self.format("Time(s)", "Scope", "Info")
        self.file.write(dis)

    
    def add_line(self, scope, msg):
        
        mtime = "%.6f          " % self.gtime.get_time()
        scope = scope.ljust(24)
        for i in msg: 
            self.file.write(u"%s%s%s\n" % (mtime, scope, i))
        
        
        
    def trace_script(self, msg):
        self.add_line("Script", [msg])

    def trace_io(self, interface, data):
        self.add_line(interface, [data])

    def trace_result(self, name, des):
        try:
            scope = self.SCOPE_MAPPING[name]
        except KeyError:
            scope = "sequence"

        l = self.format_result(name, des)
        self.add_line(scope, l)
                      
                      
    def trace_report(self, msg):
        self.file.write(msg)

    def trace_warning(self, des):
        self.add_line("Warning", [des["msg"]])
        
    def trace_env(self, scope, data):
        self.add_line(scope, [data])

    def trace_layer(self, scope, data):
        self.add_line(scope, [data])





