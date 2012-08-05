
import pytestemb.interface_io as interface_io






class Interface_echo(interface_io.Interface_io):
    
    def __init__(self, name):
        interface_io.Interface_io.__init__(self, name)
        self.data = None
        
        
    def send(self, data):
        self.data = data
        self.trace_io(self.name, "TX :: %s" % self.data)
    
        
    def receive(self):
        self.trace_io(self.name, "RX :: %s" % self.data)
        return self.data
        
        
        
        
__interface__ = {}

 
def create():
    __interface__["echo"] = Interface_echo("echo")   


def start():
    __interface__["echo"].start()

   
def stop():   
    __interface__["echo"].stop()
    
def send(data):   
    __interface__["echo"].send(data)

def receive():
    return __interface__["echo"].receive()    
    
    
    
    
            