import numpy as np
import random as r
import time
from matplotlib import pyplot as plt
import matplotlib.colors as mplc

np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
#==============functions go here===================
def generateAnts(numAnts):               #WORKS!    # creates global antInfo array 
  global antInfo                                    # stores all info ant needs to make next decision, based on prev decision                                 # (current x,y , last x,y , hasFood?)
  antInfo = np.zeros((numAnts,7), dtype = int)      # (0,1 = current x,y ;2 = last (vacant);3 = hasFood? ;4 = success? ;5 = time;6 = ant)
  return antInfo
#==================================================
def generateFoodMap(X,Y,xFood,yFood,foodSize):    #WORKS!       # creates food map, same size as pheromone map, also places food at a random point in food map
  global foodMap
  foodMap = np.zeros([X,Y])
  #r.seed(randomSeed)							    # if dont want it to be random, assign x and y index to food position OR implement seed
  #randXindex = int(round((X-1)*r.random()))		    # random() = [0,1)
  #randYindex = int(round((Y-1)*r.random()))
  foodMap[yFood][xFood] = foodSize
  return foodMap
#==================================================
def generatePheromoneMap(X,Y,start_color):           #WORKS!    #intializes pheromone map to zeros
  global pheromone
  pheromone = np.full([X,Y],start_color)              #small value rrather than zeros saved a lot of headaches (dividing by zero when normalizing). still "equal playing field"
  #pheromone[1][0] = r.random() * 0.1   #E       
  #pheromone[1][1] = r.random() * 0.1   #S        #otherwise I divide by 0 if no adjacent pheromone
  #pheromone[0][1] = r.random() * 0.1   #SE
  return pheromone
#==================================================
def layPheromone(ant,randPher,foodPher,antInfo,pheromone,max_color): #WORKS!  #@ ants new position, add pheromone value p to exisitng pheromone amount
  newX = antInfo[ant][0]
  newY = antInfo[ant][1]
  hasFood = antInfo[ant][3]
  make_max_color_if = pheromone>max_color
  im_too_big = make_max_color_if.any()
  if(hasFood==False):
    pheromone[:][:]
    #pheromone[newY][newX] = pheromone[newY][newX] + randPher #array indices are array[y][x] <------> (x,y) (see notes)
  elif(hasFood==True):
    pheromone[newY][newX] = pheromone[newY][newX] + foodPher
  if (im_too_big == True):
    pheromone[:][:] = find_n_replace_with(pheromone,make_max_color_if,max_color)
  return pheromone[:][:]
#==================================================
def addTime(ant,antInfo):          #works
	antInfo[ant][5] += 1
#==================================================
def find_n_replace_with(array,condition_on_array,number):
  result_y , result_x = np.where(condition_on_array)
  for i in range(len(result_y)):
    array[result_y[i]][result_x[i]] = number
  return array[:][:]
#==================================================
#==================================================
'''
def reducePheromoneSub(pheromone,cond,decayRateSub):       # What it does - reduces the pheromone level by multiplying the previous level by p=[0,1]
  has_neg = (pheromone<0).any()
  all_pos = (pheromone>0).all()
  all_zeros = (pheromone==0).all()
  too_small = (pheromone<decayRateSub).any()
  minimum = np.amin(pheromone)
  num = 0.03
  if all_pos == True:
    return pheromone[:][:] - decayRateSub 
  elif too_small==True:
    return find_n_replace_with(pheromone,pheromone<decayRateSub,num)
  elif all_zeros == True:
    return pheromone.fill(num)
  elif has_neg == True:
    pheromone[:][:] = pheromone - decayRateSub
    return find_n_replace_with(pheromone,cond,num)
'''
#==================================================
def reducePheromoneMult(pheromone, decayRate):
  return pheromone*decayRate
#==================================================
def normalizeMe(array, ant, antInfo):                 # Works!
  lastMove = antInfo[ant][2]
  array[lastMove] = 0.0								  # don't backtrack, instead of more complicated backtrack-dampening function
  normalized = array/sum(array)
  if ((array==0).all())==True:
  	array
  else:
    return normalized                                 
#==================================================
def leftWall(X,Y,xNow,yNow):            #WORKS!     # returns true is (xNow,yNow) is on left wall, not a corner
  return ( xNow==0 and (yNow!=0 and yNow!=(Y-1)) )
def rightWall(X,Y,xNow,yNow):           #WORKS!
  return ( xNow==(X-1) and (yNow!=0 and yNow!=(Y-1)) )
def topWall(X,Y,xNow,yNow):             #WORKS!
  return ( yNow==0 and (xNow!=0 and xNow!=(X-1)) )
