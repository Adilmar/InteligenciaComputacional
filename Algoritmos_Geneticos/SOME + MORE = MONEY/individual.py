#!/usr/bin/python
# D. Vrajitoru, C463/B551 Spring 2008

# A class implementing an individual to use with the genetic algorithm.

# An individual or chromosome is a simple list of values.
# A population is a list of individuals

from random import *

# A shallow copy of a list
def copy_list(list):
    newlist = []
    for x in list:
        newlist.append(x)
    return newlist

class Individual:
    def __init__(self, size=0):
        self.chromosome = []
        for i in range(size):
            self.chromosome.append(0)
        self.size = size
        self.fit = 0

    # A function that will be called when we use an object of this
    # class in a print statement. It should return a string.
    def __repr__(self):
        s = "chr: %s f: %f len: %d" %(str(self.chromosome),
                                      self.fit, self.size)
        return s

    # A copy function that might come in useful
    def copy(self):
        ind = Individual()
        ind.chromosome = copy_list(self.chromosome)
        ind.fit = self.fit
        ind.size = self.size
        return ind

    # Initialize an individual from a regular list.
    def fromlist(self, L):
        self.size = len(L)
        self.chromosome = copy_list(L)
        self.fit = 0

    # This function compares two objects of type individual by
    # comparing their fitness values. This should make the sorting of
    # a whole population by the fitness easier. Whenever we write
    # something like ind1 < ind2, this function is used.
    def __cmp__(self, other):
        if self.fit < other.fit:
            return -1
        elif self.fit == other.fit:
            return 0
        else:
            return 1

    # A function creating a random configuration of genes in the
    # individual.
    def init_random(self, limit=10):
        for i in range(self.size):
            self.chromosome[i] = randint(0,limit-1) # 0-9

    # A mutation that replaces a gene with its opposite. Our genes
    # here have an decimal representation 0-9, so the opposite of a
    # value is 9-value
    def mutation_opp(self, prob):
        for i in range(self.size):
            r = random() # float between 0 and 1
            if r <= prob:
                self.chromosome[i] = 9-self.chromosome[i]

    # The 1-point crossover. The change happens in place. We'll assume
    # that the parents have the same size.
    def crossover_1pt(self, parent2):
        site = randint(0,self.size-1)
        for i in range(site):
            self.chromosome[i],parent2.chromosome[i] = parent2.chromosome[i],self.chromosome[i] # the famous swap
            
if __name__ == '__main__':
    x = Individual(10)
    x.init_random()
    print x
    x.mutation_opp(1) # should give us the complete opposite
    print x
    p1 = Individual(20)
    p2 = Individual(20)
    p1.init_random()
    p2.init_random()
    print "Parents:\n", p1, "\n", p2
    p1.crossover_1pt(p2)
    print "Children:\n", p1, "\n", p2
    
## Example of run:
## chr: [5, 9, 2, 8, 6, 8, 4, 3, 0, 8] f: 0.000000 len: 10
## chr: [4, 0, 7, 1, 3, 1, 5, 6, 9, 1] f: 0.000000 len: 10
## Parents:
## chr: [1, 2, 2, 1, 1, 7, 7, 1, 7, 7, 6, 7, 3, 2, 2, 0, 2, 3, 1, 2] f: 0.000000 len: 20
## chr: [6, 7, 2, 7, 7, 6, 2, 9, 3, 0, 8, 3, 5, 3, 7, 1, 9, 7, 0, 9] f: 0.000000 len: 20
## Children:
## chr: [6, 7, 2, 7, 7, 6, 2, 9, 7, 7, 6, 7, 3, 2, 2, 0, 2, 3, 1, 2] f: 0.000000 len: 20
## chr: [1, 2, 2, 1, 1, 7, 7, 1, 3, 0, 8, 3, 5, 3, 7, 1, 9, 7, 0, 9] f: 0.000000 len: 20
