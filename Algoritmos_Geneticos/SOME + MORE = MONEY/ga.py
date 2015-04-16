#!/usr/bin/python
# D. Vrajitoru, C463/B551 Spring 2008

# A simple genetic algorithm to solve a cryptarythmetic problem.

from individual import *

# A wrapper function for the evaluation so that we can evaluate
# something else with a minimum of reprogramming.
def eval_ind(ind):
    eval_sendmoremoney(ind)

# Compute the fitness based on the cryptarithmetic problem:
#   S E N D +
#   M O R E 
# ========= =
# M O N E Y
def eval_sendmoremoney(ind):
    D = ind.chromosome[0]
    E = ind.chromosome[1]
    M = ind.chromosome[2]
    N = ind.chromosome[3]
    O = ind.chromosome[4]
    R = ind.chromosome[5]
    S = ind.chromosome[6]
    Y = ind.chromosome[7]
    x1 = ind.chromosome[8]
    x2 = ind.chromosome[9]
    x3 = ind.chromosome[10]
    fitness = 0
    fitness += eval_plus(D, E, Y, x1)
    fitness += eval_plus(N, R, E, x2)
    fitness += eval_plus(E, O, N, x3)
    fitness += eval_plus(S, M, O, M)
    # Add 0.1 for every gene in the chromosome that is unique:
    for i in range(ind.size):
        if (not ind.chromosome[i] in ind.chromosome[0:i] and
            not ind.chromosome[i] in ind.chromosome[(i+1):(ind.size-1)]):
            fitness += 0.1
    ind.fit = fitness

# Returns a value that is maximal when
# A+B = C and x=0 or A+B=10+C and x=1
def eval_plus(A, B, C, x):
    # val1 computes the difference between A+B anc C, divides it by 18
    # which is the maximum possible to get a value between 0 and 1,
    # and then takes 1- this value to returne the maximum value when
    # A+B=C. Then adds a similar quantity for x such that the maximum
    # value is obtained when x = 0
    val1 = 1.0 - abs(A+B-C)/18.0 + 1-x/9.0
    # val2 computes the same thing for A+B = 10+C 
    val2 = 1.0 - abs(A+B-10-C)/19.0 + 1-abs(x-1)/9.0
    return max(val1, val2)

# An implementation of the fitness-proportionate selection. We pass in
# the cdf of the fitness as a parameter because we don't want to
# recompute it for every new individual that we want to select. The
# function returns the index of the selected individual.
def selection(cdf):
    size = len(cdf)
    r = random() * cdf[size-1]
    i = 0
    while cdf[i] < r:
        i += 1
    return i

# Builds a new generation from an existing one.
# mutt is a flag for the mutation type: 1 - opposite, 2 = random
# cp is a probability of crossover
# cm is a probability for mutation, passed on to the mutation function.
# elite is a flag for the elitist option: 0 no, 1 yes
def new_generation(population, mutt=1, cp=0.8, cm=0.01, elite=0):
    try:
        pop_size = len(population)
    except:
        print population
    cdf = [population[0].fit]
    for i in range(1,pop_size):
        cdf.append(cdf[len(cdf)-1]+population[i].fit)
    new_gen = []
    for i in range(pop_size/2):
        p1 = selection(cdf)
        p2 = selection(cdf)
        c1 = population[p1].copy()
        c2 = population[p2].copy()
        r = random()
        if r <= cp:
            c1.crossover_1pt(c2)
        if mutt == 1:
            c1.mutation_opp(cm)
            c2.mutation_opp(cm)
        new_gen.append(c1)
        new_gen.append(c2)
    if elite:
        new_gen.append(population[pop_size-1].copy())
    # We are sorting the population by the fitness but we would really
    # only need to move the best one to the end of the population.
    for i in range(pop_size):
        eval_ind(new_gen[i])
    new_gen.sort()
    return new_gen

# Initializes a population with a given number of random individuals
# of a given size. Then it evaluates all of them and sorts the
# population by fitness. It returns this population.
def random_population(ind_size, pop_size):
    population = []
    for i in range(pop_size):
        ind = Individual(ind_size)
        ind.init_random()
        eval_ind(ind)
        population.append(ind)
    population.sort()
    return population

# The mighty genetic algorithm itself with a given number of generations.
def run_ga(ind_size, pop_size, gen_number,
           mutt=1, cp=0.8, cm=0.01, elite=0):
    population = random_population(ind_size, pop_size)
    print "Starting from the best individual:", population[pop_size-1]
    for i in range(gen_number):
        new_gen = new_generation(population, mutt, cp, cm, elite)
        del population[0:pop_size]
        population = new_gen
    print "The best solution is:", population[pop_size-1]

if __name__ == '__main__':
    run_ga(11, 20, 200, 1, 0.8, 0.01, 1)
