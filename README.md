# Final Project in AI course at Reykjavik University

## How to run
1. Create a .csv file using `create_example_data.py`, or use one of the available files in `productive_data`. The list `countries`specify in which countries the locations should be.

2. Specify the .csv file in the main of `run_experiments.py`, as well as the int representing how many times you want to run the experiment. Then execute using `python3 run_experiments.py`.

3. The number of node expansions are printed every 100th expansion, so make sure you see the output.

4. Eventually, when the search finishes, it will open a browser tab and display the chosen route. The results of the experiments are saved to `results.txt`

htmls contains a few route results which are interactive and can be opened, and plots contains the same thing but saved as images.

## Components

### create_example_data
Generates a .csv file, to be used as input data for the state creation, based on a list of country codes. 

### run_experiments
Runs the experiments. In the main it is possible to change which .csv file should be used, and how many times the search should be run.

### environment
Handles retrieveing successor states, and calculates haversine distances.

### search
Contains the A* implementation, as well as a node class. 

### heuristics
A few implementations of different heuristics. 