def bottomWall(X,Y,xNow,yNow):          #WORKS!
  return ( yNow==(Y-1) and (xNow!=0 and xNow!=(X-1)) )
def isWall(l,r,t,b):
  return (l or r or t or b)
#==================================================
def generateWallOptionArray(x,y,t,r,b,l):     # WORKS! --- generates choicepheromone[yFood][xFood]Array when ant is on near wall, but not corner
  choiceArray = np.zeros(8,dtype = float)
  if(t==True):    #spots 0,1,2 == 0.
    choiceArray[0] = 0.  #NW
    choiceArray[1] = 0.  #N
    choiceArray[2] = 0.  #NE
    choiceArray[3] = pheromone[y][x-1] + foodMap[y][x-1]      #W
    choiceArray[4] = pheromone[y][x+1] + foodMap[y][x+1]      #E
    choiceArray[5] = pheromone[y+1][x-1] + foodMap[y+1][x-1]  #SW
    choiceArray[6] = pheromone[y+1][x] + foodMap[y+1][x]      #S
    choiceArray[7] = pheromone[y+1][x+1] + foodMap[y+1][x+1]  #SE
  if(r==True):    #spots 2,4,7 == 0.
    choiceArray[0] = pheromone[y-1][x-1] + foodMap[y-1][x-1]  #NW
    choiceArray[1] = pheromone[y-1][x] + foodMap[y-1][x]      #N
    choiceArray[2] = 0.  #NE
    choiceArray[3] = pheromone[y][x-1] + foodMap[y][x-1]      #W
    choiceArray[4] = 0.  #E
    choiceArray[5] = pheromone[y+1][x-1] + foodMap[y+1][x-1]  #SW
    choiceArray[6] = pheromone[y+1][x] + foodMap[y+1][x]  #S
    choiceArray[7] = 0.  #SE
  if(b==True):    #spots 5,6,7 == 0.
    choiceArray[0] = pheromone[y-1][x-1] + foodMap[y-1][x-1]  #NW
    choiceArray[1] = pheromone[y-1][x] + foodMap[y-1][x]      #N
    choiceArray[2] = pheromone[y-1][x+1] + foodMap[y-1][x+1]  #NE
    choiceArray[3] = pheromone[y][x-1] + foodMap[y][x-1]      #W
    choiceArray[4] = pheromone[y][x+1] + foodMap[y][x+1]      #E
    choiceArray[5] = 0.  #SW
    choiceArray[6] = 0.  #S
    choiceArray[7] = 0.  #SE
  if(l==True):    #spots 0,3,5 == 0.
    choiceArray[0] = 0.  #NW
    choiceArray[1] = pheromone[y-1][x] + foodMap[y-1][x]      #N
    choiceArray[2] = pheromone[y-1][x+1] + foodMap[y-1][x+1]  #NE
    choiceArray[3] = 0.  #W
    choiceArray[4] = pheromone[y][x+1] + foodMap[y][x+1]      #E
    choiceArray[5] = 0.  #SW
    choiceArray[6] = pheromone[y+1][x] + foodMap[y+1][x]      #S
    choiceArray[7] = pheromone[y+1][x+1] + foodMap[y+1][x+1]  #SE
  return choiceArray
#==================================================
def ULcorner(X,Y,xNow,yNow):       # All WORK!     #UL corner
  return ( xNow==0 and yNow==0 )
def URcorner(X,Y,xNow,yNow):                       #UR corner
  return ( xNow==(X-1) and yNow==0 )
def BRcorner(X,Y,xNow,yNow):                       #BR corner
  return ( xNow==(X-1) and yNow==(Y-1) )
def BLcorner(X,Y,xNow,yNow):                       #BL corner
  return ( xNow==0 and yNow==(Y-1) )
def isCorner(UL,UR,BR,BL):            # WORKS!     #returns true if (xNow,yNow) is corner
  return ( UL or UR or BR or BL )     
