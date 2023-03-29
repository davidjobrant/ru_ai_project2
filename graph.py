import math
from environment import Environment
#from state import State
import collections
import copy
from a_star_3 import AStar
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import time
import plotly.graph_objects as go
import numpy as np
from numpy import pi, sin, cos
import os
# to add: venue size, h
State = collections.namedtuple('State',('name', 'location', 'country', 'continent', 'hype', 'visited'))

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
    countries = []
    i = 0
    for l in data:
        if i != 0:
        # name, location (lat, lon), country, hype 
            name.append(l[0])
            lat.append(float(l[1]))
            lon.append(float(l[2]))
            countries.append(l[3])
            states.append(State(l[0], (float(l[1]), float(l[2])), l[3], l[4], l[5], tuple()))
        i+=1
    return states, name, lat, lon, countries

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
    remaining = len(path)
    first = None
    for point in path: 
        if remaining == len(path):
            first = point.location
        lat, lon = point.location
        print(lat, lon)
        print(prev)
        if remaining == 1:
            last = point
        if prev:
            plt.plot([prev[1], lon],[prev[0], lat])
        prev = (lat, lon)
        remaining -= 1
    plt.plot([prev[1], first[1]],[prev[0], first[0]])

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

def point_sphere(lon, lat):
    #associate the cartesian coords (x, y, z) to a point on the  globe of given lon and lat
    #lon longitude
    #lat latitude
    lon = lon*pi/180
    lat = lat*pi/180
    x = cos(lon) * cos(lat) 
    y = sin(lon) * cos(lat) 
    z = sin(lat) 
    return np.array([x, y, z])

def slerp(A=[100, 45], B=[-50, -25], dir=-1, n=100):
    #Spherical "linear" interpolation
    """
    A=[lonA, latA] lon lat given in degrees; lon in  (-180, 180], lat in ([-90, 90])
    B=[lonB, latB]
    returns n points on the great circle of the globe that passes through the  points A, B
    #represented by lon and lat
    #if dir=1 it returns the shortest path; for dir=-1 the complement of the shortest path
    """
    As = point_sphere(A[0], A[1])
    Bs = point_sphere(B[0], B[1])
    alpha = np.arccos(np.dot(As,Bs)) if dir==1 else  2*pi-np.arccos(np.dot(As,Bs))
    if abs(alpha) < 1e-6 or abs(alpha-2*pi)<1e-6:
        return A
    else:
        t = np.linspace(0, 1, n)
        P = sin((1 - t)*alpha) 
        Q = sin(t*alpha)
        #pts records the cartesian coordinates of the points on the chosen path
        pts =  np.array([a*As + b*Bs for (a, b) in zip(P,Q)])/sin(alpha)
        #convert cartesian coords to lons and lats to be recognized by go.Scattergeo
        lons = 180*np.arctan2(pts[:, 1], pts[:, 0])/pi
        lats = 180*np.arctan(pts[:, 2]/np.sqrt(pts[:, 0]**2+pts[:,1]**2))/pi
        return lons, lats

def new_plot_try(df, path, user_in):
    #############################
    fig = go.Figure()
    #Define the map:
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon =df['lon'], #New York
        lat = df['lat'],#Sydney
        #hoverinfo = 'text',
        text = df['country'],
        mode = 'markers',
        showlegend = False,
        marker_size=5,
        hovertemplate =
            "%{text}<br>" +
            "longitude: %{lon}<br>" +
            "latitude: %{lat}<br>" + "<extra></extra>",
        
        line = dict(
                    width = 3,
                    color = 'rgb(68, 68, 68)'
            )
        ))

    prev = None
    prev_point = None
    remaining = len(path)
    path.append(copy.deepcopy(path[len(path)-1]))
    first = None
    i = 0
    for point in path: 
        if remaining == len(path):
            first = point
        lat, lon = point.location
        print(lat, lon)
        print(prev)
        if remaining == 1:
            last = point
        if prev:
            #plt.plot([prev[1], lon],[prev[0], lat])
            lons = [prev[1], lon]
            lats = [prev[0], lat]
            fig.add_trace(
                go.Scattergeo(
                #locationmode = 'USA-states',
                lon = lons,
                lat = lats,
                mode = 'markers+lines',
                line = dict(width = 3,color = 'red'),
                name = prev_point.country,
                text = "Stop nbr: " + str(i))
                )
        prev = (lat, lon)
        prev_point = point
        remaining -= 1
        i+=1
    #lons = [first.location[1], last.location[1] ]
    #lats = [first.location[0], last.location[0] ]
    #print("lon lats", lons, lats)
    i+=1

    
    fig.update_geos(
    #visible=False, resolution=50,
    showcountries=True, #, countrycolor="RebeccaPurple"
    #projection_type="orthographic"
    )
    #fig.add_trace(
    #        go.Scattergeo(
    #            locationmode = 'USA-states',
    #            lon = lons,
    #            lat = lats,
    #            mode = 'lines',
    #            line = dict(width = 1,color = 'red')))
    #Draw the complement of the shortest path 
    #lons, lats = slerp(A= [151.2093, -33.8688], B = [-74, 40.7128], dir=-1)
    #fig.add_trace(
    #        go.Scattergeo(
    #            locationmode = 'USA-states',
    #            lon = lons,
    #            lat = lats,
    #            mode = 'lines',
    #           line = dict(width = 2,color = 'green')))
    fig.show()
    #if not os.path.exists("plots"):
    #    os.mkdir("plots")
    
    #fig.write_image(f"images/{user_in}.png")


def main():
    coordinates = parse_coordinates('productive_data/base_case.csv')
    states, name, lat, lon, countries = create_states(coordinates)
    print(states)

    remaining_locations = {}
    remaining_countries = set()
    i = 0
    for s in states: 

        remaining_countries.add(s.country)
        remaining_locations[s.name] = s
        i+=1
    
    env = Environment(states[0], states, remaining_locations, remaining_countries)
    search = AStar(env)

    #print(states[0], states[1])
    #print("Enter name of test:\n")
    #user_in = input("Enter name of test:\n")
    user_in = "template"
    start = time.time()
    path, last_node = search.a_star(states[0], states[0])

    end = time.time()

    path_names = []
    print("-----------------------------------------------")
    print("PATH\n")
    for s in path: 
        print(s.country)
        path_names.append(s.name)
    print("-----------------------------------------------")

    df = pd.DataFrame()
    df['name'] = name
    df['country'] = countries
    df['lat'] = lat
    df['lon'] = lon
    df['data'] = 1
    df.loc[df["name"].isin(path_names), "data"] = 5
    #print(df)

    print("Total locations:",len(states), "\n")
    print("Locations in path:",len(path), ", expected:", len(remaining_countries))
    print("Total route distance:", last_node.g)
    print("Total route hype scoure:", last_node.total_hype)
    # TODO calculate env scor ebased on total distance, and how many flights are domestic or not  
    print("Total env score:", last_node.g * 156, "g")
    print("Time elapsed", end - start)
    print("Node expansions:", search.nb_node_expansions)
    print("Frontier size:", search.max_frontier_size)
    print("-----------------------------------------------")

    print(len(states))
    print(len(path), f"({len(remaining_countries)})")
    print(round(last_node.g), "km")
    print(last_node.total_hype)
    # TODO calculate env scor ebased on total distance, and how many flights are domestic or not  
    print(round(last_node.g * 156), "g")
    print(end - start, "s")
    print(search.nb_node_expansions)
    print( search.max_frontier_size)
    print("-----------------------------------------------")

    new_plot_try(df, path, user_in)


if __name__=="__main__":
    main()
