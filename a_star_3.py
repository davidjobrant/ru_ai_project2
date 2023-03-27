import math
from environment import Environment
#from state import State
import collections
import heapq
import sys

State = collections.namedtuple('State',('location'))

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, state: State, visited_countries, parent= None):
        self.parent = parent
        self.state = state
        self.remaining_locations = []
        self.visited_locations = {}
        self.visited_countries = visited_countries

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

    def get_cost(self, current, child, env): 
        # TODO calculate haversine from this node to last node in remaining_locations
        #total = 0   
        #prev = child.state
        #for s in self.path_so_far:
        #    total += haversine(prev, s) 
        #    prev = s
        #total = haversine(prev, end_state) 
        #print("total cost:", total)
        return haversine(current.state, child.state) 
    
    def get_cost_old(self, current, child, env):
        cost = 0
        # if two countries are the same, penalize 
        countries = []
        #print("Cost path so far", self.path_so_far)
        for s in self.path_so_far:
            countries.append(s.country)
        
        #if len(countries) > len(set(countries)):
            #print("THIS IS TRUE")
            #cost += len(countries) - len(set(countries)) * 100
        #cost -= len(self.visited_countries) * 100000
        # if a country on the continent has not been visited yet, penalize
        '''TODO if countries does not contain all countries from a visited continent, PENALIZE'''

        missing = len(env.missing_country(current))
        if missing == []:
            missing = 0
        cost += missing* 100

        cost += haversine(self.state, child.state)
        #print("COST", cost)
        return cost 
    
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
    def old_heuristic(self, child, end_state): 
        # TODO calculate haversine from this node to last node in remaining_locations
        total = 0   
        prev = child
        for name, s in self.env.remaining_locations.items():
            total += haversine(prev, s) 
            prev = s
        total = haversine(prev, end_state) 
       # print("total heur:", total)
        return total
    
    def heuristic(self,node, env):
        state = node.state
        unvisited_states = [s for s in env.remaining_locations.values() if s.country not in node.visited_countries]
        #print("unvisited states", unvisited_states)
        remaining_continents = set(s.continent for s in unvisited_states)
        if state.country not in node.visited_countries:
            remaining_continents.add(state.continent)
        continent_priority = {}
        for continent in remaining_continents:
            count = sum(1 for s in unvisited_states if s.continent == continent)
            continent_priority[continent] = count
        if continent_priority:

            max_priority_continent = max(continent_priority, key=continent_priority.get)
        else: 
            max_priority_continent = "Europe"
        #print("MAX", max_priority_continent)
        if state.continent == max_priority_continent:
            #print("total heur:", 0)

            return 0
        else:
            #print("total heur:", 100000000)

            return 100





    def a_star(self, start, end):
        # Create start and end node
 
        start_node = Node(start, set(), None)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(end, set(), None)
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
            #if current_node == end_node:

            #print(self.env.remaining_countries)
            visited = current_node.state.visited + (current_node.state.country, )
            if all(item in visited for item in self.env.remaining_countries):
                print("END")
                path = []
                current = current_node
                while current is not None:
                    path.append(current.state)
                    current = current.parent
                return path[::-1] # Return reversed path

            print("CURRENT", current_node.state, "\n", "f:", current_node.g, "\n")
            #print("PATH SO FAR", current_node.path_so_far, "\n")

            #print("VISITED COUNTRIES", current_node.visited_countries, "\n")



            # TODO trying to get only relevant children
            #children = self.env.get_next_states(current_node)
            children = self.env.get_valid_locations(current_node)

            #print("valid locations", children, "\n")
            for c in children:
                #print("CHILD: ", c)

                
                child = Node(c, current_node.visited_countries, current_node)
                #child.visited_countries.add(c.country)

                path = []
                current = child
                visited_countries = set()
                while current is not None:
                    path.append(current.state)
                    visited_countries.add(current.state.country)
                    current = current.parent
                child.path_so_far =  path[::-1] # Return reversed path
                child.visited_countries = visited_countries
                
                #child.g = child.get_cost()
                #print(child.g)
                # H is the heuristic — estimated distance from the current node to the end node.

                #child.h = self.heuristic(child.state, end_node.state)
                child.h = self.heuristic(child, self.env)
                child.g = current_node.g + current_node.get_cost(current_node, child, self.env)
                #print("child.g")
                #print(child.g)
                child.f = child.g + child.h

                if child.state in closed_map:
                    continue
                elif child.state in open_map and child.g >= open_map[child.state]:
                    continue
                else: 
                    open_map[child.state] = child.g
                    heapq.heappush(open_list, child)

            self.env.visited_countries.add(current_node.state.country)
            closed_map[current_node.state] = current_node.g
        print(len(closed_map))

