"""
File: evo.py
Description: An evolutionary computing framework for multiobjective optimization
"""
import random as rnd
import copy
from functools import reduce
from profiler import profile
import time

class Environment:
    def __init__(self):
        """Environment constructor"""
        self.pop = {}    # evaluation -> solution  eg: ((cost, 5), (time, 3), (dist, 10))->city sequences
        # if two solutions have exact same evaluation treat as duplicates so only one solution exists -> keys are unique
        self.fitness = {}  # objectives/fitness functions: name -> f
        self.agents = {}   # agents: name -> (operator/function, num_solutions_input)
        # number of solutions to feed agent, usually 1 sometimes 2

    def add_fitness_criteria(self, name, f):  # register objectives with population
        """Add or declare an objective to the framework"""
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):  # operator that operates on solutions producing new solutions as output
        """Register a named agent with the framework
        the operator (op) function defines what the agent does
        k defines the number of input solutions that the agent operates on"""
        self.agents[name] = (op, k)

    def add_solution(self, sol):  # need to evaluate solution as add it to population
        """Evaluate and add a solution to the population """
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        # for each name and function, create tuple with name and evauluation of function
        self.pop[eval] = sol

    def size(self):
        """Size of current population"""
        return len(self.pop)

    def get_random_solutions(self, k=1):
        """Pick k random solutions from the population and return as list"""
        if self.size() == 0:
            return []
        else:
            popvals = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(popvals)) for _ in range(k)]  # generate random choice and return copied solutions

    def run_agent(self, name):
        """Invoke an agent against the population"""
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)  # agents always take in a list of solutions
        self.add_solution(new_solution)

    @staticmethod
    def _dominates(p, q):
        """p, q are the evaluations of the solutions (not actual solutions)"""
        pscores = [score for _, score in p]  # extracting out p and q scores
        qscores = [score for _, score in q]

        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))  # compute all differences

        min_diff = min(score_diffs)
        max_diff = max(score_diffs)

        return min_diff >= 0.0 and max_diff > 0.0  # assuming minimization
        # try to capture idea of p dominates q if p is at least as good as q for every objective but strictly better at one objective

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Environment._dominates(p, q)}
    # find all other points q, where p dominates q, then subtract dominated points from set

    def remove_dominated(self):
        nds = reduce(Environment._reduce_nds, self.pop.keys(), self.pop.keys())
        # start with population keys, then boil down to non dominated keys
        self.pop = {k:self.pop[k] for k in nds}
        # figuring out which keys are non dominated, then looking at solution for keys and rebuilding pop dictionary
        # just has keys from non dominated set, throw out dominated solutions

    @profile
    def evolve(self, n=1, dom=100, status=100, time_max=600):
        current_time = time.time_ns()

        agent_names = list(self.agents.keys())

        for i in range(n):
            pick = rnd.choice(agent_names)
            self.run_agent(pick)

            if i % dom == 0:  # every dom number of generations remove dominated points
                self.remove_dominated()

            if i % status == 0:
                print("Iteration:", i)
                print("Population Size:", self.size())
                print(self)

            if (time.time_ns() - current_time)/10**9 > time_max:
                break

        self.remove_dominated()  # cleaning up population one last time

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval, sol in self.pop.items():
            rslt += str(dict(eval)) + "\n"
            # for each solution convert evaluation and solution to string and then output
        return rslt




