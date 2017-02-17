import sys

moveList = [{'up':None,'left':None,'right':1,'down':3},
            {'up':None,'left':0,'right':2,'down':4},
            {'up':None,'left':1,'right':None,'down':5},
            {'up':0,'left':None,'right':4,'down':6},
            {'up':1,'left':3,'right':5,'down':7},
            {'up':2,'left':4,'right':None,'down':8},
            {'up':3,'left':None,'right':7,'down':None},
            {'up':4,'left':6,'right':8,'down':None},
            {'up':5,'left':7,'right':None,'down':None}]

class gameState():
    
    def __init__(state):
        self.state = state
        
        self.blankPos = self.state.find('0')
        
        
    def goalState():
        
        if self.state == "012345678":
            return 1
        else:
            return 0
        
    def getChildren(action):
            
        newBlankPos = moveList[self.blankPos][action]
            
        if newBlankPos != None:
            stateList = list(self.state)
            stateList[self.blankPos],stateList[newBlankPos] = stateList[newBlankPos],stateList[self.blankPos]
            newState = ''.join(stateList)
                
            return gameState(newState)
        
        return None
                
        
        
class Queue():
    
    def __init__(self):
        self.values = []
    
    def push(self,x):
        self.values = self.values + [x]
        
    def pop(self,x):
        top = self.values[0]
        self.values = self.values[1:]
        return top
        
    def isEmpty(self):
        if len(self.values)==0:
            return 1
        else:
            return 0
        
    def length(self,x):
        return len(self.values)
    
class Stack():
    
    def __init__(self):
        self.values = []
    
    def push(self,x):
        self.values = [x] + self.values 
    
    def isEmpty(self):
        if len(self.values)==0:
            return 1
        else:
            return 0
    def pop(self,x):
        top = self.values[0]
        self.values = self.values[1:]
        return top
    
    def length(self,x):
        return len(self.values)



class bfs():
    
    def __init__(x):
        self.startState = x
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size=0
        self.search_depth = 0
        self.max_search_depth = 0
        self.running_time = 0
        self.max_ram_usage = 0
        
        explored = set()
        fringe = Queue()
        fringe.push(x)
        path = []
        self.solve(fringe,path,depth=0)
        
        
    def solve(fringe,explored,path,depth):
                
        if fringe.isEmpty()==0:
            topNode = fringe.pop()
        
            explored.add(topNode)
            if topNode.goalState()==1:
                return path
                
        	for action in ['up','left','right','down']:
                
                newState = topNode.getChildren(action)
                
                if newState != None and newState not in fringe.values and newState not in explored:
                    fringe.push(newState)
                    newPath = path + [action]
                    depth = len(newPath)
                    sol = solve(fringe,explored,newPath,depth)
                    return sol
                    
            
        
