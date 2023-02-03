# ES_1-Lmax
This Python script uses Evolution Strategy (ES) to minimize maximum lateness on a single machine (1||L<sub>max</sub>).  
## Evolution Strategy (ES)

The implemented Evolution-Strategy-Algorithm uses "Tournament Selection" to generate a new parent population at the beginning of the generation cycle.
It uses Order Crossover (OX) for recombination, followed by Swap Mutation. 
At the end of the generation cycle it uses plus-selection (&mu;+&lambda;) to find the individuals with the best fitness for the next cylce.
## (1||L<sub>max</sub>)

The Evolution-Strategy-Algorithm is trying to find an optimal schedule to minimize maximum lateness on a single machine.  

The (1||L<sub>max</sub>) scheduling problem that is solved by this script consists of following jobs:   

| **Job** | 1 | 2 | 3  | 4  | 5 | 6  | 7  | 8  | 9  | 10 | 11 | 12 | 13 | 14 | 15 |
|---------|:-:|:-:|:--:|:--:|:-:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **_p<sub>j</sub>_**  | 4 | 4 | 5  | 2  | 1 | 3  | 4  | 7  | 5  | 3  | 2  | 4  | 6  | 3  | 2  |
| **_d<sub>j</sub>_**  | 6 | 8 | 10 | 15 | 4 | 10 | 17 | 20 | 30 | 30 | 20 | 50 | 40 | 60 | 40 |

**_p<sub>j</sub>_** = processing time   
**_d<sub>j</sub>_** = due dates  


