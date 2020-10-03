import numpy as np

#Trade based on predictions of price movement.
#The strategy is simplistic.
#At any given point one holds either all stock or all cash.
def trade(pred,price):

 npreds = len(pred)   
# print('\nnpreds     = ',npreds)
# print('\nlen(price) = ',len(price)) 

 cash  = np.empty([npreds],float)
 stock = np.empty([npreds],float)

 cash[:]  = -99999999.0
 stock[:] = -99999999.0

# A trade is triggered only if prediction changes sign (UP to DW or DW to UP)
# If the last prediction is same, one holds the position.
 
 for i in np.arange(npreds):
  #The first trade - either buy one stock or hold equivalent value in cash
  if i==0:
   if pred[i]=='UP':
    cash[i] = 0.0
    stock[i] = 1.0
    investment =  price[i]
   else:  
    cash[i]  = price[i]
    stock[i] = 0.0
    investment = price[i]     
  else:
   if pred[i]=='UP':
    if pred[i-1]=='DW':    #if cash[i-1]>0.0:
     cash[i] = 0.0
     stock[i] = cash[i-1]/price[i]
    else: 
     cash[i]  = cash[i-1]   #HOLD
     stock[i] = stock[i-1]    
   else:
    if pred[i-1]=='UP':     #if stock[i-1]>0.0:
     cash[i]  = stock[i-1]*price[i]
     stock[i] = 0.0
    else: 
     cash[i]  = cash[i-1]  #HOLD
     stock[i] = stock[i-1]

 return investment,stock,cash     
    

#For a model sum up profit/loss from each prediction
#Return this gradient metric
def magnitude_move(pred,true_move,move_magn):

 npreds = len(pred)   
# print('\nnpreds     = ',npreds)

 sum_magn = 0

 hitmiss = []
 
 for i in np.arange(npreds):
  if true_move[i] == pred[i] :
    sum_magn += np.abs(move_magn[i])
    hitmiss.append('CORRECT')
  else:
    sum_magn -= np.abs(move_magn[i])
    hitmiss.append('WRONG')

 return(hitmiss,sum_magn)
