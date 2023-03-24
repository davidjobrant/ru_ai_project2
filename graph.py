import math
from environment import Environment
#from state import State
import collections
import copy
from a_star_3 import AStar
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

# to add: venue size, h
State = collections.namedtuple('State',('name', 'location', 'country', 'hype', 'continent'))

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
            coordinates.append(line.rstrip().split(','))
    print(coordinates)
    return coordinates

def create_states(data):
    states = []
    lat = []
    lon = []
    name = []
    for l in data:
        # name, location (lat, lon), country, hype 
        name.append(l[0])
        lat.append(float(l[1]))
        lon.append(float(l[2]))
        states.append(State(l[0], (float(l[1]), float(l[2])), l[3], l[4], l[5]))
    return states, name, lat, lon

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

def create_plot(df, path):
    # From GeoPandas, our world map data
    worldmap = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    # Creating axes and plotting world map
    fig, ax = plt.subplots(figsize=(12, 6))
    worldmap.plot(color="lightgrey", ax=ax)

    # Plotting our Impact Energy data with a color map
    x = df['lon']
    y = df['lat']
    z = df['data']
    plt.scatter(x, y, s=20*z, c=z, alpha=1, vmin=0, vmax=5)
                #cmap='autumn')
    plt.colorbar(label='In Tour ')
    prev = None
    for point in path: 
        lat, lon = point.location
        print(lat, lon)
        print(prev)
        if prev:
            plt.plot([prev[1], lon],[prev[0], lat])
        prev = (lat, lon)

    # Creating axis limits and title
    plt.xlim([-180, 180])
    plt.ylim([-90, 90])

    #first_year = df["Datetime"].min().strftime("%Y")
    #last_year = df["Datetime"].max().strftime("%Y")
    #p#lt.title("NASA: Fireballs Reported by Government Sensors\n" +     
    #        str(first_year) + " - " + str(last_year))
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

def main():
    coordinates = parse_coordinates('data/coordinates_2.txt')
    states, name, lat, lon = create_states(coordinates)
    print(states)
    #graph = create_test_graph(states)

    #for g,v in graph.items():
    #    print(g,"value", v)
    remaining_locations = {}
    remaining_countries = set()
    i = 0
    for s in states: 
        #if i == 0:
        #    pass
        remaining_countries.add(s.country)
        remaining_locations[s.name] = s
        i+=1
    
    env = Environment(states[0], states, remaining_locations, remaining_countries)
    search = AStar(env)

    print(states[0], states[1])
    path = search.a_star(states[0], states[2])
    path_names = []
    print("VISTED AFTER SEARCH", env.visited_countries)
    print("PATH END")
    for s in path: 
        print(s)
        path_names.append(s.name)
    #print("PATH END", path)

    df = pd.DataFrame()
    df['name'] = name
    df['lat'] = lat
    df['lon'] = lon
    df['data'] = 1
    df.loc[df["name"].isin(path_names), "data"] = 5
    print(df)
    create_plot(df, path)


if __name__=="__main__":
    main()
