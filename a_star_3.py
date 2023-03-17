import math
from environment import Environment
#from state import State
import collections
import heapq
import sys

State = collections.namedtuple('State',('location'))

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, state: State, parent= None, remaining_locations=[]):
        self.parent = parent
        self.state = state
        self.remaining_locations = []
        self.visited_locations = {}

        self.path_so_far = []

        # potential variables: 

        # locations of the remaining concert venues 

        # maybe not relevant in the state because these values are not changing 
        # but probably relevent in the heuristics
        # -> so then do we need them in the state for that reason? 
        # venue size 
        # artist buzz
        # environmental footprint 

        self.g = 0
        self.h = 0
        self.f = 0
    
    def get_cost(self):
        if len(self.path_so_far) == 0:
            return 100000000000          
        return 10 - len(self.path_so_far) * 100000000000 
    
    def is_goal_state(self):
        return self.path_so_far == 8

    def __str__(self):
        return f"location: {self.state.location}"

    def __eq__(self, other):
        return self.state == other.state

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (self.f < other.f)

    def __gt__(self, other):
        return (self.f > other.f)

    def __le__(self, other):
        return (self.f < other.f) or (self == other)

    def __ge__(self, other):
        return (self.f > other.f) or (self == other)

def haversine(coord1, coord2):
    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1.location
    lon2, lat2 = coord2.location

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    meters = round(meters, 3)
    km = round(km, 3)

    #print(f"Distance: {meters} m")
    #print(f"Distance: {km} km")

    return meters

def heuristic(child, end_node): 
        
    return haversine(child, end_node) * 10

class AStar:
    def __init__(self, env):
        self.g_score = {}
        self.env = env


    """
    TODO: Issue now is that we don't create the children nodes while looping, we already have a provided list. Therefore the parent
    nodes aren't assigned. 
    So somehow, we need to create the states as we loop through them to be able to retrieve the path in the end. 
    Might not work to have them seperated in a list in the Environment env.
    - Maybe we still could, just have a different typ of object "state" which is stored there
    - When looping, we create nodes based on those remaining states. 
    - Potentially? 
    """
    
    def a_star(self, graph, start, end):
        # Create start and end node
 
        start_node = Node(start, None)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(end, None)
        end_node.g = end_node.h = end_node.f = 0
        # Initialize both open and closed list
        open_list = []
        open_map = { start_node.state: start_node.g } 
        closed_map = dict()
        closed_list = []

        print("START", start_node)

        # Add the start node
        heapq.heappush(open_list, start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = heapq.heappop(open_list)
            
            # Found the goal
            #print("LEN", len(closed_map))
            #print(current_node)
            #print(end_node)
            # TODO this check is wrong 
            if current_node == end_node:
                print("END")
                path = []
                current = current_node
                while current is not None:
                    path.append(current.state)
                    current = current.parent
                return path[::-1] # Return reversed path
        
            # get children here 
            # THIS WORKS!
            #children = graph[current_node.state]
            #print("CURRENT", current_node.state)

            # TODO trying to get only relevant children
            children = self.env.get_next_states(current_node)
            print("children", children)
            for c in children:
                print("CHILD: ", c)
                child = Node(c, current_node)
                #current_node.visited_locations[c.name] = c

                path = []
                current = current_node
                while current is not None:
                    path.append(current.state)
                    current = current.parent
                child.path_so_far =  path[::-1] # Return reversed path
                
                #child.g = child.get_cost()
                #print(child.g)
                # H is the heuristic — estimated distance from the current node to the end node.
                child.h = heuristic(child.state, end_node.state)
                child.f = child.get_cost() + child.h

                if child.state in closed_map:
                     continue
                elif child.state in open_map and child.g >= open_map[child.state]:
                    continue
                else: 
                    print("we here")
                    open_map[child.state] = child.g
                    heapq.heappush(open_list, child)

            #printself.env.remaining_locations)
            self.env.remaining_locations.pop(current_node.state.name)
            closed_map[current_node.state] = current_node.g
        print(len(closed_map))

