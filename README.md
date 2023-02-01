# ES_1-Lmax
This Python script uses Evolution Strategy (ES) to minimize maximum lateness on a single machine (1||L<sub>max</sub>).  
## Evolution Strategy (ES)

The implemented Evolution-Strategy-Algorithm uses "Tournament Selection" to generate a new parent population at the beginning of the generation cycle.
It uses Order Crossover (OX) for recombination, followed by Swap Mutation. 
At the end of the generation cycle it uses plus-selection to find the individuals with the best fitness for the next cylce.
