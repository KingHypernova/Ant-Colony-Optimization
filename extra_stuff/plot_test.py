# had this problem - https://stackoverflow.com/questions/19341365/setting-two-arrays-equal

import antLib as a
import numpy as np
import random as r
import time
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib.animation as animation

def get_set_ants(ant_color, hasFood_color, master, ant, antInfo):
  x = antInfo[ant][0]
  y = antInfo[ant][1]
  hasFood = antInfo[ant][3]
  if hasFood == False:    # If no food, ant is black
    return ant_color
  elif hasFood == True:   # if has food, ant is food color
    return hasFood_color

def get_set_pheromone(pheromone):  #map all pher vals to 0<p<= max_color
  make_min_cond = pheromone<0.1
  im_too_small = make_min_cond.any() 
  all_same = (pheromone[:][:]==pheromone[X-1][Y-1]).all()
  minimum = np.amin(pheromone)
  if (all_same == False) and (im_too_small == True):    # after succes, makes ant random walk when it looks like there's no pheromone (otherwise it folows the now invisible path it took to drop food off at nest)
    pheromone[:][:] = a.find_n_replace_with(pheromone,make_min_cond,minimum)
  return pheromone[:][:]

def get_set_food(foodColor, xFood, yFood, foodSize):
  if foodSize > 0:
    master[yFood][xFood] = foodColor
  elif foodSize == 0:
    master[yFood][xFood] = white
  return master[yFood][xFood]

def get_set_all(pheromone, matrix, max_color, black, green, ant, antInfo, xFood, yFood):
  matrix = get_set_pheromone(pheromone, matrix, max_color)
  #matrix = get_set_food(green, matrix, print('pheromone 3--- ' , pheromone)xFood, yFood)
  #matrix = get_set_ants(black, green, matrix, ant, antInfo)
  return matrix

def debugNeg(ant, antInfo):
  x = antInfo[ant][0]
  y = antInfo[ant][1]
  if x<0 or y<0:
    print("I WENT OUT OF BOUNDS FUCK ME")
    exit() 

#=============World data initialization==============
global numAnts, timeData, choiceArray, foodSize
timeData = np.array([[0,0,0,0,0,0,0]])         #remove first(this) row later

numAnts = 10        #int(sys.argv[1])
foodSize = 10

global X, Y, xFood, yFood, nestX, nestY
X = 10            #int(sys.argv[2]) #increments of 5 (food placement)  # X size of world  **Recall array elements will be [0,4]
Y = 10            #int(sys.argv[3]) # Y size of world
xFood = int(X*(4/5))
yFood = int(Y*(4/5))
nestX = 0                 #for parts of the program to reference, cant change this here
nestY = 0

decayRateMult = .9             # pheromone decay rate
decayRateSub = .02
randPher = 1.             # how much pheromone an ant lays
foodPher = 10.
foodWeight = 100          # treat adjacent food as a super strong weighting factor , to be considered (added) to pheromone level
homingWeight = 10000

#===========Color stuff==============
black_rgba = (0.0, 0.0, 0.0, 1.0)
green_rgba = (0.0, 230./256., 64./256., 1.0)
cmap, ant_cmap = a.create_ant_cmap(black_rgba, green_rgba)

global black, green, max_color
white = 0.0
max_color = (1.0 - 2./cmap.N - 0.00000001)*foodPher    # max color value
min_green = (1.0 - 2./cmap.N)*foodPher 
green = (1.0 - 1.5/cmap.N)*foodPher 
max_green = (1.0 - 1./cmap.N - 0.00000001)*foodPher 
min_black = (1.0 - 1./cmap.N)*foodPher 
black = foodPher 
#========GENERATE WORLD==========
#global antTime, antInfo, foodMap
antTime = 0
antInfo = a.generateAnts(numAnts)
foodMap = a.generateFoodMap(X,Y,xFood,yFood,foodSize)
pheromone = a.generatePheromoneMap(X,Y,1.0)
master = np.zeros((X,Y))              # intialize master array
#======================================================

plt.ion()

get_set_food(green, xFood, yFood,foodSize)
master[0][0] = get_set_ants(black, green, master, 0, antInfo)

fig = plt.subplot(131)
master_obj = fig.matshow(master, cmap=ant_cmap, vmin=0.0, vmax=foodPher)

ax = plt.subplot(132)
fig.colorbar(master_obj)

graph = plt.subplot(133)
graph.plot([1,2,3],[1,2,3])

plt.pause(.001)

i=0
while antTime<100000:

  for ant in range(numAnts):

    options = a.generateOptionArray(ant,antInfo,X,Y,homingWeight, antTime)
    choice = a.choose(options, ant, antInfo)      # normalize Roll Biased Die
    a.updatePosition(ant,antInfo,choice)
    foodSize = a.checkIfHasFood(ant,antInfo,xFood,yFood,foodSize)
    pheromone[:][:] = a.layPheromone(ant,randPher,foodPher,antInfo,pheromone,max_color)
    a.checkIfSuccess(ant,antInfo,antTime,timeData,nestX,nestY)

  pheromone[:][:] = a.reducePheromoneMult(pheromone,decayRateMult)
  master[:][:] = get_set_pheromone(pheromone)
  master[yFood][xFood] = get_set_food(green,xFood,yFood,foodSize)     # color the food
  for i in range(numAnts):
    master[antInfo[i][1]][antInfo[i][0]] = get_set_ants(black, green, master, i, antInfo)
  antTime+=1

  master_obj.set_data(master)
  plt.draw()
  plt.pause(.001)

plt.ioff()    
plt.show()
