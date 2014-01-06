import logging

ID = "help"
permission = 0

help_log = logging.getLogger("HelpModule")

def execute(self, name, params, channel, userdata, rank):
    if len(params) > 0:
        cmdname = params[0]
        try:
            help = self.helper.getCmdHelp(cmdname)
        except KeyError as error:
            print str(error)
            self.sendNotice(name, "No such command exists.")
            return
    else:
        self.sendNotice(name, "Specify a command you want to know more about.")
        return
    
    if self.rankconvert[rank] < help.rank:
        self.sendNotice(name, "Command is restricted.")
        help_log.debug("Looking up command '%s', but it is restricted.", name, cmdname)
        return
    
    if help.custom_handler != None:
        help.__run_custom_handler__(self, name, params, channel, userdata, rank)
        
    elif len(params) == 1:
        help_log.debug("Looking up command '%s'", name, cmdname)
        arglist = [self.cmdprefix+cmdname]
        
        for arg in help.arguments:
            argname = arg[0]
            optional = arg[2]
            
            if optional == False:
                arglist.append("<"+arg[0]+">")
            else:
                arglist.append("("+arg[0]+")")
        
        self.sendNotice(name, "Command usage: "+" ".join(arglist))
        
        if len(help.description) == 1:
            self.sendNotice(name, "Command description: "+help.description[0])
        elif len(help.description) > 1:
            self.sendNotice(name, "Command description: "+help.description[0])
            for line in help.description[1:]:
                self.sendNotice(name, line)
        else:
            self.sendNotice(name, "Command description: No description given.")
        
        
        
        
    elif len(params) > 1:
        cmdname = params[0]
        argname = " ".join(params[1:])
        
        found = False
        
        help_log.debug("Looking up argument '%s' for command '%s'", argname, cmdname)
        
        for arg in help.arguments:
            if argname.lower() == arg[0].lower():
                
                optional_or_required = arg[2] == False and "REQUIRED" or "OPTIONAL"
                
                self.sendNotice(name, "Argument description for '{0}' [{1}]: {2}".format(arg[0], optional_or_required, arg[1]))
                found = True
                break
                
        if found == False:
            self.sendNotice(name, "The command does not have such an argument")
    else:
        self.sendNotice(name, "No arguments provided.")

def test(self, name, params, channel, userdata, rank):
    print name

def __initialize__(self, Startup):
    entry = self.helper.newHelp(ID)
    
    entry.addDescription("The 'help' command shows you the descriptions and arguments of commands that have added an entry to the internal Help Database.")
    entry.addDescription("You can only view the help of a command if you are authorized to use the command.")
    entry.addArgument("command name", "The name of the command you want to know about.")
    entry.addArgument("argument name", "The name of the argument you want to know about.", optional = True)
    entry.rank = 0
    
    self.helper.registerHelp(entry, overwrite = True)