import copy
import pandas as pd
import awoc 
import collections
import math 
State = collections.namedtuple('State',('name', 'location', 'country', 'hype', 'continent', 'visited'))

class Environment:

    def __init__(self, start_state, locations, remaining_locations, countries):
        self.current_state = start_state
        self.start_state = start_state
        self.remaining_locations = remaining_locations # actualy states 

        self.countries = countries
        self.locations = locations
        self.listf_of_continents = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
        
        self.visited_countries = set()
        self.awoc = awoc.AWOC()
        self.continents_with_countries = {}
        self.created_states = {}

    def missing_country(self, node):
        list = []
        state = node.state
        countries_in_continent = self.awoc.get_countries_list_of(state.continent)
        for name, s in self.remaining_locations.items(): 
            if s.country in countries_in_continent and s.country not in node.visited_countries:
                list.append(s)
        '''
        TODO 
        what do we want to do if list is empty
        because that means that the other countries aren't in this continent
        '''
        return list
    
    def haversine(self, coord1, coord2):
        '''
            Caculates the haversine distance between two nodes. 
        '''
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

        return km

    # maybe cache remaining countries
    # cached_remaining_countries[state] = state.visited

    def get_locations_and_create_states(self, node, continent):
        self.remaining_locations
        list = []
        if continent not in self.continents_with_countries:
            countries_in_continent = self.awoc.get_countries_list_of(continent)
            self.continents_with_countries[continent] = countries_in_continent
        else:
            countries_in_continent = self.continents_with_countries[continent]

        '''
            TODO
            We don't want to loop through all of these elements every time.
            Would be nice to only loop through the ones that are actually legal
            And the ones that have not been visited yet
            Idea is to use a cache somehow
        '''
        for name, s in self.remaining_locations.items(): 
            if s.country in countries_in_continent and s.country not in node.visited_countries:
                new_state = State(s.name, s.location, s.country, s.hype, s.continent, tuple(node.visited_countries))
                self.created_states[new_state] = new_state
                list.append(new_state)
        #print("LIST:", list)
        return list
    
    def get_next_continent(self, rem, continent):
        remaining_continents = rem
        neighbour = {
            'North America': 'South America',
            'South America': 'Africa',
            'Africa': 'Europe',
            'Europe': 'Asia',
            'Asia': 'Oceania',
            'Oceania': 'Antarctica',
            'Antarctica': 'North America'
        }
        next_continent = neighbour[continent]
        while next_continent not in remaining_continents:
            next_continent = neighbour[next_continent]
        return next_continent
    
    def get_valid_locations(self, node):
        self.listf_of_continents = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']      
        rem = self.listf_of_continents
        continent = node.state.continent
        locations = self.get_locations_and_create_states(node, continent)

        checked_continents = set(continent)
        while len(locations) == 0 and len(checked_continents) != len(rem):
            checked_continents.add(continent)
            node.visited_continents.add(continent)

            if node.visited_countries:
                if all(item in node.visited_countries for item in locations):
                    rem.remove(continent)
                if rem:
                    continent = self.get_next_continent(rem, continent)
                    locations = self.get_locations_and_create_states(node, continent)
                else:
                    break
        return locations
    
