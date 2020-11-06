import numpy as np
import random as r

np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

def same_array(a1,a2):
  print(a1==a2)
  print(np.all(a1==a2))

def find_n_replace_with(array,condition_on_array,number):
  result_y , result_x = np.where(condition_on_array)
  for i in range(len(result_y)):
    array[result_y[i]][result_x[i]] = number
  return array

q = np.random.rand(3,3) * 2 - 1.0
#print(q)
'''
cond = q<-0.0
a = 333

result_y , result_x = np.where(cond)
#print(result_y, result_x)
for i in range(len(result_y)):
  q[result_y[i]][result_x[i]] = a

#print(q)
#print(index_list)
q = find_n_replace_with(q,cond,a)

#print(q)
'''
rando = r.uniform(.001,.01)
#print(rando)
print(q)

#find_n_replace_with(q,q<0.5,)
#np.where(np.amin(q)==True):