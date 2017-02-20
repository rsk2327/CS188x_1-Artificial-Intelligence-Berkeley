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
    
    def __init__(self,state):
        self.state = state
        
        self.blankPos = self.state.find('0')
        self.path=[]
        
        
    def goalState(self):
        
        if self.state == "012345678":
            return 1
        else:
            return 0
        
    def getChildren(self,action):
            
        newBlankPos = moveList[self.blankPos][action]
        
          
        if newBlankPos != None:
            stateList = list(self.state)
            stateList[self.blankPos],stateList[newBlankPos] = stateList[newBlankPos],stateList[self.blankPos]
            newState = ''.join(stateList)
            
            childState = gameState(newState)
            childState.path = self.path + [action]
            return childState
        
        return None
                
        
        
class Queue():
    
    def __init__(self):
        self.values = []
    
    def push(self,x):
        self.values = self.values + [x]
        
    def pop(self):
        top = self.values[0]
        self.values = self.values[1:]
        return top
        
    def isEmpty(self):
        if len(self.values)==0:
            return 1
        else:
            return 0
        
    def length(self):
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
    def pop(self):
        top = self.values[0]
        self.values = self.values[1:]
        return top
    
    def length(self):
        return len(self.values)


class bfs():
    
    def __init__(self,x):
        self.startNode = x
        self.nodes_expanded = 0
        self.fringe_size = 0
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0
        self.running_time = 0
        self.max_ram_usage = 0
        
        self.explored = set()
        self.fringe = Queue()
        self.fringe.push(x)
		
        self.bfsPath = []
        
    def solve(self):
        
        if self.fringe.isEmpty()==0:
            
            self.fringe_size = self.fringe.length()
            
            if self.fringe_size > self.max_fringe_size:
                self.max_fringe_size = self.fringe_size
            
            topNode = self.fringe.pop()
            self.fringe_size = self.fringe.length()
            
            self.search_depth = len(topNode.path)
            
            if self.search_depth > self.max_search_depth:
                self.max_search_depth = self.search_depth
            
            self.explored.add(topNode.state)
            
            self.nodes_expanded += 1
            
            if topNode.goalState() == 1:
                self.bfsPath = topNode.path
                return topNode.path
                
            for action in ["up","down","left","right"]:
                newState =  topNode.getChildren(action)
                
                if newState != None and newState.state not in self.fringe.values and newState.state not in self.explored:
                    self.fringe.push(newState)
                    
            
            sol = self.solve()
            return sol
            


checkState = gameState('125340678')
checkState.path=[]

a = bfs(checkState)
sol = a.solve()
print "sol is "
print a.bfsPath
print a.nodes_expanded
print a.fringe_size
print a.max_fringe_size
print a.search_depth
print a.max_search_depth
