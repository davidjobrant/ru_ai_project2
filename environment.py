import copy
import pandas as pd
import awoc 
class Environment:

    def __init__(self, start_state, locations, remaining_locations, remaining_countries):
        self.current_state = start_state
        self.start_state = start_state
        self.remaining_locations = remaining_locations # actualy states 
        self.remaining_countries = remaining_countries
        self.locations = locations
        self.remaining_continents = ['North America', 'South America', 'Africa','Europe']
        #self.remaining_continents = ['Asia', 'Africa', 'North America', 'South America', 'Antarctica', 'Europe', 'Australia']

        self.visited_countries = set() # because of starting node
        self.awoc = awoc.AWOC()


    def get_remaining_locations(self):
        return self.remaining_locations
    

    def chat_gpt_heuristic(self, node, env):
        print( env.remaining_locations)
        state = node.state
        unvisited_states = [s for s in env.remaining_locations.values() if s.country not in node.visited_countries]
        remaining_continents = set(s.continent for s in unvisited_states)
        if state.country not in node.visited_countries:
            remaining_continents.add(state.continent)
        continent_priority = {}
        for continent in remaining_continents:
            count = sum(1 for s in unvisited_states if s.continent == continent)
            continent_priority[continent] = count
        max_priority_continent = max(continent_priority, key=continent_priority.get)
        if state.continent == max_priority_continent:
            return 0
        else:
            return max_priority_continent
    
    def get_next_states(self, node):
        state = node.state
        list = []
        #print("GET NEXT STATES")
        print("REM", self.remaining_locations)
        print(len(self.remaining_locations))
        #if len(self.remaining_locations) > 2:
        rem = copy.deepcopy(self.remaining_locations)
            #rem.pop("J")
        # if within the same country, only return those states
        for name,s in rem.items(): 
            #print(s.name not in node.visited_locations)
            if state.country == s.country:
                list.append(s)
        
        # TODO somehow prioritize finishing a country first! idk how? 
        if len(list) == 0 or len(list) == 1:
            for name, s in rem.items(): 
                if int(s.hype) >= 9:
                    list.append(s)

        if len(list) == 0:
            print("locations:", rem)

            return rem
        else: 
            print("locations:", list)
            return list 
        # otherwise, return all locations with hype over x

    def get_neigbours(self, country):
        neighbours = pd.read_csv('data/neighbours.csv')
        print("COUNTRY",country)
        return neighbours.loc[neighbours['country_code'] == country]
    
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

    def old_get_locations(self, node, continent):
        rem = copy.deepcopy(self.remaining_locations)
        list = []
        countries_in_continent = self.awoc.get_countries_list_of(continent)
        for name, s in rem.items(): 
            #print("s.country", s.country)
            #print("visited_countries", node.visited_countries)
            #print(s.country in countries_in_continent and s.country not in node.visited_countries)

            if s.country in countries_in_continent and s.country not in node.visited_countries:
                list.append(s)
        #print("AFTER CONTINENT", list)
        return list

        # if all locations within a continent are visited, move on to the next continent

    def get_locations(self, node, continent):
        rem = copy.deepcopy(self.remaining_locations)
        list = []
        countries_in_continent = self.awoc.get_countries_list_of(continent)
        for name, s in rem.items(): 
            if s.country in countries_in_continent and s.country not in node.visited_countries:
                list.append(copy.deepcopy(s))
        return list
    
    def get_valid_locations(self, node):
        rem = copy.deepcopy(self.remaining_continents)

        continent = node.state.continent
        locations = self.get_locations(node, continent)

        checked_continents = set(continent)
        while len(locations) == 0 and len(checked_continents) != len(rem):
            checked_continents.add(continent)

            if node.visited_countries:
                if all(item in node.visited_countries for item in locations):
                    rem.remove(continent)
                if rem:
                    continent = rem[0]
                    locations = self.get_locations(node, continent)
                else:
                    break
        return locations
    

    def old_get_valid_locations(self, node):
        state = node.state
        list = []
        #print("VISITED", self.visited_countries)
        #print("REM", self.remaining_locations)
        #print(len(self.remaining_locations))
        rem = copy.deepcopy(self.remaining_locations)
        #if len(self.remaining_locations) > 2: 
        #    if "J" in self.remaining_locations:
        #        rem.pop("J")

        # if country population over 100M: return within same country
        # if not, return locations in bordering countries
        #neighbours = self.get_neigbours(state.country)['neighbor_name'].values.tolist()
        #print("NEIGHBOURS", neighbours)
        #for name, s in rem.items(): 
        #    if s.country in neighbours and s.country not in self.visited_countries:
        #        list.append(s)
        #print("AFTER NEIGHBOURS", list)
        rem = copy.deepcopy(self.remaining_continents)

        continent = state.continent
        locations = self.get_locations(node, continent)
        #if node.visited_countries:
        #    if all(item in node.visited_countries for item in locations):
        #        print("removing ", continent)
        #            # TODO replace wth check to make sure we find all locations
        #        self.remaining_continents.remove(continent)
        checked_continents = set(continent)
        # while len(locations) == 0 and len(checked_continents) != len(rem):
        #     #print("V1", node.visited_countries)
        #     #print("L2",locations)
        #     if node.visited_countries:
        #         # TODO THIS check does not make sense here becaus list is always gonna have length 0
        #         print("visited countries", node.visited_countries)
        #         if all(item in node.visited_countries for item in locations):
        #             print("removing ", continent)
        #                 # TODO replace wth check to make sure we find all locations
        #             rem.remove(continent)
            
        #         continent = rem[0]
        #         locations = self.get_locations(node, continent)
        #         checked_continents.add(continent)

        list = locations
        #print("LIST", list)

        # countries_in_continent = self.awoc.get_countries_list_of(state.continent)
        # print("count in cont", countries_in_continent)
        # if state.continent in self.remaining_continents:
        #     self.remaining_continents.remove(state.continent)

        # # get the locations for these countries 
        # for name, s in rem.items(): 
        #     #print("s.country", s.country)
        #     #print("visited_countries", node.visited_countries)
        #     print(s.country in countries_in_continent and s.country not in self.visited_countries)

        #     if s.country in countries_in_continent and s.country not in self.visited_countries:
        #         list.append(s)
        # print("AFTER CONTINENT", list)

        # # if no bordering countries, then look at continents 
        # # TODO somehow need to keep track of when we're "done" with a continent?
        # #if len(list) == 0:
        # #    for name, s in rem.items(): 
        # #        print(s.country)
        # #        print(s.country in neighbours)
        # #        if state.continent == s.continent:
        # #            list.append(s)
        # #            #self.visited_countries.append(s)
        # #    print(list)
        
        # # TODO somehow prioritize finishing a country first! idk how? 
        # #if len(list) == 0 or len(list) == 1:
        # #    for name, s in rem.items(): 
        # #       if int(s.hype) >= 9:
        # #            list.append(s)

        # if len(list) == 0:
        #     # means we're done with this continent 
        #     # pick closest continent:
        #     print(self.remaining_continents)
        #     continent = self.remaining_continents[0]
        #     countries_in_continent = self.awoc.get_countries_list_of(continent)
        #     print("visited_countries", node.visited_countries)
        #     print("NEW CONTINENT", continent)
        #     if continent in self.remaining_continents:
        #         self.remaining_continents.remove(continent)

        #     for name, s in rem.items(): 
        #         print(s.country in countries_in_continent and s.country not in self.visited_countries)

        #         if s.country in countries_in_continent and s.country not in self.visited_countries:
        #             list.append(s)
        #     print("AFTER 2ND CONTINENT", list)
        #     #list = rem.values()
        # print("LIST", list)
        return list
        #else: 
        #    print("locations:", list)
        #    return list 
        # otherwise, return all locations with hype over x


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

