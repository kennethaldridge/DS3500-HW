"""
File: cmdline_run.py
Description: Code that allows users to run the animation using command line arguments
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse
import animal_field as af
import numpy as np
import matplotlib.colors as colors

# Default values for each parameter
SIZE = 400  # x/y dimensions of the field
WRAP = True  # When moving beyond the border, do we wrap around to the other side
GRASS_RATE = 0.1  # Probability of grass growing at any given location, e.g., 10%
INIT_RABBITS = 40  # Number of starting rabbits
INIT_FOXES = 10  # Number of starting foxes
SPEED = 1  # Number of generations per frame
MAX_FOX_CYCLES = 10  # How many generations foxes can go without food


def animate(i, field, im):
    """Animation function"""
    for _ in range(SPEED):
        field.generation()
    im.set_array(field.total_field)
    plt.title("Generation: " + str(i * SPEED) + " Grass: " + str(field.count_grass()) +
              " Rabbits: " + str(len(field.get_animals('rabbit'))) +
              " Foxes: " + str(len(field.get_animals('fox'))))
    return im,


def make_plot(field, start_rabbits, start_foxes, field_size):
    """Make a plot after 1000 generations"""
    num_grass = field.count_grass()
    num_rabbits = len(field.get_animals('rabbit'))
    num_foxes = len(field.get_animals('fox'))

    counts_dict = {'Grass': num_grass, 'Rabbits': num_rabbits, 'Foxes': num_foxes}

    plt.bar(list(counts_dict.keys()), list(counts_dict.values()))
    plt.xlabel('Type of Organism')
    plt.ylabel('Counts')
    plt.title(f'Count of Grass, Rabbits, and Foxes After 1000 generations. Start Rabbits: {start_rabbits} Start Foxes: {start_foxes} Field Size: {field_size}')
    plt.savefig('count_viz.jpg')

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Artificial life simulation.')
    parser.add_argument('--grass_growth', type=float, default=GRASS_RATE, help='The rate at which grass grows back')
    parser.add_argument('--k', type=int, default=MAX_FOX_CYCLES, help='How many generations foxes can go without eating')
    parser.add_argument('--size', type=int, default=SIZE, help='Size of the field')
    parser.add_argument("--wrap", help="Whether to allow animals to wrap around the field", action="store_true")
    parser.add_argument('--init_rabbits', type=int, default=INIT_RABBITS, help='Number of initial rabbits')
    parser.add_argument('--init_foxes', type=int, default=INIT_FOXES, help='Number of initial foxes')
    args = parser.parse_args()

    # get all the parse arguments
    grass_growth = args.grass_growth
    max_cycles = args.k
    if args.wrap:
        wrap = True
    else:
        wrap = False
    size = args.size
    init_rabbits = args.init_rabbits
    init_foxes = args.init_foxes

    # Create the ecosystem
    field = af.Field(size=size, growth_rate=grass_growth)

    # Initialize with some animals
    for _ in range(init_rabbits):
        field.add_animal(af.Animal(animal_type='rabbit', field_size=size, wrap=wrap))
    for _ in range(init_foxes):
        field.add_animal(af.Animal(animal_type='fox', fox_max_cycles=max_cycles, field_size=size, wrap=wrap))

    # no grass = black, grass = green, rabbits = blue, foxes = red
    clist = ['black', 'green', 'blue', 'red']
    my_cmap = colors.ListedColormap(clist)

    # Set up the image object
    array = np.zeros(shape=(size, size), dtype=int)
    fig = plt.figure(figsize=(10, 10))
    im = plt.imshow(array, cmap=my_cmap, interpolation='hamming', aspect='auto', vmin=0, vmax=3)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im), frames=1000, interval=1, repeat=False)
    plt.show()

    make_plot(field=field, start_foxes=init_foxes, start_rabbits=init_rabbits, field_size=size)


if __name__ == '__main__':
    main()
