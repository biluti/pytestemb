# -*- coding: UTF-8 -*-

"""
PyTestEmb Project : utils gathered some utils function
"""

__author__      = "$Author: jmbeguinet $"
__copyright__   = "Copyright 2009, The PyTestEmb Project"
__license__     = "GPL"
__email__       = "jm.beguinet@gmail.com"



import os
import sys
import types




def to_unicode(instr):
    if type(instr) == types.UnicodeType:
        return instr
    else:
        try:
            return unicode(str(instr), "utf-8")
        except UnicodeDecodeError:
            ascii_text = "%s" % (str(instr).encode('string_escape'))
            return unicode(ascii_text)


def get_script_name():
    return os.path.splitext(os.path.split(sys.argv[0])[1])[0]



def str_dict(d):
    res = []
    for key,value in d.iteritems():
        l = u"'%s':'%s'" % (unicode(key), unicode(value))
        res.append(l)
    return u"{%s}" % ", ".join(res)






