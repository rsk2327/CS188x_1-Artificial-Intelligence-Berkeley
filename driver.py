import sys
import resource
import time

moveList = [{'Up':None,'Left':None,'Right':1,'Down':3},
            {'Up':None,'Left':0,'Right':2,'Down':4},
            {'Up':None,'Left':1,'Right':None,'Down':5},
            {'Up':0,'Left':None,'Right':4,'Down':6},
            {'Up':1,'Left':3,'Right':5,'Down':7},
            {'Up':2,'Left':4,'Right':None,'Down':8},
            {'Up':3,'Left':None,'Right':7,'Down':None},
            {'Up':4,'Left':6,'Right':8,'Down':None},
            {'Up':5,'Left':7,'Right':None,'Down':None}]

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
            self.explored.add(topNode.state)
            
            
            
            if topNode.goalState() == 1:
                self.bfsPath = topNode.path
                return topNode.path

            self.nodes_expanded += 1
                
            for action in ["Up","Down","Left","Right"]:
                newState =  topNode.getChildren(action)
                
                if newState != None and newState.state not in self.fringe.values and newState.state not in self.explored:
                    self.fringe.push(newState)
                    
                    if len(newState.path) > self.max_search_depth:
                        self.max_search_depth = len(newState.path)

            sol = self.solve()
            return sol
            

algo = sys.argv[0]
startingState = "".join([sys.argv[2][i*2] for i in range(9)])

checkState = gameState(startingState)
checkState.path=[]
start = time.clock()

if algo =="bfs":
    a = bfs(checkState)
    sol = a.solve()
elif algo =="dfs":
    a = bfs(checkState)
    sol = a.solve()
else:
    a = bfs(checkState)
    sol = a.solve()


end = time.clock()


timeTaken = end-start

print a.bfsPath
print a.nodes_expanded
print a.fringe_size
print a.max_fringe_size
print a.search_depth
print a.max_search_depth
print resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0

f = open('output.txt','w')

f.write("path_to_goal: ")
f.write(str(a.bfsPath))
f.write("\n")

f.write("cost_of_path: ")
f.write(str(len(a.bfsPath)))
f.write("\n")

f.write("nodes_expanded: ")
f.write(str(a.nodes_expanded))
f.write("\n")

f.write("fringe_size: ")
f.write(str(a.fringe_size))
f.write("\n")

f.write("max_fringe_size: ")
f.write(str(a.max_fringe_size))
f.write("\n")

f.write("search_depth: ")
f.write(str(a.search_depth))
f.write("\n")

f.write("max_search_depth: ")
f.write(str(a.max_search_depth))
f.write("\n")

f.write("running_time: ")
f.write(str(timeTaken))
f.write("\n")

f.write("max_ram_usage: ")
f.write(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0))
f.write("\n")


f.close()


