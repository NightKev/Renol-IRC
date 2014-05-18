

ID = "JOIN"

def execute(self, sendMsg, prefix, command, params):
    print "SOMEBODY JOINED CHANNEL:"
    print prefix
    print params
    
    part1 = prefix.partition("!")
    part2 = part1[2].partition("@")
    
    name = part1[0]
    ident = part2[0]
    host = part2[2]
    
    channel = self.retrieveTrueCase(params)
    
    if self.Bot_Auth.doesExist(name) and not self.Bot_Auth.isRegistered(name):
            self.whoisUser(name)
    
    self.events["channeljoin"].tryAllEvents(self, name, ident, host, channel)
    
    if channel != False:
        nothere = True
        for derp in self.channelData[channel]["Userlist"]:
            if derp[0] == name:
                nothere = False
                break
        
        if nothere == True:
            self.channelData[channel]["Userlist"].append((name, ""))
        else:
            self.__CMDHandler_log__.debug("%s has joined channel %s, "
                                          "but he is already in the user list!", name, channel)
    else:
        self.__CMDHandler_log__.debug("Channel mismatch: %s has joined channel '%s', "
                                      "But retrieveTrueCase returned False.", name, params)