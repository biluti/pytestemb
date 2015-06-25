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
import unicodedata



def to_unicode(instr):
    return filter_string(_to_unicode(instr))
    
    
def _to_unicode(instr):
    if type(instr) == types.UnicodeType:
        return instr
    else:
        try:
            return unicode(str(instr), "utf-8")
        except UnicodeDecodeError:
            ascii_text = "%s" % (str(instr).encode('string_escape'))
            return unicode(ascii_text)


def filter_string(instr):
    """ filter control character"""
    toreplace = {}
    for ch in instr:
        if unicodedata.category(ch)[0] == "C":
            toreplace[ch] = None
    for r in toreplace.keys():
        if r in ["\n", "\t"]:
            continue
        else:
            instr = instr.replace(r, "<0x%.4X>" % ord(r))       
    return instr


def get_script_name():
    return os.path.splitext(os.path.split(sys.argv[0])[1])[0]



def str_dict(dic):
    res = []
    for key, value in dic.iteritems():
        ll = u"'%s':'%s'" % (unicode(key), unicode(value))
        res.append(ll)
    return u"{%s}" % ", ".join(res)







