import retro
import numpy as np
import cv2 
import neat
import pickle
#import os

env = retro.make(game='Airstriker-Genesis')#Spiel wird geladen

def get_image(inx, iny, ob):
    env.render()
    ob = cv2.resize(ob, (inx, iny))
    ob = cv2.cvtColor(ob, cv2.COLOR_BGR2GRAY)
    return ob

def img_flatten(ob):
    imgarray = np.ndarray.flatten(ob)
    return imgarray

def get_action(nnOutput):
    action = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    action[0] = nnOutput[0]
    action[6] = nnOutput[1]
    action[7] = nnOutput[2]
    return action


def eval_genomes(genomes, config):
    
##  In der Funktion eval_genomes(genomes, config)werden die KNNs angewendet.
##  Die Funktion braucht zwei Argumente genomes, config.
##  Das erste Argument genomes ist eine Liste aller Individuen der aktuellen Population
##  und das zweite Argument config ist die Konfiguration,
##  welche in der Strukturdatei festgelegt wurde.

    for genome_id, genome in genomes:
        
        ob = env.reset()
        inx, iny, inc = env.observation_space.shape
        
        inx = int(inx/8)
        iny = int(iny/8)

        net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        
        fitness_current = 0
        frame = 0
        frame_max = 0
        
        done = False
        
        while not done:
    
            image = get_image(inx, iny, ob)
            imgarray = img_flatten(image)
            
            nnOutput = net.activate(imgarray)
    
            action = get_action(nnOutput)
            ob, rew, done, info = env.step(action)

            frame += 1
            
            if frame > frame_max:
                fitness_current += 1
                frame_max = frame            
            if info['lives'] == 2:
                done = True
                print(fitness_current)
                frame = 0
            genome.fitness = fitness_current
                
            
   

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, #Konfiguration wird festgelegt.
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')

p = neat.Population(config) #Population wird erschaffen


p.add_reporter(neat.StdOutReporter(True))#Ausgabetext für Konsole mit Liste der Arten und weiteren Infos des Trainings
stats = neat.StatisticsReporter()
p.add_reporter(stats)

p.add_reporter(neat.Checkpointer(10))#Backup wird jede 10. Generation erschaffen.

winner = p.run(eval_genomes)


with open('winner.pkl', 'wb') as output:#Jedes Output welches vom besten KNN errechnet wurde, wird gespeichert. So kann das Spiel des besten KNN rekonstruiert werden.
        pickle.dump(winner, output, 1)


