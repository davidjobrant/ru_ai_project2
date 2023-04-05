from environment import Environment
import collections
import copy
from search import AStar
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import time
import plotly.graph_objects as go
import numpy as np
from numpy import pi, sin, cos
from heuristics import DistanceHeuristic, HypeHeuristic, DistanceAndCountriesHeuristic, DjikstraHeuristic

State = collections.namedtuple('State',('name', 'location', 'country', 'continent', 'hype', 'visited'))

def read_input_data(filename):
    '''
        Reads input data from a specified file
    '''
    coordinates = []
    with open(filename) as file:
        for line in file:
            coordinates.append(line.rstrip().split(','))
    print(coordinates)
    return coordinates

def create_states(data):
    '''
        Creates states based on a data list. 
    '''
    states, lat, lon, name, countries, hype = [], [], [], [], [], []

    i = 0
    for l in data:
        if i != 0:
            name.append(i)
            lat.append(float(l[1]))
            lon.append(float(l[2]))
            countries.append(l[3])
            hype.append(l[5])
            states.append(State(l[0], (float(l[1]), float(l[2])), l[3], l[4], l[5], tuple()))
        i+=1
    return states, name, lat, lon, countries, hype


def point_sphere(lon, lat):
    '''
        Associate the cartesian coords (x, y, z) to a point on the  globe of given lon and lat
    '''
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

def scatter_plot(df, path):
    '''
        Visualises the path on a worldmap using plotly. 
    '''
    fig = go.Figure()
    #Define the map:
    fig.add_trace(go.Scattergeo(
        locationmode = 'USA-states',
        lon =df['lon'], #New York
        lat = df['lat'],#Sydney
        #hoverinfo = 'text',
        text = df['country'] + "<br>" + "Hype: " + df['hype'],
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
    i = 0
    for point in path: 
        lat, lon = point.location
        print(lat, lon)
        print(prev)
        print(i)
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
                text = "Stop nbr: " + str(i) + "<br>" + "Hype: " + str(point.hype))
                )
        prev = (lat, lon)
        prev_point = point
        remaining -= 1
        i+=1

    # Remove comment for circular projection instead of a flat worldmap
    fig.update_geos(
        showcountries=True, 
        #projection_type="orthographic"
    )
    
    fig.show()
    #if not os.path.exists("plots"):
    #    os.mkdir("plots")
    
    #fig.write_image(f"images/{user_in}.png")



def run_experiments(coordinates, nbr_of_times):
    for i in range(nbr_of_times):    
        one_iteration(coordinates)

def one_iteration(coordinates):
    states, name, lat, lon, countries, hype = create_states(coordinates)
    print(states)

    remaining_locations = {}
    remaining_countries = set()
    i = 0
    for s in states: 
        remaining_countries.add(s.country)
        remaining_locations[s.name] = s
        i+=1
    
    # Creates env, heuristic, search
    env = Environment(states[0], states, remaining_locations, remaining_countries)
    heuristic = DistanceHeuristic(env)
    search = AStar(env, heuristic)

    start = time.time()
    path, last_node = search.a_star(states[0], states[1])
    end = time.time()

    path_names = []
    print("-----------------------------------------------")
    print("PATH\n")
    for s in path: 
        print(s)
        path_names.append(s.name)
    print("-----------------------------------------------")

    df = pd.DataFrame()
    df['name'] = name
    df['country'] = countries
    df['lat'] = lat
    df['lon'] = lon
    df['data'] = 1
    df['hype'] = hype
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
    print("Worse g-values", search.worse_g_value)
    print("Already closed:", search.already_closed)
    print("-----------------------------------------------")

    results = f"Experiment Results \n \
        {len(states)} \n \
        {len(path)} {len(remaining_countries)} \n \
        {round(last_node.g)}\n \
        {last_node.total_hype} \n \
        {round(last_node.g * 156)} \n \
        {end - start} \n \
        {search.nb_node_expansions} \n \
        {search.max_frontier_size} \n \
        {search.worse_g_value} \n \
        {search.already_closed} \n"
    
    with open('results.txt', 'a') as f:
        f.write(results)
    
    # TODO calculate env scor ebased on total distance, and how many flights are domestic or not  

    print("-----------------------------------------------")
    print("Worse g-values", search.worse_g_value)
    print("Already closed:", search.already_closed)
    
    scatter_plot(df, path)

def main():
    # choose file to run
    coordinates = read_input_data('productive_data/100_25.csv')
    #coordinates = parse_coordinates('productive_data/50_30.csv')

    # the number represents how many times the search should be run.
    run_experiments(coordinates, 1)

if __name__=="__main__":
    main()



