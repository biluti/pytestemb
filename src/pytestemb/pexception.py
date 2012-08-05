





class PytestembError(Exception):
    "Exception raised by Pytestemb"
    def __init__(self, info):
        Exception.__init__(self)
        self.info = info
    def __str__(self):
        return self.info.__str__()  
    
    
