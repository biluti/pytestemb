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
import json
import socket
import codecs
import hashlib
import platform
import datetime


import logging.handlers



import pytestemb.utils as utils
import pytestemb.gtime as gtime




class Trace(object):
    def __init__(self):
        self.gtime = gtime.Gtime.create()
        self.result = None
        self.started = False
           

    def set_result(self, result):
        self.result = result
        

    def start(self):
        pass
    
    def stop(self):
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
    
    
    TRACE_OCTOPYLOG = "octopylog"
    TRACE_STDOUT    = "stdout"
    TRACE_TXT       = "txt"
    TRACE_LOGSTASH  = "logstash"
    TRACE_NONE      = "none"
    
                   
    
    def __init__(self):
        Trace.__init__(self)
        self.dictra = dict()
        self.lm = list()
        self._ueid = self._gen_ueid() # unique execution id


    def get_trace_file(self):
        
        if self.dictra.has_key(self.TRACE_TXT):
            return self.dictra[self.TRACE_TXT].get_filename()
        else:
            return None 
        


    def _gen_ueid(self):
        md = hashlib.md5()
        md.update(utils.get_script_name())
        md.update(time.strftime("%d_%m_%Y_%H_%M_%S", self.gtime.start_date))
        return md.hexdigest()[0:16].upper()

    def get_ueid(self):
        return self._ueid
        
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
            self.lm.append(tra)
        else:
            pass

    def set_result(self, result):            
        for i in self.lm:
            i.set_result(result)

    def start(self):
        for i in self.lm:
            i.start()            
    
    def stop(self):
        for i in self.lm:
            i.stop()    

    def trace_script(self, msg):
        for i in self.lm:
            i.trace_script(msg)
            
    def trace_io(self, interface, data):
        for i in self.lm:
            i.trace_io(interface, data)     
            
    def trace_result(self, name, des):
        for i in self.lm:
            i.trace_result(name, des)

    def trace_warning(self, msg):
        for i in self.lm:
            i.trace_warning(msg)

    def trace_env(self, scope, data):
        for i in self.lm:
            i.trace_env(scope, data)
            
    def trace_layer(self, scope, data):
        for i in self.lm:
            i.trace_layer(scope, data)
    
    def trace_report(self, msg):
        for i in self.lm:
            i.trace_report(msg)     
            
    def trace_json(self, obj):
        for i in self.lm:
            i.trace_json(obj)
        

    def add_traces(self, interfaces):
        for interface in interfaces:
            if interface == self.TRACE_OCTOPYLOG:
                self.add_trace(self.TRACE_OCTOPYLOG, TraceOctopylog())
            elif interface == self.TRACE_STDOUT:
                self.add_trace(self.TRACE_STDOUT,    TraceStdout())
            elif interface == self.TRACE_TXT:
                self.add_trace(self.TRACE_TXT,       TraceTxt())
            elif interface == self.TRACE_LOGSTASH:
                self.add_trace(self.TRACE_LOGSTASH,  TraceLogstash())                
            elif interface == self.TRACE_NONE:
                pass
            else:
                raise ValueError("Invalid interfaces")




class TraceOctopylog(Trace):

    def __init__(self):
        Trace.__init__(self)
        self._scope = {}

    def start(self):
        if self.started:
            return
        else:
            self.started = True
            
        self.sockethandler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        self.rootlogger = logging.getLogger("pytestemb")
        self.rootlogger.setLevel(logging.INFO)
        self.rootlogger.addHandler(self.sockethandler)

        des = dict({"type":"octopylog"})
        self.result.trace_ctrl(des)
        self.trace_header()
    
    
    def stop(self):
        if self.started:
            self.rootlogger.removeHandler(self.rootlogger)
            self.sockethandler.close()
            self.started = False        
        else:
            return
    
    
    def trace_header(self):
        self.trace_scope("trace", "#"*64)
        self.trace_scope("trace", "# %s" % time.strftime("Start %d/%m/%Y @ %H:%M:%S", self.gtime.start_date))
        self.trace_scope("trace", "# UEID : '%s'" % TraceManager.get().get_ueid())
        self.trace_scope("trace", "#"*64)
        

    def trace_scope(self, scope, msg):
        
        try:
            self._scope[scope]
        except KeyError:
            self._scope[scope] = logging.getLogger("pytestemb.%s" % scope)
        finally:
            self._scope[scope].info(msg)


    def _trace_multiline(self, scope, msg):
        ALIGN = 13
        
        msg = msg.strip("\n\r")
        msg = msg.splitlines()
        if len(msg) == 1 :
            self.trace_scope(scope, msg[0])
        else :
            self.trace_scope(scope, "Start multiline :")
            for index, line in enumerate(msg):
                ln = "%d" % index
                ln = ln.ljust(ALIGN)
                self.trace_scope(scope, "%s%s" % (ln, line))

        
        

    def trace_script(self, msg):
        self._trace_multiline("script", msg)


    def trace_io(self, interface, data):        
        self._trace_multiline("io.%s" % interface, data)

    def trace_result(self, name, des):      
        if      name == "assert_ko":
            scope = "result_ko"
        else:
            scope = "result"
        for ll in self.format_result(name, des):
            self.trace_scope(scope, ll)

    def trace_warning(self, des):
        self.trace_scope("warning", des["msg"])

    def trace_env(self, scope, data):
        self._trace_multiline("env.%s" % scope, data)

    def trace_layer(self, scope, data):
        self._trace_multiline("layer.%s" % scope, data)

    def trace_report(self, msg):
        self.trace_scope("report", msg.replace("\n", ""))

    def trace_json(self, obj):
        sjson = json.dumps(obj)
        self.trace_scope("json", sjson)        
        
        

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
        
    def stop(self):
        if self.started:
            self.started = False        
        else:
            return


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
        
    def trace_json(self, obj):
        sjson = json.dumps(obj)
        self._write(sjson)      






