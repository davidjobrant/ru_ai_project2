from environment import Environment
from queue import PriorityQueue
import collections
State = collections.namedtuple('State',('name', 'location', 'country', 'hype', 'continent', 'visited'))

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, state: State, visited_countries, parent= None):
        self.parent = parent
        self.state = state
        self.remaining_locations = []
        self.visited_locations = {}
        self.visited_countries = visited_countries
        self.visited_continents = set()

        self.path_so_far = []
        self.total_distance = 0
        self.total_hype = 0

        self.g = 0
        self.h = 0
        self.f = 0

    def get_cost(self, current, child, env): 
        '''
            Calculates the haversine distance from the current node to a child.
        '''
        cost = env.haversine(current.state, child.state) 
        return cost
    
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

class AStar:
    def __init__(self, env, heuristics):
        self.env = env
        self.heuristics = heuristics

        self.g_score = {}
        self.nb_node_expansions = 0
        self.max_frontier_size = 0
        self.goal_node = None
        self.cached_visited = {}
        self.worse_g_value = 0
        self.already_closed = 0

    def is_goal_state(self, visited):
        '''
            Checks whether all countries has been visited. If they have, it's a goal state.
        '''
        return len(self.env.countries) == len(visited)


    def a_star(self, start, end):
        '''
            The A* algorithm, which tries to find a legal path from the start node until all countries have been visited. 
            If there exists a path, it's returned, otherwise None.
        '''
        # Create start and end node
 
        start_node = Node(start, set(), None)
        start_node.g = start_node.h = start_node.f = 0

        end_node = Node(end, set(), None)
        end_node.g = end_node.h = end_node.f = 0
        
        open_list = PriorityQueue()

        start_node.visited_countries.add(start.country)
        
        open_map = { start_node.state: start_node.g } 
        closed_map = dict()

        print("START", start_node)

        # Add the start node
        #heapq.heappush(open_list, start_node)
        open_list.put(start_node)

        # Loop until open list is emtpy
        while not open_list.empty():
            # Get the current node
            current_node = open_list.get()
            # Get the countries visited so far
            visited = current_node.state.visited + (current_node.state.country, )
            # Check if the current node is a goal state
            if self.is_goal_state(visited):
                print("END\n")
                path = []
                current = current_node
                while current is not None:
                    path.append(current.state)
                    current = current.parent
                return path[::-1], current_node # Return reversed path

            # Retrieves the legal successor states
            children = self.env.get_valid_locations(current_node)
            
            for c in children:
                child = Node(c, current_node.visited_countries, current_node)
                child.total_hype = current_node.total_hype + int(c.hype)

                # Calculates and sets the h, g and f values for this node
                child.h = self.heuristics.eval(child , end_node)
                child.g = current_node.g + current_node.get_cost(current_node, child, self.env)
                child.f = child.g + child.h

                if child.state in closed_map:
                    self.already_closed += 1
                    continue

                if child.state in open_map:
                    if child.g >= open_map[child.state]:
                        self.worse_g_value +=1
                        continue
                    else: 
                        open_list.queue.remove(child)

                open_map[child.state] = child.g
                open_list.put(child)

                # Caches the visited countries to make the search faster
                if c in self.cached_visited:
                    visited_countries = self.cached_visited[c]
                else:
                    current = child
                    visited_countries = set()
                    visited_continents = set()
                    while current is not None:
                        visited_countries.add(current.state.country)
                        visited_continents.add(current.state.continent)
                        current = current.parent
                        
                child.visited_countries = visited_countries
                self.cached_visited[c] = visited_countries
                
            self.env.visited_countries.add(current_node.state.country)

            # Mark current state as explored 
            closed_map[current_node.state] = current_node.g

            self.nb_node_expansions += 1
            if self.nb_node_expansions % 100 == 0:
                print(self.nb_node_expansions)
            self.max_frontier_size = max(self.max_frontier_size, open_list.qsize())

        print(len(closed_map))