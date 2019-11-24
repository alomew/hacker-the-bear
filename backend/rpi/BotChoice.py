from Stacey.aiml.script.bot import smarter


import random

class randBot():

    bot = None

    def __init__(self):
        self.mode = random.randint(1,2)
        if self.mode==1:# Stacey
            self.bot = smarter("")
            pass
        else: # Standard
            self.bot = smarter("standard")
            pass
        return
        
    def sendMessage(self, message):
        return self.bot.sendMessage(message)
