"""
File: drake_equation.py
Description: Using the Distribution object, get an estimate for the Drake Equation of the
"""
from prob_dist import Distribution


def main():
    R = Distribution(type='uniform', min=1.5, max=3.0, bins=10)

    fp = Distribution(type='discrete', dist={1: 1.0})

    ne = Distribution(type='normal', mean=3, sd=1, bins=10)

    f1 = Distribution(type='discrete', dist={1: 1.0})

    fi = Distribution(type='normal', mean=0.75, sd=0.5, bins=10)

    fc = Distribution(type='normal', mean=0.95, sd=0.05, bins=10)

    L = Distribution(type='normal', mean=500, sd=300, bins=10)

    N = R * fp * ne * f1 * fi * fc * L

    print(f'Expected Value: {N.ex_val()}')
    print(f'Standard Deviation: {N.standard_dev()}')
    N.plot(title='Distribution of Drake Equation', yscale='linear', trials=20, bins=10)


if __name__ == "__main__":
    main()