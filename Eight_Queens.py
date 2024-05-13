# Importing the numpy library as np
import numpy as np

# Function to initialize the population with random positions for 8 queens
def init_pop(pop_size):
    # Generating a random population of size pop_size, where each individual represents a placement of 8 queens on the board
    return np.random.randint(8, size=(pop_size, 8))

# Function to calculate the fitness value for each individual in the population
def calc_fitness(population):
    # Initialize an empty list to store fitness values for each individual
    fitness_vals = []
    # Iterate over each individual in the population
    for x in population:
        # Initialize penalty for the current individual
        penalty = 0
        # Iterate over each queen position in the current individual
        for i in range(8):
            r = x[i]  # Row of the current queen
            # Check if any other queen threatens the current queen
            for j in range(8):
                if i == j:
                    continue
                d = abs(i - j)  # Calculate the distance between the two queens
                # Check if the other queen is in the same column or diagonals as the current queen
                if x[j] in [r, r - d, r + d]:
                    penalty += 1  # Increment penalty if threat is detected
        fitness_vals.append(penalty)  # Add penalty to the fitness values list
    # Return the fitness values as a numpy array
    #  Negative values are used to represent fitness, where lower penalty is better
    return -1 * np.array(fitness_vals)

# Function for selection
def selection(population, fitness_vals):
    # Make a copy of fitness values
    probs = fitness_vals.copy()
    # Make all fitness values positive and add 1 to avoid negative values
    probs += abs(probs.min()) + 1
    # Normalize probabilities
    probs = probs / probs.sum()
    N = len(population)
    indices = np.arange(N)
    # Perform selection based on probabilities
    selected_indices = np.random.choice(indices, size=N, p=probs)
    selected_population = population[selected_indices]
    return selected_population

# Function for crossover operation
def crossover(parent1 , parent2 , pc):
    r = np.random.random() # value between 0 and 1
    if r < pc:
        # Choose a random crossover point
        m = np.random.randint(1, 8)
        # Perform crossover to create two children
        child1 = np.concatenate([parent1[:m], parent2[m:]])
        child2 = np.concatenate([parent2[:m], parent1[m:]])
    else:
        # If crossover doesn't occur, children are copies of parents
        child1 = parent1.copy()
        child2 = parent2.copy()
    return child1, child2

# Function for mutation operation
def mutation(individual, pm):
    r = np.random.random()
    if r < pm:
        # Choose a random gene to mutate
        m = np.random.randint(8)
        # Mutate the selected gene to a random value
        individual[m] = np.random.randint(8)
    return individual

# Function for performing crossover and mutation on selected population
def crossover_mutation(selected_pop, pc, pm):
    N = len(selected_pop)
    # Initialize a new population array
    new_pop = np.empty((N, 8), dtype=int)
    # Iterate over pairs of individuals for crossover
    for i in range(0, N, 2):
        parent1 = selected_pop[i]
        parent2 = selected_pop[i + 1]
        # Perform crossover to produce two children
        child1, child2 = crossover(parent1, parent2, pc)
        # Assign children to new population
        new_pop[i] = child1
        new_pop[i + 1] = child2
    # Mutate each individual in the new population
    for i in range(N):
        mutation(new_pop[i], pm)
    return new_pop

# Main function to solve the 8-queens problem using a genetic algorithm
def eight_queens(pop_size, max_generations, pc=0.7, pm=0.01):
    # Initialize the population with random placements of queens
    population = init_pop(pop_size)
    # Initialize the best fitness value found so far to None
    best_fitness_overall = None
    # Iterate over a maximum number of generations
    for i_gen in range(max_generations):
        # Calculate fitness values for the current population
        fitness_vals = calc_fitness(population)
        # Find the index of the individual with the highest fitness value
        best_i = fitness_vals.argmax()
        # Get the best fitness value
        best_fitness = fitness_vals[best_i]
        # Updatebest fitness value and solution if a better solution is found
        if best_fitness_overall is None or best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            best_solution = population[best_i]
        # Print generation number and best fitness value found so far
        print(f'\rgen = {i_gen + 1}  f = {-best_fitness} ', end='')
        # If the optimal solution is found (fitness value is 0), break the loop
        if best_fitness == 0:
            print('\nfound optimal solution')
            break
        # Perform selection to choose individuals for crossover
        selected_pop = selection(population, fitness_vals)
        # Perform crossover and mutation to generate a new population
        population = crossover_mutation(selected_pop, pc, pm)
    # Print a new line to separate the output
    print()
    # Print the best solution found
    print(best_solution)

# Call the main function to solve the 8-queens problem
eight_queens(pop_size=100, max_generations=10000, pc=0.7, pm=0.01)
