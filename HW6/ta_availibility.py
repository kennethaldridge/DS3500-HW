"""
File: ta_availibility.py
Description: Use evolutionary based computing to assign TAs to labs
"""
from evo import Environment
from profiler import Profiler, profile
import random as rnd
import numpy as np
import pandas as pd
import csv


sections = pd.read_csv('sections.csv')
tas = pd.read_csv('tas.csv')
rows = len(tas)  # get number of TAs to assign
cols = len(sections)  # get the number of lab sections


# Objectives
@profile
def overallocation(array):
    """Sum the number of overallocation penalties for the TAs"""
    return sum((array.sum(axis=1) - np.array(tas['max_assigned']) > 0)) # sum all rows (TAs) and get only those above max assigned


@profile
def time_conflicts(array):
    """Find the number of time conflicts"""
    time_conflict = 0

    for i in range(len(array)):
        assigned_times = set()

        # Iterate through each TA
        for j in array[i]:
            if array[i, j] == 1:
                section_time = sections.loc[j, 'daytime']

                # If a TA is already in that assigned time slot, add another time conflict and then go to the next TA
                if section_time in assigned_times:
                    time_conflict += 1
                    break

                else:
                    assigned_times.add(section_time)

    return time_conflict


@profile
def undersupport(array):
    """Sum number of undersupport penalties for the TAs"""
    return sum((np.array(sections['min_ta']) - array.sum(axis=0)>0))  # Count how many TAs are under the minimum for each section


@profile
def unwilling(array):
    """Find the amount of times a TA was assigned to a section they were unwilling to be assigned to"""
    # convert unpreferred, unwilling, and preffered for each section to an array
    unwill_array = np.array(tas.iloc[:, 3:4 + cols])

    # Set U's to 1 and else to 0
    unwill_array = np.where(unwill_array == 'U', 1, 0)

    # Find where TAs assigned to sections unwilling and then sum up amount
    return np.sum(np.array(unwill_array & array))


@profile
def unpreferred(array):
    """Find amount of times TA was assigned to section they did not prefer to be assigned to"""
    # convert unpreferred, unwilling, and preffered for each section to an array
    unpref_array = np.array(tas.iloc[:, 3:4 + cols])

    # Set W's to 1 and else to 0
    unpref_array = np.where(unpref_array == 'W', 1, 0)

    # Find where TAs assigned to sections unwilling and then sum up amount
    return np.sum(np.array(unpref_array & array))


# Agents
@profile
def toggle_random(solutions):
    """An agent that toggles a random TA/Section assignment"""
    array = solutions[0]

    # get a random row and column
    rand_row = rnd.randint(0, rows-1)
    rand_col = rnd.randint(0, cols-1)

    # toggle the number at that point
    if array[rand_row, rand_col] == 0:
        array[rand_row, rand_col] = 1
    else:
        array[rand_row, rand_col] = 0

    return array


@profile
def get_and(solutions): # potentially do 'and': keep assignment if both sols have assigment
    """An agent that does the 'and' operation (if 1 and 1 keep 1, else 0)"""
    array1 = solutions[0]
    array2 = solutions[1]

    return array1 & array2


@profile
def swap_assignments(solutions):
    """Swap each assignment (0 -> 1 and 1 -> 0)"""
    array = solutions[0]

    return (~array) + 2  # the ~ reverses bits (for integer is (-x) - 1, so add by 2 to swap 0s and 1s)


def main():

    # create the environment
    E = Environment()

    # register the fitness functions
    E.add_fitness_criteria("overallocation", overallocation)
    E.add_fitness_criteria("time_conflicts", time_conflicts)
    E.add_fitness_criteria("undersupport", undersupport)
    E.add_fitness_criteria("unpreferred", unpreferred)
    E.add_fitness_criteria("unwilling", unwilling)

    # register the agents
    E.add_agent("toggle_random", toggle_random, k=1)
    E.add_agent("get_and", get_and, k=2)
    E.add_agent("swap_assignments", swap_assignments, k=1)

    # Adding 2 initial solutions
    array1 = np.random.randint(low=0, high=2, size=(rows, cols))
    E.add_solution(array1)
    array2 = np.random.randint(low=0, high=2, size=(rows, cols))
    E.add_solution(array2)

    # Run the evolver
    E.evolve(1000000, 1000, 1000, time_max=600)

    # Print final result
    print(E)

    # Report time
    Profiler.report()

    # Initialize list of solution dictionaries and column headers
    sols_list = list()
    col_headers = list()

    # Iterate through solutions
    for i, eval in enumerate(E.pop.keys()):
        # Turn solution into dictionary and add to list with the group name
        sol_row = dict(eval)
        sol_row['groupname'] = 'kensidfn'
        sols_list.append(sol_row)

        # First iteration add the keys to column header list
        if i == 0:
            col_headers = list(sol_row.keys())

    with open('solutions.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=col_headers)

        writer.writeheader()

        writer.writerows(sols_list)


if __name__ == "__main__":
    main()
