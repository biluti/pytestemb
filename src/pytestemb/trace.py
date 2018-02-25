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
import codecs
import hashlib
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
            
            if "msg" in des:
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
            
            if "msg" in des:
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
            if "msg" in des:
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
    TRACE_LOG_TXT   = "logtxt"
                   
    
    def __init__(self):
        Trace.__init__(self)
        self.dictra = dict()
        self.lm = list()
        self._ueid = self._gen_ueid() # unique execution id


    def get_trace_file(self):
        
        if self.TRACE_TXT in self.dictra:
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
    def create(cls, txt, sock):
        cls.__single = cls()
        cls.__single.add_traces(txt, sock)
        return cls.__single
    
    @classmethod
    def get(cls):
        return cls.__single 
        
    def add_trace(self, name, tra):
        if name not in self.dictra:
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
        
        if not isinstance(obj, dict):
            raise TypeError("Obj must be a Python dict, get type : %s" % obj.__class__.__name__)
            
        for k in obj.iterkeys():
            if not isinstance(k, basestring):
                raise TypeError("Obj key:'%s' must be a string, get type: %s" %  (k, obj.__class__.__name__))
        
        for i in self.lm:
            i.trace_json(obj)
        

    def add_traces(self, txt=None, sock=None):
        
        if txt is not None:
            self.add_trace(self.TRACE_TXT, TraceLoggingTxt(txt))    
        if sock is not None:
            self.add_trace(self.TRACE_OCTOPYLOG, TraceOctopylog(sock))            
    




class TraceOctopylog(Trace):

    def __init__(self, port):
        Trace.__init__(self)
        self.port = port
        self._scope = {}

    def start(self):
        if self.started:
            return
        else:
            self.started = True
            
        self.sockethandler = logging.handlers.SocketHandler("localhost", self.port)
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
        if len(msg) == 1:
            self.add_line(scope, msg)
        else:
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
        self.add_line("json", [sjson])
         






        
class TraceLoggingTxt(Trace):

    SIZE_SCOPE = 24
    
    SCOPE_MAPPING = {   "assert_ko":"result",
                        "assert_ok":"result",
                        "py_exception":"exception",}


    def __init__(self, destination):
        Trace.__init__(self)
        self.destination = destination
        self.file = None
        self.logger = logging.getLogger("pytestemb") 
        
        

    def get_filename(self):
        if self.file is None:
            return self.file
        else:
            self.file.flush()
            return self.file.name


    def start(self):     

        pathfile =  os.path.join(self.destination, self.gen_file_name())
 
        ch = logging.FileHandler(pathfile, mode='w', encoding="utf-8", delay=False)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formater())
  
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(ch)

        
        # create file
        des = dict({"type":"log", "file":pathfile})
        self.result.trace_ctrl(des)
        self.add_header()
        
        
    @classmethod
    def formater(cls):
        FIELDS = []
        FIELDS.append("%(asctime)s")
        FIELDS.append("%(name)24s")
        FIELDS.append("%(levelname)7s")
        FIELDS.append("%(message)s")
        formatter = logging.Formatter(" | ".join(FIELDS))
        return formatter

        
    
    def stop(self):
        pass

    @staticmethod
    def gen_file_name():
        name_script = utils.get_script_name()
        name_hash = TraceManager.get().get_ueid()
        return "%s_%s.log" % (name_script, name_hash)


    def _log(self, msg):
        self.logger.info(msg.strip("\n"))
        


    def add_header(self):
        self._log("Script file    : %s" % sys.argv[0])
        
    
    def add_line(self, scope, msg):
        #scope = scope.ljust(TraceTxt.SIZE_SCOPE)
        for i in msg: 
            self._log("[{}] {}".format(scope, i))


    def _trace_multiline(self, scope, msg):
        ALIGN = 13
        
        msg = msg.strip("\n\r")
        msg = msg.splitlines()
        if len(msg) == 1:
            self.add_line(scope, msg)
        else:
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
        self._log(msg)

    def trace_warning(self, des):
        self.add_line("Warning", [des["msg"]])
        
    def trace_env(self, scope, data):
        self._trace_multiline(scope, data)

    def trace_layer(self, scope, data):
        self._trace_multiline(scope, data)
        
    def trace_json(self, obj):
        sjson = json.dumps(obj)
        self.add_line("json", [sjson])
                
        
