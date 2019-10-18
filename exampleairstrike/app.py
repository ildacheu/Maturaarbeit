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




        
ob = env.reset()
inx, iny, inc = env.observation_space.shape
        
inx = int(inx/8)
iny = int(iny/8)

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, #Konfiguration wird festgelegt.
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         'config-feedforward')

p = neat.Population(config) #Population wird erschaffen


p.add_reporter(neat.StdOutReporter(True))#Ausgabetext für Konsole mit Liste der Arten und weiteren Infos des Trainings
stats = neat.StatisticsReporter()
p.add_reporter(stats)


        
fitness_current = 0
frame = 0
frame_max = 0

with open('winner.pkl', 'rb') as input_file:
    genome = pickle.load(input_file)

net = neat.nn.recurrent.RecurrentNetwork.create(genome, config)      
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
                
            


