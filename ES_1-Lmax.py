import numpy as np
import enum

class Job:

    def __init__(self, number, process_time, due_date):
        self.number = number
        self.process_time = process_time
        self.due_date = due_date


class Strategy(enum.Enum):
    plus  = "plus"
    comma = "comma"


class ES_SingleMachine:

    def __init__(self):
       pass


    #This method creates an initial population for the Evolution-Strategy.
    #To achieve this the given list of jobs is permutated several times.
    #jobs: A list of Job-Objects
    #size: The desired size of the initial population
    def initial_population(self, jobs, size):

        population = []        

        for i in range(size):
            np.random.shuffle(jobs)
            population.append(jobs[:]) #pass list by value: [:]
        
        return population


    #The main loop of the Evolution-Strategy-Algorithm.
    #population: Initial set of individuals
    #mu: Size of the parent population
    #_lambda: Size of the offspring population
    #strategy: Strategy.plus for (mu+lambda) and Strategy.comma for (mu,lambda)-Selection
    #_iter: Number of iterations for the Evolution-Strategy algorithm    
    def evolution_strategy(self, population, mu, _lambda, strategy, _iter):

        if mu < 2:
            raise ValueError("The mu value must be at least 2.")

        if _lambda < 1:
            raise ValueError("The _lambda value must be at least 1.")

        for i in range(_iter):            
            #Generation cycle of the ES-Algorithm
            parent_pop      = self.tournament_selection(population, mu, 2)
            rec_offspring   = self.recombination(parent_pop, _lambda)
            mut_offspring   = self.swap_mutation(rec_offspring)
            next_generation = self.selection(mut_offspring, parent_pop, mu, strategy)          
            population      = next_generation[:,0]
            #Print the next generation before the start of the next iteration:
            print("Iteration", i+1, ":")
            for k in next_generation:
                print(k[1], " : ", [j.number for j in k[0]])
            #Print the average of all fitness values:
            sum = 0
            for j in next_generation:
                sum = sum + j[1]
            average = sum / len(next_generation)
            print('-' * 65)
            print("Average - Iteration", i+1, ":", average)
            print('-' * 65)

        #Determine the best individual:
        best_ind = next_generation[0][0]
        best_val = next_generation[0][1]

        print("Best job scheduling sequence:")        
        print([j.number for j in best_ind])
        print("Maximum Lateness:")
        print(best_val)

        return (best_ind, best_val)


    #Objective function for the one-machine maximum lateness scheduling problem. 1||Lmax
    #jobs: A list of Job-Objects
    def maximum_lateness(self, jobs):

        t = 0
        lateness = 0

        for j in jobs:
            t = t + j.process_time
            lateness = lateness + max(0, t - j.due_date)

        return lateness


    #Tournament Selection is used to generate a new parent population.
    #population: Initial population of the current generation 
    #number: Number of parents that should be selected
    #k: Number of indiviuals which should be compared during each tournament selection    
    def tournament_selection(self, population, number, k):
                    
        parent_population = []


        for i in range(number):
            #Select k individuals at random from the initial population:
            random_indices     = np.random.choice(len(population), size = k, replace=False)
            population         = np.array(population)
            random_individuals = list(population[random_indices])

            #Determine the fitness of the randomly choosen individuals:
            fitness_werte = []

            for z in random_individuals:
                fitness_werte.append(self.maximum_lateness(z))

            #Add the individual with best (smallest) fitness to the new parent population:
            min_element = random_individuals[np.argmin(fitness_werte)]        
            parent_population.append(min_element)       
        
        return parent_population


    #Replication through recombination with Order Crossover (OX)
    #parent_population: Parent population of the current generation
    #number: Number of offspring that should be generated
    def recombination(self, parent_population, number):        

        rec_offspring = []

        while len(rec_offspring) < number:
            #Select two individuals at random from the parent population:
            random_indices = np.random.choice(len(parent_population), size = 2, replace=False)

            p1 = parent_population[random_indices[0]]
            p2 = parent_population[random_indices[1]]

            #Two offspring individuals are created from the two parent individuals:
            c1 = self.order_crossover(p1, p2)
            c2 = self.order_crossover(p2, p1)
            
            #The second offspring is only added if the desired number hasn't been reached yet:
            rec_offspring.append(c1)

            if len(rec_offspring) < number:                                
                rec_offspring.append(c2)

        return rec_offspring


    #Order Crossover (OX) is applied on two parent individuals.
    #to create one offspring individual. 
    #p1: Parent Individual 1
    #p2: Parent Individual 2
    def order_crossover(self, p1, p2):
        
        #Choose two cut-points:
        cut_1 = int(len(p1)*2/9) #2/9 of all elements are before the first cut point 
        cut_2 = int(len(p1)*6/9) #3/9 of all elements are after the last cut point

        #Recombine p2 starting from the second cut-point:
        segment_3   = p2[cut_2:]
        segment_1u2 = p2[:cut_2]
        child_elements = np.concatenate((segment_3, segment_1u2), axis = 0)

        #Mid-Segment of p1:
        mid_segment = p1[cut_1:cut_2]

        #Remove the mid-segment-elements of p1 from recombined p2:
        mid_indices = []
        for i in mid_segment:
            mid_indices.append(np.where(child_elements == i))
            
        child_elements = np.delete(child_elements, mid_indices)

        #Combine the child elements with the mid segment of p1.
        #Start inserting the child elements after the mid segment.
        #Insert the remaining child elements before the mid segment.
        c_segment_3 = child_elements[:-cut_1]
        c_segment_1 = child_elements[-cut_1:]        
        child = np.concatenate((c_segment_1, mid_segment, c_segment_3), axis = 0)

        return child


    #Variation through Swap-Mutation
    #offspring_ind: A recombined offspring individual
    def swap_mutation(self, offspring_ind):

        #Swap two elements at random inside the offspring individual:
        for child in offspring_ind:
            random_indices = np.random.choice(len(child), size = 2, replace=False)

            random_index1 = random_indices[0]
            random_index2 = random_indices[1]

            swap_value1 = child[random_index1]
            swap_value2 = child[random_index2]
                   
            child[random_index1] = swap_value2
            child[random_index2] = swap_value1

        #Return the mutated offspring individual:
        return offspring_ind


    #Selection of individuals with the best fitness.
    #offspring: Recombined and mutated offspring.
    #parent_population: Parent population of the current generation.
    #number: Number of individuals that should be selected for the next generation.
    #strategy: Strategy.plus for Plus-Selection or Strategy.comma for Comma-Selection
    def selection(self, offspring, parent_population, number, strategy):

        # Type checking:
        if not isinstance(strategy, Strategy):
            raise TypeError('strategy must either be Strategy.plus or Strategy.comma')

        #Best individuals are selected from the offspring and parent population:
        if(strategy == Strategy.plus):
            individuals = np.concatenate((offspring, parent_population), axis = 0)
        #Best individuals are selected from the offspring population only:
        elif(strategy == Strategy.comma):
            individuals = np.array(offspring)

        fitness_of_individuals = []
        
        #Determine the fitness of each individual:
        for i in individuals:
            fitness_of_individuals.append([i, self.maximum_lateness(i)])

        #Sort by fitness and select the best individuals:
        fitness_of_individuals = np.array(fitness_of_individuals)
        min_fitness_indices    = np.argsort(fitness_of_individuals[:,1])[:number]
        best_individuals       = fitness_of_individuals[min_fitness_indices]

        return best_individuals
            
        