class TraceTxt(Trace):
    
    SIZE_ATIME = 28
    SIZE_MTIME = 12
    SIZE_SCOPE = 24
    
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


    def get_filename(self):
        if self.file is None:
            return self.file
        else:
            self.file.flush()
            return self.file.name


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
            raise
        self.result.trace_ctrl(des)
        self.add_header()


    def stop(self):
        if self.started:
            self.file.close()
            self.started = False        
        else:
            return

    @staticmethod
    def gen_file_name():
        name_script = utils.get_script_name()
        name_hash = TraceManager.get().get_ueid()
        return "%s_%s.pyt" % (name_script, name_hash)

    @staticmethod
    def format(atime, mtime, scope, msg):
        atime = atime.ljust(TraceTxt.SIZE_ATIME)
        mtime = mtime.ljust(TraceTxt.SIZE_MTIME)
        scope = scope.ljust(TraceTxt.SIZE_SCOPE)
        return "%s%s%s%s\n"  % (atime, mtime, scope, msg)

    
    
    def add_header(self):
        dis = ""
        dis += "Script file    : %s\n" % sys.argv[0]
        dis += "Date           : %s\n" % time.strftime("%d/%m/%Y %H:%M:%S", self.gtime.start_date)
        dis += "\n%s\n" % self.format("System time", "Timestamp", "Scope", "Info")
        self.file.write(dis)

    
    def add_line(self, scope, msg):
        atime =  datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")
        atime = atime.ljust(TraceTxt.SIZE_ATIME)
        mtime = "%.6f" % self.gtime.get_time()
        mtime = mtime.ljust(TraceTxt.SIZE_MTIME)
        scope = scope.ljust(TraceTxt.SIZE_SCOPE)
        for i in msg: 
            self.file.write(u"%s%s%s%s\n" % (atime, mtime, scope, i))


    def _trace_multiline(self, scope, msg):
        ALIGN = 13
        
        msg = msg.strip("\n\r")
        msg = msg.splitlines()
        if len(msg) == 1 :
            self.add_line(scope, msg)
        else :
            data = []
            data.append("Start multiline :")
            for index, line in enumerate(msg):
                ln = "%d" % index
                ln = ln.ljust(ALIGN)
                data.append("%s%s" % (ln, line))  
            
            self.add_line(scope, data)    
        
        
    def trace_script(self, msg):
        self._trace_multiline("script", msg)
               
    def trace_io(self, interface, data):
        self._trace_multiline(interface, data)

    def trace_result(self, name, des):
        try:
            scope = self.SCOPE_MAPPING[name]
        except KeyError:
            scope = "sequence"

        ll = self.format_result(name, des)
        self.add_line(scope, ll)
                      
                      
    def trace_report(self, msg):
        self.file.write(msg)

    def trace_warning(self, des):
        self.add_line("Warning", [des["msg"]])
        
    def trace_env(self, scope, data):
        self._trace_multiline(scope, data)

    def trace_layer(self, scope, data):
        self._trace_multiline(scope, data)
        
    def trace_json(self, obj):
        sjson = json.dumps(obj)
        self.add_line("json", sjson)
         







