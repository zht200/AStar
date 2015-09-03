# Name: Zhitan Zhang
# AStar.py
# Iterative AStar.py Search of a problem space.
# Example:
# python3 AStar.py EightPuzzleWithHeuristics h_euclidean puzzle2a

import sys

if sys.argv==[''] or len(sys.argv)<4:
  print("Please enter the name of a problem template, "
        "the name of a heuristic evaluation function to use, "
        "and the name of a puzzle instance file that contains a particular initial state. ")
  print("For example: python3 AStar.py EightPuzzleWithHeuristics h_euclidean puzzle2a")
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])
  h_heuristics = Problem.HEURISTICS[sys.argv[2]]
  Puzzle = importlib.import_module(sys.argv[3])
  


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

def runAStar():
  initial_state = Puzzle.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(Problem.DESCRIBE_STATE(initial_state))
  global COUNT, BACKLINKS
  COUNT = 0
  BACKLINKS = {}
  IterativeAStar(initial_state)
  print(str(COUNT)+" states examined.")

def IterativeAStar(initial_state):
  global COUNT, BACKLINKS

  OPEN = [initial_state]
  CLOSED = []
  BACKLINKS[Problem.HASHCODE(initial_state)] = -1

  g_score = {}
  g_score[Problem.HASHCODE(initial_state)] = 0
  h_score = {}
  h_score[Problem.HASHCODE(initial_state)] = h_heuristics(initial_state)
  f_score = {}
  f_score[Problem.HASHCODE(initial_state)] = h_score[Problem.HASHCODE(initial_state)]

  while OPEN != []:
    S = OPEN[0]
    lowest_f_score = f_score[Problem.HASHCODE(S)]
    for element in OPEN:
      if f_score[Problem.HASHCODE(element)] < lowest_f_score:
        S = element
        lowest_f_score = f_score[Problem.HASHCODE(element)]

    OPEN.remove(S)
    CLOSED.append(S)

    if Problem.GOAL_TEST(S):
      print(Problem.GOAL_MESSAGE_FUNCTION(S))
      backtrace(S)
      return

    COUNT += 1
    if (COUNT % 32)==0:
       print(".",end="")
       if (COUNT % 128)==0:
         print("COUNT = "+str(COUNT))
         print("len(OPEN)="+str(len(OPEN)))
         print("len(CLOSED)="+str(len(CLOSED)))

    tentative_shorter = False
    for op in Problem.OPERATORS:
      if op.precond(S):
        new_state = op.state_transf(S)
        if not occurs_in(new_state, CLOSED):
          tentative_g_score = g_score[Problem.HASHCODE(S)] + 1 #takes 1 move to the new state
          if new_state not in OPEN:
            OPEN.append(new_state)
            tentative_shorter = True
          elif tentative_g_score < g_score[Problem.HASHCODE(new_state)]:
            tentative_shorter = True
          if tentative_shorter:
            BACKLINKS[Problem.HASHCODE(new_state)] = S
            g_score[Problem.HASHCODE(new_state)] = tentative_g_score
            h_score[Problem.HASHCODE(new_state)] = h_heuristics(new_state)
            f_score[Problem.HASHCODE(new_state)] = g_score[Problem.HASHCODE(new_state)] + h_score[Problem.HASHCODE(new_state)]

def backtrace(S):
  global BACKLINKS

  path = []
  while not S == -1:
    path.append(S)
    S = BACKLINKS[Problem.HASHCODE(S)]
  path.reverse()
  print("Solution path: ")
  for s in path:
    print(Problem.DESCRIBE_STATE(s))
  return path    
  

def occurs_in(s1, lst):
  for s2 in lst:
    if Problem.DEEP_EQUALS(s1, s2): return True
  return False

if __name__=='__main__':
  runAStar()

