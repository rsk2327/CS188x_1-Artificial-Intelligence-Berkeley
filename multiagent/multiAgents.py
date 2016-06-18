# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import numpy as np
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        ghostPos = newGhostStates[0].getPosition()

            
        ghostCost = -50/(np.e**manhattanDist(ghostPos,newPos))
        if manhattanDist(newPos,ghostPos)<=1:
            ghostCost +=-1500    
        foodCost = -closestFoodDist(newPos,newFood.asList())
        foodCount = -30*len(newFood.asList())
        return ghostCost + foodCost + foodCount


def closestFoodDist(newPos,foodList):
    
    if len(foodList)>0:
        foodList.sort(key = lambda x : manhattanDist(x,newPos))
        return euclidDist(newPos,foodList[0])
    else:
        return 0
        
def closestFoodDist2(newPos,foodList):
    
    if len(foodList)>0:
        foodList.sort(key = lambda x : manhattanDist(x,newPos))
        return manhattanDist(newPos,foodList[0])
    else:
        return 0
        
def euclidDist(xy1, xy2):
    "The Manhattan distance heuristic for a PositionSearchProblem"

    return np.sqrt((xy1[0] - xy2[0])**2 + (xy1[1] - xy2[1])**2)
    
def manhattanDist(xy1, xy2):
    "The Manhattan distance heuristic for a PositionSearchProblem"

    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


    

        
            

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        ghostCount = gameState.getNumAgents()
        agentIndex=0
        maxVal = -999999.0  
        bestAction = 0
        depth = 1
        verbose=0
        
        successor={}
        for i in range((ghostCount-1)):
            successor[i]=i+1
        successor[(ghostCount-1)]=0
        nextAgent = successor[agentIndex]
        
        for action in gameState.getLegalActions(agentIndex):
            if verbose==1: print "Action : ",action
            nextState = gameState.generateSuccessor(agentIndex,action)
            actionVal = self.minNode(nextAgent,depth,nextState,successor,verbose)
            if actionVal>maxVal:
                maxVal = actionVal
                bestAction = action
            if verbose==1: print "Action : ",action," Cost : ", actionVal
        
        return bestAction
        
            
    def minNode(self,agentIndex,depth,gameState,successor,verbose):
    
        minVal = 999999.0  
        nextAgent = successor[agentIndex]
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth
    
        if gameState.getLegalActions(agentIndex)==[]:
            if verbose==1: print "No more legal actions. Returning ",self.evaluationFunction(gameState)
            return self.evaluationFunction(gameState)
    
        if nextAgent==0:
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                minVal = min(minVal, self.maxNode(nextAgent, depth, nextState,successor,verbose))
            if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",minVal
            return minVal
        else:
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                minVal = min(minVal, self.minNode(nextAgent, depth, nextState,successor,verbose))
            if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",minVal
            return minVal
            
    def maxNode(self,agentIndex,depth,gameState,successor,verbose):    
        
        depth += 1
        maxVal=-999999.0  
        nextAgent = successor[agentIndex]
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth

        if depth==(self.depth+1) or gameState.getLegalActions(agentIndex)==[]:
            if verbose==1: print "Reached terminal state or ran out of actions. Returned ",self.evaluationFunction(gameState)
            return self.evaluationFunction(gameState)
        
        
        for action in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, action)
            maxVal = max(maxVal, self.minNode(nextAgent,depth,nextState,successor,verbose))
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",maxVal
        return maxVal
            

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ghostCount = gameState.getNumAgents()
        agentIndex=0
        maxVal = -999999.0  
        bestAction = 0
        depth = 1
        verbose=0
        alpha,beta = -999999.0, 999999.0
        
        successor={}
        for i in range((ghostCount-1)):
            successor[i]=i+1
        successor[(ghostCount-1)]=0
        nextAgent = successor[agentIndex]
        
        for action in gameState.getLegalActions(agentIndex):
            if verbose==1: print "Action : ",action
            nextState = gameState.generateSuccessor(agentIndex,action)
            actionVal = self.minNode(nextAgent,depth,nextState,successor,verbose,alpha,beta)
            if actionVal>maxVal:
                maxVal = actionVal
                alpha = actionVal
                bestAction = action
            if verbose==1: print "Action : ",action," Cost : ", actionVal
        
        return bestAction
    
    def minNode(self,agentIndex,depth,gameState,successor,verbose,alpha,beta): 
        minVal = 999999.0  
        nextAgent = successor[agentIndex]
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth
    
        if gameState.getLegalActions(agentIndex)==[]:
            if verbose==1: print "No more legal actions. Returning ",self.evaluationFunction(gameState)
            return self.evaluationFunction(gameState)
    
        if nextAgent==0:
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                minVal = min(minVal, self.maxNode(nextAgent, depth, nextState,successor,verbose,alpha,beta))
                if minVal<alpha:
                    return minVal
                beta = min(beta,minVal)
            if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",minVal
            return minVal
        else:
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                minVal = min(minVal, self.minNode(nextAgent, depth, nextState,successor,verbose,alpha,beta))
                if minVal<alpha:
                    return minVal
                beta = min(minVal,beta)
            if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",minVal
            return minVal
            
            
            
    def maxNode(self,agentIndex,depth,gameState,successor,verbose,alpha,beta):      
        depth += 1
        maxVal=-999999.0  
        nextAgent = successor[agentIndex]
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth

        if depth==(self.depth+1) or gameState.getLegalActions(agentIndex)==[]:
            if verbose==1: print "Reached terminal state or ran out of actions. Returned ",self.evaluationFunction(gameState)
            return self.evaluationFunction(gameState)
        
        
        for action in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, action)
            maxVal = max(maxVal, self.minNode(nextAgent,depth,nextState,successor,verbose,alpha,beta))
            if maxVal>beta:
                return maxVal
            alpha = max(alpha,maxVal)
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",maxVal
        return maxVal

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        ghostCount = gameState.getNumAgents()
        agentIndex=0
        maxVal = -999999.0  
        bestAction = 0
        depth = 1
        verbose=0
       
        
        successor={}
        for i in range((ghostCount-1)):
            successor[i]=i+1
        successor[(ghostCount-1)]=0
        nextAgent = successor[agentIndex]
        
        for action in gameState.getLegalActions(agentIndex):
            if verbose==1: print "Action : ",action
            nextState = gameState.generateSuccessor(agentIndex,action)
            actionVal = self.minNode(nextAgent,depth,nextState,successor,verbose)
            if actionVal>maxVal:
                maxVal = actionVal
                bestAction = action
            if verbose==1: print "Action : ",action," Cost : ", actionVal
        
        return bestAction
        
    def minNode(self,agentIndex,depth,gameState,successor,verbose): 
        expectVal = [] 
        nextAgent = successor[agentIndex]
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth
    
        if gameState.getLegalActions(agentIndex)==[]:
            if verbose==1: print "No more legal actions. Returning ",self.evaluationFunction(gameState)
            return self.evaluationFunction(gameState)
    
        if nextAgent==0:
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                expectVal.append(self.maxNode(nextAgent, depth, nextState,successor,verbose))
            if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",np.mean(expectVal)
            return np.mean(expectVal)
        else:
            for action in gameState.getLegalActions(agentIndex):
                nextState = gameState.generateSuccessor(agentIndex,action)
                expectVal.append(self.minNode(nextAgent, depth, nextState,successor,verbose))
            if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",np.mean(expectVal)
            return np.mean(expectVal)
            
            
            
    def maxNode(self,agentIndex,depth,gameState,successor,verbose):      
        depth += 1
        maxVal=-999999.0  
        nextAgent = successor[agentIndex]
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth

        if depth==(self.depth+1) or gameState.getLegalActions(agentIndex)==[]:
            if verbose==1: print "Reached terminal state or ran out of actions. Returned ",self.evaluationFunction(gameState)
            return self.evaluationFunction(gameState)
        
        
        for action in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, action)
            maxVal = max(maxVal, self.minNode(nextAgent,depth,nextState,successor,verbose))
        if verbose==1: print "Agent : ",agentIndex," at depth ",depth," returned ",maxVal
        return maxVal

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodCount= len(newFood.asList())
        
    ghostPos = newGhostStates[0].getPosition()
    ghostCost = -10/(np.e**(10*manhattanDist(ghostPos,newPos)))
    if manhattanDist(ghostPos,newPos)==0:
        ghostCost += -5000
    
#    if newScaredTimes[0]>1:
#        ghostCost += 70
    
    foodCost = -50*closestFoodDist(newPos,newFood.asList())
    
    foodCountCost = -1500*foodCount
    
        
#    if foodCountCost+1000>foodCost:
#        foodCountCost = -50*len(newFood.asList())
    
#    print "currPos :",newPos," ghostCost :",ghostCost," foodCost : ",foodCost," foodCount : ",foodCountCost," totalCost :",(ghostCost + foodCost + foodCountCost)
    
    return ghostCost + foodCost + foodCountCost

# Abbreviation
better = betterEvaluationFunction

