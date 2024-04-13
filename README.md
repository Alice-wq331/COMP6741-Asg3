# COMP6741 Assignment 3
Group members:<br>
- Jangar Enkhbaatar (z5519242)<br>
- Lingyue Feng (z5446236)<br>
- Qi Wang (z5434112)<br>

## Alternative 1 - PACE challenge 2024 (Heuristics track)
- Report (https://github.com/Alice-wq331/COMP6741-Asg3/blob/main/PACE%202024%20Challenge%20Report_%20Heuristic%20Approaches%20to%20One-Sided%20Crossing%20Minimization.docx)
## Commmands
1. For verifying results of the split algorithm on tiny & medium-size graphs:<br>
pace2024tester --test Pace2024-Testsets/medium_test_set ./code_files/split.sh
2. For verifying results of the 10-iterative-split algorithm on tiny & medium-size graphs:<br>
pace2024tester --test Pace2024-Testsets/medium_test_set ./code_files/split_iterative.sh
3. Test the result and running time of iterative split on large graphs:<br>
run split_heuristic_public.py in local IDE <br>
p.s. In this file, we adjust the number of iterations according to the size of graph, and check wether it can finish within 5 minutes
   


