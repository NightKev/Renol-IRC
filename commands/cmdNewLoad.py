import imp

ID = "newload"
permission = 3

def execute(self, name, params, channel, userdata, rank):
    files = self.__ListDir__("commands")
    currentlyLoaded = [self.commands[cmd][1] for cmd in self.commands]
    
    for item in currentlyLoaded:
        filename = item.partition("/")[2]
        files.remove(filename)
    
    if len(files) == 0:
        self.sendMessage(channel, "No new commands found.")
    else:
        if len(files) == 1:
            self.sendMessage(channel, "1 new command found.")
        else:
            self.sendMessage(channel, "{0} new commands found.".format(len(files)))
        
        for filename in files:
            path = "commands/"+filename
            module = imp.load_source("RenolIRC_"+filename[0:-3], path)
            cmd = module.ID
            
            self.commands[cmd] = (module, path)
            
            try:
                if not callable(module.__initialize__):
                    module.__initialize__ = False
                    self.__CMDHandler_log__.log("File {0} does not use an initialize function".format(filename))
            except AttributeError:
                module.__initialize__ = False
                self.__CMDHandler_log__.log("File {0} does not use an initialize function".format(filename))
            
            if module.__initialize__ != False:
                module.__initialize__(self, True)
            
            self.sendMessage(channel, "{0} has been loaded.".format(path))
            self.__CMDHandler_log__.info("File {0} has been newly loaded.".format(filename))


def __initialize__(self, Startup):
    entry = self.helper.newHelp(ID)
    
    entry.addDescription("The 'newload' command will load any newly added plugins that have not been loaded yet without reloading other plugins.")
    entry.rank = permission
    
    self.helper.registerHelp(entry, overwrite = True)