#==================================================
def generateCornerOptionArray(x,y,UL,UR,BR,BL,antTime):   #WORKS!     #ARGUMENT ORDER MATTERS --- does what it says
  choiceArray = np.zeros(8,dtype = float)                 
  if(UL==True):          # 1st move
  	choiceArray[0] = 0.  #NW
  	choiceArray[1] = 0.  #N
  	choiceArray[2] = 0.  #NE
  	choiceArray[3] = 0.  #W
  	choiceArray[4] = pheromone[y][x+1] + foodMap[y][x+1]       #E
  	choiceArray[5] = 0.  #SW
  	choiceArray[6] = pheromone[y+1][x] + foodMap[y+1][x]       #S
  	choiceArray[7] = pheromone[y+1][x+1] + foodMap[y+1][x+1]   #SE
  if(UR==True):
    choiceArray[0] = 0.  #NW
    choiceArray[1] = 0.  #N
    choiceArray[2] = 0.  #NE
    choiceArray[3] = pheromone[y][x-1] + foodMap[y][x-1]       #W
    choiceArray[4] = 0.  #E
    choiceArray[5] = pheromone[y+1][x-1] + foodMap[y+1][x-1]   #SW
    choiceArray[6] = pheromone[y+1][x] + foodMap[y+1][x]       #S
    choiceArray[7] = 0.  #SE
  if(BR==True):
    choiceArray[0] = pheromone[y-1][x-1] + foodMap[y-1][x-1]   #NW
    choiceArray[1] = pheromone[y-1][x] + foodMap[y-1][x]       #N
    choiceArray[2] = 0.  #NE
    choiceArray[3] = pheromone[y][x-1] + foodMap[y][x-1]       #W
    choiceArray[4] = 0.  #E
    choiceArray[5] = 0.  #SW
    choiceArray[6] = 0.  #S
    choiceArray[7] = 0.  #SE
  if(BL==True):
    choiceArray[0] = 0.  #NW
    choiceArray[1] = pheromone[y-1][x] + foodMap[y-1][x]       #N
    choiceArray[2] = pheromone[y-1][x+1] + foodMap[y-1][x+1]   #NE
    choiceArray[3] = 0.  #W
    choiceArray[4] = pheromone[y][x+1] + foodMap[y][x+1]       #E
    choiceArray[5] = 0.  #SW
    choiceArray[6] = 0.  #S
    choiceArray[7] = 0.  #SE
  #print(choiceArray)
  return choiceArray
#==================================================
def generateMiddleOptionArray(x,y):              #WORKS!    #generate choiceArray for ant in any midle spot          
  choiceArray = np.zeros(8,dtype = float)
  choiceArray[0] = pheromone[y-1][x-1] + foodMap[y-1][x-1]  #NW
  choiceArray[1] = pheromone[y-1][x] + foodMap[y-1][x]      #N
  choiceArray[2] = pheromone[y-1][x+1] + foodMap[y-1][x+1]  #NE
  choiceArray[3] = pheromone[y][x-1] + foodMap[y][x-1]      #W
  choiceArray[4] = pheromone[y][x+1] + foodMap[y][x+1]      #E
  choiceArray[5] = pheromone[y+1][x-1] + foodMap[y+1][x-1]  #SW
  choiceArray[6] = pheromone[y+1][x] + foodMap[y+1][x]      #S
  choiceArray[7] = pheromone[y+1][x+1] + foodMap[y+1][x+1]  #SE
  return choiceArray
#==================================================
def generateHomingOptionArray(X,Y,x,y,homingWeight):  #WORKS! #see notes
  choiceArray = np.zeros(8,dtype=float)
  if(leftWall(X,Y,x,y)==True):          #move 0 or 1 only
  	choiceArray[1] = homingWeight            #go up more likely
  	choiceArray[2] = homingWeight - 400.
  elif(topWall(X,Y,x,y)==True):         #move 0 or 3 only                       
  	choiceArray[3] = homingWeight            #go left more likely
  	choiceArray[5] = homingWeight - 400.
  else:
  	choiceArray[0] = homingWeight
  	choiceArray[1] = homingWeight - 400.
  	choiceArray[3] = homingWeight - 400.
  return choiceArray
#==================================================
def generateOptionArray(ant,antInfo,X,Y,homingWeight, antTime):  #WORKS   #generates option array for ANY ant location
  x = antInfo[ant][0]
  y = antInfo[ant][1]
  hasFood = antInfo[ant][3]
  success = antInfo[ant][4]
  UL = ULcorner(X,Y,x,y)
  UR = URcorner(X,Y,x,y)
  BR = BRcorner(X,Y,x,y)
  BL = BLcorner(X,Y,x,y)
  t = topWall(X,Y,x,y)
  b = bottomWall(X,Y,x,y)
  r = rightWall(X,Y,x,y)
  l = leftWall(X,Y,x,y)
  if(hasFood==False):
    if(isCorner(UL,UR,BR,BL)==True):
      cA = generateCornerOptionArray(x,y,UL,UR,BR,BL,antTime)
    elif(isWall(t,r,b,l)==True):
      cA = generateWallOptionArray(x,y,t,r,b,l)
    else:
      cA = generateMiddleOptionArray(x,y)
  elif(hasFood==True):
  	cA = generateHomingOptionArray(X,Y,x,y,homingWeight)
  return cA
