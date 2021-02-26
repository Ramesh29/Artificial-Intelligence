from queue import Queue
from queue import LifoQueue
import time
import sys
import math

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):
    """docstring for PuzzleState"""
    def __init__(self, config, n, parent=None, action="Initial", cost=0, mdist=0):
        if n*n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")
        self.id = int(''.join([str(i) for i in config ]))
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        self.mdist = mdist
    

        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row = i // self.n
                self.blank_col = i % self.n
                break

    def display(self):
        for i in range(self.n):
            line = []
            offset = i * self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)

    def move_left(self):
        if self.blank_col == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        if self.blank_col == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):
        if self.blank_row == 0:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):
        if self.blank_row == self.n - 1:
            return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):
        """expand the node"""
        # add child nodes in order of UDLR
        if len(self.children) == 0:
            up_child = self.move_up()
            if up_child is not None:
                self.children.append(up_child)
            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)
            left_child = self.move_left()
            if left_child is not None:
                self.children.append(left_child)
            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)
        return self.children
    
    def check_goal(self):
      if self.config == tuple(map(int, list("012345678"))):
        return True
      else:
        return False
      
      
      
      
# class to store states prioritized by the 
# minimum manhattan distance to final state
class PriorityQueue:
  def __init__(self):
    self.queue = []
    
  def manhattanDistance(self, config ):
    fconfig = [ int(d) for d in list("012345678")]
    d = 0
    for t in config:
      if t == 0:
        continue
      d = d + abs(config.index(t)//3 - fconfig.index(t)//3 ) + abs(config.index(t)%3 - fconfig.index(t)%3)
  
    return d

  def empty(self):
    if len(self.queue) == 0:
      return True
    return False
  
    # before putting into frontier calculate 
    # manhattan distance from parent to state 
    # and state to final config
  def put(self, state):
    
    # mdist = manhattanDistance from this state to final state
    state.mdist = self.manhattanDistance(state.config)
    # fx = cost to get to this node + mdist
    state.fx = state.cost + state.mdist
    # append this state to the queue
    self.queue.append(state)

  
  # return the state with minimum manhattan distance to final state
  def get(self):
    try:
      min = 0
      for i in range(len(self.queue)):
        if self.queue[i].fx < self.queue[min].fx:
          min = i
      state = self.queue[min]
      del self.queue[min]
      return state
    except IndexError:
      print()
      exit()
      
class Search:
  def __init__(self, state, sm):
    self.state = state
    self.sm = sm
    self.visited = []

  
  def dfs(self):
    frontier = LifoQueue()
    excludes = set()
    final_config = tuple(map(int, "012345678"))
    
    frontier.put(self.state)
    max_depth = 0
    count = 0
    while not frontier.empty():
      state = frontier.get()        
      excludes.add(state.id)
      
      if state.config == final_config:
        return (state,count, max_depth )
      count = count + 1
      children_list = state.expand()
      r_childrenlist = [ c for c in children_list if c is not None ]
      r_childrenlist.reverse()
      
      for c in r_childrenlist:
        if c.id not in excludes:
          frontier.put(c)
          if c.cost > max_depth:
            max_depth = c.cost
          excludes.add(c.id)
          
    return None,count, max_depth

  
  def bfs(self):
    frontier = Queue()
    excludes = set()
    final_config = tuple(map(int, "012345678"))
    
    frontier.put(self.state)
    max_depth = 0
    count = 0
    while not frontier.empty():
      state = frontier.get()
      excludes.add(state.id)
      
      if state.config == final_config:
        return (state,count, max_depth)
      count = count + 1
      children_list = state.expand()
      for c in children_list:
        if c.id not in excludes:
          frontier.put(c)
          if c.cost > max_depth:
            max_depth = c.cost          
          excludes.add(c.id)
          
    return None,count, max_depth
  
  def ast(self):
    frontier = PriorityQueue()
    excludes = set()
    final_config = tuple(map(int, "012345678"))
    
    # pusth the initial state to frontier
    frontier.put(self.state)
    max_depth = 0
    count = 0
    while not frontier.empty():
      state = frontier.get()
      # exclude this state from future addtion to the queue.
      excludes.add(state.id)
      # if this is the final state, we are done.
      if state.config == final_config:
        return (state,count, max_depth)
      # if not,expand its children
      count = count + 1
      children_list = state.expand()   
      for c in children_list:
        if c.id not in excludes:
          frontier.put(c)
          if c.cost > max_depth:
            max_depth = c.cost          
          if c.cost > max_depth:
            max_depth = c.cost
          excludes.add(c.id)
          
    return None,count, max_depth  
  
  def writeOutput(self, state, count, runtime , max_depth ):
    if state is None:
      print("No path to final state found")
      return
    
    #print("Final state is : ")
    #state.display()
    pathToGoal = []
    depth = 0
    cost = state.cost
    while(  state.parent is not None ):
      pathToGoal.append(state.action)
      depth = depth + 1
      state = state.parent
    pathToGoal.reverse()
    
    # calculate the RAM usage
    ram = 0
    if sys.platform == "win32":
      import psutil
      ram = psutil.Process().memory_info().rss / 1000000
    else:
      import resource
      ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000000
      
    # write to file
    f = open("output.txt", "w")
    f.write("path_to_goal: " + str(pathToGoal) + "\n" )
    f.write("cost_of_path: " + str(cost) + "\n" )
    f.write("nodes_expanded: " + str(count) + "\n" )
    f.write("search_depth: " + str(cost) + "\n")
    f.write("max_search_depth: " + str(max_depth) + "\n")
    f.write("running_time: " + str(runtime) + "\n")
    f.write("max_ram_usage: " + str(ram) + "\n")

  def doSearch(self):
    if self.sm == "bfs":
      start_time = time.time()
      state, count, max_depth = self.bfs()
      end_time = time.time() - start_time
    elif self.sm == "dfs":
      start_time = time.time()
      state, count, max_depth = self.dfs()
      end_time = time.time() - start_time
    elif self.sm == "ast":
      start_time = time.time()
      state, count, max_depth = self.ast()
      end_time = time.time() - start_time
    
    self.writeOutput(state,count, end_time , max_depth )
 
def main():
    sm = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = tuple(map(int, begin_state))
    size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, size)
    
    search = Search(hard_state, sm)
    search.doSearch()
    
    
    
if __name__ == "__main__":
  main()