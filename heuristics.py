
class Heuristic():
    	# return an estimate of the remaining cost of reaching a goal state from state s

    def __init__(self, env):
        self.env = env
    
    def eval(self, node, end_node):
        raise NotImplementedError()
	
class DistanceHeuristic(Heuristic):
	
    def eval(self, node, end_node):
	    return self.env.haversine(node.state, end_node.state)

class HypeHeuristic(Heuristic):
    def eval(self, node, end_node):
        # hype is a value between 1-10
        hype = int(node.state.hype)
        if hype >= 9:
             return 10 * (10 - hype)
        if hype >= 7: 
            return 50 * (10 - hype)
        if hype >= 5:
            return 100 * (10 - hype)
        return 500 * (10 - hype)

class DjikstraHeuristic(Heuristic):
    def eval(self, node, end_node):
        return 0
    

class DistanceAndCountriesHeuristic(Heuristic):
    def eval(self, node, end_node):
        estimated_distance = self.env.haversine(node.state, end_node.state)
        #print("dist", estimated_distance)
        env_countries = 100 * (len(self.env.countries) - len(node.state.visited))
        #print("countries", env_countries)
        total = estimated_distance + env_countries
        return total

class CountriesHeuristic(Heuristic):
    def eval(self, node, end_node):
        #estimated_distance = self.env.haversine(node.state, end_node.state)
        #print("dist", estimated_distance)
        env_countries = 100 * (len(self.env.countries) - len(node.state.visited))
        #print("countries", env_countries)
        #total = estimated_distance + env_countries
        return env_countries

class DistanceAndHyperHeuristic(Heuristic):
    def eval(self, node, end_node):
	    return self.env.haversine(node.state, end_node.state)