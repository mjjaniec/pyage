[![Stories in Ready](https://badge.waffle.io/vucalur/pyage.png?label=ready&title=Ready)](https://waffle.io/vucalur/pyage)
[![Build Status](https://travis-ci.org/vucalur/pyage_shopping.svg)](https://travis-ci.org/vucalur/pyage_shopping)
# Job scheduling problems with pyage platform - Computational intelligence

## Team
* Michał Janiec
* Wojciech Krzystek

Contact: See committer emails :)

## Theoretical background

### Flow shop

1. <http://www.flowshop.mfbiz.pl/sformulowanie-problemu.php> (Polish only)
1. Anna Ławrynowicz _Genetic algorithms for advanced planning and scheduling in supply networks_, Difin, 2013 ( *GAFAPAS* )  
par. Scheduling in various machine environments p.34-36

### Open shop

1. <http://en.wikipedia.org/wiki/Open-shop_scheduling>
1. Solving open shop with GA: *GAFAPAS* par. Open shop scheduling problem p. 112-113

### Crossover operators
1. *GAFAPAS* chapt. 3.5. Crossover, par. Cycle crossover (CX) p. 62-67

### EMAS

1. <https://www.age.agh.edu.pl/agent-based-computing>


## Running
### Single-run instructions
As described here: <https://github.com/maciek123/pyage/wiki#running-your-own-configuration>  
With proper config from [pyage/conf folder](https://github.com/vucalur/pyage_shopping/tree/master/pyage/conf)

**Example:**

`flowshop_emas_conf.py` - Basic config of flow shop solver with EMAS approach, local machine only.   
Solves small problem (the first one from [`tai20x5.txt`](https://github.com/vucalur/pyage_shopping/blob/master/input_data/tai20_5.txt))
Calculations are terminated after 10 seconds and the best found solution is returned

### More sophisticated benchmarks
`launcher.py` - Facilitates execution automation and collecting results.
Can be used for repeating execution for single configuration or running multiple configurations in series.  
*Warning:* Executing cartesian product of different configurations can take long time.
Calculations for benchmarks (below) took about 48hrs.

## Algorithm interface
### Input
* `time_matrix` - matrix of execution times of a particular job on a particular processor.  
Format: `time_matrix[processor_id][job_id]` denotes time needed to perform job `job_id`th on the `processor_id`th processor.  
See [`input_data` folder](https://github.com/vucalur/pyage_shopping/blob/master/input_data/) for more benchmarks for the solver.  
Due to characteristics of the problem (NP), strict solutions are unknown, but acceptable makespan range is specified for each.
  
### Output
* `makespan` - total time needed to process all the jobs
* permutation yielding calculated `makespan`. for further clarification see: [PermutationGenotype documentation](https://github.com/vucalur/pyage_shopping/blob/master/pyage/solutions/evolution/genotype.py)
* `results` (flow shop only) - `results[processor_id][job_id]` is the time of completion job `job_id`th on `processor_id`th processor.   
Time is absolute: Calculated since the beginning of processing all the jobs.  


## Implementing *-shop scheduling problem in pyage

* `PerumtationGenotype` - Specifies a representaiton of a specimen. Contains:
 * `self.permutation` = list of int -  genes. Flow shop: jobs permutation, open shop: see *GAFAPAS*
 * `self.fitness` = int - fitness

* `Initializer` - Initializes population with specimens

* `*Evaluation` calculates makespan for permutation represented by currently processed specimen, based on `time_matrix`. `fitness = -makespan`
 * `time_matrix` passed as constructor parameter

* `PermutationMutation` mutates a specimen
 * `count` - constructor parameter
 * `def mutate(self, genotype)` - performs `count` swaps of randomly chosen `permutation` items

* `MemeticPermutationMutation` - performs multiple mutations (multiple samples * multiple rounds) of a specimen and chooses the one yielding the best makespan,
to be the outcome for a processed specimen
  
* `FirstHalfSwapsCrossover` produces a child of two specimens based of both parents features. 
 * `def cross(self, p1, p2)` - finds a minimal list of swaps required to transform `p1` into `p2` and performs half of it, yielding a in-between specimen from `p1` to `p2`.  
  See *GAFAPAS* chapt. 3.5. Crossover, par. Cycle crossover (CX) p. 62-67 for more details.

## Benchmarks
<https://docs.google.com/document/d/17MDBkl22GAAb_Qb3xXM0eSGsVnH4iVcxAXOaNVnm5uc/edit?usp=sharing>
 
## Random solver - as reference solution
To show solution correctness, `random_solver.py` has been implemented.  
Results on sample problem:
 
* Genetic Algorithm: makespan: 1297
* random solver: makespan: ~ 1312
