import copy
import pandas as pd
import awoc 
import collections

State = collections.namedtuple('State',('name', 'location', 'country', 'hype', 'continent', 'visited'))

class Environment:

    def __init__(self, start_state, locations, remaining_locations, remaining_countries):
        self.current_state = start_state
        self.start_state = start_state
        self.remaining_locations = remaining_locations # actualy states 
        self.remaining_countries = remaining_countries
        self.locations = locations
        self.remaining_continents = ['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America']
        
        self.visited_countries = set()
        self.awoc = awoc.AWOC()
        self.continents_with_countries = {}

    
    def missing_country(self, node):
        list = []
        state = node.state
        countries_in_continent = self.awoc.get_countries_list_of(state.continent)
        for name, s in self.remaining_locations.items(): 
            #print("------------")
            #print("s.country", s.country)
            #print("countries in cont", countries_in_continent)
            #print("path", node.path_so_far)

            #print("visited_countr", node.visited_countries)
            #print("------------")

            if s.country in countries_in_continent and s.country not in node.visited_countries:
                list.append(s)
        #print("MISSING", list)
        '''
        TODO 
        what do we want to do if list is empty
        because that means that the other countries aren't in this continent
        '''
        return list

    def get_locations(self, node, continent):
        rem = copy.deepcopy(self.remaining_locations)
        list = []
        if continent not in self.continents_with_countries:
            countries_in_continent = self.awoc.get_countries_list_of(continent)
            self.continents_with_countries[continent] = countries_in_continent
        else:
            countries_in_continent = self.continents_with_countries[continent]
        for name, s in rem.items(): 
            if s.country in countries_in_continent and s.country not in node.visited_countries:
                list.append(copy.deepcopy(s))
        return list, node.visited_countries

    def get_locations_and_create_states(self, node, continent):
        rem = copy.deepcopy(self.remaining_locations)
        list = []
        if continent not in self.continents_with_countries:
            countries_in_continent = self.awoc.get_countries_list_of(continent)
            self.continents_with_countries[continent] = countries_in_continent
        else:
            countries_in_continent = self.continents_with_countries[continent]
        for name, s in rem.items(): 
            if s.country in countries_in_continent and s.country not in node.visited_countries:
                list.append(copy.deepcopy(s))
        return list, node.visited_countries
    
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
        #print("CONT", continent)
        #print("NEXT", next_continent)
        return next_continent
    
    def get_valid_locations(self, node):
        rem = copy.deepcopy(self.remaining_continents)

        continent = node.state.continent
        locations, node_visited_countries = self.get_locations(node, continent)

        checked_continents = set(continent)
        while len(locations) == 0 and len(checked_continents) != len(rem):
            checked_continents.add(continent)

            if node.visited_countries:
                if all(item in node.visited_countries for item in locations):
                    rem.remove(continent)
                if rem:
                    # TODO do this smarter
                    #continent = rem[0]
                    continent = self.get_next_continent(rem, continent)
                    locations, node_visited_countries = self.get_locations(node, continent)
                else:
                    break
        if locations:
            return self.create_states_for_valid_locations(locations, node_visited_countries)
        return locations
    
    def create_states_for_valid_locations(self, locations, node_visited_countries):
        new_states = []
        '''
        TODO
        We need to get visited countries here somehow 
        '''
        '''
        TODO
        Create the new states as we're appeding the valid locations instead of looping again  
        '''
        for l in locations:
            new_states.append(State(l.name, l.location, l.country, l.hype, l.continent, tuple(node_visited_countries)))

        return new_states


    def is_goal_state(self, state):
        # it is a goal state if all venues has been visited 
        # and if we are back in the start state
        return len(state.remaining_locations) == 0 and state == self.start_state

    def get_current_state(self):
        return self.current_state

    # TODO: should return a list of legal successor states
    # Probably all remaining venues except the goal? 
    # Problem: the goal state is probably the start state
    # 
    def get_successor_states(self, state):
        pass

