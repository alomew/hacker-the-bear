

class Database:

    def __init__(self):
        days = ["first", "second", "third", "forth", "fifth"]
        self.first, self.second, self.third, self.forth, self.fifth = [], [], [], [], []

    def receive(self, timefile):
        self.first, self.second, self.third, self.forth, self.fifth = timefile[0], timefile[1], timefile[2], timefile[3], timefile[4]
        self.current = self.first

    def timedens(self):
        accum = []
        dens = []
        for i in range(len(self.first)):
            temp = self.first[i]
            accum.append(int(temp.strftime("%H")))
        for i in range(0,24):
            c=0
            for j in range(len(accum)):
                if accum[j] == i:
                    c = c+1
            dens.append(c)
        return dens

    def convnum(self,gaplength = 3):
        timelist = []
        timedif = []
        for i in range(len(self.current)):
            temp = self.current[i]
            temphour = int(temp.strftime("%H"))
            tempmin = int(temp.strftime("%M"))
            tempnum = 100*temphour + tempmin
            timelist.append(tempnum)
        for i in range(len(timelist) - 1):
            tempdif = timelist[i+1] - timelist[i]
            timedif.append(tempdif)
        convno=1
        for i in range(len(timedif)):
            if timedif[i] >= gaplength:
                convno = convno + 1
        return convno

    def weirdtimes(self):
        intlist, timelist = [], []
        for i in range(len(self.first)):
            temp = self.first[i]
            intlist.append(int(temp.strftime("%H")))
        for i in range(len(intlist)):
            if intlist[i] <= 5:
                timelist.append(intlist[i])
        timelist = list(dict(timelist))
        return timelist

    #Either is 0 or -1
    def avg(self, either):
        temp = []
        if len(self.first) >=1:
            temp.append(self.first)
        if len(self.second) >=1:
            temp.append(self.second)
        if len(self.third) >=1:
            temp.append(self.third)
        if len(self.forth) >=1:
            temp.append(self.forth)
        if len(self.fifth) >=1:
            temp.append(self.fifth)

        avg = 0
        for i in range(len(temp)):
            time = temp[i]
            inttime = int(time[either].strftime("%H"))
            if inttime <= 5:
                inttime = 0
            avg = avg + inttime

        return avg//len(temp)

    def weeklyconvocompare(self):
        weekly = []
        self.current = self.first
        temp = self.convnum()
        weekly.append(temp)
        self.current = self.second
        temp = self.convnum()
        weekly.append(temp)
        self.current = self.third
        temp = self.convnum()
        weekly.append(temp)
        self.current = self.forth
        temp = self.convnum()
        weekly.append(temp)
        self.current = self.fifth
        temp = self.convnum()
        weekly.append(temp)
        self.current = self.first
        return weekly

    def avgmood(self, mooddata):
        tempmood = []
        for i in len(mooddata):
            if mooddata[i] != 0:
                tempmood.append(mooddata[i])
        avg = sum(tempmood)/len(tempmood)
        newavg = "{0:.2f}".format(avg)
        return newavg



    def analysis(self, timefile, user_name, mooddata):
        self.receive(timefile)
        timedens = self.timedens() #List of 24 elements, the number of convos per hour
        weeklycon = self.weeklyconvocompare() #List of 5 elements, the number of convos per day
        weird = self.weirdtimes() #If woken at weird times, can be an empty list
        avgtime = [self.avg(0), self.avg(-1)] #List of 2 elements, average first chat and average last chat, over past 5 days
        output= str("Here is your daily update for {}. \nThey interacted with Hacker throughout the day, this is when they liked to do so,\n").format(user_name)
        for i in range(len(timedens)):
            if timedens[i] != 0:
                output += str("After {}am they conversed {} times,\n").format(i, timedens[i])
        output += str("Over the past few days, they've ")
        if not self.second:
            output += str("started to get to know Hacker well")
        else:
            output += str("talked to Hacker quite a lot! Heres the numbers, \nYesterday they chatted {} times, \n2 days ago they chatted {} times, \n").format(weeklycon[0], weeklycon[1])
        if len(self.third) >=1:
            output += str("3 days ago they chatted {} times, \n").format(weeklycon[2])
        if len(self.forth) >= 1:
            output += str("4 days ago they chatted {} times, \n").format(weeklycon[3])
        if len(self.fifth) >= 1:
            output += str("5 days ago they chatted {} times. \n ").format(weeklycon[4])

        if not weird:
            output += str("We are also glad to tell you that {} did not talk to Hacker at any odd times! \n").format(user_name)
        else:
            output += str("Unfortunatly, {} woke up at {} am last night, and chatted to Hacker. You might want to check up on them!").format(user_name, weird[0])
        output += str("Over the past 5 days, on average, {} first talks to Hacker at").format(user_name)
        if avgtime[0] <= 12:
            output += str(" {} am").format(avgtime[0])
        else:
            output += str(" {} pm").format(avgtime[0])
        output += str(" and their last conversion is at")
        if avgtime[1] <= 12:
            output += str(" {} am.").format(int(avgtime[1]))
        else:
            output += str(" {} pm. ").format(int(avgtime[1])-12)
        output += str("We hope you're enjoying the service, if you have any feedback please reply to this text!")
        mood = self.avgmood(mooddata)
        if mood <= 4:
            text = str("It doesn't look like {} had the best day yesterday. We recommend you check up with them, but hopefully you might understand why by clicking the following link. www.hackerthehuskey.tech").format(user_name)
        else:
            text = str("It looks like {} had a pretty good day yesterday, click the following link to understand more. www.hackerthehuskey.tech").format(user_name)
        return output, text
