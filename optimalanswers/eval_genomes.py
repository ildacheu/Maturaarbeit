import tictactoe
import neat
import pickle
import random
import heapq
import numpy as np
import os
import visualize

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
        self.game = tictactoe.game()

        while not done:

            if self.start % 2 and not self.game.win(self.moves, self.fieldX, self.fieldO):
                nnOutput = net.activate(self.posarray)

                self.game.tictactoeX(decision_nn(nnOutput), self.start , self.moves,
                self.fieldX, self.fieldO, self.dict)

                current_max_fitness = current_max_fitness + self.game.fit
                self.return_values()

            if not self.start % 2 and not self.game.win(self.moves, self.fieldX, self.fieldO):

                self.game.tictactoeO(self.start , self.moves,
                self.fieldX, self.fieldO, self.dict)

                self.posarray = return_pos(self.fieldX, self.fieldO)
                self.return_values()

            if not self.game.fit == 0:
                current_max_fitness = current_max_fitness + 5
            else:
                gamenumber += 1
                self.makenewgame()

            if self.game.win(self.moves, self.fieldX, self.fieldO):
                gamenumber += 1
                self.makenewgame()

            if gamenumber == 1:
                done = True
        final_fitness = current_max_fitness / 30
        return final_fitness
def eval_genomes(genome, config):

    worky = Worker(genome, config)
    return worky.work()

def train(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)


    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5, filename_prefix = 'generation-'))
    pe = neat.ParallelEvaluator(4, eval_genomes)
    winner1 = p.run(pe.evaluate, 40)
    visualize.draw_net(config, winner1)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)
    with open('winner.pkl', 'wb') as output:
        pickle.dump(winner1, output)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    train(config_path)
