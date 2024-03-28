import heapq
import torch
class Node():
    def __init__(self, state, action = None, parent = None, cost = 1):
        self.state = state
        self.action = action 
        self.parent = parent
        self.cost = cost # the cost from initial cost to current state.
        if self.parent is not None:
            self.cost += self.parent.cost
    def __lt__(self, other):
        return self.cost < other.cost
    
class stackFrontier():
    """
        for DFS
    """
    def __init__(self):
        self.frontier = []
        
    def add(self, node):
        self.frontier.append(node)
    
    def remove(self):
        self.frontier = self.frontier[:-1]
    
    def empty(self):
        return len(self.frontier) == 0
    

def string_to_state(input_string):
    rows = input_string.strip().split("\n")
    state = [[int(num) for num in row.strip().split()] for row in rows]
    return torch.tensor(state)

def maze_to_string(state, toPrint = False):
    """
        input a maze and return the source stirng 
    """

def initialState():
    """
        define the format of state input and operation     
        return a initial state
    """
    inputSource = """
1 15 7 10
9 14 4 11
8 5 0 6
13 3 2 12
"""
    state = string_to_state(inputSource)
    initialNode = Node(state = state, cost = 0)
    return initialNode
    
def goalTest(state):
    """
        input a state and test it, if reaching goal, return True 
    """
    target = torch.tensor([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
    return torch.all(state == target)

def getCost(state):
    """
        input the cost from current node to the next, return the cost
    """

    pass

def getIndex(state, target = 0):
    indices = torch.where(state == target)
    if len(indices[0]) > 0:
        return indices[0][0].item(), indices[1][0].item()
    return None # Return none if not found, but impossible

def getActions(state):
    """
        input a state, return all of the possible actions made by the agent. 
    """
    row, col = getIndex(state)
    actions = ["up", "down", "left", "right"]
    if row == 0:
        actions.remove("up")
    if row == 3:
        actions.remove("down")
    if col == 0:
        actions.remove("left")
    if col == 3:
        actions.remove("right")
 
    return actions
def swapElements(state, pos1, pos2):
    """
        swap elements in place
    """
    new_state = state.clone()
    new_state[pos1], new_state[pos2] = new_state[pos2], new_state[pos1]
    return new_state

def transitionModel(state, action):
    """
        input the state and action, transist this state to next state and return 
    """
    row, col = getIndex(state)
    if action == "up":
        new_state = swapElements(state, (row, col), (row-1, col))
    if action == "down":
        new_state = swapElements(state, (row, col), (row+1, col))
    if action == "left":
        new_state = swapElements(state, (row, col), (row, col-1))
    if action == "right":
        new_state = swapElements(state, (row, col), (row+1, col+1))
    return new_state

def heuristic_normal(state):
    """Normal one, directly based on the distance."""
    target = torch.tensor([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]])
    return torch.sum(abs(state - target)) # maybe its great for tensor type in calculating...
def successors(parent):
    state = parent.state
    actions = getActions(state)
    next_nodes = []
    for action in actions:
        next_state = transitionModel(state, action)
        new_node = Node(next_state, action, parent, 1)
        next_nodes.append(new_node)
    return next_nodes

def a_star(initial_state, goal_test, heuristic, memory_limit = 10000):
    frontier = []
    heapq.heappush(frontier, (0, Node(initial_state))) # (pathcost_given_by_g+f, node)
    explored = set()
    while frontier:
        if len(frontier) + len(explored) > memory_limit:
            print("Memory limit exceeded.")
            return None
        _, current_node = heapq.heappop(frontier)
        if goal_test(current_node.state):
            return current_node
        explored.add(current_node.state)
        for next_node in successors(current_node):
            if next_node.state not in explored:
                h = heuristic(next_node.state)
                g = current_node.cost + 1
                f = g + h
                heapq.heappush(frontier, (f, next_node))
    return None # No solution

def getPath(start, end, model):
    """
        and the optimized path from start to the end. 
        if found, return series. Else return None
    """
    if model is "A*":
        a_star(start, end, "A*")

def main():
    start = initialState()
    end = goalTest()
    getPath(start, end, "A*")