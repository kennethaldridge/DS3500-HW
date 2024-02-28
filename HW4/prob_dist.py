"""
File: prob_dist.py
Description: File containing the class Distribution which represents a probability distribution
"""
import copy
import matplotlib.pyplot as plt
from collections import defaultdict
import math
import continuous_functions as cont
import random
import seaborn as sns


class Distribution:
    """A model for discrete random variables where outcomes are numeric"""

    def __init__(self, type='discrete', dist=None, **kwargs):
        """
        Construct the distribution
        :param type: Specifies if the distribution is discrete, normal or uniform
        """
        if type == 'discrete' and dist is not None:
            self.dist = copy.deepcopy(dist)

        elif type == 'normal':
            self.dist = cont.norm_dist(mean=kwargs['mean'], sd=kwargs['sd'], bin_count=kwargs['bins'], val_count=1000)

        elif type == 'uniform':
            self.dist = cont.uni_dist(a=kwargs['min'], b=kwargs['max'], bins=kwargs['bins'])

        else:
            self.dist = {}  # outcome -> p(outcome)

    def __getitem__(self, x):
        """Returns a probability given a value of the probability distribution"""
        return self.dist.get(x, 0.0)

    def __setitem__(self, x, p):
        """Sets a probability given for a value of the probability distribution"""
        self.dist[x] = p

    def apply(self, other, op):
        """
        Helper apply binary operator to self and other
        :param other: The other distribution to be operated with
        :param op: Operation to be preformed
        :return Z: New distribution
        """
        Z = Distribution()
        items = self.dist.items()
        oitems = other.dist.items()

        for x, px in items:
            for y, py in oitems:
                Z[op(x, y)] += px * py
                # value is sum, probability is multiplication of probabilities

        return Z

    def applyscalar(self, a, op):
        """
        Helper function to apply a scalar operator to the distribution
        :param a: scalar value
        :param op: operator to preform
        :return: New distribution
        """
        Z = Distribution()
        items = self.dist.items()

        for x, p in items:
            Z[op(x, a)] += p

        return Z

    def __add__(self, other):
        """Distribution addition operator"""
        return self.apply(other, lambda x, y: x + y)

    # one side of equation is not DRV, just number, scalar has to be left side
    def __radd__(self, a):
        """Scalar addition operator"""
        return self.applyscalar(a, lambda x, c: c + x)

    def __sub__(self, other):
        """Distribution subtraction operator"""
        return self.apply(other, lambda x, y: x - y)

    def __rsub__(self, a):
        """Scalar subtraction operator"""
        return self.applyscalar(a, lambda x, c: c - x)

    def __mul__(self, other):
        """Distribution multiplication operator"""
        return self.apply(other, lambda x, y: x * y)

    def __rmul__(self, a):
        """Scalar multiplication operator"""
        return self.applyscalar(a, lambda x, c: c * x)

    def __truediv__(self, other):
        """Distribution division operator"""
        # might require div by 0 handling
        return self.apply(other, lambda x, y: x / y)

    def __pow__(self, other):
        """Distribution power operator"""
        return self.apply(other, lambda x, y: x ** y)

    def __repr__(self):
        """String representation of the distribution"""
        xp = sorted(self.dist.items())
        rslt = ''

        for x, p in xp:
            rslt += str(round(x, 8)) + " : " + str(round(p, 8)) + "\n"

        return rslt

    def random_sample(self):
        """
        Builds a random sample of values based on a discrete probability distribution
        :return: a random sample of values
        """
        return random.choices(population=list(self.dist.keys()),
                              weights=list(self.dist.values()), k=1)[0]

    def cum_dist(self):
        """
        Builds the cumulative distribution from the probability distribution
        :return cum_dist: the cumulative distribution
        """
        cum_dist = defaultdict()  # initialize cumulative probability distribution dict
        cum_prob = 0.0  # initialize cumulative probability

        for x, p in self.dist.items():
            cum_prob += p
            cum_dist[x] = cum_prob

        return cum_dist

    def plot(self, title='', yscale='linear', show_cum_dist=False, trials=0, bins=20):
        """
        Plots the probability distribution
        :param title: The title of the plot
        :param yscale: The y-axis scale, can be a linear or logarithmic scale
        :param show_cum_dist: Whether to show the cumulative distribution line
        :param trials: The number of points to sample when using a random sample of the distribution
        :param bins: The number of bins to use when plotting a distribution with a random sample
        """

        # add line that shows cumulative distribution
        if show_cum_dist:
            cum_dist = self.cum_dist()
            plt.plot(list(cum_dist.keys()), list(cum_dist.values()))

        if trials == 0:
            plt.bar(list(self.dist.keys()), list(self.dist.values()))

        else:
            sample = [self.random_sample() for i in range(trials)]
            sns.displot(sample, kind='hist', stat='probability', bins=bins)

        plt.yscale(yscale)  # set scale
        plt.xlabel('Value x')
        plt.ylabel('Probability p(x)')
        plt.title(title)
        plt.show()

    def ex_val(self):
        """
        Finds the expected value of the distribution
        :return ex: the expected value of the distribution
        """
        ex = 0  # initialize expected value at 0
        for x, prob in self.dist.items():
            ex += (x * prob)

        return ex

    def standard_dev(self):
        """
        Finds the standard deviation of the distribution
        :return: the standard deviation of the distribution
        """
        var = 0
        ex = self.ex_val()

        for x, p in self.dist.items():
            var += p * ((x-ex)**2)

        return math.sqrt(var)