#=================================================
def choose(options, ant, antInfo):                #WORKS!        # returns choice number
  options = normalizeMe(options, ant, antInfo)
  weights = np.zeros_like(options)
  weights[0] = options[0]
  for w in range(7):
    weights[w+1] = weights[w] + options[w+1] 
  pick = r.random()
  tempChoice = 0
  for c in range(8):
    if(pick<=weights[c]):
      tempChoice = c
      break
  return tempChoice
#=================================================
def updatePosition(ant,antInfo,choice):   # WORKS!  #based on choice, move ant, update lastMove
  x = antInfo[ant][0]
  y = antInfo[ant][1]
  if(choice==0):  #
    antInfo[ant][0] = x-1  
    antInfo[ant][1] = y-1
    antInfo[ant][2] = 7
  elif(choice==1):#
    antInfo[ant][1] = y-1
    antInfo[ant][2] = 6
  elif(choice==2):#
    antInfo[ant][0] = x+1
    antInfo[ant][1] = y-1
    antInfo[ant][2] = 5
  elif(choice==3):
    antInfo[ant][0] = x-1
    antInfo[ant][1] = y
    antInfo[ant][2] = 4
  elif(choice==4):
    antInfo[ant][0] = x+1
    antInfo[ant][2] = 3
  elif(choice==5):
    antInfo[ant][0] = x-1
    antInfo[ant][1] = y+1
    antInfo[ant][2] = 2
  elif(choice==6):
    antInfo[ant][1] = y+1
    antInfo[ant][2] = 1
  elif(choice==7):	
    antInfo[ant][0] = x+1
    antInfo[ant][1] = y+1
    antInfo[ant][2] = 0
#=================================================
def checkIfHasFood(ant,antinfo,xFood,yFood,foodSize):       #WORKS       #if hungry and on food, take food, reduce food size (on map)
  xNew = antInfo[ant][0]
  yNew = antInfo[ant][1]
  hasFood = antInfo[ant][3]
  if(xNew==xFood and yNew==yFood and hasFood==False and foodSize>0):
    antInfo[ant][3] = 1                 # hasFood == True
    foodSize -= 1 
  return foodSize
#=================================================
def checkIfSuccess(ant,antInfo,time,timeData,nestX,nestY):
  xNew = antInfo[ant][0]
  yNew = antInfo[ant][1]
  hasFood = antInfo[ant][3]
  if(xNew==nestX and yNew==nestY and hasFood==True):
    antInfo[ant][4] += 1              # success == True
    antInfo[ant][5] = time
    appendMe = np.array([antInfo[ant][:]])            #convert antInfo array to array of lists?
    timeData = np.append(timeData,appendMe,axis=0)    #record ant number and time in timeData array
    antInfo[ant][3] = 0         #deposit food and start over
  return timeData

#=================================================
#=====================visuals=====================
#=================================================

def create_ant_cmap(ant_rgba, food_rgba):   #colors are rgba tuples
  global cmap, ant_cmap
  cmap = plt.cm.Oranges             # load pyplot colorbar
  ant_rgba = ant_rgba
  food_rgba = food_rgba
  cmaplist = [cmap(i) for i in range(cmap.N)]   # iterate it into a list. cmap.N==256
  cmaplist[cmap.N-1] = ant_rgba       # redefine last list color to black
  cmaplist[cmap.N-2] = food_rgba
  ant_cmap = mplc.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, cmap.N)      # create custom cmap object
  return cmap, ant_cmap
'''
def get_set_ants(color, hasFood_color, matrix, ant, antInfo):
  x = antInfo[ant][0]
  y = antInfo[ant][1]
  hasFood = antInfo[ant][3]
  if hasFood == False:    # If no food, ant is black
    matrix[y][x] = color
    return matrix
  elif hasFood == True:   # if has food, ant is food color
    matrix[y][x] = hasFood_color
    return matrix
  return matrix

def get_set_pheromone(pheromone, matrix, max_color):  #map all pher vals to 0<p<= max_color
  if np.all(pheromone == pheromone[0]):
    matrix = pheromone
    return matrix
  else:
    maximum = np.amax(pheromone)
    pheromone = (pheromone / maximum) * max_color   # scales all pheromone values to be at most the value of max_color
    matrix = pheromone
    return matrix

def get_set_food(foodColor, matrix, xFood, yFood):
  #y = np.nonzero(foodMap)[0]    # np.nonzero returns list of arrays
  #x = np.nonzero(foodMap)[1]    # 1st num is position of array, 2nd num is index of inner-array
  matrix[yFood][xFood] = foodColor
  return matrix

def get_set_all(pheromone, matrix, max_color, black, green, ant, antInfo, xFood, yFood):
  matrix = get_set_pheromone(pheromone, matrix, max_color)
  matrix = get_set_food(green, matrix, xFood, yFood)
  matrix = get_set_ants(black, green, matrix, ant, antInfo)
  return matrix
'''