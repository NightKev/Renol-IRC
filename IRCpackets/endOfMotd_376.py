ID = "376"


        
def execute(self, sendMsg, prefix, command, params):
    print self.channels
    self.joinChannel(sendMsg, self.channels)
        
    sendMsg("MODE "+",".join(self.channels), 4)
    for chan in self.channels:
        sendMsg("TOPIC "+chan, 4)
    
    if isinstance(self.auth, str):
        sendMsg(self.auth, 5)
    
    for cmd in self.commands:
        if self.commands[cmd][0].__initialize__ != False:
            self.commands[cmd][0].__initialize__(self)
    
        