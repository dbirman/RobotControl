# Dash will turn to the sound he hears and then drives 40cm towards it

from robot import *
import time
import numpy as np
import random as rand

# events
# 1 - turn left 90 degrees
# 2 - turn right 90 degrees
# 3 - drive forward 10 cm
# 4 - turn lights red
# 5 - turn lights green

tprobs = np.zeros((5,5))
events = np.zeros((5,5))
loopback = 2 # how far to look back when you improve 
lr = 0.2

def updateProbs():
  # search events, anytime you find an event, increase its probability by learning rate
  for i in range(0,5):
    for j in range(0,5):
      if events[i,j]>0:
        tprobs[i,j] = tprobs[i,j] + (1-tprobs[i,j])*lr
  tprobs = np.divide(throbs,np.sum(throbs))

def now():
  int(round(time.time()*1000))

lastevent = -1
next = now()

def fireEvent(event):
  if event==0:
    dash.turn(-90)
  elif event==1:
    dash.turn(90)
  elif event==2:
    dash.drive(100)
  elif event==3:
    dash.colorAll(255,0,0,255,0,0,255,0,0)
  else:
    dash.colorAll(0,255,0,0,255,0,0,255,0)

def event():
  # if we are waiting to do something, just return
  if now() < next:
    return
  # pick a random event to perform, based on our last event, always have a 50% chance of pausing for 1 second
  if rand.random()<0.5:
    next = now() + 1000
    return
  # event
  event = -1
  if lastevent==-1:
    event = rand.randint(0,4)
  else:
    probs = tprobs[lastevent]
    sports = np.zeros(5)
    for i in range(0,5):
      sprobs[i] = np.sum(probs[:i+1])
    choice = rand.random()
    for i in range(0,5):
      if choice<sprobs[i]:
        event = i
        break
  fireEvent(event)
  lastevent = event
  next = now() + 1000

def superstitious():
  # stay alive until they press enter
  while not (sys.stdin in select.select([sys.stdin], [], [], 0)[0]):
    # check if a clap was recorded
    if dash.clap:
      dash.playBeep()
      print('Clap!')
      updateProbs()
    else:
      event()

def main():
    global dash
    dash = robot(getRobotDevice())
    print("Press {enter} to stop demo")
    superstitious()
    dash.disconnect()

ble.run_mainloop_with(main)
