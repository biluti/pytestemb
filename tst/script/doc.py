








import pytestemb.pydoc as pydoc





if __name__ == "__main__":
    


    pd = pydoc.DocGen("/home/jmb/workspace/pytestemb/tst/script")

    r = pd.scan_project("2x")
    r.remove("2x.script_object_04")
    r.remove("2x.script_object_05")
    r.remove("2x.script_introspection_01")
    
    for p in r:
        print pd.script_doc(p)
    
    
    print pd.script_doc("2x.script_doc_01")

