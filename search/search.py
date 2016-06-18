# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""


import util
from util import *
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

def prevPos(pos,move):
    
    if move=="North":
        return (pos[0],pos[1]-1)
    elif move=="South":
        return (pos[0],pos[1]+1)
    elif move=="East":
        return (pos[0]-1,pos[1])
    else:
        return (pos[0]+1,pos[1])

def actionList(lastMove,start,end):
    
    actions=[]
    node = end
    
    while node != start:
        actions.append(lastMove[node])
        node = prevPos(node,lastMove[node])
    
    actions=actions[::-1]
    n=Directions.NORTH
    s=Directions.SOUTH
    w=Directions.WEST
    e=Directions.EAST
    
    print "Length of actionList :", len(actions)
    ActionList = []
    for i in range(len(actions)): 
        if actions[i]=="North":
            ActionList.append(n)
        elif actions[i]=="South":
            ActionList.append(s)
        elif actions[i]=="West":
            ActionList.append(w)
        else:
            ActionList.append(e)
        
    return ActionList
    
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    startState = problem.getStartState()
    
    #Initializing the fringe and closed set    
    fringe = Stack()
    fringe.push((startState,[],0))    
    closedSet= []
    
    
    
    while not fringe.isEmpty():
        
        node = fringe.pop()
        

        if problem.isGoalState(node[0]):
            return node[1]
          
        
        if not node[0] in closedSet:
            for successor in problem.getSuccessors(node[0]):
                if not successor[0] in closedSet:
                    newSuccessor = (successor[0],node[1]+[successor[1]],successor[2])
                    fringe.push(newSuccessor)
            closedSet.append(node[0])

    
    return []


    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    startState = problem.getStartState()
    
    #Initializing the fringe and closed set    
    fringe = Queue()
    fringe.push((startState,[],0))    
    closedSet= []
    
    
    
    while not fringe.isEmpty():
        
        node = fringe.pop()
        

        if problem.isGoalState(node[0]):
            return node[1]
          
            
        if not node[0] in closedSet:
            for successor in problem.getSuccessors(node[0]):
                if not successor[0] in closedSet:
                    newSuccessor = (successor[0],node[1]+[successor[1]],successor[2])
                    fringe.push(newSuccessor)
            closedSet.append(node[0])

    return []
   

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    
    #Initializing the fringe and closed set    
    fringe = PriorityQueue()
    fringe.push((startState,[],0),0)    
    closedSet= []
    
    
    
    while not fringe.isEmpty():
        
        node = fringe.pop()
    
        if problem.isGoalState(node[0]):
            return node[1]
          
            
        if not node[0] in closedSet:
            for successor in problem.getSuccessors(node[0]):
                if not successor[0] in closedSet:
                    newSuccessor = (successor[0],node[1]+[successor[1]],node[2]+successor[2])
                    fringe.push(newSuccessor, node[2]+successor[2])
            closedSet.append(node[0])

    
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    
    #Initializing the fringe and closed set    
    fringe = PriorityQueue()
    fringe.push((startState,[],0),0)    
    closedSet= []
    
    while not fringe.isEmpty():
        node = fringe.pop()
        
        if problem.isGoalState(node[0]):
            return node[1]
          
        if not node[0] in closedSet:
            for successor in problem.getSuccessors(node[0]):
                if not successor[0] in closedSet:
                    newSuccessor = (successor[0], node[1]+[successor[1]], node[2]+successor[2])
                    totalCost = newSuccessor[2] + heuristic(successor[0],problem)
                    fringe.push(newSuccessor,totalCost)
            closedSet.append(node[0])

    return []
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