if __name__ == '__main__':

    jobs = []

    #Job(number, process_time, due_time)
    jobs.append(Job(1, 4, 6))
    jobs.append(Job(2, 4, 8))
    jobs.append(Job(3, 5, 10))
    jobs.append(Job(4, 2, 15))
    jobs.append(Job(5, 1, 4))
    jobs.append(Job(6, 3, 10))
    jobs.append(Job(7, 4, 17))
    jobs.append(Job(8, 7, 20))
    jobs.append(Job(9, 5, 30))
    jobs.append(Job(10, 3, 30))
    jobs.append(Job(11, 2, 20))
    jobs.append(Job(12, 4, 50))
    jobs.append(Job(13, 6, 40))
    jobs.append(Job(14, 3, 60))
    jobs.append(Job(15, 2, 40))

    machine = ES_SingleMachine()

    #Create an initial population by permuting the given job sequence: 
    initial = machine.initial_population(jobs, 20)

    #Execution of the Evolution-Strategy-Algorithm (4+12)
    minimum = machine.evolution_strategy(initial, 4, 12, Strategy.plus, 100)


    ###Output after first iteration:
    #-----------------------------------------------------------------
    #Iteration 1 :
    #133  :  [9, 11, 5, 6, 4, 1, 14, 10, 2, 8, 13, 3, 12, 15, 7]
    #133  :  [9, 11, 5, 6, 4, 1, 14, 10, 2, 8, 13, 3, 12, 15, 7]
    #176  :  [4, 8, 15, 5, 11, 6, 13, 14, 1, 9, 12, 3, 10, 2, 7]
    #206  :  [14, 8, 3, 2, 4, 5, 12, 15, 9, 13, 10, 1, 7, 6, 11]
    #-----------------------------------------------------------------
    #Average - Iteration 1 : 162.0
    #-----------------------------------------------------------------


    ###Output after last iteration:
    #-----------------------------------------------------------------
    #Iteration 100 :
    #53  :  [5, 1, 2, 6, 4, 7, 11, 3, 9, 10, 15, 13, 8, 12, 14]
    #53  :  [5, 1, 2, 6, 4, 7, 11, 3, 9, 10, 15, 13, 8, 12, 14]
    #53  :  [5, 1, 2, 6, 4, 7, 11, 3, 9, 10, 15, 13, 8, 12, 14]
    #53  :  [5, 1, 2, 6, 4, 7, 11, 3, 9, 10, 15, 13, 8, 12, 14]
    #-----------------------------------------------------------------
    #Average - Iteration 100 : 53.0
    #-----------------------------------------------------------------
    #Best job scheduling sequence:
    #[5, 1, 2, 6, 4, 7, 11, 3, 9, 10, 15, 13, 8, 12, 14]
    #Maximum Lateness:
    #53
