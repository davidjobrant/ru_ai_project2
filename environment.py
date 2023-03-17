
class Environment:

    def __init__(self, start_state, locations, graph):
        self.current_state = start_state
        self.start_state = start_state
        #self.remaining_locations = remaining_locations

        self.locations = locations

        self.graph = graph


    def get_remaining_locations(self):
        return self.remaining_locations
    
    def get_next_states(self, state):
        list = []

        # if within the same country, only return those states
        for l in self.locations: 
            if state.country

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
