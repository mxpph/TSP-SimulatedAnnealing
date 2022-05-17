import numpy
import matplotlib.pyplot as plt

NUM_CITIES = 50

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance(a, b):
        return ((a.x - b.x)**2 + (a.y - b.y)**2)

    @staticmethod
    def get_total_distance(cities): # City array
        distance = 0
        for i, j in zip(cities[:-1], cities[1:]):
            distance += City.get_distance(i, j)
        distance += City.get_distance(cities[0], cities[-1])

        return distance

if __name__ == '__main__':
    cities = []
    for _ in range(NUM_CITIES):
        cities.append(City(numpy.random.uniform(), numpy.random.uniform()))

    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)
    ax1.set_title("Random")
    ax2.set_title("Simulated annealing")

    # Plot edges
    for i, j in zip(cities[:-1], cities[1:]):
        ax1.plot([i.x, j.x], [i.y, j.y], 'b')
    ax1.plot([cities[0].x, cities[-1].x], [cities[0].y, cities[-1].y], 'b')

    # Plot cities
    for c in cities:
        ax1.plot(c.x, c.y, 'r.')

    # Simulated annealing algorithm
    cost = City.get_total_distance(cities)

    T = 20                  # Temperature
    alpha = 0.98            # Geometric decay constant (0.8 < a < 0.995)
    chain_length = 500      # Chain length

    for i in range(int(numpy.ceil(numpy.log(0.0001/T) / numpy.log(alpha)))):
        print(i, 'cost = ', cost, 'T = ', T)
        T = T * alpha

        for j in range(chain_length):
            # Reverse a section of the tour to obtain a new solution.
            r1, r2 = numpy.random.randint(1, len(cities), size=2)

            if r1 > r2:
                temp = r2
                r2 = r1
                r1 = temp

            store = cities.copy()
            cities = cities[0:r1] + cities[r2:(r1-1):-1] + cities[(r2+1):] # Reverse section

            # Determine the cost of this new solution.
            cost_new = City.get_total_distance(cities)

            # If the new cost is lower, always accept this solution.
            if cost_new < cost:
                cost = cost_new
            else:
                # Otherwise, accept this solution according
                # to the probability acceptance function
                x = numpy.random.uniform()
                if x < numpy.exp(-(cost_new - cost) / T):
                    cost = cost_new
                else:
                    # If not accepted then swap back.
                    cities = store

    # Plot simulated annealing solution
    for i, j in zip(cities[:-1], cities[1:]):
        ax2.plot([i.x, j.x], [i.y, j.y], 'b')
    ax2.plot([cities[0].x, cities[-1].x], [cities[0].y, cities[-1].y], 'b')

    for c in cities:
        ax2.plot(c.x, c.y, 'r.')

    plt.show()

