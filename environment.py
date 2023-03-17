
class Environment:

    def __init__(self, start_state, locations, remaining_locations, graph):
        self.current_state = start_state
        self.start_state = start_state
        self.remaining_locations = remaining_locations # actualy states 
        self.locations = locations

        self.graph = graph


    def get_remaining_locations(self):
        return self.remaining_locations
    
    def get_next_states(self, node):
        state = node.state
        list = []
        #print("GET NEXT STATES")
        print("REM", self.remaining_locations)
        print(len(self.remaining_locations))
        # if within the same country, only return those states
        for name,s in self.remaining_locations.items(): 
            #print(s.name not in node.visited_locations)
            if state.country == s.country :
                list.append(s)
        
        if len(list) == 0 or len(list) == 1:
            for name, s in self.remaining_locations.items(): 
                if int(s.hype) >= 7:
                    list.append(s)

        if len(list) == 0:
            print("locations:", self.remaining_locations)

            return self.remaining_locations
        else: 
            print("locations:", list)
            return list 
        # otherwise, return all locations with hype over x


        return list


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

    def get_cost(self, state):
        """
            Return the cost of traversing this way
            - Haversing
            - Environemntal Impact
            - Venue size 

        """
        return 1 + 50 * len(state)
