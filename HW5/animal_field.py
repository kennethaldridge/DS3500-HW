"""
File: animal_field.py
Description: Houses code for the Animal and Field classes
"""


import random as rnd
import copy
import numpy as np

class Animal:
    def __init__(self, animal_type, field_size, wrap, **kwargs):
        """Constructor for animal
        :param animal_type: defines whether the animal is a rabbit or fox
        :param field_size: defines the size of the field the animals are in
        :param wrap: True or False whether animals can wrap to other side of the field
        :param kwargs: User defines the max cycles that foxes can go without eating
        """
        self.field_size = field_size
        self.x = rnd.randrange(0, self.field_size)
        self.y = rnd.randrange(0, self.field_size)
        self.wrap = wrap

        self.type = animal_type

        self.k_cycles = 0      # intializes how many generations the animal has gone without eating

        if self.type == 'rabbit':
            self.max_cycles = 0
        elif self.type == 'fox':
            self.max_cycles = kwargs['fox_max_cycles']

    def reproduce(self):
        """Reproduces the animal"""
        return copy.deepcopy(self)

    def eat(self, amount):
        """Animal eats, resetting generations since eaten"""
        if amount > 0:
            self.k_cycles = 0

    def move(self):
        """Moves the animal"""
        move_range = []
        if self.type == 'rabbit':   # rabbit can move up to 1 space away
            move_range = [-1, 0, 1]
        elif self.type == 'fox':  # fox can move up to 2 spaces away
            move_range = [-2, -1, 0, 1, 2]

        if self.wrap:     # if wrap is true, allow animal to wrap around field
            self.x = (self.x + rnd.choice(move_range)) % self.field_size
            self.y = (self.y + rnd.choice(move_range)) % self.field_size
        else:
            self.x = min(self.field_size - 1, max(0, (self.x + rnd.choice(move_range))))
            self.y = min(self.field_size - 1, max(0, (self.y + rnd.choice(move_range))))


class Field:
    """ A field is a patch of grass with 0 or more animals hopping around
    in search of food """

    def __init__(self, growth_rate, size):
        """Constructor for field
        :param growth_rate: Defines growth rate of grass
        :param size: defines size of field
        """
        self.size = size
        self.field = np.ones(shape=(self.size, self.size), dtype=int)
        self.animals = []   # intialize array of animals in field
        self.growth_rate = growth_rate

    def add_animal(self, animal):
        """adds an animal to the array of animals"""
        self.animals.append(animal)

    def move(self):
        """Moves all animals in the field"""
        for animal in self.animals:
            animal.move()
            animal.k_cycles += 1  # add another generation without food to the animals

    def eat(self):
        """ All animals try to eat at their current location """
        for animal in self.animals:
            if animal.type == 'rabbit':   # rabbits eat grass at their current location
                food_amount = self.field[animal.x, animal.y]
                animal.eat(food_amount)
                self.field[animal.x, animal.y] = 0

            elif animal.type == 'fox':
                # find each rabbit that is at the current location of the fox and eat those rabbits
                prey = [a for a in self.animals if a.type == 'rabbit' and a.x == animal.x and a.y == animal.y]
                for prey_animal in prey:
                    animal.eat(1)
                    self.animals.remove(prey_animal)

    def survive(self):
        """ Get the surviving animals in the field"""
        self.animals = [a for a in self.animals if a.k_cycles <= a.max_cycles]  # get all surviving animals

    def reproduce(self):
        """Have animals in field reproduce"""
        born = []

        for animal in self.animals:
            offspring_count = 0

            # only animals that have eaten in the current generation can reproduce
            if animal.type == 'rabbit' and animal.k_cycles == 0:  # rabbits can have 1 or 2 children
                offspring_count = rnd.randint(1, 2)
            elif animal.type == 'fox' and animal.k_cycles == 0:  # foxes can have 1 child
                offspring_count = 1

            for _ in range(offspring_count):
                born.append(animal.reproduce())

        self.animals += born

    def grow(self):
        """Grow back grass"""
        growloc = (np.random.rand(self.size, self.size) < self.growth_rate) * 1  # produce grass at the rate of grass growth
        self.field = np.maximum(self.field, growloc)  # return the new field

    def generation(self):
        """ Run one generation of animal actions """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()
        self.get_total_field()

    def get_animals(self, animal_type):
        """Get all animals of a certain type
        :param animal_type: Type of animal to get
        :return animal_list: list of all the animals of that type in the field
        """
        animal_list = []

        for animal in self.animals:
            if animal.type == animal_type:
                animal_list.append(animal)

        return animal_list

    def count_grass(self):
        """Count the amount of grass in the field"""
        unique, counts = np.unique(self.field, return_counts=True)
        nums = dict(zip(unique, counts))
        return nums[1]

    def get_total_field(self):
        """Get the total field with grass, rabbits, and foxes"""
        rabbits_locs = []
        foxes_locs = []

        # get the animal locations for rabbits and foxes
        for animal in self.animals:
            x = animal.x
            y = animal.y
            if animal.type == 'rabbit':
                rabbits_locs.append((x, y))
            elif animal.type == 'fox':
                foxes_locs.append((x, y))

        # get the field of where the rabbits are
        rabbits_arr = np.zeros((self.size, self.size), dtype=int)
        if len(rabbits_locs) > 0:
            rabbits_arr[tuple(np.array(rabbits_locs).T)] = 2

        # get the field of where the foxes are
        foxes_arr = np.zeros((self.size, self.size), dtype=int)
        if len(foxes_locs) > 0:
            foxes_arr[tuple(np.array(foxes_locs).T)] = 3

        # get the total field array, foxes are 3, rabbits are 2, grass is 1, no grass is 0
        total_field = np.maximum(np.maximum(self.field, rabbits_arr), foxes_arr)

        self.total_field = total_field


