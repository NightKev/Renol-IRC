from datetime import datetime

ID = "watchdog"
permission = 3
privmsgEnabled = True

def choose_singular_or_plural(num, singular, plural):
    if num > 1:
        return "{0} {1}".format(num, plural)
    elif num == 1:
        return "{0} {1}".format(num, singular)
    else:
        return None

def execute(self, name, params, channel, userdata, rank, chan):
    if len(params) == 0:
        uptime = datetime.now() - self.startupTime
        
        weeks = uptime.days / 7
        days = uptime.days % 7
        
        hours = uptime.seconds / (60*60)
        minutes = (uptime.seconds % (60*60)) / 60
        
        timeList = []
        
        weekString  = choose_singular_or_plural(weeks, "week", "weeks")
        dayString   = choose_singular_or_plural(days, "day", "days")
        hourString  = choose_singular_or_plural(hours, "hour", "hours")
        minString   = choose_singular_or_plural(minutes, "minute", "minutes")
        
        if weekString   != None: timeList.append(weekString)
        if dayString    != None: timeList.append(dayString)
        if hourString   != None: timeList.append(hourString)
        if minString    != None: timeList.append(minString)
        
        if len(timeList) == 0:
            timeList.append("Just started")
        
        self.sendMessage(channel, "Uptime: " + ", ".join(timeList))
        
        stats = {}
        
        for eventType in self.events:
            average = None
            minimum = None
            maximum = None
            
            for event in self.events[eventType].__events__:
                eventStats = self.events[eventType].__events__[event]["stats"]
                
                if average == None:
                    average, minimum, maximum = eventStats["average"], eventStats["min"], eventStats["max"]
                else:
                    if eventStats["min"] < minimum:
                        minimum = eventStats["min"]
                    if eventStats["max"] > maximum:
                        maximum = eventStats["max"]
                    average = (average + eventStats["average"]) / 2
            
            stats[eventType] = [average, minimum, maximum]
        
        dataOutput = []
        
        for event in stats:
            average, minimum, maximum = stats[event]
            if average == None:
                average, minimum, maximum = 0, 0, 0
            
            # The micro prefix in unicode
            dataOutput.append(u"{0}: [{1}\u00B5s/{2}\u00B5s/{3}\u00B5s]".format(event, 
                                                          round(minimum / (10**-6), 2), 
                                                          round(maximum / (10**-6), 2), 
                                                          round(average / (10**-6), 2)
                                                          )
                              )
        
        finalString = "Event statistics: (min/max/average): "+", ".join(dataOutput)
        
        self.sendMessage(channel, finalString)
    
    else:
        eventType = params[0]
        
        if eventType in self.events:
            eventStats = {}
            
            dataOutput = []
            
            for event in self.events[eventType].__events__:
                stats = self.events[eventType].__events__[event]["stats"]
                average, minimum, maximum = stats["average"], stats["min"], stats["max"]
                
                if average == None:
                    average, minimum, maximum = 0, 0, 0
                
                # The micro prefix in unicode
                dataOutput.append(u"{0}: [{1}\u00B5s/{2}\u00B5s/{3}\u00B5s]".format(event,
                                                                    round(minimum / (10**-6), 2),
                                                                    round(maximum / (10**-6), 2),
                                                                    round(average / (10**-6), 2)
                                                                    )
                                  )
            
            self.sendMessage(channel, "Statistics for event type '{0}': {1}".format(eventType,
                                                                                    ", ".join(dataOutput)
                                                                                    )
                             )
                
        else:
            self.sendMessage(channel, "No such event type.")
    
    
    