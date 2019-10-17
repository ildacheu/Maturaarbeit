import os
import time
import random




waystowin = ((1,2,3),
             (4,5,6),
             (7,8,9),
             (1,4,7),
             (2,5,8),
             (3,6,9),
             (1,5,9),
             (3,5,7))

corners = ['1','3','7','9']
edges = ['2','4','6','8']

class game:
    def __init__(self):
        global fieldX, fieldO, dict
        #self.decison_AI = decision_AI

    def fitness(self, r, fitnessp, fieldX, fieldO):
        fit = 0
        if fitnessp == "xwin":
            fit = 15
        if fitnessp == "owin":
            fit = -1
        if fitnessp == "tie":
            fit = 10
        if fitnessp == "not":
            fit = 0
        if fitnessp == "same":
            fit = 1
            for row in waystowin:
                if row[0] in fieldX and row[1] in fieldX:
                    if row[2] not in fieldO:
                        fit = 4
                        continue

                elif row[0] in fieldX and row[2] in fieldX:
                    if row[1] not in fieldO:
                        fit = 4
                        continue
                elif row[1] in fieldX and row[2] in fieldX:
                    if row[0] not in fieldO:
                        fit = 4
                        continue
                #else:
                    #fit = 2
                    #print("same")

            for row in waystowin:
                if row[0] in fieldO and row[1] in fieldO:
                    if row[2] not in fieldX:
                        fit = -30
                        continue
                if row[0] in fieldO and row[2] in fieldO:
                    if row[1] not in fieldX:
                        fit = -30
                        continue
                if row[1] in fieldO and row[2] in fieldO:
                    if row[0] not in fieldX :
                        fit = -30
                        continue
                #else:
                    #fit = 2

        self.fit = fit

    def reutrn_values(self, i, r, fieldX, fieldO, dict, fitnessp):
        self.start = i
        self.moves = r
        self.fieldX = fieldX
        self.fieldO = fieldO
        self.dict = dict
        self.fintessp = fitnessp

    def win(self , counter, fieldX, fieldO):
        global fitnessp
        fitnessp = ''
        for row in waystowin:
            #print(row[0], row[1], row[2])
            if row[0] in fieldX and row[1] in fieldX and row[2] in fieldX:
                fitnessp = "xwin"
                #print("X wins")
                return True

            if row[0] in fieldO and row[1] in fieldO and row[2] in fieldO:
                fitnessp = "owin"
                #print("O wins")
                return True
            else:
                fitnessp = 'same'
        if counter == 9:
            fitnessp = "tie"
            #print("That's a tie")
            return True




    def oppann(self, i, fieldX, fieldO):
        possibledecisions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        corners = ['1','3','7','9']
        decision = ''
        #print(i)
        #print(fieldX, fieldO)
        count = 0
        solutionfound = False
        if fieldX[1] == 0 and i == 2:
            decision = random.choice(corners)
            #while not solutionfound:
             #   decision = random.choice(corners)
              #  if int(decision) in fieldX or int(decision) in fieldO:
               #     corners = corners.remove(decision)
                #else:
                 #   solutionfound = True
        if not fieldX[1] == 0 and i == 2:
            if str(fieldX[1]) in corners or str(fieldX[1]) in edges:
                decision = '5'
            elif 5 in fieldX:
               decision = random.choice(corners)
        if str(fieldX[1]) in corners and str(fieldX[3]) in corners and i == 4:
            decision = random.choice(edges)
        if str(fieldO[2]) in corners and str(fieldX[3]) in edges and i == 4:
            if fieldO[2] == 1 and fieldX[3] == 2:
                decision = '7'
            if fieldO[2] == 1 and fieldX[3] == 4:
                decision = '3'
            if fieldO[2] == 1 and fieldX[3] == 8:
                decision = random.choice(['3', '7'])
            if fieldO[2] == 1 and fieldX[3] == 6:
                decision = random.choice(['3', '7'])
            if fieldO[2] == 3 and fieldX[3] == 2:
                decision = '9'
            if fieldO[2] == 3 and fieldX[3] == 6:
                decision = '1'
            if fieldO[2] == 3 and fieldX[3] == 4:
                decision = random.choice(['1', '9'])
            if fieldO[2] == 3 and fieldX[3] == 8:
                decision = random.choice(['1', '9'])
            if fieldO[2] == 9 and fieldX[3] == 6:
                decision = '7'
            if fieldO[2] == 9 and fieldX[3] == 8:
                decision = '3'
            if fieldO[2] == 9 and fieldX[3] == 4:
                decision = random.choice(['3', '7'])
            if fieldO[2] == 9 and fieldX[3] == 2:
                decision = random.choice(['3', '7'])
            if fieldO[2] == 7 and fieldX[3] == 8:
                decision = '1'
            if fieldO[2] == 7 and fieldX[3] == 4:
                decision = '9'
            if fieldO[2] == 7 and fieldX[3] == 2:
                decision = random.choice(['1', '9'])
            if fieldO[2] == 7 and fieldX[3] == 6:
                decision = random.choice(['1', '9'])
        if str(fieldO[2]) in corners and str(fieldO[4]) in corners and str(fieldX[3]) in edges and str(fieldX[5]) in edges and i == 6:
            decision = '5'
        if str(fieldX[5]) in corners and fieldX[3] == 5 and i == 6:
            for qw in corners:
                if int(qw) not in fieldX and int(qw) not in fieldO:
                    decision = qw
        if str(fieldX[1]) in edges and str(fieldX[3]) in edges and i == 4:
            decision = random.choice(corners)

        if str(fieldO[2]) in corners and str(fieldX[3]) in corners and i == 4:
            corners.remove(str(fieldO[2]))
            corners.remove(str(fieldX[3]))
            decision = random.choice(corners)

        if str(fieldO[2]) in corners and str(fieldX[3]) in corners and str(fieldO[4]) in corners and i == 6:
            corners.remove(str(fieldO[2]))
            corners.remove(str(fieldX[3]))
            corners.remove(str(fieldO[4]))
            decision = random.choice(corners)
        if fieldX[3] == 5 and i == 4:
            if fieldO[2] == 1:
                decision = '9'
            if fieldO[2] == 9:
                decision = '1'
            if fieldO[2] == 3:
                decision = '7'
            if fieldO[2] == 7:
                decision = '3'






        for row in waystowin:
            if row[0] in fieldX and row[1] in fieldX:
                if row[2] not in fieldX and row[2] not in fieldO:
                    decision = str(row[2])
            if row[0] in fieldX and row[2] in fieldX:
                if row[1] not in fieldX and row[1] not in fieldO:
                    decision = str(row[1])
            if row[1] in fieldX and row[2] in fieldX:
                if row[0] not in fieldX and row[0] not in fieldO:
                    decision = str(row[0])

        for row in waystowin:
            if row[0] in fieldO and row[1] in fieldO:
                if row[2] not in fieldO and row[2] not in fieldX:
                    decision = str(row[2])
            if row[0] in fieldO and row[2] in fieldO:
                if row[1] not in fieldX and row[1] not in fieldO:
                    decision = str(row[1])
            if row[1] in fieldO and row[2] in fieldO:
                if row[0] not in fieldX and row[0] not in fieldO:
                    decision = str(row[0])

        if decision == '':
            for tr in fieldX:
                if not tr == 0:
                    possibledecisions.remove(tr)
            for te in fieldO:
                if not te == 0:
                    possibledecisions.remove(te)
            decision = str(random.choice(possibledecisions))
        #print(decision)
        return decision



    def draw(self, decisionplayer, index, i, r, fieldX, fieldO, dict):
        integer = int(decisionplayer)
        if integer in fieldX or integer in fieldO:
            #print("You bloody idiot")
            notvalueable = "not"
            self.win(r, fieldX, fieldO)
            self.fitness(r, notvalueable, fieldX, fieldO)
            self.reutrn_values(i, r, fieldX, fieldO, dict, fitnessp)
        elif not 1 <= integer <= 9:
            print("You bloody idiot")
            self.win(r, fieldX, fieldO)
            self.fitness(r, fitnessp, fieldX, fieldO)
            self.reutrn_values(i, r, fieldX, fieldO, dict, fitnessp)
        else:
            field = "field" + decisionplayer
            dict[field] = index
            ##os.system("cls")
            # print(dict["field1"] + "¦" + dict["field2"] + "¦" + dict["field3"])
            # print("__¦__¦__")
            # print(dict["field4"] + "¦" + dict["field5"] + "¦" + dict["field6"])
            # print("__¦__¦__")
            # print(dict["field7"] + "¦" + dict["field8"] + "¦" + dict["field9"])
            # print("  ¦  ¦  ")

            if index == "X ":
                fieldX[i] = integer
            if index == "O ":
                fieldO[i] = integer
            i = i + 1
            r = r + 1
            self.win(r, fieldX, fieldO)
            self.fitness(r, fitnessp, fieldX, fieldO)
            self.reutrn_values(i, r, fieldX, fieldO, dict, fitnessp)




    def tictactoeX(self, decision_AI, i, r, fieldX, fieldO, dict):
        decisionplayer = decision_AI #input('X is playing. What field are you choosing?: ')
        self.draw(decisionplayer, "X ", i, r, fieldX, fieldO, dict)

    def tictactoeO(self, i, r, fieldX, fieldO, dict):
        decisionplayer =  self.oppann(i, fieldX, fieldO)
        #decisionplayer = input('O is playing. What field are you choosing?: ')
        self.draw(decisionplayer, "O ", i, r, fieldX, fieldO, dict)
