# Name: Zhitan Zhang
# EightPuzzleWithHeuristics.py

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Eight Puzzle with Heuristics"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Z. Zhang']
PROBLEM_CREATION_DATE = "19-APR-2015"
PROBLEM_DESC=\
'''This formulation of the Eight Puzzle with Heuristics problem uses generic
Python 3 constructs and has been tested with Python 3.4.
It is designed to work according to the QUIET tools interface.
'''
#</METADATA>

#<COMMON_CODE>
def DEEP_EQUALS(s1,s2):
  for i in range(len(s1)):
    if not s1[i] == s2[i]:
        return False
  return True

def DESCRIBE_STATE(state):
  return "\n" + str(state) + "\n"

def HASHCODE(s):
  return str(s)

def copy_state(s):
  return s[:]

def can_move(s,From,To):
  try:
   if s[To] == 0:
       return True
   return False
  except (Exception) as e:
   print(e)

def move(s,From,To):
  news = copy_state(s) # start with a deep copy.
  temp = news[From]
  news[From] = news[To]
  news[To] = temp
  return news # return new state

def goal_test(s):
  for i in range(len(s)):
    if not s[i] == i:
      return False
  return True

def goal_message(s):
  return "The Puzzle Transport is Triumphant!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

import math
'''euclidean_distance is a dictionary with 
    all possible combinations of two tile positions as keys and 
	corresponding euclidean distances as values.'''
euclidean_distance = {(0,1):1,(0,2):2,(0,3):1,(0,4):math.sqrt(2),(0,5):math.sqrt(5),(0,6):2,(0,7):math.sqrt(5),(0,8):math.sqrt(8),
            (1,2):1,(1,3):math.sqrt(2),(1,4):1,(1,5):math.sqrt(2),(1,6):math.sqrt(5),(1,7):2,(1,8):math.sqrt(5),
            (2,3):math.sqrt(5),(2,4):math.sqrt(2),(2,5):1,(2,6):math.sqrt(8),(2,7):math.sqrt(5),(2,8):2,(3,4):1,(3,5):2,
            (3,6):1,(3,7):math.sqrt(2),(3,8):math.sqrt(5),(4,5):1,(4,6):math.sqrt(2),(4,7):1,(4,8):math.sqrt(2),
            (5,6):math.sqrt(5),(5,7):math.sqrt(2),(5,8):1,(6,7):1,(6,8):2,(7,8):1}
def h_euclidean(s):
  global euclidean_distance
  distance = 0
  for i in range(len(s)):
    if not i == s[i]:
      if (i,s[i]) in euclidean_distance.keys():
        distance += euclidean_distance[(i,s[i])]
      else: #if (a,b) not in keys, then (b,a) must in the keys
        distance += euclidean_distance[(s[i],i)]
  return distance

def h_hamming(s):
  number = 0
  for i in range(len(s)):
    if not i == s[i]:
      number += 1
  return number

'''column_distance is a dictionary with 
    all possible combinations of two tile positions as keys and 
	corresponding column distances as values.'''
column_distance = {(0,1):1,(0,2):2,(0,3):0,(0,4):1,(0,5):2,(0,6):0,(0,7):1,(0,8):2,
            (1,2):1,(1,3):1,(1,4):0,(1,5):1,(1,6):1,(1,7):0,(1,8):1,
            (2,3):2,(2,4):1,(2,5):0,(2,6):2,(2,7):1,(2,8):0,(3,4):1,(3,5):2,
            (3,6):0,(3,7):1,(3,8):2,(4,5):1,(4,6):1,(4,7):0,(4,8):1,
            (5,6):2,(5,7):1,(5,8):0,(6,7):1,(6,8):2,(7,8):1}
'''row_distance is a dictionary with 
    all possible combinations of two tile positions as keys and 
	corresponding row distances as values.'''
row_distance = {(0,1):0,(0,2):0,(0,3):1,(0,4):1,(0,5):1,(0,6):2,(0,7):2,(0,8):2,
            (1,2):0,(1,3):1,(1,4):1,(1,5):1,(1,6):2,(1,7):2,(1,8):2,
            (2,3):1,(2,4):1,(2,5):1,(2,6):2,(2,7):2,(2,8):2,(3,4):0,(3,5):0,
            (3,6):1,(3,7):1,(3,8):1,(4,5):0,(4,6):1,(4,7):1,(4,8):1,
            (5,6):1,(5,7):1,(5,8):1,(6,7):0,(6,8):0,(7,8):0}
def h_manhattan(s):
  distance = 0
  for i in range(len(s)):
    if not i == s[i]:
      if (i,s[i]) in column_distance.keys():
        distance += column_distance[(i,s[i])]
      else: #if (a,b) not in keys, then (b,a) must in the keys
        distance += column_distance[(s[i],i)]
      if (i,s[i]) in row_distance.keys():
        distance += row_distance[(i,s[i])]
      else: #if (a,b) not in keys, then (b,a) must in the keys
        distance += row_distance[(s[i],i)]
  return distance
#</COMMON_CODE>

#<OPERATORS>
puzzle_combinations = [(0,1),(0,3),(1,0),(1,4),(1,2),(2,1),(2,5),(3,0),(3,4),(3,6),(4,1),(4,3),(4,7),(4,5),(5,2),(5,4),
                       (5,8),(6,3),(6,7),(7,6),(7,4),(7,8),(8,7),(8,5)]
OPERATORS = [Operator("Move puzzle from "+str(p)+" to "+str(q),
                      lambda s,p=p,q=q: can_move(s,p,q),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p=p,q=q: move(s,p,q) )
             for (p,q) in puzzle_combinations]
#</OPERATORS>

#<GOAL_TEST>
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION>
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if 'BRYTHON' in globals():
 from EightPuzzleWithHeuristicsVisForBrython import set_up_gui as set_up_user_interface
 from EightPuzzleWithHeuristicsVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from EightPuzzleWithHeuristicsVisForTKINTER import set_up_gui
#</STATE_VIS>

HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming':h_hamming, 'h_manhattan':h_manhattan}