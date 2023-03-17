import math
from environment import Environment
#from state import State
import collections
import copy
from a_star_3 import AStar

State = collections.namedtuple('State',('name', 'location', 'country', 'hype'))

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, state: State, parent= None, remaining_locations=[]):
        self.parent = parent
        self.state = state
        self.remaining_locations = []

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

def heuristic():
    pass
    # this heuristic should be give a shorter distance than the actual one 

'''
    Calculate distance using the Haversine Formula
'''

def parse_coordinates(filename):
    coordinates = []
    with open(filename) as file:
        for line in file:
            coordinates.append(line.rstrip().split(' '))
    print(coordinates)
    return coordinates

def create_states(data):
    states = []
    for l in data:
        # name, location (lat, lon), country, hype 
        states.append(State(l[0], (float(l[1]), float(l[2])), l[3], l[4]))
    return states

def create_graph(states):
    graph = {}
    i = 0
    for s in states: 
        states_2 = copy.deepcopy(states)
        states_2.remove(s)
        graph[s] = states_2

    return graph

def create_test_graph(states):
    graph = {}
    i = 0
    for s in states: 
        if i == 7:
            i = 0
        graph[s] = [states[i+1], states[i+2]]
        i+=1
    return graph

def main():
    coordinates = parse_coordinates('data/coordinates_2.txt')
    states = create_states(coordinates)
    print(states)
    graph = create_test_graph(states)

    for g,v in graph.items():
        print(g,"value", v)
    remaining_locations = {}
    i = 0
    for s in states: 
        #if i == 0:
        #    pass
        remaining_locations[s.name] = s
        i+=1
    
    env = Environment(states[0], states, remaining_locations, graph)
    search = AStar(env)

    print(states[0], states[1])
    path = search.a_star(graph, states[0], states[9])
    print("PATH", path)


if __name__=="__main__":
    main()
