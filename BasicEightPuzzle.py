# Name: Zhitan Zhang
# BasicEightPuzzle.py
 
#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Z. Zhang']
PROBLEM_CREATION_DATE = "18-APR-2015"
PROBLEM_DESC=\
'''This formulation of the Basic Eight Puzzle problem uses generic
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
#</COMMON_CODE>
 
#<COMMON_DATA>
puzzle = [1, 0, 2, 3, 4, 5, 6, 7, 8]
#</COMMON_DATA>
 
#<INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: puzzle
#</INITIAL_STATE>
 
#<OPERATORS>
'''Puzzle_combinations:
   0 1 2
   3 4 5
   6 7 8
   For example, 
   0 can be moved to 1 or 3, 
   1 can be moved to 0 or 4 or 2, 
   2 can be moved to 1 or 5, etc.'''
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
 from BasicEightPuzzleVisForBrython import set_up_gui as set_up_user_interface
 from BasicEightPuzzleVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from BasicEightPuzzleVisForTKINTER import set_up_gui
#</STATE_VIS>