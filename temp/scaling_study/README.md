# OpenMP Scaling Performance Analysis

This assignment requires you to write a C++ program that uses OpenMP parallelization to perform a computational task and then demonstrate strong and weak scaling on an HPC resource. As part of this assignment, you will produce all the required code, scripts, final scaling plots, and a report.

## Learning Outcomes

- Ability to write parallel C++ programs using OpenMP demonstrating strong and weak scaling.
- Demonstrate an understanding of the concepts of strong and weak scaling, and be able to explain how these concepts relate to parallel performance.
- How to use an HPC resource to collect and analyze execution time data for parallel programs.
- How to create plots that effectively communicate the results of parallel scaling experiments.
- Gain experience with version control tools (e.g., Git and GitHub) to manage code development and submission.
- Reflection on the experience and identify areas for improvement in their development process.

## Instructions

In this assignment, you will write a C++ program to demonstrate strong and weak scaling using OpenMP on UIC's ACER Extreme resource. Your program should simulate a computational task and show how the execution time varies with the number of cores used for parallel execution.

1. Write a C++ program that performs a computational task using OpenMP parallelization. The program should have a **work task** function that simulates some computational work. The program should accept a parameter that specifies the number of **work tasks**. (For example, you can use a `sleep` function in the **work task** function to simulate computational load) To make things more interesting [extra credit], add some random variation to the **work tasks** for each thread. 
2. Implement both strong and weak scaling experiments using the program you wrote. For strong scaling, fix the problem size and vary the number of threads used to solve it. For weak scaling, keep the amount of work per thread constant and vary the total number of threads used to solve the problem. Use the following number of cores: 1, 2, 4, 8, and 16.
3. Collect the execution times for each experiment, and plot the results for both strong and weak scaling. Your plots should have the number of cores used on the x-axis and the execution time on the y-axis.
4. Ensure that the largest run on 16 cores has a runtime that does not exceed 10 minutes. 

## Submission

Submit your code, plots, and a brief report describing your findings. Briefly explain the strong and weak scaling and how your results demonstrate these concepts. **Extra Credit:** if you add randomness to the simulated work unit (note you added the randomness in your final report).

1. Check your code into GitHub as described in the course documentation. Make sure to do your work on your **development** branch and issue a *pull request* when your code is ready to grade.
2. Include the following in your repository:
 - C++ scaling code, as a single file that takes on command line number of units of work (will either be the same value or growing value depending on which study you are doing) (*scaling_study.cc*) 
 - the PBS submission script for the ACER system (*runme.pbs*)
 - a Makefile that builds the executable *scaling_study* when the command `make scaling_study` is executed (*Makefile*)
 - two plots (*strong.png* and *weak.png*) 
 - lessons learned pdf (*report.pdf*) where you describe your process to developing the code (your *git commits* should also reflect this, what were the challenges, what did they learn, what do you wish you knew at the start, how long did it take you to complete the assignment and what would you change in future versions of assignment
 
## Grading

Your assignment will be graded on the following criteria:
 - Correctness and completeness of the code
 - Clarity and quality of the plots
 - Adequacy of the report
 - Demonstration of understanding of strong and weak scaling concepts