class TraceLogstash(Trace):


    DEFAULT_DIR = "/tmp/logstash"

    SCOPE_MAPPING = {   "assert_ko":    "result",
                        "assert_ok":    "result",
                        "py_exception": "exception",}
    
    TYPE_LOG = "pytestemb_log"
    TYPE_RES = "pytestemb_result"
    TYPE_CUS = "pytestemb_cus"
    TYPE_STA = "pytestemb_statistic"

    def __init__(self):
        Trace.__init__(self)
        self.file = None
        self._base_data = None
        

    def start(self):
        
        self.create_base_data()
        if self.started:
            return
        else:
            self.started = True        

        if not(os.path.lexists(TraceLogstash.DEFAULT_DIR)):
            os.mkdir(TraceLogstash.DEFAULT_DIR)

        pathfile =  os.path.join(TraceLogstash.DEFAULT_DIR, self.gen_file_name())
        des = dict({"type":"json", "file":pathfile})
        try :
            self.file = codecs.open(pathfile, encoding="utf-8", mode="w", buffering=-1)
        except (IOError), (error):
            self.file = None
            des["error"] = error.__str__()
            raise
        self.result.trace_ctrl(des)

    @staticmethod
    def gen_file_name():
        name_script = utils.get_script_name()
        name_hash = TraceManager.get().get_ueid()
        return "%s_%s.json" % (name_script, name_hash)
    
        
    def stop(self):
        if self.started:
            self.file.close()
            self.started = False        
        else:
            return

    def _trace_multiline(self, scope, msg):
        ALIGN = 13
        
        msg = msg.strip("\n\r")
        msg = msg.splitlines()
        if len(msg) == 1 :
            self.add_evts(scope, msg)
        else :
            data = []
            for index, line in enumerate(msg):
                ln = "%d" % index
                ln = ln.ljust(ALIGN)
                data.append("%s%s" % (ln, line))
            self.add_evts(scope, data)    


    def create_base_data(self):
        data = {}
        data["jenkins_build_name"]    = os.getenv('BUILD_TAG', None)
        data["jenkins_node_name"]     = os.getenv('NODE_NAME', None)
        data["jenkins_build_url"]     = os.getenv('BUILD_URL', None)
        data["jenkins_job_name"]      = os.getenv('JOB_NAME', None)      
        data["jenkins_build_number"]  = os.getenv('BUILD_NUMBER', None)
        data["package_version"]       = os.getenv('PACKAGE_VERSION', None)  
        data["host"]                  = socket.gethostname()
        data["script"]                = utils.get_script_name()
        data["source"]                = "pytestemb"
        self._base_data = data

    def get_base_data(self):
        return dict(self._base_data)

    def add_evts(self, scope, msg):
        for m in msg:
            data = self.get_base_data()
            data["type"]     = self.TYPE_LOG
            data["scope"]    = scope
            data["msg"]      = m
            sjson = json.dumps(data)
            self.file.write(sjson + "\n")

    
    def trace_script(self, msg):
        self._trace_multiline("script", msg)

    def trace_io(self, interface, data):
        self._trace_multiline(interface, data)

    def trace_result(self, name, des):
        try:
            scope = self.SCOPE_MAPPING[name]
        except KeyError:
            scope = "sequence"

        ll = self.format_result(name, des)
        self.add_evts(scope, ll)
                      
                      
    def trace_report(self, msg):
        
        if msg.startswith("| Case"):
            case = msg.split("|")[1].strip(" ").replace("Case ", "").strip("'")
            result = msg.split("|")[2].strip(" ")
            result = result.replace("?", "na").lower()
            
            data = self.get_base_data()
            data["type"]     = self.TYPE_RES
            data["case"]     = case
            data["result"]   = result
        
        elif msg.startswith("| Script time execution"):
            timex = float(msg.split("|")[2].strip(" ").replace("(sec)", "").strip("'"))

            data = self.get_base_data()
            data["type"]    = self.TYPE_STA
            data["timex"]   = timex
   
        else:
            return
        
        sjson = json.dumps(data)
        self.file.write(sjson + "\n")                 


    def trace_warning(self, des):
        self.add_evts("Warning", [des["msg"]])
        
    def trace_env(self, scope, data):
        self._trace_multiline(scope, data)

    def trace_layer(self, scope, data):
        self._trace_multiline(scope, data)
    
    def trace_json(self, obj):
        
        data = self.get_base_data()
        data["type"] = self.TYPE_CUS
        
        data.update(obj)
        
        sjson = json.dumps(data)
        self.file.write(sjson + "\n")     
        
