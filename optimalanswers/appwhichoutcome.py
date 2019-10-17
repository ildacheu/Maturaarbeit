import tictactoewhichoutcome
import neat
import pickle
import random
import heapq
import numpy as np
import os
import visualize



def decision_nnn(nnOutput, fieldX, fieldO):
    ter = nnOutput.index(max(nnOutput)) + 1
    if ter in fieldX or ter in fieldO:
        ret = heapq.nlargest(11, nnOutput)

        for w in range(9):
            tur = nnOutput.index(ret[w]) + 1
            if not tur in fieldX:
                if not tur in fieldO:
                    return str(tur)
    return str(ter)

def return_pos(fieldX, fieldO):
        posarray =[0,0,0,0,0,0,0,0,0]
        for g in fieldO:
            if not g == 0:
                s = g - 1
                posarray[s] = 1
        for w in fieldX:
            if not w == 0:
                s = w - 1
                posarray[s] = -1
        return posarray

def decision_nn(nnOutput):
    return str(nnOutput.index(max(nnOutput)) + 1)

class Worker(object):
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config


    def makenewgame(self):
        self.counter = 0
        self.moves = 0
        self.start = 2 #random.randint(1, 2)
        self.fieldX = [0,0,0,0,0,0,0,0,0,0,0]
        self.fieldO = [0,0,0,0,0,0,0,0,0,0,0]
        self.posarray = [0,0,0,0,0,0,0,0,0]
        self.dict = { "field1" : "  ", "field2" : "  ", "field3" : "  ", "field4" : "  ","field5" : "  ","field6" : "  ","field7" : "  ","field8" : "  ","field9" : "  "}

    def return_values(self):
        self.start = self.game.start
        self.moves = self.game.moves
        self.fieldX = self.game.fieldX
        self.fieldO = self.game.fieldO
        self.dict = self.game.dict

    def work(self):


        net = neat.nn.recurrent.RecurrentNetwork.create(self.genome, self.config)
        self.makenewgame()
        current_max_fitness = 0
        gamenumber = 0
        done = False
        owin = 0
        xwin = 0
        tie = 0
        stops = 0
        self.game = tictactoewhichoutcome.game()

        while not done:

            if self.start % 2 and not self.game.win(self.moves, self.fieldX, self.fieldO):
                nnOutput = net.activate(self.posarray)
                #print(nnOutput)
                self.game.tictactoeX(decision_nnn(nnOutput, self.fieldX, self.fieldO), self.start , self.moves,
                self.fieldX, self.fieldO, self.dict)

                current_max_fitness = current_max_fitness + self.game.fit
                self.return_values()

            if not self.start % 2 and not self.game.win(self.moves, self.fieldX, self.fieldO):

                self.game.tictactoeO(self.start , self.moves,
                self.fieldX, self.fieldO, self.dict)

                self.posarray = return_pos(self.fieldX, self.fieldO)
                self.return_values()

            if self.game.fit == 0:
                current_max_fitness = current_max_fitness - 100
                gamenumber += 1
                self.makenewgame()

            if self.game.win(self.moves, self.fieldX, self.fieldO):
                outcome = self.game.fintessp
                if outcome == 'owin':
                    owin += 1
                if outcome == 'xwin':
                    xwin += 1
                if outcome == 'tie':
                    tie += 1
                if outcome == 'not':
                    stops += 1
                gamenumber += 1
                self.makenewgame()

            if gamenumber == 10000:
                print('stops :', stops, 'owin :', owin, 'xwin :', xwin, 'tie : ', tie)
                done = True

        #return current_max_fitness

with open('winner.pkl', 'rb') as input_file:
    genome = pickle.load(input_file)
    print('\nBest genome:\n{!s}'.format(genome))

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'config-feedforward')

worky = Worker(genome, config)
worky.work()



