
"""
The Help Module allows the user to define a help entry for his command
This help entry will be added to the internal Help Database which is looked
up with the bot's help command.
Users can also define descriptions for each argument their command takes, and they can flag
the argument as optional or not. The help command will use this information to format the
resulting text accordingly.

Example of usage in commands/showHelp.py, with added comments:

#We need to define a __initialize__ function so that the code is executed on startup:
def __initialize__(self, Startup):

    # self.helper is a HelpModule object.
    # Using help.newHelp, we are creating a new HelpEntity object with the ID, i.e. the name of the command,
    # as the first argument. In this case, ID is the string "help". 
    # Using non-string values can have unforseen consequences, please use a string.
    
    entry = self.helper.newHelp(ID) 


    # We add two lines of descriptions to our help entry. They will be put out as seperate
    # NOTICE messages to the user when he looks up the help information.
    
    entry.addDescription("The 'help' command shows you the descriptions and arguments of commands that have added an entry to the internal Help Database.")
    entry.addDescription("You can only view the help of a command if you are authorized to use the command.")
    
    
    # We add two arguments, "command name" and "argument name", and their descriptions to the help entry.
    # Please note that arguments can only have one line, although long lines will be broken into several 
    # NOTICE messages later by the sendNotice function in the help command.
    #
    # We flag the "argument name" argument as optional, this only has an aesthetic function so that the user
    # knows which arguments are required and which ones are optional and can be left out.
    
    entry.addArgument("command name", "The name of the command you want to know about.")
    entry.addArgument("argument name", "The name of the argument you want to know about.", optional = True)
    
    
    # We set the rank for the command information. Per default, the rank is already 0 for every HelpEntity object,
    # but you want to change the rank value to a higher number to restrict unauthorized users from
    # reading the description. You can set the rank value to a lower number than your command if you don't
    # mind users reading the description of a command they cannot use.
    
    entry.rank = 0
    
    
    # Finally, we register this entry with the bot's HelpModule object. This will add the entry to its
    # internal Help Database which is used by the help command. The registerHelp method will raise a 
    # RuntimeError if the command entry already exists, you may want to set overwrite = True if you don't mind
    # overwriting the previous entry, e.g. on command reload.
    
    self.helper.registerHelp(entry, overwrite = True)




# Commands that require more complicated help functions can define their own help handler.
# In that case, the help command will pass on its arguments to the custom help handler function.
#
# The help command will still handle checking if the command exists in the internal database and
# if the user is allowed to read the help information, please consider that when you define a 
# function for showing information about the command.

def helpHandler(self, name, params, channel, userdata, rank):
    print "Hi, I am an example for a custom help handler!"
    
def __initialize__(self, Startup):
    entry = self.helper.newHelp(commandName)
    entry.setCustomHandler(helpHandler)
    entry.rank = 0
    self.helper.registerHelp(entry, overwrite = True)
    
"""

class HelpEntity():
    def __init__(self, cmdname):
        self.cmdname = cmdname
        
        self.arguments = []
        
        self.description = []
        
        self.rank = 0
    
        self.custom_handler = None
        
    def addDescription(self, description):
        if isinstance(description, basestring):
            self.description.append(description)
        else:
            raise TypeError("Wrong type! Should be subclass of basestring, but is {0}: {1}".format(type(description), description))
    
    def addArgument(self, argument, description = None, optional = False):
        if not isinstance(argument, basestring):
            raise TypeError("Wrong type! Should be subclass of basestring, but is {0}: {1}".format(type(argument), argument))
        
        if optional != False and optional != True:
            raise TypeError("Wrong type! Variable 'optional' should be False or True, but is {0}: {1}".format(type(description), description))
        
        if description == None:
            self.arguments.append((argument, None, optional))
        elif isinstance(description, basestring):
            self.arguments.append((argument, description, optional))
        else:
            raise TypeError("Wrong type! Variable 'description' should be None or subclass of basestring, but is {0}: {1}".format(type(description), description))
    
    def setCustomHandler(self, func):
        if not callable(func):
            raise TypeError("Wrong type! Custom handler should be callable, but is {0}: {1}".format(type(func), func))
        else:
            self.custom_handler = func
    
    def __run_custom_handler__(self, bot_self, *args):
        self.custom_handler(bot_self, *args)
        
class HelpModule():
    def __init__(self):
        self.helpDB = {}
    
    def newHelp(self, cmdname):
        return HelpEntity(cmdname)
    
    def registerHelp(self, helpObject, overwrite = False):
        if not isinstance(helpObject, HelpEntity):
            raise TypeError("Invalid Object provided: '{0}' (type: {1})".format(helpObject, type(helpObject)))
        elif helpObject.cmdname in self.helpDB and overwrite == False:
            raise RuntimeError("Conflict Error: A command with such a name already exists!")
        elif helpObject.cmdname in self.helpDB and overwrite == True:
            print "ATTENTION: A command with such a name is already registered."
            self.helpDB[helpObject.cmdname] = helpObject
        else:
            self.helpDB[helpObject.cmdname] = helpObject
    
    def unregisterHelp(self, cmdname):
        del self.helpDB[cmdname]
        
    
    def getCmdHelp(self, cmdname):
        return self.helpDB[cmdname]